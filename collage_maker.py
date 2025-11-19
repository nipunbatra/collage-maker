#!/usr/bin/env python3
"""
Modular Collage Maker - Extensible plugin-based collage creation system
"""

import os
import sys
import json
import click
import requests
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import all style modules to register them
from collage_core import CollageStyleRegistry
from styles import basic_styles, creative_styles, geometric_styles, example_new_style


def create_sample_captions():
    """Create sample captions file"""
    sample_captions = {
        "sample_1.jpg": "Golden sunset over mountains",
        "sample_2.jpg": "Peaceful lake reflection",
        "sample_3.jpg": "Vibrant city nightscape",
        "sample_4.jpg": "Autumn forest pathway",
        "sample_5.jpg": "Ocean waves crashing",
        "sample_6.jpg": "Beautiful cherry blossoms",
        "sample_7.jpg": "Majestic snow-capped peaks",
        "sample_8.jpg": "Serene beach paradise"
    }
    
    with open("sample_images/captions.json", "w") as f:
        json.dump(sample_captions, f, indent=2)
    
    print("Created sample captions.json file")


def download_sample_images():
    """Download sample images for testing"""
    sample_folder = "sample_images"
    os.makedirs(sample_folder, exist_ok=True)
    
    # Picsum sample images for consistent testing
    sample_urls = [
        "https://picsum.photos/800/600?random=1",
        "https://picsum.photos/800/600?random=2", 
        "https://picsum.photos/800/600?random=3",
        "https://picsum.photos/800/600?random=4",
        "https://picsum.photos/800/600?random=5",
        "https://picsum.photos/800/600?random=6",
        "https://picsum.photos/800/600?random=7",
        "https://picsum.photos/800/600?random=8",
    ]
    
    print("Downloading sample images...")
    for i, url in enumerate(sample_urls):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(f"{sample_folder}/sample_{i+1}.jpg", "wb") as f:
                    f.write(response.content)
                print(f"Downloaded sample_{i+1}.jpg")
        except Exception as e:
            print(f"Error downloading sample_{i+1}.jpg: {e}")
    
    # Create captions file
    create_sample_captions()
    print(f"\nSample images downloaded to '{sample_folder}/' folder")
    print("You can now create collages with: python collage_maker.py --folder sample_images --style mandala")


