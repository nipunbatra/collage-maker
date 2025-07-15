#!/usr/bin/env python3
"""
Creative Collage Styles - Additional artistic layout algorithms
"""

import os
import random
import math
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import click

class CreativeCollageMaker:
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
    
    def create_spiral_collage(self, images):
        """Create a spiral arrangement of images"""
        if not images:
            return None
        
        collage = Image.new('RGB', self.output_size, self.background_color)
        selected_images = random.sample(images, min(len(images), 15))
        
        # Spiral parameters
        image_size = 120
        spiral_spacing = 30
        
        for i, img_data in enumerate(selected_images):
            # Calculate spiral position
            angle = i * 0.8  # Angle increment
            radius = 20 + i * spiral_spacing  # Increasing radius
            
            x = self.center_x + int(radius * math.cos(angle))
            y = self.center_y + int(radius * math.sin(angle))
            
            # Process image
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
        
        return collage
    
    def create_hexagon_collage(self, images):
        """Create hexagonal honeycomb layout"""
        if not images:
            return None
        
        collage = Image.new('RGB', self.output_size, self.background_color)
        selected_images = random.sample(images, min(len(images), 20))
        
        # Hexagon parameters
        hex_size = 100
        hex_width = int(hex_size * math.sqrt(3))
        hex_height = int(hex_size * 1.5)
        
        # Calculate grid
        cols = self.output_size[0] // hex_width + 2
        rows = self.output_size[1] // hex_height + 2
        
        image_index = 0
        
        for row in range(rows):
            for col in range(cols):
                if image_index >= len(selected_images):
                    break
                
                # Calculate hexagon center
                x = col * hex_width
                if row % 2 == 1:  # Offset every other row
                    x += hex_width // 2
                
                y = row * hex_height
                
                # Skip if outside canvas
                if x + hex_size > self.output_size[0] or y + hex_size > self.output_size[1]:
                    continue
                
                # Create hexagonal image
                img_data = selected_images[image_index]
                img = img_data['image'].copy()
                img = self._resize_and_crop(img, hex_size * 2, hex_size * 2)
                
                # Create hexagon mask
                mask = Image.new('L', (hex_size * 2, hex_size * 2), 0)
                draw = ImageDraw.Draw(mask)
                
                # Calculate hexagon points
                points = []
                for i in range(6):
                    angle = i * math.pi / 3
                    px = hex_size + int(hex_size * 0.8 * math.cos(angle))
                    py = hex_size + int(hex_size * 0.8 * math.sin(angle))
                    points.append((px, py))
                
                draw.polygon(points, fill=255)
                
                # Apply mask
                img.putalpha(mask)
                
                # Position on collage
                collage.paste(img, (x, y), img)
                image_index += 1
        
        return collage
    
    def create_film_strip_collage(self, images):
        """Create film strip/contact sheet style"""
        if not images:
            return None
        
        # Film strip background (dark)
        collage = Image.new('RGB', self.output_size, (20, 20, 20))
        
        # Film parameters
        frame_width = 200
        frame_height = 150
        margin = 20
        perforation_size = 8
        
        # Calculate grid
        cols = (self.output_size[0] - margin * 2) // (frame_width + margin)
        rows = (self.output_size[1] - margin * 2) // (frame_height + margin)
        
        selected_images = random.sample(images, min(len(images), rows * cols))
        
        # Draw film perforations
        draw = ImageDraw.Draw(collage)
        perforation_spacing = 20
        
        # Top and bottom perforations
        for x in range(0, self.output_size[0], perforation_spacing):
            # Top perforations
            draw.rectangle([x, 0, x + perforation_size, perforation_size], fill=(40, 40, 40))
            # Bottom perforations
            draw.rectangle([x, self.output_size[1] - perforation_size, x + perforation_size, self.output_size[1]], fill=(40, 40, 40))
        
        # Left and right perforations
        for y in range(0, self.output_size[1], perforation_spacing):
            # Left perforations
            draw.rectangle([0, y, perforation_size, y + perforation_size], fill=(40, 40, 40))
            # Right perforations
            draw.rectangle([self.output_size[0] - perforation_size, y, self.output_size[0], y + perforation_size], fill=(40, 40, 40))
        
        # Place images in frames
        for i, img_data in enumerate(selected_images):
            row = i // cols
            col = i % cols
            
            x = margin + perforation_size + col * (frame_width + margin)
            y = margin + perforation_size + row * (frame_height + margin)
            
            # Process image
            img = img_data['image'].copy()
            img = self._resize_and_crop(img, frame_width - 10, frame_height - 10)
            
            # Add white border (film frame)
            framed = Image.new('RGB', (frame_width, frame_height), (240, 240, 240))
            frame_x = (frame_width - img.width) // 2
            frame_y = (frame_height - img.height) // 2
            framed.paste(img, (frame_x, frame_y))
            
            collage.paste(framed, (x, y))
        
        return collage
    
    def create_scrapbook_collage(self, images):
        """Create artistic scrapbook style with overlapping"""
        if not images:
            return None
        
        collage = Image.new('RGB', self.output_size, (250, 245, 235))  # Cream background
        selected_images = random.sample(images, min(len(images), 12))
        
        # Scrapbook elements
        tape_color = (220, 200, 160, 180)  # Semi-transparent tape
        
        for i, img_data in enumerate(selected_images):
            # Random size and position
            size_factor = random.uniform(0.8, 1.5)
            img_width = int(200 * size_factor)
            img_height = int(150 * size_factor)
            
            x = random.randint(0, max(0, self.output_size[0] - img_width))
            y = random.randint(0, max(0, self.output_size[1] - img_height))
            
            # Process image
            img = img_data['image'].copy()
            img = self._resize_and_crop(img, img_width, img_height)
            
            # Add white border (photo border)
            border_width = random.randint(8, 15)
            bordered = Image.new('RGB', 
                               (img_width + border_width * 2, img_height + border_width * 2), 
                               (255, 255, 255))
            bordered.paste(img, (border_width, border_width))
            
            # Random rotation
            angle = random.randint(-15, 15)
            rotated = bordered.rotate(angle, expand=True, fillcolor=self.background_color)
            
            # Adjust position for rotation
            final_x = max(0, min(x - (rotated.width - bordered.width) // 2, 
                               self.output_size[0] - rotated.width))
            final_y = max(0, min(y - (rotated.height - bordered.height) // 2, 
                               self.output_size[1] - rotated.height))
            
            collage.paste(rotated, (final_x, final_y))
            
            # Add tape effect
            tape_overlay = Image.new('RGBA', self.output_size, (0, 0, 0, 0))
            tape_draw = ImageDraw.Draw(tape_overlay)
            
            # Random tape positions
            for _ in range(random.randint(1, 3)):
                tape_x = final_x + random.randint(-20, rotated.width - 20)
                tape_y = final_y + random.randint(-10, rotated.height - 10)
                tape_w = random.randint(40, 80)
                tape_h = random.randint(15, 25)
                
                tape_draw.rectangle([tape_x, tape_y, tape_x + tape_w, tape_y + tape_h], 
                                  fill=tape_color)
            
            collage = Image.alpha_composite(collage.convert('RGBA'), tape_overlay).convert('RGB')
        
        return collage
    
    def create_puzzle_collage(self, images):
        """Create jigsaw puzzle piece layout"""
        if not images:
            return None
        
        collage = Image.new('RGB', self.output_size, (240, 240, 240))
        selected_images = random.sample(images, min(len(images), 16))
        
        # Puzzle parameters
        piece_size = 150
        overlap = 20
        
        # Calculate grid
        cols = (self.output_size[0] - overlap) // (piece_size - overlap)
        rows = (self.output_size[1] - overlap) // (piece_size - overlap)
        
        for i, img_data in enumerate(selected_images[:rows * cols]):
            row = i // cols
            col = i % cols
            
            x = col * (piece_size - overlap)
            y = row * (piece_size - overlap)
            
            # Process image
            img = img_data['image'].copy()
            img = self._resize_and_crop(img, piece_size, piece_size)
            
            # Create puzzle piece mask (simplified)
            mask = Image.new('L', (piece_size, piece_size), 0)
            draw = ImageDraw.Draw(mask)
            
            # Basic puzzle piece shape
            points = [
                (10, 10), (piece_size - 10, 10),
                (piece_size - 10, piece_size // 2 - 15),
                (piece_size - 5, piece_size // 2),
                (piece_size - 10, piece_size // 2 + 15),
                (piece_size - 10, piece_size - 10),
                (piece_size // 2 + 15, piece_size - 10),
                (piece_size // 2, piece_size - 5),
                (piece_size // 2 - 15, piece_size - 10),
                (10, piece_size - 10),
                (10, piece_size // 2 + 15),
                (5, piece_size // 2),
                (10, piece_size // 2 - 15)
            ]
            
            draw.polygon(points, fill=255)
            
            # Apply mask
            img.putalpha(mask)
            
            # Add shadow
            shadow = Image.new('RGBA', (piece_size + 5, piece_size + 5), (0, 0, 0, 50))
            collage.paste(shadow, (x + 2, y + 2), shadow)
            
            # Paste piece
            collage.paste(img, (x, y), img)
        
        return collage
    
    def save_collage(self, collage, output_path):
        """Save collage with quality enhancement"""
        if collage:
            enhancer = ImageEnhance.Sharpness(collage)
            collage = enhancer.enhance(1.1)
            
            collage.save(output_path, 'JPEG', quality=95, optimize=True)
            print(f"Creative collage saved to: {output_path}")

def main():
    maker = CreativeCollageMaker(output_size=(1920, 1080))
    images = maker.load_images('sample_images')
    
    if not images:
        print("No images found!")
        return
    
    print(f"Found {len(images)} images")
    
    # Create creative examples
    styles = [
        ("spiral", "create_spiral_collage"),
        ("hexagon", "create_hexagon_collage"),
        ("filmstrip", "create_film_strip_collage"),
        ("scrapbook", "create_scrapbook_collage"),
        ("puzzle", "create_puzzle_collage"),
    ]
    
    for style_name, method_name in styles:
        print(f"Creating {style_name} collage...")
        method = getattr(maker, method_name)
        collage = method(images)
        
        if collage:
            filename = f"creative_{style_name}.jpg"
            maker.save_collage(collage, filename)
            print(f"✓ Created {filename}")

if __name__ == "__main__":
    main()