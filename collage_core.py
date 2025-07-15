#!/usr/bin/env python3
"""
Collage Core - Base classes and utilities for all collage styles
"""

import os
import random
import math
import json
from abc import ABC, abstractmethod
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance


class CollageBase(ABC):
    """Base class for all collage styles"""
    
    def __init__(self, output_size=(1920, 1080), background_color=(245, 245, 245)):
        self.output_size = output_size
        self.background_color = background_color
        self.center_x = output_size[0] // 2
        self.center_y = output_size[1] // 2
        self.min_padding = 3
    
    @abstractmethod
    def create_collage(self, images, **kwargs):
        """Create collage - must be implemented by each style"""
        pass
    
    @property
    @abstractmethod
    def style_name(self):
        """Return the name of this style"""
        pass
    
    @property
    def description(self):
        """Return description of this style"""
        return f"{self.style_name} collage style"
    
    def load_images(self, folder_path):
        """Load images from folder with caption support"""
        supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        images = []
        
        # Load captions
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
    
    def _resize_to_fit(self, img, target_size, crop=False):
        """Resize image to fit within target size"""
        if crop:
            return self._resize_and_crop(img, target_size[0], target_size[1])
        else:
            img.thumbnail(target_size, Image.Resampling.LANCZOS)
            return img
    
    def _create_circular_mask(self, size):
        """Create circular mask for images"""
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        return mask
    
    def _rectangles_overlap(self, rect1, rect2):
        """Check if two rectangles overlap"""
        return not (rect1[2] < rect2[0] or rect2[2] < rect1[0] or 
                   rect1[3] < rect2[1] or rect2[3] < rect1[1])
    
    def save_collage(self, collage, output_path):
        """Save collage with enhanced quality"""
        if collage:
            # Enhance image quality
            enhancer = ImageEnhance.Sharpness(collage)
            collage = enhancer.enhance(1.1)
            
            enhancer = ImageEnhance.Contrast(collage)
            collage = enhancer.enhance(1.03)
            
            collage.save(output_path, 'JPEG', quality=95, optimize=True)
            print(f"Collage saved to: {output_path}")
        else:
            print("No collage to save")


class Rectangle:
    """Helper class for rectangle operations"""
    
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
    
    def center(self):
        return (self.x + self.width // 2, self.y + self.height // 2)


class CollageStyleRegistry:
    """Registry for all available collage styles"""
    
    _styles = {}
    
    @classmethod
    def register(cls, style_class):
        """Register a new collage style"""
        style_instance = style_class()
        cls._styles[style_instance.style_name] = style_class
        return style_class
    
    @classmethod
    def get_style(cls, style_name):
        """Get a style class by name"""
        return cls._styles.get(style_name)
    
    @classmethod
    def list_styles(cls):
        """List all available styles"""
        return list(cls._styles.keys())
    
    @classmethod
    def create_collage(cls, style_name, folder_path, output_size=(1920, 1080), **kwargs):
        """Create collage using specified style"""
        style_class = cls.get_style(style_name)
        if not style_class:
            raise ValueError(f"Unknown style: {style_name}")
        
        style_instance = style_class(output_size=output_size)
        images = style_instance.load_images(folder_path)
        
        if not images:
            print("No images found!")
            return None
        
        return style_instance.create_collage(images, **kwargs)


def register_style(style_class):
    """Decorator to register a collage style"""
    return CollageStyleRegistry.register(style_class)