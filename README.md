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
- **23 Background Presets**: Stunning gradients (sunset, ocean, twilight, golden) and solid colors (charcoal, navy, cream)
- **Modular Architecture**: Plugin-based system for infinite extensibility
- **Professional Quality**: Zero wasted space, smart cropping, enhanced output
- **Caption Support**: JSON/TXT files or automatic extraction from filenames
- **Multiple Formats**: Social media ready sizes and custom dimensions

## Background Options

```bash
# List all available backgrounds
python collage_maker.py --list-backgrounds

# Use gradient backgrounds
python collage_maker.py --folder photos --style mandala --background sunset
python collage_maker.py --folder photos --style grid --background ocean
python collage_maker.py --folder photos --style polaroid --background vintage

# Use solid color backgrounds
python collage_maker.py --folder photos --style hexagon --background charcoal
python collage_maker.py --folder photos --style spiral --background navy
```

**Available Gradients**: sunset, ocean, aurora, lavender, coral, mint, rose, twilight, golden, arctic, noir, peach, emerald, vintage

**Available Solids**: white, black, cream, charcoal, slate, navy, forest, burgundy, mocha

## Documentation

- **Full Documentation**: https://nipunbatra.github.io/collage-maker/
- **Developer Guide**: See MODULAR_SYSTEM.md for extending with new styles
- **Examples Gallery**: 25+ example collages showcasing all styles

## License

MIT License - feel free to use for personal or commercial projects.