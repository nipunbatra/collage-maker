#!/usr/bin/env python3
"""
Create diverse collage examples with different configurations
"""

import os
import shutil
from collage_maker import CollageMaker

def create_grid_with_config(images, rows, cols, width, height, output_name, add_frames=True):
    """Create grid with specific row/column configuration"""
    collage_maker = CollageMaker(output_size=(width, height))
    collage = collage_maker.create_grid_collage(images, rows=rows, cols=cols, add_frames=add_frames)
    if collage:
        collage_maker.save_collage(collage, output_name)
        return True
    return False

def main():
    # Load images
    collage_maker = CollageMaker()
    images = collage_maker.load_images('sample_images')
    
    if not images:
        print("No images found!")
        return
    
    print(f"Found {len(images)} images")
    
    # Create examples with different grid configurations
    examples = [
        # Grid variations
        {"rows": 1, "cols": 5, "width": 1500, "height": 300, "name": "grid_1x5_banner.jpg", "desc": "Banner style (1x5)"},
        {"rows": 5, "cols": 1, "width": 400, "height": 2000, "name": "grid_5x1_tower.jpg", "desc": "Tower style (5x1)"},
        {"rows": 2, "cols": 2, "width": 800, "height": 800, "name": "grid_2x2_square.jpg", "desc": "Perfect square (2x2)"},
        {"rows": 3, "cols": 2, "width": 1200, "height": 1800, "name": "grid_3x2_portrait.jpg", "desc": "Portrait grid (3x2)"},
        {"rows": 2, "cols": 4, "width": 1600, "height": 800, "name": "grid_2x4_wide.jpg", "desc": "Wide grid (2x4)"},
        {"rows": 1, "cols": 3, "width": 1200, "height": 400, "name": "grid_1x3_triptych.jpg", "desc": "Triptych style (1x3)"},
        {"rows": 3, "cols": 3, "width": 900, "height": 900, "name": "grid_3x3_instagram.jpg", "desc": "Instagram style (3x3)"},
    ]
    
    for example in examples:
        print(f"Creating {example['desc']}...")
        success = create_grid_with_config(
            images, 
            example["rows"], 
            example["cols"], 
            example["width"], 
            example["height"], 
            example["name"]
        )
        if success:
            print(f"✓ Created {example['name']}")
        else:
            print(f"✗ Failed to create {example['name']}")
    
    # Create examples without frames
    print("\nCreating examples without frames...")
    
    frameless_examples = [
        {"style": "grid", "width": 1200, "height": 800, "name": "grid_no_frames.jpg"},
        {"style": "mosaic", "width": 1200, "height": 800, "name": "mosaic_no_frames.jpg"},
        {"style": "polaroid", "width": 1200, "height": 800, "name": "polaroid_no_frames.jpg"},
        {"style": "magazine", "width": 1200, "height": 800, "name": "magazine_no_frames.jpg"},
    ]
    
    for example in frameless_examples:
        print(f"Creating {example['name']} without frames...")
        collage_maker = CollageMaker(output_size=(example["width"], example["height"]))
        
        if example["style"] == "grid":
            collage = collage_maker.create_grid_collage(images, add_frames=False)
        elif example["style"] == "mosaic":
            collage = collage_maker.create_mosaic_collage(images, add_frames=False)
        elif example["style"] == "polaroid":
            collage = collage_maker.create_polaroid_collage(images, add_frames=False)
        elif example["style"] == "magazine":
            collage = collage_maker.create_magazine_collage(images, add_frames=False)
        
        if collage:
            collage_maker.save_collage(collage, example["name"])
            print(f"✓ Created {example['name']}")
    
    # Create social media format examples
    print("\nCreating social media format examples...")
    
    social_examples = [
        {"style": "grid", "width": 1080, "height": 1080, "name": "instagram_square_grid.jpg", "desc": "Instagram Square"},
        {"style": "mosaic", "width": 1080, "height": 1920, "name": "instagram_story_mosaic.jpg", "desc": "Instagram Story"},
        {"style": "magazine", "width": 1200, "height": 630, "name": "facebook_cover_magazine.jpg", "desc": "Facebook Cover"},
        {"style": "polaroid", "width": 1024, "height": 512, "name": "twitter_header_polaroid.jpg", "desc": "Twitter Header"},
        {"style": "grid", "width": 1920, "height": 1080, "name": "youtube_thumbnail_grid.jpg", "desc": "YouTube Thumbnail"},
    ]
    
    for example in social_examples:
        print(f"Creating {example['desc']}...")
        collage_maker = CollageMaker(output_size=(example["width"], example["height"]))
        
        if example["style"] == "grid":
            collage = collage_maker.create_grid_collage(images)
        elif example["style"] == "mosaic":
            collage = collage_maker.create_mosaic_collage(images)
        elif example["style"] == "polaroid":
            collage = collage_maker.create_polaroid_collage(images)
        elif example["style"] == "magazine":
            collage = collage_maker.create_magazine_collage(images)
        
        if collage:
            collage_maker.save_collage(collage, example["name"])
            print(f"✓ Created {example['name']}")
    
    print("\n🎉 All examples created successfully!")

if __name__ == "__main__":
    main()