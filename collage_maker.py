#!/usr/bin/env python3
"""
Collage Maker - Create beautiful photo collages from a folder of images
Inspired by Google Photos and Apple Photos automatic collages
"""

import os
import random
import math
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import click
import requests
from io import BytesIO

class CollageMaker:
    def __init__(self, output_size=(1920, 1080), background_color=(245, 245, 245)):
        self.output_size = output_size
        self.background_color = background_color
        self.padding = 8
        self.shadow_offset = 3
        self.shadow_blur = 5
        
    def load_images(self, folder_path):
        """Load images from folder with caption support"""
        supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        images = []
        
        # Load captions from JSON or TXT file
        captions = self._load_captions(folder_path)
        
        for filename in os.listdir(folder_path):
            if any(filename.lower().endswith(ext) for ext in supported_formats):
                try:
                    img_path = os.path.join(folder_path, filename)
                    img = Image.open(img_path)
                    img = img.convert('RGB')  # Ensure RGB mode
                    
                    # Get caption from file or extract from filename
                    caption = captions.get(filename, self._extract_caption(filename))
                    
                    images.append({
                        'image': img,
                        'filename': filename,
                        'caption': caption
                    })
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
                    
        return images
    
    def _load_captions(self, folder_path):
        """Load captions from JSON or TXT file"""
        captions = {}
        
        # Try JSON file first
        json_path = os.path.join(folder_path, 'captions.json')
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    captions = json.load(f)
            except Exception as e:
                print(f"Error loading captions.json: {e}")
        
        # Try TXT file format: filename: caption
        txt_path = os.path.join(folder_path, 'captions.txt')
        if os.path.exists(txt_path):
            try:
                with open(txt_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if ':' in line:
                            filename, caption = line.split(':', 1)
                            captions[filename.strip()] = caption.strip()
            except Exception as e:
                print(f"Error loading captions.txt: {e}")
        
        return captions
    
    def _extract_caption(self, filename):
        """Extract caption from filename (remove extension)"""
        return os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ').title()
    
    def _add_shadow(self, img, shadow_color=(0, 0, 0, 60)):
        """Add shadow to image"""
        # Create shadow
        shadow = Image.new('RGBA', 
                          (img.width + self.shadow_offset * 2, img.height + self.shadow_offset * 2), 
                          (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rectangle([self.shadow_offset, self.shadow_offset, 
                             img.width + self.shadow_offset, img.height + self.shadow_offset], 
                            fill=shadow_color)
        
        # Blur shadow
        shadow = shadow.filter(ImageFilter.GaussianBlur(self.shadow_blur))
        
        # Composite
        result = Image.new('RGBA', shadow.size, (0, 0, 0, 0))
        result.paste(shadow, (0, 0))
        result.paste(img, (0, 0))
        
        return result
    
    def _add_frame(self, img, frame_width=8, frame_color=(255, 255, 255)):
        """Add frame to image"""
        framed = Image.new('RGB', 
                          (img.width + frame_width * 2, img.height + frame_width * 2), 
                          frame_color)
        framed.paste(img, (frame_width, frame_width))
        return framed
    
    def _resize_to_fit(self, img, target_size, crop=False):
        """Resize image to fit within target size"""
        if crop:
            # Crop to exact size maintaining aspect ratio
            img_ratio = img.width / img.height
            target_ratio = target_size[0] / target_size[1]
            
            if img_ratio > target_ratio:
                # Image is wider, crop width
                new_width = int(img.height * target_ratio)
                left = (img.width - new_width) // 2
                img = img.crop((left, 0, left + new_width, img.height))
            else:
                # Image is taller, crop height
                new_height = int(img.width / target_ratio)
                top = (img.height - new_height) // 2
                img = img.crop((0, top, img.width, top + new_height))
            
            return img.resize(target_size, Image.Resampling.LANCZOS)
        else:
            # Fit within bounds maintaining aspect ratio
            img.thumbnail(target_size, Image.Resampling.LANCZOS)
            return img
    
    def create_grid_collage(self, images, rows=2, cols=3, add_frames=True):
        """Create a grid-based collage"""
        if not images:
            return None
            
        # Calculate cell dimensions
        cell_width = (self.output_size[0] - (cols + 1) * self.padding) // cols
        cell_height = (self.output_size[1] - (rows + 1) * self.padding) // rows
        
        # Create background
        collage = Image.new('RGB', self.output_size, self.background_color)
        
        # Select random images if we have more than needed
        selected_images = random.sample(images, min(len(images), rows * cols))
        
        for i, img_data in enumerate(selected_images):
            row = i // cols
            col = i % cols
            
            # Calculate position
            x = col * (cell_width + self.padding) + self.padding
            y = row * (cell_height + self.padding) + self.padding
            
            # Resize image to fit cell (crop to exact size)
            img = img_data['image'].copy()
            img = self._resize_to_fit(img, (cell_width, cell_height), crop=True)
            
            # Add frame if requested
            if add_frames:
                img = self._add_frame(img, frame_width=4)
                # Resize again to fit in cell
                img = self._resize_to_fit(img, (cell_width, cell_height))
            
            # Center the image in the cell
            img_x = x + (cell_width - img.width) // 2
            img_y = y + (cell_height - img.height) // 2
            
            collage.paste(img, (img_x, img_y))
            
        return collage
    
    def create_mosaic_collage(self, images, add_frames=True):
        """Create a mosaic-style collage with better space utilization"""
        if not images:
            return None
            
        collage = Image.new('RGB', self.output_size, self.background_color)
        
        # Define size categories with better distribution
        sizes = [
            (380, 280),  # Large landscape
            (280, 380),  # Large portrait
            (280, 200),  # Medium landscape
            (200, 280),  # Medium portrait
            (200, 200),  # Square
        ]
        
        positions = []
        used_images = random.sample(images, min(len(images), 12))
        
        # Place larger images first
        for i, img_data in enumerate(used_images):
            # Use larger sizes for first few images
            if i < 3:
                size = random.choice(sizes[:2])  # Large sizes
            elif i < 6:
                size = random.choice(sizes[2:4])  # Medium sizes
            else:
                size = sizes[4]  # Square for remaining
            
            placed = False
            attempts = 0
            
            while not placed and attempts < 200:
                margin = 20
                x = random.randint(margin, self.output_size[0] - size[0] - margin)
                y = random.randint(margin, self.output_size[1] - size[1] - margin)
                
                # Check for overlap with existing positions
                new_rect = (x, y, x + size[0], y + size[1])
                overlap = False
                
                for pos in positions:
                    if self._rectangles_overlap(new_rect, pos):
                        overlap = True
                        break
                
                if not overlap:
                    img = img_data['image'].copy()
                    img = self._resize_to_fit(img, size, crop=True)
                    
                    if add_frames:
                        img = self._add_frame(img, frame_width=3)
                        img = self._resize_to_fit(img, size)
                    
                    # Center in allocated space
                    final_x = x + (size[0] - img.width) // 2
                    final_y = y + (size[1] - img.height) // 2
                    
                    collage.paste(img, (final_x, final_y))
                    positions.append(new_rect)
                    placed = True
                
                attempts += 1
                
        return collage
    
    def create_polaroid_collage(self, images, add_frames=True):
        """Create a polaroid-style collage with better layout"""
        if not images:
            return None
            
        collage = Image.new('RGB', self.output_size, self.background_color)
        
        # Polaroid dimensions
        polaroid_width = 280
        polaroid_height = 340
        photo_width = 240
        photo_height = 240
        
        selected_images = random.sample(images, min(len(images), 8))
        positions = []
        
        for i, img_data in enumerate(selected_images):
            # Create polaroid background
            polaroid = Image.new('RGB', (polaroid_width, polaroid_height), (255, 255, 255))
            
            # Add photo
            img = img_data['image'].copy()
            img = self._resize_to_fit(img, (photo_width, photo_height), crop=True)
            
            # Center photo on polaroid
            photo_x = (polaroid_width - img.width) // 2
            photo_y = 15
            polaroid.paste(img, (photo_x, photo_y))
            
            # Add caption
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 14)
            except:
                font = ImageFont.load_default()
            
            draw = ImageDraw.Draw(polaroid)
            caption = img_data['caption']
            if len(caption) > 25:
                caption = caption[:22] + "..."
            
            # Center caption
            bbox = draw.textbbox((0, 0), caption, font=font)
            text_width = bbox[2] - bbox[0]
            text_x = (polaroid_width - text_width) // 2
            draw.text((text_x, photo_y + photo_height + 15), caption, fill=(60, 60, 60), font=font)
            
            # Add frame if requested
            if add_frames:
                polaroid = self._add_frame(polaroid, frame_width=2, frame_color=(250, 250, 250))
            
            # Random rotation
            angle = random.randint(-12, 12)
            rotated = polaroid.rotate(angle, expand=True, fillcolor=self.background_color)
            
            # Find non-overlapping position
            placed = False
            attempts = 0
            
            while not placed and attempts < 100:
                margin = 30
                max_x = max(0, self.output_size[0] - rotated.width - margin)
                max_y = max(0, self.output_size[1] - rotated.height - margin)
                
                if max_x > margin and max_y > margin:
                    x = random.randint(margin, max_x)
                    y = random.randint(margin, max_y)
                    
                    new_rect = (x, y, x + rotated.width, y + rotated.height)
                    overlap = False
                    
                    for pos in positions:
                        if self._rectangles_overlap(new_rect, pos):
                            overlap = True
                            break
                    
                    if not overlap:
                        collage.paste(rotated, (x, y))
                        positions.append(new_rect)
                        placed = True
                
                attempts += 1
                
        return collage
    
    def create_magazine_collage(self, images, add_frames=True):
        """Create a magazine-style collage with featured image"""
        if not images:
            return None
            
        collage = Image.new('RGB', self.output_size, self.background_color)
        
        # Select images
        selected_images = random.sample(images, min(len(images), 8))
        
        # Featured image (large, left side)
        featured = selected_images[0]
        feature_width = self.output_size[0] // 2 - self.padding * 2
        feature_height = self.output_size[1] - self.padding * 2
        
        featured_img = featured['image'].copy()
        featured_img = self._resize_to_fit(featured_img, (feature_width, feature_height), crop=True)
        
        if add_frames:
            featured_img = self._add_frame(featured_img, frame_width=6)
            featured_img = self._resize_to_fit(featured_img, (feature_width, feature_height))
        
        # Center featured image
        feat_x = self.padding + (feature_width - featured_img.width) // 2
        feat_y = self.padding + (feature_height - featured_img.height) // 2
        collage.paste(featured_img, (feat_x, feat_y))
        
        # Add caption for featured image
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 18)
        except:
            font = ImageFont.load_default()
        
        draw = ImageDraw.Draw(collage)
        caption = featured['caption']
        if len(caption) > 30:
            caption = caption[:27] + "..."
        
        # Position caption below featured image
        caption_y = feat_y + featured_img.height + 10
        draw.text((feat_x, caption_y), caption, fill=(40, 40, 40), font=font)
        
        # Right side smaller images
        remaining_images = selected_images[1:]
        right_start_x = self.output_size[0] // 2 + self.padding
        right_width = self.output_size[0] // 2 - self.padding * 2
        
        # Create grid on right side
        rows = 3
        cols = 2
        cell_width = (right_width - self.padding) // cols
        cell_height = (self.output_size[1] - self.padding * 2) // rows
        
        for i, img_data in enumerate(remaining_images[:rows * cols]):
            row = i // cols
            col = i % cols
            
            x = right_start_x + col * (cell_width + self.padding // 2)
            y = self.padding + row * (cell_height + self.padding // 2)
            
            img = img_data['image'].copy()
            img = self._resize_to_fit(img, (cell_width - 10, cell_height - 10), crop=True)
            
            if add_frames:
                img = self._add_frame(img, frame_width=3)
                img = self._resize_to_fit(img, (cell_width - 10, cell_height - 10))
            
            # Center in cell
            img_x = x + (cell_width - img.width) // 2
            img_y = y + (cell_height - img.height) // 2
            collage.paste(img, (img_x, img_y))
        
        return collage
    
    def create_heart_collage(self, images, add_frames=True):
        """Create a heart-shaped collage"""
        if not images:
            return None
            
        collage = Image.new('RGB', self.output_size, self.background_color)
        
        # Heart shape points (scaled to output size)
        center_x = self.output_size[0] // 2
        center_y = self.output_size[1] // 2
        scale = min(self.output_size[0], self.output_size[1]) // 3
        
        # Generate heart-shaped positions
        heart_positions = []
        for t in range(0, 360, 20):  # 18 positions
            rad = math.radians(t)
            # Heart equation: x = 16sin³(t), y = 13cos(t) - 5cos(2t) - 2cos(3t) - cos(4t)
            x = 16 * (math.sin(rad) ** 3)
            y = 13 * math.cos(rad) - 5 * math.cos(2 * rad) - 2 * math.cos(3 * rad) - math.cos(4 * rad)
            
            # Scale and center
            x = center_x + int(x * scale / 16)
            y = center_y - int(y * scale / 16)  # Flip Y
            
            heart_positions.append((x, y))
        
        # Place images at heart positions
        selected_images = random.sample(images, min(len(images), len(heart_positions)))
        image_size = (120, 120)
        
        for i, (pos_x, pos_y) in enumerate(heart_positions[:len(selected_images)]):
            img_data = selected_images[i]
            img = img_data['image'].copy()
            img = self._resize_to_fit(img, image_size, crop=True)
            
            if add_frames:
                img = self._add_frame(img, frame_width=3)
                img = self._resize_to_fit(img, image_size)
            
            # Create circular mask
            mask = Image.new('L', img.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, img.width, img.height), fill=255)
            
            # Apply mask
            img.putalpha(mask)
            
            # Position on collage
            final_x = pos_x - img.width // 2
            final_y = pos_y - img.height // 2
            
            # Ensure within bounds
            final_x = max(0, min(final_x, self.output_size[0] - img.width))
            final_y = max(0, min(final_y, self.output_size[1] - img.height))
            
            collage.paste(img, (final_x, final_y), img)
        
        return collage
    
    def _rectangles_overlap(self, rect1, rect2):
        """Check if two rectangles overlap"""
        return not (rect1[2] < rect2[0] or rect2[2] < rect1[0] or 
                   rect1[3] < rect2[1] or rect2[3] < rect1[1])
    
    def save_collage(self, collage, output_path):
        """Save collage to file"""
        if collage:
            # Enhance image quality
            enhancer = ImageEnhance.Sharpness(collage)
            collage = enhancer.enhance(1.1)
            
            collage.save(output_path, 'JPEG', quality=95, optimize=True)
            print(f"Collage saved to: {output_path}")
        else:
            print("No collage to save")

def create_sample_captions():
    """Create sample captions file"""
    sample_captions = {
        "sample_1.jpg": "Golden sunset over mountains",
        "sample_2.jpg": "Peaceful lake reflection",
        "sample_3.jpg": "Vibrant city nightscape",
        "sample_4.jpg": "Autumn forest pathway",
        "sample_5.jpg": "Ocean waves crashing",
        "sample_6.jpg": "Beautiful cherry blossoms",
        "sample_7.jpg": "Majestic snow-capped peaks",
        "sample_8.jpg": "Serene beach paradise"
    }
    
    with open("sample_images/captions.json", "w") as f:
        json.dump(sample_captions, f, indent=2)
    
    print("Created sample captions.json file")

def download_sample_images():
    """Download sample images for testing"""
    sample_folder = "sample_images"
    os.makedirs(sample_folder, exist_ok=True)
    
    # Unsplash sample images with specific themes
    sample_urls = [
        "https://picsum.photos/800/600?random=1",
        "https://picsum.photos/800/600?random=2", 
        "https://picsum.photos/800/600?random=3",
        "https://picsum.photos/800/600?random=4",
        "https://picsum.photos/800/600?random=5",
        "https://picsum.photos/800/600?random=6",
        "https://picsum.photos/800/600?random=7",
        "https://picsum.photos/800/600?random=8",
    ]
    
    for i, url in enumerate(sample_urls):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(f"{sample_folder}/sample_{i+1}.jpg", "wb") as f:
                    f.write(response.content)
                print(f"Downloaded sample_{i+1}.jpg")
        except Exception as e:
            print(f"Error downloading sample_{i+1}.jpg: {e}")
    
    # Create captions file
    create_sample_captions()

@click.command()
@click.option('--folder', '-f', help='Folder containing images')
@click.option('--output', '-o', default='collage.jpg', help='Output filename')
@click.option('--style', '-s', type=click.Choice(['grid', 'mosaic', 'polaroid', 'magazine', 'heart', 'all']), 
              default='grid', help='Collage style')
@click.option('--width', '-w', default=1920, help='Output width')
@click.option('--height', '-h', default=1080, help='Output height')
@click.option('--no-frames', is_flag=True, help='Disable frames on images')
@click.option('--download-samples', is_flag=True, help='Download sample images')
def main(folder, output, style, width, height, no_frames, download_samples):
    """Create beautiful photo collages from a folder of images"""
    
    if download_samples:
        download_sample_images()
        return
    
    if not folder:
        print("Error: --folder is required when not downloading samples")
        return
    
    if not os.path.exists(folder):
        print(f"Error: Folder '{folder}' does not exist")
        return
    
    # Initialize collage maker
    collage_maker = CollageMaker(output_size=(width, height))
    
    # Load images
    print(f"Loading images from {folder}...")
    images = collage_maker.load_images(folder)
    
    if not images:
        print("No images found in the folder")
        return
    
    print(f"Found {len(images)} images")
    
    # Create collages based on style
    if style == 'all':
        styles = ['grid', 'mosaic', 'polaroid', 'magazine', 'heart']
    else:
        styles = [style]
    
    add_frames = not no_frames
    
    for style_name in styles:
        print(f"Creating {style_name} collage...")
        
        if style_name == 'grid':
            collage = collage_maker.create_grid_collage(images, add_frames=add_frames)
        elif style_name == 'mosaic':
            collage = collage_maker.create_mosaic_collage(images, add_frames=add_frames)
        elif style_name == 'polaroid':
            collage = collage_maker.create_polaroid_collage(images, add_frames=add_frames)
        elif style_name == 'magazine':
            collage = collage_maker.create_magazine_collage(images, add_frames=add_frames)
        elif style_name == 'heart':
            collage = collage_maker.create_heart_collage(images, add_frames=add_frames)
        
        if collage:
            output_filename = f"{os.path.splitext(output)[0]}_{style_name}.jpg"
            collage_maker.save_collage(collage, output_filename)

if __name__ == "__main__":
    main()