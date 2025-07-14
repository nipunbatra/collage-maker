#!/usr/bin/env python3
"""
Collage Maker - Create beautiful photo collages from a folder of images
"""

import os
import random
import math
from PIL import Image, ImageDraw, ImageFont
import click
import requests
from io import BytesIO

class CollageMaker:
    def __init__(self, output_size=(1920, 1080), background_color=(255, 255, 255)):
        self.output_size = output_size
        self.background_color = background_color
        self.padding = 10
        
    def load_images(self, folder_path):
        """Load images from folder"""
        supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        images = []
        
        for filename in os.listdir(folder_path):
            if any(filename.lower().endswith(ext) for ext in supported_formats):
                try:
                    img_path = os.path.join(folder_path, filename)
                    img = Image.open(img_path)
                    img = img.convert('RGB')  # Ensure RGB mode
                    images.append({
                        'image': img,
                        'filename': filename,
                        'caption': self._extract_caption(filename)
                    })
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
                    
        return images
    
    def _extract_caption(self, filename):
        """Extract caption from filename (remove extension)"""
        return os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ').title()
    
    def create_grid_collage(self, images, rows=2, cols=3):
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
            
            # Resize image to fit cell
            img = img_data['image'].copy()
            img = self._resize_to_fit(img, (cell_width, cell_height))
            
            # Center the image in the cell
            img_x = x + (cell_width - img.width) // 2
            img_y = y + (cell_height - img.height) // 2
            
            collage.paste(img, (img_x, img_y))
            
        return collage
    
    def create_mosaic_collage(self, images):
        """Create a mosaic-style collage with varying sizes"""
        if not images:
            return None
            
        collage = Image.new('RGB', self.output_size, self.background_color)
        
        # Define different size categories
        sizes = [
            (400, 300),  # Large
            (300, 200),  # Medium
            (200, 150),  # Small
        ]
        
        positions = []
        used_images = random.sample(images, min(len(images), 8))
        
        for i, img_data in enumerate(used_images):
            size = random.choice(sizes)
            
            # Find available position
            placed = False
            attempts = 0
            
            while not placed and attempts < 100:
                x = random.randint(0, self.output_size[0] - size[0])
                y = random.randint(0, self.output_size[1] - size[1])
                
                # Check for overlap
                overlap = False
                for pos in positions:
                    if self._rectangles_overlap((x, y, x + size[0], y + size[1]), pos):
                        overlap = True
                        break
                
                if not overlap:
                    img = img_data['image'].copy()
                    img = self._resize_to_fit(img, size)
                    collage.paste(img, (x, y))
                    positions.append((x, y, x + size[0], y + size[1]))
                    placed = True
                
                attempts += 1
                
        return collage
    
    def create_polaroid_collage(self, images):
        """Create a polaroid-style collage with rotated images"""
        if not images:
            return None
            
        collage = Image.new('RGB', self.output_size, self.background_color)
        
        # Polaroid dimensions
        polaroid_width = 300
        polaroid_height = 350
        photo_width = 260
        photo_height = 260
        
        selected_images = random.sample(images, min(len(images), 6))
        
        for i, img_data in enumerate(selected_images):
            # Create polaroid background
            polaroid = Image.new('RGB', (polaroid_width, polaroid_height), (255, 255, 255))
            
            # Add photo
            img = img_data['image'].copy()
            img = self._resize_to_fit(img, (photo_width, photo_height))
            
            # Center photo on polaroid
            photo_x = (polaroid_width - img.width) // 2
            photo_y = 20
            polaroid.paste(img, (photo_x, photo_y))
            
            # Add caption
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
            except:
                font = ImageFont.load_default()
            
            draw = ImageDraw.Draw(polaroid)
            caption = img_data['caption'][:20] + "..." if len(img_data['caption']) > 20 else img_data['caption']
            
            # Center caption
            bbox = draw.textbbox((0, 0), caption, font=font)
            text_width = bbox[2] - bbox[0]
            text_x = (polaroid_width - text_width) // 2
            draw.text((text_x, photo_y + photo_height + 20), caption, fill=(0, 0, 0), font=font)
            
            # Random rotation
            angle = random.randint(-15, 15)
            rotated = polaroid.rotate(angle, expand=True, fillcolor=self.background_color)
            
            # Random position
            max_x = self.output_size[0] - rotated.width
            max_y = self.output_size[1] - rotated.height
            
            if max_x > 0 and max_y > 0:
                x = random.randint(0, max_x)
                y = random.randint(0, max_y)
                collage.paste(rotated, (x, y))
                
        return collage
    
    def _resize_to_fit(self, img, target_size):
        """Resize image to fit within target size while maintaining aspect ratio"""
        img.thumbnail(target_size, Image.Resampling.LANCZOS)
        return img
    
    def _rectangles_overlap(self, rect1, rect2):
        """Check if two rectangles overlap"""
        return not (rect1[2] < rect2[0] or rect2[2] < rect1[0] or 
                   rect1[3] < rect2[1] or rect2[3] < rect1[1])
    
    def save_collage(self, collage, output_path):
        """Save collage to file"""
        if collage:
            collage.save(output_path, 'JPEG', quality=90)
            print(f"Collage saved to: {output_path}")
        else:
            print("No collage to save")

def download_sample_images():
    """Download sample images for testing"""
    sample_folder = "sample_images"
    os.makedirs(sample_folder, exist_ok=True)
    
    # Unsplash sample images (free to use)
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

@click.command()
@click.option('--folder', '-f', help='Folder containing images')
@click.option('--output', '-o', default='collage.jpg', help='Output filename')
@click.option('--style', '-s', type=click.Choice(['grid', 'mosaic', 'polaroid', 'all']), 
              default='grid', help='Collage style')
@click.option('--width', '-w', default=1920, help='Output width')
@click.option('--height', '-h', default=1080, help='Output height')
@click.option('--download-samples', is_flag=True, help='Download sample images')
def main(folder, output, style, width, height, download_samples):
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
        styles = ['grid', 'mosaic', 'polaroid']
    else:
        styles = [style]
    
    for style_name in styles:
        print(f"Creating {style_name} collage...")
        
        if style_name == 'grid':
            collage = collage_maker.create_grid_collage(images)
        elif style_name == 'mosaic':
            collage = collage_maker.create_mosaic_collage(images)
        elif style_name == 'polaroid':
            collage = collage_maker.create_polaroid_collage(images)
        
        if collage:
            output_filename = f"{os.path.splitext(output)[0]}_{style_name}.jpg"
            collage_maker.save_collage(collage, output_filename)

if __name__ == "__main__":
    main()