#!/usr/bin/env python3
"""
Modular Collage Maker - Extensible plugin-based collage creation system
"""

import os
import sys
import click
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import all style modules to register them
from collage_core import CollageStyleRegistry
from styles import basic_styles, creative_styles, geometric_styles, example_new_style


@click.command()
@click.option('--folder', '-f', help='Folder containing images')
@click.option('--output', '-o', default='collage.jpg', help='Output filename')
@click.option('--style', '-s', help='Collage style')
@click.option('--width', '-w', default=1920, help='Output width')
@click.option('--height', '-h', default=1080, help='Output height')
@click.option('--no-frames', is_flag=True, help='Disable frames on images')
@click.option('--list-styles', is_flag=True, help='List all available styles')
@click.option('--download-samples', is_flag=True, help='Download sample images for testing')
def main(folder, output, style, width, height, no_frames, list_styles, download_samples):
    """Create beautiful photo collages with modular extensible styles"""
    
    if list_styles:
        print("Available collage styles:")
        for style_name in sorted(CollageStyleRegistry.list_styles()):
            style_class = CollageStyleRegistry.get_style(style_name)
            style_instance = style_class()
            print(f"  {style_name:12} - {style_instance.description}")
        return
    
    if download_samples:
        from collage_maker_legacy import download_sample_images
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
            collage = CollageStyleRegistry.create_collage(
                style_name, 
                folder, 
                output_size=(width, height),
                add_frames=add_frames
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