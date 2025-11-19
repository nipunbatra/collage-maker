#!/usr/bin/env python3
"""
Creative Collage Styles - Artistic and unique layouts
"""

import random
import math
from PIL import Image, ImageDraw, ImageFont
from collage_core import CollageBase, register_style


@register_style
class SpiralStyle(CollageBase):
    """Spiral arrangement of circular images"""
    
    @property
    def style_name(self):
        return "spiral"
    
    @property
    def description(self):
        return "Spiral arrangement of circular images from center outward"
    
    def create_collage(self, images, **kwargs):
        """Create spiral collage"""
        if not images:
            return None

        collage = self._create_background()
        selected_images = random.sample(images, min(len(images), 15))

        image_size = 120
        spiral_spacing = 30
        
        for i, img_data in enumerate(selected_images):
            # Calculate spiral position
            angle = i * 0.8
            radius = 20 + i * spiral_spacing
            
            x = self.center_x + int(radius * math.cos(angle))
            y = self.center_y + int(radius * math.sin(angle))
            
            # Process image
            img = img_data['image'].copy()
            img = self._resize_and_crop(img, image_size, image_size)
            
            # Apply circular mask
            mask = self._create_circular_mask((image_size, image_size))
            img.putalpha(mask)
            
            # Position on collage
            final_x = max(0, min(x - image_size // 2, self.output_size[0] - image_size))
            final_y = max(0, min(y - image_size // 2, self.output_size[1] - image_size))
            
            collage.paste(img, (final_x, final_y), img)
        
        return collage


@register_style
class HexagonStyle(CollageBase):
    """Hexagonal honeycomb layout"""
    
    @property
    def style_name(self):
        return "hexagon"
    
    @property
    def description(self):
        return "Tessellated hexagonal layout like honeycomb"
    
    def create_collage(self, images, **kwargs):
        """Create hexagonal honeycomb collage"""
        if not images:
            return None

        collage = self._create_background()
        selected_images = random.sample(images, min(len(images), 20))

        hex_size = 100
        hex_width = int(hex_size * math.sqrt(3))
        hex_height = int(hex_size * 1.5)
        
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
                
                if x + hex_size > self.output_size[0] or y + hex_size > self.output_size[1]:
                    continue
                
                # Create hexagonal image
                img_data = selected_images[image_index]
                hexagon_img = self._create_hexagon_image(img_data, hex_size)
                
                collage.paste(hexagon_img, (x, y), hexagon_img)
                image_index += 1
        
        return collage
    
    def _create_hexagon_image(self, img_data, hex_size):
        """Create hexagon-shaped image"""
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
        
        img.putalpha(mask)
        return img


@register_style
class FilmStripStyle(CollageBase):
    """Film strip/contact sheet style"""
    
    @property
    def style_name(self):
        return "filmstrip"
    
    @property
    def description(self):
        return "Classic film strip with perforations and frames"
    
    def create_collage(self, images, **kwargs):
        """Create film strip collage"""
        if not images:
            return None
        
        # Dark film background
        collage = Image.new('RGB', self.output_size, (20, 20, 20))
        
        frame_width = 200
        frame_height = 150
        margin = 20
        perforation_size = 8
        
        # Calculate grid
        cols = (self.output_size[0] - margin * 2) // (frame_width + margin)
        rows = (self.output_size[1] - margin * 2) // (frame_height + margin)
        
        selected_images = random.sample(images, min(len(images), rows * cols))
        
        # Draw perforations
        self._draw_perforations(collage, perforation_size)
        
        # Place images in frames
        for i, img_data in enumerate(selected_images):
            row = i // cols
            col = i % cols
            
            x = margin + perforation_size + col * (frame_width + margin)
            y = margin + perforation_size + row * (frame_height + margin)
            
            frame = self._create_film_frame(img_data, frame_width, frame_height)
            collage.paste(frame, (x, y))
        
        return collage
    
    def _draw_perforations(self, collage, perf_size):
        """Draw film perforations"""
        draw = ImageDraw.Draw(collage)
        spacing = 20
        
        # Top and bottom perforations
        for x in range(0, self.output_size[0], spacing):
            draw.rectangle([x, 0, x + perf_size, perf_size], fill=(40, 40, 40))
            draw.rectangle([x, self.output_size[1] - perf_size, x + perf_size, self.output_size[1]], fill=(40, 40, 40))
        
        # Left and right perforations
        for y in range(0, self.output_size[1], spacing):
            draw.rectangle([0, y, perf_size, y + perf_size], fill=(40, 40, 40))
            draw.rectangle([self.output_size[0] - perf_size, y, self.output_size[0], y + perf_size], fill=(40, 40, 40))
    
    def _create_film_frame(self, img_data, frame_width, frame_height):
        """Create a single film frame"""
        img = img_data['image'].copy()
        img = self._resize_and_crop(img, frame_width - 10, frame_height - 10)
        
        # Add white border (film frame)
        framed = Image.new('RGB', (frame_width, frame_height), (240, 240, 240))
        frame_x = (frame_width - img.width) // 2
        frame_y = (frame_height - img.height) // 2
        framed.paste(img, (frame_x, frame_y))
        
        return framed


@register_style
class ScrapbookStyle(CollageBase):
    """Artistic scrapbook with overlapping and tape effects"""
    
    @property
    def style_name(self):
        return "scrapbook"
    
    @property
    def description(self):
        return "Artistic scrapbook with overlapping photos and tape effects"
    
    def create_collage(self, images, **kwargs):
        """Create scrapbook collage"""
        if not images:
            return None
        
        # Cream background
        collage = Image.new('RGB', self.output_size, (250, 245, 235))
        selected_images = random.sample(images, min(len(images), 12))
        
        tape_color = (220, 200, 160, 180)
        
        for i, img_data in enumerate(selected_images):
            # Random size and position
            size_factor = random.uniform(0.8, 1.5)
            img_width = int(200 * size_factor)
            img_height = int(150 * size_factor)
            
            x = random.randint(0, max(0, self.output_size[0] - img_width))
            y = random.randint(0, max(0, self.output_size[1] - img_height))
            
            # Create photo with border
            photo = self._create_scrapbook_photo(img_data, img_width, img_height)
            
            # Random rotation
            angle = random.randint(-15, 15)
            rotated = photo.rotate(angle, expand=True, fillcolor=self.background_color)
            
            # Position
            final_x = max(0, min(x - (rotated.width - photo.width) // 2, 
                               self.output_size[0] - rotated.width))
            final_y = max(0, min(y - (rotated.height - photo.height) // 2, 
                               self.output_size[1] - rotated.height))
            
            collage.paste(rotated, (final_x, final_y))
            
            # Add tape effect
            collage = self._add_tape_effect(collage, final_x, final_y, rotated, tape_color)
        
        return collage
    
    def _create_scrapbook_photo(self, img_data, width, height):
        """Create scrapbook photo with white border"""
        img = img_data['image'].copy()
        img = self._resize_and_crop(img, width, height)
        
        border_width = random.randint(8, 15)
        bordered = Image.new('RGB', 
                           (width + border_width * 2, height + border_width * 2), 
                           (255, 255, 255))
        bordered.paste(img, (border_width, border_width))
        
        return bordered
    
    def _add_tape_effect(self, collage, x, y, rotated_img, tape_color):
        """Add tape strips over the photo"""
        tape_overlay = Image.new('RGBA', self.output_size, (0, 0, 0, 0))
        tape_draw = ImageDraw.Draw(tape_overlay)
        
        # Random tape positions
        for _ in range(random.randint(1, 3)):
            tape_x = x + random.randint(-20, rotated_img.width - 20)
            tape_y = y + random.randint(-10, rotated_img.height - 10)
            tape_w = random.randint(40, 80)
            tape_h = random.randint(15, 25)
            
            tape_draw.rectangle([tape_x, tape_y, tape_x + tape_w, tape_y + tape_h], 
                              fill=tape_color)
        
        return Image.alpha_composite(collage.convert('RGBA'), tape_overlay).convert('RGB')


@register_style
class PuzzleStyle(CollageBase):
    """Jigsaw puzzle piece layout"""
    
    @property
    def style_name(self):
        return "puzzle"
    
    @property
    def description(self):
        return "Interlocking jigsaw puzzle pieces"
    
    def create_collage(self, images, **kwargs):
        """Create puzzle piece collage"""
        if not images:
            return None

        collage = self._create_background()
        selected_images = random.sample(images, min(len(images), 16))
        
        piece_size = 150
        overlap = 20
        
        cols = (self.output_size[0] - overlap) // (piece_size - overlap)
        rows = (self.output_size[1] - overlap) // (piece_size - overlap)
        
        for i, img_data in enumerate(selected_images[:rows * cols]):
            row = i // cols
            col = i % cols
            
            x = col * (piece_size - overlap)
            y = row * (piece_size - overlap)
            
            puzzle_piece = self._create_puzzle_piece(img_data, piece_size)
            
            # Add shadow
            shadow = Image.new('RGBA', (piece_size + 5, piece_size + 5), (0, 0, 0, 50))
            collage.paste(shadow, (x + 2, y + 2), shadow)
            
            collage.paste(puzzle_piece, (x, y), puzzle_piece)
        
        return collage
    
    def _create_puzzle_piece(self, img_data, piece_size):
        """Create a single puzzle piece"""
        img = img_data['image'].copy()
        img = self._resize_and_crop(img, piece_size, piece_size)
        
        # Create puzzle piece mask
        mask = Image.new('L', (piece_size, piece_size), 0)
        draw = ImageDraw.Draw(mask)
        
        # Simplified puzzle piece shape
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
        
        img.putalpha(mask)
        return img