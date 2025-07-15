#!/usr/bin/env python3
"""
Example: How to create a new collage style

This file demonstrates how easy it is to add a new style to the modular system.
Just inherit from CollageBase, implement the required methods, and use the @register_style decorator.
"""

import random
import math
from PIL import Image, ImageDraw
from collage_core import CollageBase, register_style


@register_style
class DiamondStyle(CollageBase):
    """Example: Diamond-shaped layout"""
    
    @property
    def style_name(self):
        return "diamond"
    
    @property
    def description(self):
        return "Diamond-shaped arrangement of images"
    
    def create_collage(self, images, **kwargs):
        """Create diamond collage - this is the main method you need to implement"""
        if not images:
            return None
        
        collage = Image.new('RGB', self.output_size, self.background_color)
        selected_images = random.sample(images, min(len(images), 9))
        
        # Diamond positions (center + 8 around it)
        positions = [
            (self.center_x, self.center_y),  # Center
            (self.center_x, self.center_y - 150),  # Top
            (self.center_x + 106, self.center_y - 106),  # Top-right
            (self.center_x + 150, self.center_y),  # Right
            (self.center_x + 106, self.center_y + 106),  # Bottom-right
            (self.center_x, self.center_y + 150),  # Bottom
            (self.center_x - 106, self.center_y + 106),  # Bottom-left
            (self.center_x - 150, self.center_y),  # Left
            (self.center_x - 106, self.center_y - 106),  # Top-left
        ]
        
        image_size = 100
        
        for i, img_data in enumerate(selected_images):
            if i >= len(positions):
                break
            
            x, y = positions[i]
            
            # Process image into diamond shape
            img = img_data['image'].copy()
            img = self._resize_and_crop(img, image_size, image_size)
            
            # Create diamond mask
            mask = Image.new('L', (image_size, image_size), 0)
            draw = ImageDraw.Draw(mask)
            
            # Diamond points
            diamond_points = [
                (image_size // 2, 0),  # Top
                (image_size, image_size // 2),  # Right
                (image_size // 2, image_size),  # Bottom
                (0, image_size // 2),  # Left
            ]
            
            draw.polygon(diamond_points, fill=255)
            
            # Apply mask
            img.putalpha(mask)
            
            # Position on collage
            final_x = max(0, min(x - image_size // 2, self.output_size[0] - image_size))
            final_y = max(0, min(y - image_size // 2, self.output_size[1] - image_size))
            
            collage.paste(img, (final_x, final_y), img)
        
        return collage


# You can add multiple styles in one file
@register_style  
class WaveStyle(CollageBase):
    """Example: Wave-pattern layout"""
    
    @property
    def style_name(self):
        return "wave"
    
    @property  
    def description(self):
        return "Wave-pattern flowing layout"
    
    def create_collage(self, images, **kwargs):
        """Create wave collage"""
        if not images:
            return None
        
        collage = Image.new('RGB', self.output_size, self.background_color)
        selected_images = random.sample(images, min(len(images), 12))
        
        image_size = 80
        amplitude = 100  # Wave height
        frequency = 2   # Number of wave cycles
        
        for i, img_data in enumerate(selected_images):
            # Calculate wave position
            x_progress = i / (len(selected_images) - 1) if len(selected_images) > 1 else 0
            x = int(x_progress * (self.output_size[0] - image_size))
            
            # Calculate y position based on sine wave
            wave_y = math.sin(x_progress * frequency * 2 * math.pi) * amplitude
            y = self.center_y + int(wave_y) - image_size // 2
            
            # Ensure within bounds
            y = max(0, min(y, self.output_size[1] - image_size))
            
            # Process image
            img = img_data['image'].copy()
            img = self._resize_and_crop(img, image_size, image_size)
            
            # Make circular
            mask = self._create_circular_mask((image_size, image_size))
            img.putalpha(mask)
            
            collage.paste(img, (x, y), img)
        
        return collage


# To use these new styles, just import this file in your main script
# or add the import to __init__.py in the styles package