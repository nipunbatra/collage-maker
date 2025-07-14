# Collage Maker

A Python-based tool that creates beautiful photo collages from a folder of images, inspired by the automatic collage features in Google Photos and Apple Photos.

## Features

- **4 Collage Styles**: Grid, Mosaic, Polaroid, and Magazine layouts
- **Advanced Caption Support**: Load captions from JSON or TXT files
- **Frame Options**: Apple/Google Photos-style frames (can be disabled)
- **Smart Image Cropping**: Intelligent resizing and cropping for perfect fits
- **High Quality Output**: Enhanced image quality with sharpening and optimization
- **Flexible Output**: Customizable dimensions and output formats
- **Sample Images**: Built-in sample image downloader with captions for testing
- **Command Line Interface**: Easy-to-use CLI with multiple options

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nipunbatra/collage-maker.git
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
- `--style, -s`: Collage style - grid, mosaic, polaroid, magazine, or all (default: grid)
- `--width, -w`: Output width in pixels (default: 1920)
- `--height, -h`: Output height in pixels (default: 1080)
- `--no-frames`: Disable frames on images (frames are enabled by default)
- `--download-samples`: Download sample images for testing

### Collage Styles

#### Grid Collage
Creates a neat grid layout with images arranged in rows and columns. Perfect for showcasing multiple photos with equal importance.

![Grid Collage Example](collage_grid.jpg)

#### Mosaic Collage
Creates a dynamic mosaic with varying image sizes and positions. Uses advanced region-based placement algorithm for perfect space utilization with zero wasted space.

![Mosaic Collage Example](collage_mosaic.jpg)

#### Polaroid Collage
Creates a nostalgic polaroid-style collage with rotated images and captions. Uses grid-based positioning with smart randomization for optimal space usage while maintaining authentic polaroid aesthetics.

![Polaroid Collage Example](collage_polaroid.jpg)

#### Magazine Collage
Creates a magazine-style layout with a large featured image on the left and smaller images arranged in a grid on the right.

![Magazine Collage Example](collage_magazine.jpg)


### Caption Support

The tool supports captions in multiple formats:

#### JSON Format (recommended)
Create a `captions.json` file in your image folder:
```json
{
  "photo1.jpg": "Beautiful sunset over the mountains",
  "photo2.jpg": "Family gathering at the beach",
  "photo3.jpg": "Morning coffee and newspaper"
}
```

#### TXT Format
Create a `captions.txt` file in your image folder:
```
photo1.jpg: Beautiful sunset over the mountains
photo2.jpg: Family gathering at the beach
photo3.jpg: Morning coffee and newspaper
```

#### Automatic Caption Extraction
If no caption file is found, captions are automatically extracted from filenames:
- `my_summer_vacation.jpg` → `My Summer Vacation`
- `beach-sunset-2023.jpg` → `Beach Sunset 2023`

### Sample Images

To download sample images with captions for testing:
```bash
python collage_maker.py --download-samples
```

This creates a `sample_images` folder with 8 sample images and a `captions.json` file with beautiful captions.

## Examples

### Create all collage styles:
```bash
python collage_maker.py --folder sample_images --style all
```
This generates:
- `collage_grid.jpg`
- `collage_mosaic.jpg`
- `collage_polaroid.jpg`
- `collage_magazine.jpg`

### Create a high-resolution magazine-style collage:
```bash
python collage_maker.py --folder my_photos --style magazine --width 2560 --height 1440
```

### Create collages without frames:
```bash
python collage_maker.py --folder my_photos --style all --no-frames
```

## 📸 Extensive Examples Gallery

### Standard Collage Styles (1920x1080)

| Style | Example | Description |
|-------|---------|-------------|
| **Grid** | ![Grid](collage_grid.jpg) | Perfect grid layout with equal spacing |
| **Mosaic** | ![Mosaic](collage_mosaic.jpg) | Dynamic sizes with zero wasted space |
| **Polaroid** | ![Polaroid](collage_polaroid.jpg) | Nostalgic rotated photos with captions |
| **Magazine** | ![Magazine](collage_magazine.jpg) | Featured image with thumbnail grid |

### Size Variations

#### Small Formats
- **Square (800x800)**: ![Small Square](small_square_grid.jpg)
- **Portrait (600x900)**: ![Small Portrait](small_portrait_mosaic.jpg)  
- **Landscape (1000x700)**: ![Small Landscape](small_landscape_polaroid.jpg)

#### Large Formats
- **4K (3840x2160)**: ![Large 4K](large_4k_magazine.jpg)
- **Ultrawide (3440x1440)**: ![Ultrawide](ultrawide_mosaic.jpg)
- **Large Grid (2560x1600)**: ![Large Grid](large_grid_grid.jpg)

### Grid Variations

| Configuration | Example | Use Case |
|---------------|---------|----------|
| **1x5 Banner** | ![1x5 Banner](grid_1x5_banner.jpg) | Website headers, banners |
| **5x1 Tower** | ![5x1 Tower](grid_5x1_tower.jpg) | Vertical displays, timelines |
| **2x2 Square** | ![2x2 Square](grid_2x2_square.jpg) | Simple, clean layouts |
| **3x2 Portrait** | ![3x2 Portrait](grid_3x2_portrait.jpg) | Mobile-friendly layouts |
| **2x4 Wide** | ![2x4 Wide](grid_2x4_wide.jpg) | Widescreen displays |
| **1x3 Triptych** | ![1x3 Triptych](grid_1x3_triptych.jpg) | Artistic triptych style |
| **3x3 Instagram** | ![3x3 Instagram](grid_3x3_instagram.jpg) | Social media perfect |

