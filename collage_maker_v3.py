#!/usr/bin/env python3
"""
Collage Maker v3 - ULTIMATE SPACE UTILIZATION
Advanced algorithms for zero wasted space
"""

import os
import random
import math
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import click
import requests
from io import BytesIO

class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.right = x + width
        self.bottom = y + height
    
    def intersects(self, other):
        return not (self.right <= other.x or other.right <= self.x or 
                   self.bottom <= other.y or other.bottom <= self.y)
    
    def area(self):
        return self.width * self.height

class UltimateCollageMaker:
    def __init__(self, output_size=(1920, 1080), background_color=(245, 245, 245)):
        self.output_size = output_size
        self.background_color = background_color
        self.min_padding = 3
        self.max_attempts = 500
        
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
                    img = img.convert('RGB')
                    
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
        
        json_path = os.path.join(folder_path, 'captions.json')
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    captions = json.load(f)
            except Exception as e:
                print(f"Error loading captions.json: {e}")
        
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
        """Extract caption from filename"""
        return os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ').title()
    
    def _add_frame(self, img, frame_width=4, frame_color=(255, 255, 255)):
        """Add frame to image"""
        framed = Image.new('RGB', 
                          (img.width + frame_width * 2, img.height + frame_width * 2), 
                          frame_color)
        framed.paste(img, (frame_width, frame_width))
        return framed
    
    def _resize_and_crop(self, img, target_width, target_height):
        """Resize and crop image to exact dimensions"""
        # Calculate scaling to fill the target area
        scale_x = target_width / img.width
        scale_y = target_height / img.height
        scale = max(scale_x, scale_y)  # Use max to ensure we fill the area
        
        # Resize image
        new_width = int(img.width * scale)
        new_height = int(img.height * scale)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Crop to exact size
        if new_width > target_width:
            left = (new_width - target_width) // 2
            img = img.crop((left, 0, left + target_width, new_height))
        
        if new_height > target_height:
            top = (new_height - target_height) // 2
            img = img.crop((0, top, new_width, top + target_height))
        
        return img
    
    def create_ultimate_mosaic(self, images, add_frames=True):
        """Create mosaic with ultimate space utilization using bin packing"""
        if not images:
            return None
        
        collage = Image.new('RGB', self.output_size, self.background_color)
        
        # Generate size options based on golden ratio and canvas proportions
        min_size = min(self.output_size[0], self.output_size[1]) // 8
        max_size = min(self.output_size[0], self.output_size[1]) // 2
        
        # Create diverse rectangle sizes
        sizes = []
        
        # Large rectangles (hero images)
        sizes.extend([
            (max_size, max_size * 2 // 3),  # Large horizontal
            (max_size * 2 // 3, max_size),  # Large vertical
            (max_size, max_size),           # Large square
        ])
        
        # Medium rectangles
        med_size = max_size * 2 // 3
        sizes.extend([
            (med_size, med_size // 2),      # Medium horizontal
            (med_size // 2, med_size),      # Medium vertical
            (med_size, med_size),           # Medium square
        ])
        
        # Small rectangles for filling gaps
        small_size = max_size // 2
        sizes.extend([
            (small_size, small_size),       # Small square
            (small_size * 3 // 2, small_size), # Small horizontal
            (small_size, small_size * 3 // 2), # Small vertical
        ])
        
        # Very small rectangles for tight spaces
        tiny_size = min_size
        sizes.extend([
            (tiny_size * 2, tiny_size),     # Tiny horizontal
            (tiny_size, tiny_size * 2),     # Tiny vertical
            (tiny_size, tiny_size),         # Tiny square
        ])
        
        # Place images using first-fit decreasing algorithm
        placed_rectangles = []
        selected_images = random.sample(images, min(len(images), len(sizes)))
        
        # Sort sizes by area (largest first)
        sizes.sort(key=lambda s: s[0] * s[1], reverse=True)
        
        for i, img_data in enumerate(selected_images):
            best_position = None
            best_size = None
            
            # Try each size
            for width, height in sizes:
                # Try to find a position for this size
                position = self._find_best_position(width, height, placed_rectangles)
                if position:
                    best_position = position
                    best_size = (width, height)
                    break
            
            if best_position and best_size:
                x, y = best_position
                width, height = best_size
                
                # Process image
                img = img_data['image'].copy()
                img = self._resize_and_crop(img, width, height)
                
                if add_frames:
                    img = self._add_frame(img, frame_width=2)
                    # Resize again to fit
                    img = self._resize_and_crop(img, width, height)
                
                collage.paste(img, (x, y))
                placed_rectangles.append(Rectangle(x, y, width, height))
        
        # Fill remaining gaps with smaller images
        self._fill_gaps(collage, placed_rectangles, selected_images[len(placed_rectangles):], add_frames)
        
        return collage
    
    def _find_best_position(self, width, height, placed_rectangles):
        """Find best position for rectangle using bottom-left-fill algorithm"""
        # Try positions in a systematic way
        step = 10  # Grid step size
        
        for y in range(0, self.output_size[1] - height + 1, step):
            for x in range(0, self.output_size[0] - width + 1, step):
                rect = Rectangle(x, y, width, height)
                
                # Check if this position is valid
                if not any(rect.intersects(placed) for placed in placed_rectangles):
                    return (x, y)
        
        return None
    
    def _fill_gaps(self, collage, placed_rectangles, remaining_images, add_frames):
        """Fill remaining gaps with smaller images"""
        if not remaining_images:
            return
        
        # Find gaps and fill them
        gap_sizes = [(50, 50), (100, 50), (50, 100), (100, 100), (150, 100), (100, 150)]
        
        for img_data in remaining_images[:6]:  # Limit to avoid overcrowding
            for width, height in gap_sizes:
                position = self._find_best_position(width, height, placed_rectangles)
                if position:
                    x, y = position
                    
                    img = img_data['image'].copy()
                    img = self._resize_and_crop(img, width, height)
                    
                    if add_frames:
                        img = self._add_frame(img, frame_width=1)
                        img = self._resize_and_crop(img, width, height)
                    
                    collage.paste(img, (x, y))
                    placed_rectangles.append(Rectangle(x, y, width, height))
                    break
    
    def create_perfect_polaroid(self, images, add_frames=True):
        """Create polaroid with perfect space utilization"""
        if not images:
            return None
        
        collage = Image.new('RGB', self.output_size, self.background_color)
        
        # Calculate optimal polaroid size based on canvas
        canvas_ratio = self.output_size[0] / self.output_size[1]
        
        if canvas_ratio > 1.5:  # Wide canvas
            polaroid_width = 200
            polaroid_height = 250
        elif canvas_ratio < 0.8:  # Tall canvas
            polaroid_width = 180
            polaroid_height = 230
        else:  # Square-ish canvas
            polaroid_width = 220
            polaroid_height = 270
        
        photo_width = polaroid_width - 20
        photo_height = int(photo_width * 0.8)  # 4:3 aspect ratio
        
        # Calculate grid that maximizes space usage
        margin = 15
        cols = max(1, (self.output_size[0] - margin) // (polaroid_width + margin))
        rows = max(1, (self.output_size[1] - margin) // (polaroid_height + margin))
        
        # Calculate actual spacing to center the grid
        total_width = cols * polaroid_width + (cols - 1) * margin
        total_height = rows * polaroid_height + (rows - 1) * margin
        
        start_x = (self.output_size[0] - total_width) // 2
        start_y = (self.output_size[1] - total_height) // 2
        
        selected_images = random.sample(images, min(len(images), rows * cols))
        
        for i, img_data in enumerate(selected_images):
            row = i // cols
            col = i % cols
            
            if row >= rows:
                break
            
            # Calculate position
            x = start_x + col * (polaroid_width + margin)
            y = start_y + row * (polaroid_height + margin)
            
            # Add small random offset for natural look
            x += random.randint(-10, 10)
            y += random.randint(-10, 10)
            
            # Create polaroid
            polaroid = Image.new('RGB', (polaroid_width, polaroid_height), (255, 255, 255))
            
            # Add photo
            img = img_data['image'].copy()
            img = self._resize_and_crop(img, photo_width, photo_height)
            
            photo_x = (polaroid_width - photo_width) // 2
            photo_y = 10
            polaroid.paste(img, (photo_x, photo_y))
            
            # Add caption
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 10)
            except:
                font = ImageFont.load_default()
            
            draw = ImageDraw.Draw(polaroid)
            caption = img_data['caption']
            if len(caption) > 18:
                caption = caption[:15] + "..."
            
            bbox = draw.textbbox((0, 0), caption, font=font)
            text_width = bbox[2] - bbox[0]
            text_x = (polaroid_width - text_width) // 2
            draw.text((text_x, photo_y + photo_height + 8), caption, fill=(60, 60, 60), font=font)
            
            if add_frames:
                polaroid = self._add_frame(polaroid, frame_width=1, frame_color=(250, 250, 250))
            
            # Small rotation
            angle = random.randint(-6, 6)
            rotated = polaroid.rotate(angle, expand=True, fillcolor=self.background_color)
            
            # Adjust position for rotation
            final_x = x - (rotated.width - polaroid_width) // 2
            final_y = y - (rotated.height - polaroid_height) // 2
            
            # Ensure within bounds
            final_x = max(0, min(final_x, self.output_size[0] - rotated.width))
            final_y = max(0, min(final_y, self.output_size[1] - rotated.height))
            
            collage.paste(rotated, (final_x, final_y))
        
        return collage
    
    def create_smart_magazine(self, images, add_frames=True):
        """Create magazine layout with smart space utilization"""
        if not images:
            return None
        
        collage = Image.new('RGB', self.output_size, self.background_color)
        selected_images = random.sample(images, min(len(images), 12))
        
        # Calculate optimal split based on aspect ratio
        if self.output_size[0] > self.output_size[1] * 1.3:  # Wide layout
            feature_ratio = 0.65
        else:  # More square layout
            feature_ratio = 0.55
        
        # Featured image
        featured = selected_images[0]
        feature_width = int(self.output_size[0] * feature_ratio) - 10
        feature_height = self.output_size[1] - 20
        
        featured_img = featured['image'].copy()
        featured_img = self._resize_and_crop(featured_img, feature_width, feature_height)
        
        if add_frames:
            featured_img = self._add_frame(featured_img, frame_width=4)
            featured_img = self._resize_and_crop(featured_img, feature_width, feature_height)
        
        collage.paste(featured_img, (10, 10))
        
        # Right side - dynamic grid
        remaining_images = selected_images[1:]
        right_start_x = int(self.output_size[0] * feature_ratio) + 10
        right_width = self.output_size[0] - right_start_x - 10
        
        # Calculate optimal grid for right side
        num_images = len(remaining_images)
        if num_images <= 4:
            rows, cols = 2, 2
        elif num_images <= 6:
            rows, cols = 3, 2
        elif num_images <= 9:
            rows, cols = 3, 3
        else:
            rows, cols = 4, 3
        
        cell_width = (right_width - 5) // cols
        cell_height = (self.output_size[1] - 20) // rows
        
        for i, img_data in enumerate(remaining_images[:rows * cols]):
            row = i // cols
            col = i % cols
            
            x = right_start_x + col * (cell_width + 2)
            y = 10 + row * (cell_height + 2)
            
            img = img_data['image'].copy()
            img = self._resize_and_crop(img, cell_width - 2, cell_height - 2)
            
            if add_frames:
                img = self._add_frame(img, frame_width=1)
                img = self._resize_and_crop(img, cell_width - 2, cell_height - 2)
            
            collage.paste(img, (x, y))
        
        return collage
    
    def save_collage(self, collage, output_path):
        """Save collage with enhanced quality"""
        if collage:
            # Enhance image quality
            enhancer = ImageEnhance.Sharpness(collage)
            collage = enhancer.enhance(1.1)
            
            enhancer = ImageEnhance.Contrast(collage)
            collage = enhancer.enhance(1.03)
            
            collage.save(output_path, 'JPEG', quality=95, optimize=True)
            print(f"Ultimate collage saved to: {output_path}")
        else:
            print("No collage to save")

# Test the ultimate collage maker
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python collage_maker_v3.py <folder_path>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    # Create ultimate collage maker
    maker = UltimateCollageMaker(output_size=(1920, 1080))
    
    # Load images
    images = maker.load_images(folder_path)
    
    if not images:
        print("No images found!")
        sys.exit(1)
    
    print(f"Found {len(images)} images")
    
    # Create ultimate examples
    examples = [
        ("ultimate_mosaic.jpg", "ultimate_mosaic"),
        ("ultimate_polaroid.jpg", "perfect_polaroid"),
        ("ultimate_magazine.jpg", "smart_magazine"),
    ]
    
    for filename, method in examples:
        print(f"Creating {filename}...")
        if method == "ultimate_mosaic":
            collage = maker.create_ultimate_mosaic(images)
        elif method == "perfect_polaroid":
            collage = maker.create_perfect_polaroid(images)
        elif method == "smart_magazine":
            collage = maker.create_smart_magazine(images)
        
        if collage:
            maker.save_collage(collage, filename)
            print(f"✓ Created {filename}")
        else:
            print(f"✗ Failed to create {filename}")