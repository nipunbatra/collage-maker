# Modular Collage System

## 🏗️ Architecture Overview

The collage maker is now built on a **modular, extensible architecture** that makes it easy to add new styles without modifying existing code.

### Core Components

```
collage-maker/
├── collage_core.py          # Base classes and registry
├── modular_collage_maker.py # Main CLI interface
├── styles/                  # Style modules
│   ├── __init__.py
│   ├── basic_styles.py      # Grid, Mosaic, Polaroid, Magazine
│   ├── creative_styles.py   # Spiral, Hexagon, Film, Scrapbook, Puzzle
│   ├── geometric_styles.py  # Mandala, Voronoi, Fractal, Kaleidoscope
│   └── example_new_style.py # Examples for developers
└── legacy files...          # Original single-file versions
```

## 🎨 Available Styles (13 Total)

### Basic Styles (4)
- **grid** - Perfect grid layout with equal spacing
- **mosaic** - Dynamic mosaic with zero wasted space  
- **polaroid** - Nostalgic polaroid photos with captions
- **magazine** - Magazine layout with hero image and thumbnail grid

### Creative Styles (5)
- **spiral** - Spiral arrangement of circular images from center outward
- **hexagon** - Tessellated hexagonal layout like honeycomb
- **filmstrip** - Classic film strip with perforations and frames
- **scrapbook** - Artistic scrapbook with overlapping photos and tape effects
- **puzzle** - Interlocking jigsaw puzzle pieces

### Geometric Styles (4)
- **mandala** - Mandala-style circular arrangement with multiple rings
- **voronoi** - Voronoi diagram with organic cell-like divisions
- **fractal** - Fractal recursive subdivision pattern
- **kaleidoscope** - Kaleidoscope symmetrical pattern with reflections

## 🚀 Usage

### List All Available Styles
```bash
python modular_collage_maker.py --list-styles
```

### Create Single Style
```bash
python modular_collage_maker.py --folder photos --style mandala --output my_mandala.jpg
```

### Create Multiple Styles
```bash
python modular_collage_maker.py --folder photos --style all --width 1920 --height 1080
```

### Create Examples of All Styles
```bash
python modular_collage_maker.py examples --folder sample_images --output-dir examples
```

## 🔧 Adding New Styles

Adding a new collage style is incredibly simple:

### Step 1: Create Style Class

```python
from collage_core import CollageBase, register_style

@register_style
class MyAwesomeStyle(CollageBase):
    
    @property
    def style_name(self):
        return "awesome"
    
    @property
    def description(self):
        return "My awesome collage style"
    
    def create_collage(self, images, **kwargs):
        # Your collage creation logic here
        collage = Image.new('RGB', self.output_size, self.background_color)
        
        # Process images and create your layout
        for img_data in images:
            img = img_data['image']
            # ... your layout algorithm
        
        return collage
```

### Step 2: Import in Your Module

```python
# At the top of modular_collage_maker.py or in styles/__init__.py
from styles import my_new_styles
```

### Step 3: Use Immediately

```bash
python modular_collage_maker.py --folder photos --style awesome
```

That's it! Your new style is automatically registered and available.

## 📚 API Reference

### CollageBase Class

All styles inherit from `CollageBase` which provides:

#### Required Methods
- `style_name` (property) - Unique name for the style
- `create_collage(images, **kwargs)` - Main creation method

#### Optional Properties
- `description` - Description of the style

#### Helper Methods
- `load_images(folder_path)` - Load images with caption support
- `_resize_and_crop(img, width, height)` - Resize to exact dimensions
- `_resize_to_fit(img, size, crop=False)` - Resize maintaining aspect ratio
- `_add_frame(img, width, color)` - Add frame to image
- `_create_circular_mask(size)` - Create circular mask
- `_rectangles_overlap(rect1, rect2)` - Check rectangle overlap
- `save_collage(collage, path)` - Save with quality enhancement