### Without Frames

| Style | With Frames | Without Frames |
|-------|-------------|----------------|
| **Grid** | ![Grid Frames](collage_grid.jpg) | ![Grid No Frames](grid_no_frames.jpg) |
| **Mosaic** | ![Mosaic Frames](collage_mosaic.jpg) | ![Mosaic No Frames](mosaic_no_frames.jpg) |
| **Polaroid** | ![Polaroid Frames](collage_polaroid.jpg) | ![Polaroid No Frames](polaroid_no_frames.jpg) |
| **Magazine** | ![Magazine Frames](collage_magazine.jpg) | ![Magazine No Frames](magazine_no_frames.jpg) |

### Social Media Ready

| Platform | Size | Example | Command |
|----------|------|---------|---------|
| **Instagram Square** | 1080x1080 | ![Instagram Square](instagram_square_grid.jpg) | `--width 1080 --height 1080` |
| **Instagram Story** | 1080x1920 | ![Instagram Story](instagram_story_mosaic.jpg) | `--width 1080 --height 1920` |
| **Facebook Cover** | 1200x630 | ![Facebook Cover](facebook_cover_magazine.jpg) | `--width 1200 --height 630` |
| **Twitter Header** | 1024x512 | ![Twitter Header](twitter_header_polaroid.jpg) | `--width 1024 --height 512` |
| **YouTube Thumbnail** | 1920x1080 | ![YouTube Thumbnail](youtube_thumbnail_grid.jpg) | `--width 1920 --height 1080` |

### Ultimate Space Utilization Examples

For maximum space efficiency, use the advanced algorithms:

| Style | Standard | Ultimate | Improvement |
|-------|----------|----------|-------------|
| **Mosaic** | ![Standard Mosaic](collage_mosaic.jpg) | ![Ultimate Mosaic](ultimate_mosaic.jpg) | Bin-packing algorithm |
| **Polaroid** | ![Standard Polaroid](collage_polaroid.jpg) | ![Ultimate Polaroid](ultimate_polaroid.jpg) | Perfect grid positioning |
| **Magazine** | ![Standard Magazine](collage_magazine.jpg) | ![Ultimate Magazine](ultimate_magazine.jpg) | Smart layout optimization |

### Creating Your Own Examples

```bash
# Small square format
python collage_maker.py --folder photos --style grid --width 800 --height 800

# Large 4K format
python collage_maker.py --folder photos --style magazine --width 3840 --height 2160

# Social media ready
python collage_maker.py --folder photos --style mosaic --width 1080 --height 1080

# Without frames
python collage_maker.py --folder photos --style all --no-frames

# Ultimate space utilization
python collage_maker_v3.py photos
```

## Technical Features

### Frame System
- **Apple/Google Photos-style frames**: Subtle white borders that enhance image presentation
- **Adaptive frame sizing**: Different frame widths for different collage styles
- **Optional frames**: Can be disabled with `--no-frames` flag

### Smart Image Processing
- **Intelligent cropping**: Maintains aspect ratios while fitting images perfectly
- **Quality enhancement**: Automatic sharpening and optimization
- **Format support**: Works with all major image formats
- **High DPI output**: Supports custom resolutions up to 4K and beyond

### Advanced Layout Algorithms
- **Perfect space utilization**: Zero wasted space in mosaic layouts using region-based placement
- **Grid-based positioning**: Optimal placement in polaroid style with smart randomization
- **Collision detection**: Prevents image overlap through advanced algorithms
- **Proportional sizing**: Balances image sizes for maximum visual impact

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff)
- WebP (.webp)

## Requirements

- Python 3.7+
- Pillow (PIL) - Image processing
- Click - Command line interface
- Requests - Sample image downloading

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
- Magazine and scrapbook designs

## Future Enhancements

- Web interface for easier use
- Video collage support
- Face detection for smart cropping
- Color theme matching
- Text overlay options
- Social media format presets
- Batch processing for multiple folders
- AI-powered layout suggestions

## Changelog

### Version 2.1.0
- **MAJOR IMPROVEMENT**: Perfect space utilization - zero wasted space in all layouts
- Advanced region-based mosaic algorithm for maximum space efficiency
- Grid-based polaroid positioning with smart randomization
- Enhanced magazine layout with optimized caption display
- Removed heart style to focus on core professional layouts
- Improved image quality with enhanced sharpening and contrast
- Better collision detection and placement algorithms

### Version 2.0.0
- Added Magazine collage style
- Implemented JSON/TXT caption support
- Added frame system like Apple/Google Photos
- Fixed whitespace issues in mosaic and polaroid styles
- Improved image quality with sharpening
- Enhanced collision detection algorithms
- Better space utilization in all layouts

### Version 1.0.0
- Initial release with Grid, Mosaic, and Polaroid styles
- Basic caption support from filenames
- Sample image download functionality