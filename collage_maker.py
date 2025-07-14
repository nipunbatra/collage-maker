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
        self.padding = 6
        self.shadow_offset = 2
        self.shadow_blur = 4
        
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
    
    def _add_frame(self, img, frame_width=6, frame_color=(255, 255, 255)):
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
        """Create a mosaic-style collage with perfect space utilization"""
        if not images:
            return None
            
        collage = Image.new('RGB', self.output_size, self.background_color)
        
        # Use a more systematic approach to fill the space
        # Divide canvas into regions and fill them strategically
        
        selected_images = random.sample(images, min(len(images), 15))
        
        # Define regions with exact coordinates (no gaps)
        regions = []
        
        # Large regions (for hero images)
        regions.extend([
            (0, 0, self.output_size[0] // 2, self.output_size[1] // 2),
            (self.output_size[0] // 2, 0, self.output_size[0], self.output_size[1] // 2),
            (0, self.output_size[1] // 2, self.output_size[0] // 2, self.output_size[1]),
            (self.output_size[0] // 2, self.output_size[1] // 2, self.output_size[0], self.output_size[1])
        ])
        
        # Medium regions (subdivide some large regions)
        w, h = self.output_size
        regions.extend([
            (0, 0, w // 3, h // 3),
            (w // 3, 0, 2 * w // 3, h // 3),
            (2 * w // 3, 0, w, h // 3),
            (0, h // 3, w // 3, 2 * h // 3),
            (w // 3, h // 3, 2 * w // 3, 2 * h // 3),
            (2 * w // 3, h // 3, w, 2 * h // 3),
            (0, 2 * h // 3, w // 3, h),
            (w // 3, 2 * h // 3, 2 * w // 3, h),
            (2 * w // 3, 2 * h // 3, w, h)
        ])
        
        # Small regions for variety
        regions.extend([
            (0, 0, w // 4, h // 4),
            (w // 4, 0, w // 2, h // 4),
            (w // 2, 0, 3 * w // 4, h // 4),
            (3 * w // 4, 0, w, h // 4),
            (0, h // 4, w // 4, h // 2),
            (3 * w // 4, h // 4, w, h // 2),
            (0, 3 * h // 4, w // 4, h),
            (w // 4, 3 * h // 4, w // 2, h),
            (w // 2, 3 * h // 4, 3 * w // 4, h),
            (3 * w // 4, 3 * h // 4, w, h)
        ])
        
        # Shuffle and select best regions
        random.shuffle(regions)
        
        # Use a greedy algorithm to pack rectangles
        placed_regions = []
        
        for i, img_data in enumerate(selected_images):
            if i >= len(regions):
                break
                
            best_region = None
            best_score = 0
            
            for region in regions:
                x1, y1, x2, y2 = region
                width = x2 - x1
                height = y2 - y1
                
                # Skip tiny regions
                if width < 100 or height < 100:
                    continue
                
                # Check if this region overlaps with placed regions
                overlaps = False
                for placed in placed_regions:
                    if self._rectangles_overlap(region, placed):
                        overlaps = True
                        break
                
                if not overlaps:
                    # Score based on size and position variety
                    score = width * height
                    if best_region is None or score > best_score:
                        best_region = region
                        best_score = score
            
            if best_region:
                x1, y1, x2, y2 = best_region
                width = x2 - x1 - self.padding * 2
                height = y2 - y1 - self.padding * 2
                
                # Process image
                img = img_data['image'].copy()
                img = self._resize_to_fit(img, (width, height), crop=True)
                
                if add_frames:
                    img = self._add_frame(img, frame_width=3)
                    img = self._resize_to_fit(img, (width, height))
                
                # Center in region
                final_x = x1 + self.padding + (width - img.width) // 2
                final_y = y1 + self.padding + (height - img.height) // 2
                
                collage.paste(img, (final_x, final_y))
                placed_regions.append(best_region)
        
        return collage
    
    def create_polaroid_collage(self, images, add_frames=True):
        """Create a polaroid-style collage with optimal space usage"""
        if not images:
            return None
            
        collage = Image.new('RGB', self.output_size, self.background_color)
        
        # Polaroid dimensions - smaller for better packing
        polaroid_width = 240
        polaroid_height = 290
        photo_width = 200
        photo_height = 200
        
        selected_images = random.sample(images, min(len(images), 12))
        
        # Create a grid-based approach first, then add rotation
        # Calculate how many can fit in a grid
        cols = self.output_size[0] // (polaroid_width + 20)
        rows = self.output_size[1] // (polaroid_height + 20)
        
        # Create positions in a grid with some randomness
        positions = []
        for row in range(rows):
            for col in range(cols):
                if len(positions) >= len(selected_images):
                    break
                    
                # Base grid position
                base_x = col * (polaroid_width + 20) + 50
                base_y = row * (polaroid_height + 20) + 50
                
                # Add some randomness but keep within bounds
                rand_x = random.randint(-30, 30)
                rand_y = random.randint(-30, 30)
                
                x = max(20, min(base_x + rand_x, self.output_size[0] - polaroid_width - 20))
                y = max(20, min(base_y + rand_y, self.output_size[1] - polaroid_height - 20))
                
                positions.append((x, y))
        
        # Create polaroids
        for i, img_data in enumerate(selected_images[:len(positions)]):
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
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 12)
            except:
                font = ImageFont.load_default()
            
            draw = ImageDraw.Draw(polaroid)
            caption = img_data['caption']
            if len(caption) > 20:
                caption = caption[:17] + "..."
            
            # Center caption
            bbox = draw.textbbox((0, 0), caption, font=font)
            text_width = bbox[2] - bbox[0]
            text_x = (polaroid_width - text_width) // 2
            draw.text((text_x, photo_y + photo_height + 12), caption, fill=(60, 60, 60), font=font)
            
            # Add frame if requested
            if add_frames:
                polaroid = self._add_frame(polaroid, frame_width=2, frame_color=(250, 250, 250))
            
            # Smaller rotation for better packing
            angle = random.randint(-8, 8)
            rotated = polaroid.rotate(angle, expand=True, fillcolor=self.background_color)
            
            # Use pre-calculated position
            x, y = positions[i]
            
            # Adjust for rotation expansion
            x -= (rotated.width - polaroid_width) // 2
            y -= (rotated.height - polaroid_height) // 2
            
            # Ensure within bounds
            x = max(0, min(x, self.output_size[0] - rotated.width))
            y = max(0, min(y, self.output_size[1] - rotated.height))
            
            collage.paste(rotated, (x, y))
        
        return collage
    
    def create_magazine_collage(self, images, add_frames=True):
        """Create a magazine-style collage with featured image"""
        if not images:
            return None
            
        collage = Image.new('RGB', self.output_size, self.background_color)
        
        # Select images
        selected_images = random.sample(images, min(len(images), 10))
        
        # Featured image (60% of width, full height)
        featured = selected_images[0]
        feature_width = int(self.output_size[0] * 0.6) - self.padding * 2
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
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        draw = ImageDraw.Draw(collage)
        caption = featured['caption']
        if len(caption) > 35:
            caption = caption[:32] + "..."
        
        # Position caption below featured image with background
        caption_y = feat_y + featured_img.height + 8
        caption_bg = Image.new('RGBA', (len(caption) * 10, 25), (255, 255, 255, 200))
        collage.paste(caption_bg, (feat_x, caption_y), caption_bg)
        draw.text((feat_x + 5, caption_y + 5), caption, fill=(40, 40, 40), font=font)
        
        # Right side - use remaining 40% width
        remaining_images = selected_images[1:]
        right_start_x = int(self.output_size[0] * 0.6) + self.padding
        right_width = int(self.output_size[0] * 0.4) - self.padding * 2
        
        # Create a tighter grid on right side
        rows = 4
        cols = 2
        cell_width = (right_width - self.padding) // cols
        cell_height = (self.output_size[1] - self.padding * 2) // rows
        
        for i, img_data in enumerate(remaining_images[:rows * cols]):
            row = i // cols
            col = i % cols
            
            x = right_start_x + col * (cell_width + self.padding // 2)
            y = self.padding + row * (cell_height + self.padding // 2)
            
            img = img_data['image'].copy()
            img = self._resize_to_fit(img, (cell_width - 5, cell_height - 5), crop=True)
            
            if add_frames:
                img = self._add_frame(img, frame_width=2)
                img = self._resize_to_fit(img, (cell_width - 5, cell_height - 5))
            
            # Center in cell
            img_x = x + (cell_width - img.width) // 2
            img_y = y + (cell_height - img.height) // 2
            collage.paste(img, (img_x, img_y))
        
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
            collage = enhancer.enhance(1.2)
            
            # Slight contrast enhancement
            enhancer = ImageEnhance.Contrast(collage)
            collage = enhancer.enhance(1.05)
            
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
@click.option('--style', '-s', type=click.Choice(['grid', 'mosaic', 'polaroid', 'magazine', 'all']), 
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
        styles = ['grid', 'mosaic', 'polaroid', 'magazine']
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
        
        if collage:
            output_filename = f"{os.path.splitext(output)[0]}_{style_name}.jpg"
            collage_maker.save_collage(collage, output_filename)

if __name__ == "__main__":
    main()