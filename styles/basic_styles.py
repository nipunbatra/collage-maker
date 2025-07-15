#!/usr/bin/env python3
"""
Basic Collage Styles - Grid, Mosaic, Polaroid, Magazine
"""

import random
import math
from PIL import Image, ImageDraw, ImageFont
from collage_core import CollageBase, Rectangle, register_style


@register_style
class GridStyle(CollageBase):
    """Grid-based collage with perfect alignment"""
    
    @property
    def style_name(self):
        return "grid"
    
    @property
    def description(self):
        return "Perfect grid layout with equal spacing"
    
    def create_collage(self, images, rows=2, cols=3, add_frames=True, **kwargs):
        """Create grid collage"""
        if not images:
            return None
        
        # Calculate cell dimensions
        cell_width = (self.output_size[0] - (cols + 1) * self.min_padding) // cols
        cell_height = (self.output_size[1] - (rows + 1) * self.min_padding) // rows
        
        # Create background
        collage = Image.new('RGB', self.output_size, self.background_color)
        
        # Select random images
        selected_images = random.sample(images, min(len(images), rows * cols))
        
        for i, img_data in enumerate(selected_images):
            row = i // cols
            col = i % cols
            
            # Calculate position
            x = col * (cell_width + self.min_padding) + self.min_padding
            y = row * (cell_height + self.min_padding) + self.min_padding
            
            # Process image
            img = img_data['image'].copy()
            img = self._resize_to_fit(img, (cell_width, cell_height), crop=True)
            
            if add_frames:
                img = self._add_frame(img, frame_width=4)
                img = self._resize_to_fit(img, (cell_width, cell_height))
            
            # Center in cell
            img_x = x + (cell_width - img.width) // 2
            img_y = y + (cell_height - img.height) // 2
            
            collage.paste(img, (img_x, img_y))
        
        return collage


