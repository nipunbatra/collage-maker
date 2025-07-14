# Collage Maker

A Python-based tool that creates beautiful photo collages from a folder of images, inspired by the automatic collage features in Google Photos and Apple Photos.

## Features

- **Multiple Collage Styles**: Grid, Mosaic, and Polaroid layouts
- **Automatic Caption Support**: Extracts captions from image filenames
- **Flexible Output**: Customizable dimensions and output formats
- **Sample Images**: Built-in sample image downloader for testing
- **Command Line Interface**: Easy-to-use CLI with multiple options

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/collage-maker.git
cd collage-maker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Create a grid collage from images in a folder:
```bash
python collage_maker.py --folder /path/to/images
```

### Advanced Options

```bash
python collage_maker.py --folder /path/to/images --style all --width 1920 --height 1080 --output my_collage.jpg
```

### Command Line Options

- `--folder, -f`: Folder containing images (required)
- `--output, -o`: Output filename (default: collage.jpg)
- `--style, -s`: Collage style - grid, mosaic, polaroid, or all (default: grid)
- `--width, -w`: Output width in pixels (default: 1920)
- `--height, -h`: Output height in pixels (default: 1080)
- `--download-samples`: Download sample images for testing

### Collage Styles

#### Grid Collage
Creates a neat grid layout with images arranged in rows and columns.

#### Mosaic Collage
Creates a dynamic mosaic with varying image sizes and positions.

#### Polaroid Collage
Creates a nostalgic polaroid-style collage with rotated images and captions.

### Sample Images

To download sample images for testing:
```bash
python collage_maker.py --download-samples
```

This will create a `sample_images` folder with 8 sample images from Picsum.

## Examples

### Create all collage styles:
```bash
python collage_maker.py --folder sample_images --style all
```
This generates:
- `collage_grid.jpg`
- `collage_mosaic.jpg`
- `collage_polaroid.jpg`

### Custom dimensions:
```bash
python collage_maker.py --folder my_photos --width 2560 --height 1440 --style mosaic
```

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff)
- WebP (.webp)

## Caption Support

The tool automatically extracts captions from image filenames:
- Underscores and hyphens are converted to spaces
- File extensions are removed
- Text is title-cased

Example: `my_summer_vacation.jpg` → `My Summer Vacation`

## Requirements

- Python 3.7+
- Pillow (PIL)
- Click
- Requests

## License

MIT License - feel free to use this tool for personal or commercial projects.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Inspiration

This tool was inspired by the automatic collage features in:
- Google Photos Memories
- Apple Photos Memories
- Instagram Story layouts

## Future Enhancements

- Web interface
- More collage styles
- Video support
- Face detection for better cropping
- Color theme matching
- Text overlay options