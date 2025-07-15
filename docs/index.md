---
layout: default
title: Collage Maker - Professional Photo Collages
---

# 🎨 Collage Maker

Create stunning photo collages with our professional-grade tool featuring **15+ artistic styles** and a **modular plugin architecture**.

## 🚀 Quick Start

```bash
# Install
git clone https://github.com/nipunbatra/collage-maker.git
pip install -r requirements.txt

# List all styles
python modular_collage_maker.py --list-styles

# Create your first collage
python modular_collage_maker.py --folder photos --style mandala
```

## ✨ Features

- **15+ Collage Styles** from basic grids to artistic mandalas
- **Modular Architecture** - easily extensible plugin system  
- **Perfect Space Utilization** - zero wasted space algorithms
- **Professional Quality** - rivals Apple Photos and Google Photos
- **Caption Support** - JSON/TXT files or auto-extraction
- **Multiple Formats** - social media ready sizes

## 🎨 Style Categories

### Basic Styles (4)
Professional layouts perfect for any use case
- **Grid** - Perfect alignment and spacing
- **Mosaic** - Dynamic sizes with zero waste
- **Polaroid** - Nostalgic photos with captions  
- **Magazine** - Hero image + thumbnail grid

### Creative Styles (5)
Artistic arrangements for unique presentations
- **Spiral** - Flowing outward from center
- **Hexagon** - Honeycomb tessellation
- **Film Strip** - Classic cinema aesthetic
- **Scrapbook** - Overlapping with tape effects
- **Puzzle** - Interlocking jigsaw pieces

### Geometric Styles (4)
Mathematical patterns and symmetries
- **Mandala** - Circular rings and symmetry
- **Voronoi** - Organic cell-like divisions
- **Fractal** - Recursive subdivisions
- **Kaleidoscope** - Symmetrical reflections

## 🔧 For Developers

Adding a new style takes just 3 steps:

```python
@register_style
class MyStyle(CollageBase):
    @property
    def style_name(self):
        return "mystyle"
    
    def create_collage(self, images, **kwargs):
        # Your layout algorithm
        return collage
```

**[Complete Developer Documentation →](MODULAR_SYSTEM.md)**

## 📊 Project Stats

- **15+** Collage Styles Available
- **3** Major Version Releases  
- **∞** Extensibility through plugins
- **0** Wasted Space in layouts

---

**[⭐ Star on GitHub](https://github.com/nipunbatra/collage-maker)** | **[📥 Download](https://github.com/nipunbatra/collage-maker/archive/refs/heads/master.zip)** | **[🐛 Report Issues](https://github.com/nipunbatra/collage-maker/issues)**