@click.command()
@click.option('--folder', '-f', help='Folder containing images')
@click.option('--output', '-o', default='collage.jpg', help='Output filename')
@click.option('--style', '-s', help='Collage style')
@click.option('--width', '-w', default=1920, help='Output width')
@click.option('--height', '-h', default=1080, help='Output height')
@click.option('--no-frames', is_flag=True, help='Disable frames on images')
@click.option('--rows', type=int, help='Number of rows for grid layout (grid style only)')
@click.option('--cols', type=int, help='Number of columns for grid layout (grid style only)')
@click.option('--title', help='Overall title text for the collage')
@click.option('--title-position', type=click.Choice(['top', 'bottom', 'center']), default='bottom', help='Position for title text')
@click.option('--background', '-bg', help='Background preset or color (e.g., sunset, ocean, black, "#ff5733")')
@click.option('--list-styles', is_flag=True, help='List all available styles')
@click.option('--list-backgrounds', is_flag=True, help='List all available background presets')
@click.option('--download-samples', is_flag=True, help='Download sample images for testing')
def main(folder, output, style, width, height, no_frames, rows, cols, title, title_position, background, list_styles, list_backgrounds, download_samples):
    """Create beautiful photo collages with modular extensible styles"""
    
    if list_styles:
        print("Available collage styles:")
        for style_name in sorted(CollageStyleRegistry.list_styles()):
            style_class = CollageStyleRegistry.get_style(style_name)
            style_instance = style_class()
            print(f"  {style_name:12} - {style_instance.description}")
        return

    if list_backgrounds:
        from collage_core import CollageBase
        print("Available background presets:\n")
        print("Solid Colors:")
        solids = [(k, v) for k, v in CollageBase.BACKGROUND_PRESETS.items()
                  if isinstance(v, tuple) and len(v) == 3 and isinstance(v[0], int)]
        for name, color in sorted(solids):
            print(f"  {name:12} - RGB{color}")

        print("\nGradients:")
        gradients = [(k, v) for k, v in CollageBase.BACKGROUND_PRESETS.items()
                     if isinstance(v, tuple) and len(v) == 3 and isinstance(v[0], tuple)]
        for name, (start, end, direction) in sorted(gradients):
            print(f"  {name:12} - {direction} gradient")

        print("\nUsage: python collage_maker.py --folder photos --style grid --background sunset")
        return
    
    if download_samples:
        download_sample_images()
        return
    
    if not folder:
        print("Error: --folder is required")
        print("Use --list-styles to see available styles")
        return
    
    if not style:
        print("Error: --style is required")
        print("Use --list-styles to see available styles")
        return
    
    if not os.path.exists(folder):
        print(f"Error: Folder '{folder}' does not exist")
        return
    
    # Handle 'all' style
    if style == 'all':
        styles_to_create = ['grid', 'mosaic', 'polaroid', 'magazine']
    else:
        styles_to_create = [style]
    
    # Create collages
    add_frames = not no_frames
    
    for style_name in styles_to_create:
        if style_name not in CollageStyleRegistry.list_styles():
            print(f"Error: Unknown style '{style_name}'")
            print("Use --list-styles to see available styles")
            continue
        
        print(f"Creating {style_name} collage...")
        
        try:
            # Pass custom grid dimensions and title if specified
            kwargs = {'add_frames': add_frames}
            if style_name == 'grid' and rows is not None:
                kwargs['rows'] = rows
            if style_name == 'grid' and cols is not None:
                kwargs['cols'] = cols
            if title:
                kwargs['title'] = title
                kwargs['title_position'] = title_position
            if background:
                kwargs['background'] = background

            collage = CollageStyleRegistry.create_collage(
                style_name,
                folder,
                output_size=(width, height),
                background=background,
                **kwargs
            )
            
            if collage:
                if len(styles_to_create) > 1:
                    output_filename = f"{os.path.splitext(output)[0]}_{style_name}.jpg"
                else:
                    output_filename = output
                
                # Save using the style's save method
                style_class = CollageStyleRegistry.get_style(style_name)
                style_instance = style_class(output_size=(width, height))
                style_instance.save_collage(collage, output_filename)
            else:
                print(f"Failed to create {style_name} collage")
                
        except Exception as e:
            print(f"Error creating {style_name} collage: {e}")


@click.command()
@click.option('--folder', '-f', help='Folder containing images')
@click.option('--output-dir', '-o', default='examples', help='Output directory')
def create_all_examples(folder, output_dir):
    """Create examples of all available styles"""
    
    if not folder or not os.path.exists(folder):
        print("Error: Valid --folder is required")
        return
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Creating examples for all {len(CollageStyleRegistry.list_styles())} styles...")
    
    for style_name in sorted(CollageStyleRegistry.list_styles()):
        print(f"Creating {style_name} example...")
        
        try:
            collage = CollageStyleRegistry.create_collage(
                style_name, 
                folder, 
                output_size=(1200, 800),
                add_frames=True
            )
            
            if collage:
                output_path = os.path.join(output_dir, f"example_{style_name}.jpg")
                style_class = CollageStyleRegistry.get_style(style_name)
                style_instance = style_class()
                style_instance.save_collage(collage, output_path)
                print(f"✓ Created {output_path}")
            else:
                print(f"✗ Failed to create {style_name}")
                
        except Exception as e:
            print(f"✗ Error creating {style_name}: {e}")
    
    print(f"\nAll examples saved to: {output_dir}/")


if __name__ == "__main__":
    # Check if we're being called as create_all_examples
    if len(sys.argv) > 1 and sys.argv[1] == 'examples':
        sys.argv.pop(1)  # Remove 'examples' from argv
        create_all_examples()
    else:
        main()