@register_style
class MosaicStyle(CollageBase):
    """Mosaic with perfect space utilization"""
    
    @property
    def style_name(self):
        return "mosaic"
    
    @property
    def description(self):
        return "Dynamic mosaic with zero wasted space"
    
    def create_collage(self, images, add_frames=True, **kwargs):
        """Create mosaic collage with perfect space utilization"""
        if not images:
            return None
        
        collage = Image.new('RGB', self.output_size, self.background_color)
        selected_images = random.sample(images, min(len(images), 15))
        
        # Generate regions for perfect packing
        regions = self._generate_regions()
        random.shuffle(regions)
        
        placed_regions = []
        
        for i, img_data in enumerate(selected_images):
            best_region = self._find_best_region(regions, placed_regions)
            
            if best_region:
                x1, y1, x2, y2 = best_region
                width = x2 - x1 - self.min_padding * 2
                height = y2 - y1 - self.min_padding * 2
                
                # Process image
                img = img_data['image'].copy()
                img = self._resize_and_crop(img, width, height)
                
                if add_frames:
                    img = self._add_frame(img, frame_width=3)
                    img = self._resize_to_fit(img, (width, height))
                
                # Center in region
                final_x = x1 + self.min_padding + (width - img.width) // 2
                final_y = y1 + self.min_padding + (height - img.height) // 2
                
                collage.paste(img, (final_x, final_y))
                placed_regions.append(best_region)
        
        return collage
    
    def _generate_regions(self):
        """Generate regions for mosaic placement"""
        w, h = self.output_size
        regions = []
        
        # Large regions
        regions.extend([
            (0, 0, w // 2, h // 2),
            (w // 2, 0, w, h // 2),
            (0, h // 2, w // 2, h),
            (w // 2, h // 2, w, h)
        ])
        
        # Medium regions
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
        
        # Small regions
        regions.extend([
            (0, 0, w // 4, h // 4),
            (w // 4, 0, w // 2, h // 4),
            (w // 2, 0, 3 * w // 4, h // 4),
            (3 * w // 4, 0, w, h // 4),
        ])
        
        return regions
    
    def _find_best_region(self, regions, placed_regions):
        """Find best available region"""
        for region in regions:
            x1, y1, x2, y2 = region
            width = x2 - x1
            height = y2 - y1
            
            if width < 100 or height < 100:
                continue
            
            # Check overlap
            overlaps = any(self._rectangles_overlap(region, placed) for placed in placed_regions)
            
            if not overlaps:
                return region
        
        return None


@register_style
class PolaroidStyle(CollageBase):
    """Polaroid-style collage with captions"""
    
    @property
    def style_name(self):
        return "polaroid"
    
    @property
    def description(self):
        return "Nostalgic polaroid photos with captions"
    
    def create_collage(self, images, add_frames=True, **kwargs):
        """Create polaroid collage"""
        if not images:
            return None
        
        collage = Image.new('RGB', self.output_size, self.background_color)
        
        # Adaptive polaroid size based on canvas
        canvas_ratio = self.output_size[0] / self.output_size[1]
        if canvas_ratio > 1.5:
            polaroid_width, polaroid_height = 200, 250
        elif canvas_ratio < 0.8:
            polaroid_width, polaroid_height = 180, 230
        else:
            polaroid_width, polaroid_height = 220, 270
        
        photo_width = polaroid_width - 20
        photo_height = int(photo_width * 0.8)
        
        # Calculate optimal grid
        margin = 15
        cols = max(1, (self.output_size[0] - margin) // (polaroid_width + margin))
        rows = max(1, (self.output_size[1] - margin) // (polaroid_height + margin))
        
        # Center the grid
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
            
            # Calculate position with random offset
            x = start_x + col * (polaroid_width + margin) + random.randint(-10, 10)
            y = start_y + row * (polaroid_height + margin) + random.randint(-10, 10)
            
            # Create polaroid
            polaroid = self._create_polaroid(img_data, polaroid_width, polaroid_height, 
                                           photo_width, photo_height, add_frames)
            
            # Small rotation
            angle = random.randint(-8, 8)
            rotated = polaroid.rotate(angle, expand=True, fillcolor=self.background_color)
            
            # Adjust position for rotation
            final_x = max(0, min(x - (rotated.width - polaroid_width) // 2, 
                               self.output_size[0] - rotated.width))
            final_y = max(0, min(y - (rotated.height - polaroid_height) // 2, 
                               self.output_size[1] - rotated.height))
            
            collage.paste(rotated, (final_x, final_y))
        
        return collage
    
    def _create_polaroid(self, img_data, p_width, p_height, photo_width, photo_height, add_frames):
        """Create a single polaroid"""
        polaroid = Image.new('RGB', (p_width, p_height), (255, 255, 255))
        
        # Add photo
        img = img_data['image'].copy()
        img = self._resize_and_crop(img, photo_width, photo_height)
        
        photo_x = (p_width - photo_width) // 2
        photo_y = 15
        polaroid.paste(img, (photo_x, photo_y))
        
        # Add caption
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 12)
        except:
            font = ImageFont.load_default()
        
        draw = ImageDraw.Draw(polaroid)
        caption = img_data['caption']
        if len(caption) > 18:
            caption = caption[:15] + "..."
        
        bbox = draw.textbbox((0, 0), caption, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = (p_width - text_width) // 2
        draw.text((text_x, photo_y + photo_height + 8), caption, fill=(60, 60, 60), font=font)
        
        if add_frames:
            polaroid = self._add_frame(polaroid, frame_width=2, frame_color=(250, 250, 250))
        
        return polaroid


@register_style
class MagazineStyle(CollageBase):
    """Magazine-style layout with featured image"""
    
    @property
    def style_name(self):
        return "magazine"
    
    @property
    def description(self):
        return "Magazine layout with hero image and thumbnail grid"
    
    def create_collage(self, images, add_frames=True, **kwargs):
        """Create magazine collage"""
        if not images:
            return None
        
        collage = Image.new('RGB', self.output_size, self.background_color)
        selected_images = random.sample(images, min(len(images), 12))
        
        # Calculate optimal split
        feature_ratio = 0.65 if self.output_size[0] > self.output_size[1] * 1.3 else 0.55
        
        # Featured image
        featured = selected_images[0]
        feature_width = int(self.output_size[0] * feature_ratio) - 10
        feature_height = self.output_size[1] - 20
        
        featured_img = featured['image'].copy()
        featured_img = self._resize_and_crop(featured_img, feature_width, feature_height)
        
        if add_frames:
            featured_img = self._add_frame(featured_img, frame_width=4)
            featured_img = self._resize_to_fit(featured_img, (feature_width, feature_height))
        
        collage.paste(featured_img, (10, 10))
        
        # Right side grid
        remaining_images = selected_images[1:]
        right_start_x = int(self.output_size[0] * feature_ratio) + 10
        right_width = self.output_size[0] - right_start_x - 10
        
        # Calculate optimal grid
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
                img = self._resize_to_fit(img, (cell_width - 2, cell_height - 2))
            
            collage.paste(img, (x, y))
        
        return collage