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

# Enable HEIC support
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    HEIC_SUPPORTED = True
except ImportError:
    HEIC_SUPPORTED = False


class CollageBase(ABC):
    """Base class for all collage styles"""

    # Predefined background presets
    BACKGROUND_PRESETS = {
        # Solid colors
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'cream': (255, 253, 245),
        'charcoal': (54, 57, 63),
        'slate': (47, 49, 54),
        'navy': (25, 45, 75),
        'forest': (34, 49, 39),
        'burgundy': (74, 25, 36),
        'mocha': (62, 47, 39),

        # Gradient presets (start_color, end_color, direction)
        'sunset': ((255, 87, 51), (255, 195, 113), 'diagonal'),
        'ocean': ((0, 119, 182), (144, 224, 239), 'vertical'),
        'aurora': ((15, 32, 39), (44, 83, 100), 'vertical'),
        'lavender': ((230, 230, 250), (186, 156, 205), 'diagonal'),
        'coral': ((255, 154, 139), (255, 218, 193), 'horizontal'),
        'mint': ((162, 217, 206), (227, 253, 245), 'vertical'),
        'rose': ((255, 228, 225), (255, 182, 193), 'diagonal'),
        'twilight': ((10, 10, 35), (75, 35, 100), 'vertical'),
        'golden': ((255, 215, 0), (255, 248, 220), 'radial'),
        'arctic': ((174, 198, 207), (224, 237, 241), 'vertical'),
        'noir': ((30, 30, 30), (80, 80, 80), 'diagonal'),
        'peach': ((255, 218, 185), (255, 239, 219), 'vertical'),
        'emerald': ((0, 105, 92), (129, 199, 132), 'diagonal'),
        'vintage': ((210, 180, 140), (245, 235, 220), 'vertical'),
    }

    def __init__(self, output_size=(1920, 1080), background_color=(245, 245, 245), background=None):
        self.output_size = output_size
        self.background_color = background_color
        self.background = background  # Can be preset name, tuple, or gradient spec
        self.center_x = output_size[0] // 2
        self.center_y = output_size[1] // 2
        self.min_padding = 3
        self.title_height = 80  # Reserved space for title

    def _create_background(self):
        """Create background image based on settings"""
        if self.background is None:
            return Image.new('RGB', self.output_size, self.background_color)

        # Check if it's a preset name
        if isinstance(self.background, str) and self.background in self.BACKGROUND_PRESETS:
            preset = self.BACKGROUND_PRESETS[self.background]

            # Solid color preset
            if isinstance(preset, tuple) and len(preset) == 3 and isinstance(preset[0], int):
                return Image.new('RGB', self.output_size, preset)

            # Gradient preset
            elif isinstance(preset, tuple) and len(preset) == 3:
                start_color, end_color, direction = preset
                return self._create_gradient(start_color, end_color, direction)

        # Direct gradient specification: (start_color, end_color, direction)
        elif isinstance(self.background, tuple) and len(self.background) == 3:
            if isinstance(self.background[0], tuple):
                start_color, end_color, direction = self.background
                return self._create_gradient(start_color, end_color, direction)
            else:
                # Solid color tuple
                return Image.new('RGB', self.output_size, self.background)

        # Default fallback
        return Image.new('RGB', self.output_size, self.background_color)

    def _create_gradient(self, start_color, end_color, direction='vertical'):
        """Create gradient background"""
        img = Image.new('RGB', self.output_size)
        draw = ImageDraw.Draw(img)

        width, height = self.output_size

        if direction == 'vertical':
            for y in range(height):
                ratio = y / height
                r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
                g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
                b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b))

        elif direction == 'horizontal':
            for x in range(width):
                ratio = x / width
                r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
                g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
                b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
                draw.line([(x, 0), (x, height)], fill=(r, g, b))

        elif direction == 'diagonal':
            for y in range(height):
                for x in range(width):
                    ratio = (x + y) / (width + height)
                    r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
                    g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
                    b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
                    draw.point((x, y), fill=(r, g, b))

        elif direction == 'radial':
            center_x, center_y = width // 2, height // 2
            max_dist = math.sqrt(center_x**2 + center_y**2)
            for y in range(height):
                for x in range(width):
                    dist = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                    ratio = min(dist / max_dist, 1.0)
                    r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
                    g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
                    b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
                    draw.point((x, y), fill=(r, g, b))

        return img
    
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
        if HEIC_SUPPORTED:
            supported_formats.update({'.heic', '.heif'})
        images = []
        
        # Show supported formats on first load
        formats_str = ', '.join(sorted(supported_formats))
        print(f"Supported image formats: {formats_str}")
        
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
    
    def _add_title_overlay(self, collage, title, position='bottom'):
        """Add title as overlay on the collage"""
        if not title:
            return collage
        
        # Create a copy to work with
        titled_collage = collage.copy()
        draw = ImageDraw.Draw(titled_collage)
        
        # Try to load a nice font, fall back to default
        try:
            font_size = min(self.output_size[0] // 25, 72)  # Adaptive font size
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        # Calculate text dimensions
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate position based on preference
        if position == 'top':
            text_x = (self.output_size[0] - text_width) // 2
            text_y = 20
        elif position == 'bottom':
            text_x = (self.output_size[0] - text_width) // 2
            text_y = self.output_size[1] - text_height - 20
        elif position == 'center':
            text_x = (self.output_size[0] - text_width) // 2
            text_y = (self.output_size[1] - text_height) // 2
        else:  # bottom default
            text_x = (self.output_size[0] - text_width) // 2
            text_y = self.output_size[1] - text_height - 20
        
        # Add semi-transparent background for better readability
        padding = 20
        bg_x1 = text_x - padding
        bg_y1 = text_y - padding//2
        bg_x2 = text_x + text_width + padding
        bg_y2 = text_y + text_height + padding//2
        
        # Draw background rectangle with transparency
        overlay = Image.new('RGBA', self.output_size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle([bg_x1, bg_y1, bg_x2, bg_y2], fill=(0, 0, 0, 128))
        
        # Composite the overlay
        titled_collage = Image.alpha_composite(titled_collage.convert('RGBA'), overlay)
        titled_collage = titled_collage.convert('RGB')
        
        # Draw the text
        draw = ImageDraw.Draw(titled_collage)
        draw.text((text_x, text_y), title, font=font, fill=(255, 255, 255))
        
        return titled_collage
    
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
    def create_collage(cls, style_name, folder_path, output_size=(1920, 1080), background=None, **kwargs):
        """Create collage using specified style"""
        style_class = cls.get_style(style_name)
        if not style_class:
            raise ValueError(f"Unknown style: {style_name}")

        style_instance = style_class(output_size=output_size, background=background)
        images = style_instance.load_images(folder_path)

        if not images:
            print("No images found!")
            return None

        return style_instance.create_collage(images, **kwargs)


def register_style(style_class):
    """Decorator to register a collage style"""
    return CollageStyleRegistry.register(style_class)