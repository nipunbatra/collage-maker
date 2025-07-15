#!/usr/bin/env python3
"""
Geometric Collage Styles - Mathematical and pattern-based layouts
"""

import random
import math
from PIL import Image, ImageDraw
from collage_core import CollageBase, register_style


@register_style
class MandalaStyle(CollageBase):
    """Mandala-style circular arrangement"""
    
    @property
    def style_name(self):
        return "mandala"
    
    @property
    def description(self):
        return "Mandala-style circular arrangement with multiple rings"
    
    def create_collage(self, images, **kwargs):
        """Create mandala collage"""
        if not images:
            return None
        
        collage = Image.new('RGB', self.output_size, self.background_color)
        selected_images = random.sample(images, min(len(images), 12))
        
        rings = 3
        max_radius = min(self.output_size[0], self.output_size[1]) // 2 - 50
        
        img_index = 0
        
        for ring in range(rings):
            if img_index >= len(selected_images):
                break
            
            radius = (ring + 1) * max_radius // rings
            num_images = (ring + 1) * 4
            image_size = max(60 - ring * 15, 40)
            
            for i in range(min(num_images, len(selected_images) - img_index)):
                angle = 2 * math.pi * i / num_images
                
                x = self.center_x + int(radius * math.cos(angle))
                y = self.center_y + int(radius * math.sin(angle))
                
                # Create circular image
                img_data = selected_images[img_index]
                circular_img = self._create_circular_image(img_data, image_size)
                
                final_x = max(0, min(x - image_size // 2, self.output_size[0] - image_size))
                final_y = max(0, min(y - image_size // 2, self.output_size[1] - image_size))
                
                collage.paste(circular_img, (final_x, final_y), circular_img)
                
                img_index += 1
                if img_index >= len(selected_images):
                    break
        
        # Add center image
        if img_index < len(selected_images):
            center_img = self._create_circular_image(selected_images[0], 120)
            center_x = self.center_x - 60
            center_y = self.center_y - 60
            collage.paste(center_img, (center_x, center_y), center_img)
        
        return collage
    
    def _create_circular_image(self, img_data, size):
        """Create circular image"""
        img = img_data['image'].copy()
        img = self._resize_and_crop(img, size, size)
        
        mask = self._create_circular_mask((size, size))
        img.putalpha(mask)
        
        return img


@register_style
class VoronoiStyle(CollageBase):
    """Voronoi diagram style collage"""
    
    @property
    def style_name(self):
        return "voronoi"
    
    @property
    def description(self):
        return "Voronoi diagram with organic cell-like divisions"
    
    def create_collage(self, images, **kwargs):
        """Create Voronoi diagram collage"""
        if not images:
            return None
        
        collage = Image.new('RGB', self.output_size, self.background_color)
        selected_images = random.sample(images, min(len(images), 8))
        
        # Generate seed points
        seed_points = []
        for i in range(len(selected_images)):
            x = random.randint(100, self.output_size[0] - 100)
            y = random.randint(100, self.output_size[1] - 100)
            seed_points.append((x, y))
        
        # Create Voronoi cells
        for img_idx, (seed_x, seed_y) in enumerate(seed_points):
            img_data = selected_images[img_idx]
            
            # Create mask for this cell
            mask = self._create_voronoi_mask(seed_points, img_idx)
            
            # Process image
            img = img_data['image'].copy()
            img = img.resize(self.output_size, Image.Resampling.LANCZOS)
            
            # Apply mask
            img.putalpha(mask)
            collage.paste(img, (0, 0), img)
        
        return collage
    
    def _create_voronoi_mask(self, seed_points, target_idx):
        """Create mask for Voronoi cell"""
        mask = Image.new('L', self.output_size, 0)
        
        # Sample every 4 pixels for performance
        for y in range(0, self.output_size[1], 4):
            for x in range(0, self.output_size[0], 4):
                min_dist = float('inf')
                closest_seed = -1
                
                for i, (sx, sy) in enumerate(seed_points):
                    dist = math.sqrt((x - sx) ** 2 + (y - sy) ** 2)
                    if dist < min_dist:
                        min_dist = dist
                        closest_seed = i
                
                if closest_seed == target_idx:
                    # Fill 4x4 block
                    for dy in range(4):
                        for dx in range(4):
                            if x + dx < self.output_size[0] and y + dy < self.output_size[1]:
                                mask.putpixel((x + dx, y + dy), 255)
        
        return mask


@register_style
class FractalStyle(CollageBase):
    """Fractal recursive layout"""
    
    @property
    def style_name(self):
        return "fractal"
    
    @property
    def description(self):
        return "Fractal recursive subdivision pattern"
    
    def create_collage(self, images, **kwargs):
        """Create fractal collage"""
        if not images:
            return None
        
        collage = Image.new('RGB', self.output_size, self.background_color)
        selected_images = random.sample(images, min(len(images), 16))
        
        self.img_index = 0
        self.selected_images = selected_images
        self.collage = collage
        
        # Start fractal recursion
        self._draw_fractal_rectangle(0, 0, self.output_size[0], self.output_size[1], 3)
        
        return collage
    
    def _draw_fractal_rectangle(self, x, y, width, height, depth):
        """Recursive fractal subdivision"""
        if depth <= 0 or self.img_index >= len(self.selected_images):
            return
        
        # Draw image in current rectangle
        if width > 50 and height > 50:
            img_data = self.selected_images[self.img_index % len(self.selected_images)]
            img = img_data['image'].copy()
            img = self._resize_and_crop(img, width - 4, height - 4)
            
            # Add border
            bordered = Image.new('RGB', (width, height), (255, 255, 255))
            bordered.paste(img, (2, 2))
            
            self.collage.paste(bordered, (x, y))
            self.img_index += 1
        
        # Recursive subdivision
        if depth > 1:
            half_w = width // 2
            half_h = height // 2
            
            # Split into 4 quadrants
            self._draw_fractal_rectangle(x, y, half_w, half_h, depth - 1)
            self._draw_fractal_rectangle(x + half_w, y, half_w, half_h, depth - 1)
            self._draw_fractal_rectangle(x, y + half_h, half_w, half_h, depth - 1)
            self._draw_fractal_rectangle(x + half_w, y + half_h, half_w, half_h, depth - 1)


@register_style
class KaleidoscopeStyle(CollageBase):
    """Kaleidoscope symmetrical pattern"""
    
    @property
    def style_name(self):
        return "kaleidoscope"
    
    @property
    def description(self):
        return "Kaleidoscope symmetrical pattern with reflections"
    
    def create_collage(self, images, **kwargs):
        """Create kaleidoscope collage"""
        if not images:
            return None
        
        # Create base triangle
        triangle_size = min(self.output_size[0], self.output_size[1]) // 2
        base_triangle = self._create_base_triangle(images, triangle_size)
        
        # Create kaleidoscope by reflecting the triangle
        collage = Image.new('RGB', self.output_size, self.background_color)
        
        # Create 6 reflections around center
        for i in range(6):
            angle = i * 60
            rotated = base_triangle.rotate(angle, center=(triangle_size//2, triangle_size//2))
            
            offset_x = self.center_x - triangle_size // 2
            offset_y = self.center_y - triangle_size // 2
            
            collage.paste(rotated, (offset_x, offset_y), 
                         rotated if rotated.mode == 'RGBA' else None)
        
        return collage
    
    def _create_base_triangle(self, images, triangle_size):
        """Create base triangle for kaleidoscope"""
        base_triangle = Image.new('RGB', (triangle_size, triangle_size), self.background_color)
        selected_images = random.sample(images, min(len(images), 6))
        
        segment_height = triangle_size // len(selected_images)
        
        for i, img_data in enumerate(selected_images):
            img = img_data['image'].copy()
            
            y_start = i * segment_height
            y_end = min((i + 1) * segment_height, triangle_size)
            segment_width = int((triangle_size - y_start) * 2)
            
            if segment_width > 0:
                img = self._resize_and_crop(img, segment_width, y_end - y_start)
                
                # Create triangular mask
                mask = Image.new('L', (segment_width, y_end - y_start), 0)
                mask_draw = ImageDraw.Draw(mask)
                
                points = [(0, 0), (segment_width, 0), (segment_width // 2, y_end - y_start)]
                mask_draw.polygon(points, fill=255)
                
                img.putalpha(mask)
                
                x_offset = (triangle_size - segment_width) // 2
                base_triangle.paste(img, (x_offset, y_start), img)
        
        return base_triangle