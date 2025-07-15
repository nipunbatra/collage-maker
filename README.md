# Collage Maker

A Python-based tool that creates professional photo collages from a folder of images, inspired by Google Photos and Apple Photos automatic collages.

**Website**: https://nipunbatra.github.io/collage-maker/

## Quick Start

```bash
git clone https://github.com/nipunbatra/collage-maker.git
cd collage-maker
pip install -r requirements.txt

# List all available styles
python collage_maker.py --list-styles

# Create a collage
python collage_maker.py --folder /path/to/images --style mandala
```

## Features

- **15+ Collage Styles**: Grid, Mosaic, Polaroid, Magazine, Spiral, Hexagon, Film Strip, Scrapbook, Puzzle, Mandala, Voronoi, Fractal, Kaleidoscope, and more
- **Modular Architecture**: Plugin-based system for infinite extensibility
- **Professional Quality**: Zero wasted space, smart cropping, enhanced output
- **Caption Support**: JSON/TXT files or automatic extraction from filenames
- **Multiple Formats**: Social media ready sizes and custom dimensions

## Documentation

- **Full Documentation**: https://nipunbatra.github.io/collage-maker/
- **Developer Guide**: See MODULAR_SYSTEM.md for extending with new styles
- **Examples Gallery**: 25+ example collages showcasing all styles

## License

MIT License - feel free to use for personal or commercial projects.