### CollageStyleRegistry

The registry automatically manages all styles:

```python
# Register a style (done automatically with decorator)
CollageStyleRegistry.register(MyStyle)

# Get available styles
styles = CollageStyleRegistry.list_styles()

# Create collage
collage = CollageStyleRegistry.create_collage('style_name', 'folder_path')
```

## 🎯 Best Practices

### 1. Style Organization
- Put related styles in the same module
- Use descriptive filenames (e.g., `nature_styles.py`, `artistic_styles.py`)
- Keep individual style classes focused and simple

### 2. Naming Conventions
- Style names: lowercase, no spaces (e.g., `'my_style'`)
- Class names: PascalCase with 'Style' suffix (e.g., `MyAwesomeStyle`)
- File names: snake_case (e.g., `my_styles.py`)

### 3. Error Handling
```python
def create_collage(self, images, **kwargs):
    if not images:
        return None
    
    try:
        # Your collage creation logic
        pass
    except Exception as e:
        print(f"Error in {self.style_name}: {e}")
        return None
```

### 4. Performance
- Use `random.sample()` to limit image count
- Consider canvas size when calculating dimensions
- Use helper methods for common operations

## 🔄 Migration from Legacy

The old single-file versions still work, but the modular system offers:

### Advantages
- ✅ **Extensible** - Easy to add new styles
- ✅ **Maintainable** - Separate concerns, easier debugging  
- ✅ **Testable** - Each style can be tested independently
- ✅ **Discoverable** - Automatic style registration and listing
- ✅ **Consistent** - Shared base class ensures common interface
- ✅ **Flexible** - Styles can be grouped in logical modules

### Backward Compatibility
- All original styles (grid, mosaic, polaroid, magazine) work identically
- Same command-line interface
- Same output quality and features
- Caption support maintained
- Frame options preserved

## 🚀 Future Extensions

Easy to add:
- **Social Media Styles** - Instagram, TikTok, YouTube formats
- **Artistic Styles** - Impressionist, abstract, minimalist
- **Themed Styles** - Holiday, seasonal, event-specific
- **Interactive Styles** - User-guided placement
- **AI-Powered Styles** - Content-aware layouts
- **3D Effects** - Perspective, depth, shadows

The modular architecture makes all of these straightforward to implement!

## 📝 Example: Complete New Style

```python
# styles/nature_styles.py

@register_style
class FlowerStyle(CollageBase):
    @property
    def style_name(self):
        return "flower"
    
    @property  
    def description(self):
        return "Flower petal arrangement"
    
    def create_collage(self, images, **kwargs):
        if not images:
            return None
        
        collage = Image.new('RGB', self.output_size, (240, 255, 240))  # Light green
        selected_images = random.sample(images, min(len(images), 8))
        
        petal_size = 150
        radius = 200
        
        for i, img_data in enumerate(selected_images):
            # Calculate petal position
            angle = (2 * math.pi * i) / len(selected_images)
            x = self.center_x + int(radius * math.cos(angle))
            y = self.center_y + int(radius * math.sin(angle))
            
            # Create petal-shaped image
            img = img_data['image'].copy()
            img = self._resize_and_crop(img, petal_size, petal_size)
            
            # Petal mask (ellipse)
            mask = Image.new('L', (petal_size, petal_size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((10, 0, petal_size-10, petal_size), fill=255)
            
            img.putalpha(mask)
            
            # Rotate toward center
            rotation = math.degrees(angle) + 90
            rotated = img.rotate(rotation, expand=True)
            
            # Position
            final_x = x - rotated.width // 2
            final_y = y - rotated.height // 2
            collage.paste(rotated, (final_x, final_y), rotated)
        
        return collage
```

Save this file, import it, and immediately use:
```bash
python modular_collage_maker.py --folder photos --style flower
```

The modular system makes extending the collage maker **incredibly easy**! 🎉