#!/usr/bin/env python3
"""
Advanced Artistic Collage Styles - Cutting-edge layouts
"""

import os
import random
import math
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

class AdvancedCollageMaker:
    def __init__(self, output_size=(1920, 1080), background_color=(245, 245, 245)):
        self.output_size = output_size
        self.background_color = background_color
        self.center_x = output_size[0] // 2
        self.center_y = output_size[1] // 2
        
    def load_images(self, folder_path):
        """Load images from folder"""
        supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        images = []
        
        for filename in os.listdir(folder_path):
            if any(filename.lower().endswith(ext) for ext in supported_formats):
                try:
                    img_path = os.path.join(folder_path, filename)
                    img = Image.open(img_path)
                    img = img.convert('RGB')
                    images.append({'image': img, 'filename': filename})
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
        return images
    
    def _resize_and_crop(self, img, target_width, target_height):
        """Resize and crop to exact dimensions"""
        scale_x = target_width / img.width
        scale_y = target_height / img.height
        scale = max(scale_x, scale_y)
        
        new_width = int(img.width * scale)
        new_height = int(img.height * scale)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        if new_width > target_width:
            left = (new_width - target_width) // 2
            img = img.crop((left, 0, left + target_width, new_height))
        
        if new_height > target_height:
            top = (new_height - target_height) // 2
            img = img.crop((0, top, new_width, top + target_height))
        
        return img
    
    def create_voronoi_collage(self, images):
        """Create Voronoi diagram style collage"""
        if not images:
            return None
        
        collage = Image.new('RGB', self.output_size, self.background_color)
        selected_images = random.sample(images, min(len(images), 12))
        
        # Generate random seed points
        seed_points = []
        for i in range(len(selected_images)):
            x = random.randint(100, self.output_size[0] - 100)
            y = random.randint(100, self.output_size[1] - 100)
            seed_points.append((x, y))
        
        # Create Voronoi cells
        for img_idx, (seed_x, seed_y) in enumerate(seed_points):
            img_data = selected_images[img_idx]
            
            # Create mask for this Voronoi cell
            mask = Image.new('L', self.output_size, 0)
            
            # For each pixel, check which seed point is closest
            for y in range(0, self.output_size[1], 4):  # Sample every 4 pixels for speed
                for x in range(0, self.output_size[0], 4):
                    min_dist = float('inf')
                    closest_seed = -1
                    
                    for i, (sx, sy) in enumerate(seed_points):
                        dist = math.sqrt((x - sx) ** 2 + (y - sy) ** 2)
                        if dist < min_dist:
                            min_dist = dist
                            closest_seed = i
                    
                    if closest_seed == img_idx:
                        # Fill 4x4 block
                        for dy in range(4):
                            for dx in range(4):
                                if x + dx < self.output_size[0] and y + dy < self.output_size[1]:
                                    mask.putpixel((x + dx, y + dy), 255)
            
            # Process image for this cell
            img = img_data['image'].copy()
            img = img.resize(self.output_size, Image.Resampling.LANCZOS)
            
            # Apply mask
            img.putalpha(mask)
            collage.paste(img, (0, 0), img)
        
        return collage
    
    def create_fractal_collage(self, images):
        """Create fractal-inspired recursive layout"""
        if not images:
            return None
        
        collage = Image.new('RGB', self.output_size, self.background_color)
        selected_images = random.sample(images, min(len(images), 16))
        
        def draw_fractal_rectangle(x, y, width, height, depth, img_index):
            if depth <= 0 or img_index >= len(selected_images):
                return img_index
            
            # Draw image in current rectangle
            if width > 50 and height > 50:  # Minimum size check
                img_data = selected_images[img_index % len(selected_images)]
                img = img_data['image'].copy()
                img = self._resize_and_crop(img, width - 4, height - 4)
                
                # Add border
                bordered = Image.new('RGB', (width, height), (255, 255, 255))
                bordered.paste(img, (2, 2))
                
                collage.paste(bordered, (x, y))
                img_index += 1
            
            # Recursive subdivision
            if depth > 1:
                # Split into 4 quadrants
                half_w = width // 2
                half_h = height // 2
                
                # Top-left
                img_index = draw_fractal_rectangle(x, y, half_w, half_h, depth - 1, img_index)
                # Top-right
                img_index = draw_fractal_rectangle(x + half_w, y, half_w, half_h, depth - 1, img_index)
                # Bottom-left
                img_index = draw_fractal_rectangle(x, y + half_h, half_w, half_h, depth - 1, img_index)
                # Bottom-right
                img_index = draw_fractal_rectangle(x + half_w, y + half_h, half_w, half_h, depth - 1, img_index)
            
            return img_index
        
        # Start fractal recursion
        draw_fractal_rectangle(0, 0, self.output_size[0], self.output_size[1], 3, 0)
        
        return collage
    
    def create_mandala_collage(self, images):
        """Create mandala-style circular arrangement"""
        if not images:
            return None
        
        collage = Image.new('RGB', self.output_size, self.background_color)
        selected_images = random.sample(images, min(len(images), 12))
        
        # Mandala parameters
        rings = 3
        max_radius = min(self.output_size[0], self.output_size[1]) // 2 - 50
        
        img_index = 0
        
        for ring in range(rings):
            if img_index >= len(selected_images):
                break
            
            # Calculate ring parameters
            radius = (ring + 1) * max_radius // rings
            num_images = (ring + 1) * 4  # More images in outer rings
            image_size = max(60 - ring * 15, 40)  # Smaller images in outer rings
            
            for i in range(min(num_images, len(selected_images) - img_index)):
                angle = 2 * math.pi * i / num_images
                
                x = self.center_x + int(radius * math.cos(angle))
                y = self.center_y + int(radius * math.sin(angle))
                
                # Process image
                img_data = selected_images[img_index]
                img = img_data['image'].copy()
                img = self._resize_and_crop(img, image_size, image_size)
                
                # Create circular mask
                mask = Image.new('L', (image_size, image_size), 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, image_size, image_size), fill=255)
                
                # Apply mask
                img.putalpha(mask)
                
                # Position on collage
                final_x = max(0, min(x - image_size // 2, self.output_size[0] - image_size))
                final_y = max(0, min(y - image_size // 2, self.output_size[1] - image_size))
                
                collage.paste(img, (final_x, final_y), img)
                
                img_index += 1
                if img_index >= len(selected_images):
                    break
        
        # Add center image
        if img_index < len(selected_images):
            center_img = selected_images[0]['image'].copy()
            center_size = 120
            center_img = self._resize_and_crop(center_img, center_size, center_size)
            
            # Circular mask
            mask = Image.new('L', (center_size, center_size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, center_size, center_size), fill=255)
            center_img.putalpha(mask)
            
            center_x = self.center_x - center_size // 2
            center_y = self.center_y - center_size // 2
            collage.paste(center_img, (center_x, center_y), center_img)
        
        return collage
    
    def create_origami_collage(self, images):
        """Create origami-folded paper effect"""
        if not images:
            return None
        
        collage = Image.new('RGB', self.output_size, (250, 248, 245))  # Paper color
        selected_images = random.sample(images, min(len(images), 8))
        
        for i, img_data in enumerate(selected_images):
            # Random position and size
            size = random.randint(150, 300)
            x = random.randint(0, max(0, self.output_size[0] - size))
            y = random.randint(0, max(0, self.output_size[1] - size))
            
            # Process image
            img = img_data['image'].copy()
            img = self._resize_and_crop(img, size, size)
            
            # Create origami fold effect
            fold_angle = random.choice([45, -45, 135, -135])
            
            # Create diamond/square rotation effect
            rotated = img.rotate(fold_angle, expand=True, fillcolor=(240, 240, 240))
            
            # Create fold shadow
            shadow = Image.new('RGBA', rotated.size, (0, 0, 0, 30))
            shadow_mask = Image.new('L', rotated.size, 0)
            shadow_draw = ImageDraw.Draw(shadow_mask)
            
            # Draw diagonal fold line shadow
            if fold_angle in [45, -135]:
                shadow_draw.polygon([(0, rotated.height//2), (rotated.width//2, 0), 
                                   (rotated.width, rotated.height//2), (rotated.width//2, rotated.height)], 
                                  fill=255)
            else:
                shadow_draw.polygon([(rotated.width//2, 0), (rotated.width, rotated.height//2), 
                                   (rotated.width//2, rotated.height), (0, rotated.height//2)], 
                                  fill=255)
            
            shadow.putalpha(shadow_mask)
            
            # Adjust position for rotated size
            final_x = max(0, min(x - (rotated.width - size) // 2, 
                               self.output_size[0] - rotated.width))
            final_y = max(0, min(y - (rotated.height - size) // 2, 
                               self.output_size[1] - rotated.height))
            
            # Paste shadow first
            collage = Image.alpha_composite(collage.convert('RGBA'), 
                                          Image.new('RGBA', collage.size, (0, 0, 0, 0))).convert('RGB')
            
            # Paste image
            collage.paste(rotated, (final_x, final_y))
        
        return collage
    
    def create_kaleidoscope_collage(self, images):
        """Create kaleidoscope symmetrical pattern"""
        if not images:
            return None
        
        # Create base triangle
        triangle_size = min(self.output_size[0], self.output_size[1]) // 2
        base_triangle = Image.new('RGB', (triangle_size, triangle_size), self.background_color)
        
        # Fill triangle with image segments
        selected_images = random.sample(images, min(len(images), 6))
        
        segment_height = triangle_size // len(selected_images)
        
        for i, img_data in enumerate(selected_images):
            img = img_data['image'].copy()
            
            # Create triangular segment
            y_start = i * segment_height
            y_end = min((i + 1) * segment_height, triangle_size)
            segment_width = int((triangle_size - y_start) * 2)  # Triangle width at this height
            
            if segment_width > 0:
                img = self._resize_and_crop(img, segment_width, y_end - y_start)
                
                # Create triangular mask for this segment
                mask = Image.new('L', (segment_width, y_end - y_start), 0)
                mask_draw = ImageDraw.Draw(mask)
                
                # Draw triangle part
                points = [(0, 0), (segment_width, 0), (segment_width // 2, y_end - y_start)]
                mask_draw.polygon(points, fill=255)
                
                img.putalpha(mask)
                
                # Position in base triangle
                x_offset = (triangle_size - segment_width) // 2
                base_triangle.paste(img, (x_offset, y_start), img)
        
        # Create kaleidoscope by reflecting the triangle
        collage = Image.new('RGB', self.output_size, self.background_color)
        
        # Create 6 reflections around center
        for i in range(6):
            angle = i * 60
            rotated = base_triangle.rotate(angle, center=(triangle_size//2, triangle_size//2))
            
            # Position each triangle
            offset_x = self.center_x - triangle_size // 2
            offset_y = self.center_y - triangle_size // 2
            
            collage.paste(rotated, (offset_x, offset_y), rotated if rotated.mode == 'RGBA' else None)
        
        return collage
    
    def save_collage(self, collage, output_path):
        """Save collage with quality enhancement"""
        if collage:
            enhancer = ImageEnhance.Sharpness(collage)
            collage = enhancer.enhance(1.1)
            
            collage.save(output_path, 'JPEG', quality=95, optimize=True)
            print(f"Advanced collage saved to: {output_path}")

def main():
    maker = AdvancedCollageMaker(output_size=(1920, 1080))
    images = maker.load_images('sample_images')
    
    if not images:
        print("No images found!")
        return
    
    print(f"Found {len(images)} images")
    
    # Create advanced examples
    styles = [
        ("voronoi", "create_voronoi_collage"),
        ("fractal", "create_fractal_collage"),
        ("mandala", "create_mandala_collage"),
        ("origami", "create_origami_collage"),
        ("kaleidoscope", "create_kaleidoscope_collage"),
    ]
    
    for style_name, method_name in styles:
        print(f"Creating {style_name} collage...")
        method = getattr(maker, method_name)
        collage = method(images)
        
        if collage:
            filename = f"advanced_{style_name}.jpg"
            maker.save_collage(collage, filename)
            print(f"✓ Created {filename}")

if __name__ == "__main__":
    main()