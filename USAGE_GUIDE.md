# Skateskins Ad Generator - Usage Guide

## Quick Start

### 1. Installation

#### Prerequisites
- Python 3.8 or higher
- FFmpeg (for video processing)
- 2GB+ RAM
- Storage space for videos

#### Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

#### Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Starting the Server

**Linux/macOS:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```batch
start.bat
```

**Manual Start:**
```bash
cd backend
python app.py
```

The server will start at `http://localhost:8000`

---

## Using the Web Interface

### Video Generation

#### Step 1: Upload B-Roll Clips

1. Go to the "Video Generator" tab
2. Click the upload zone or drag & drop video files
3. Supported formats: MP4, MOV, AVI

**Naming Convention (Optional but Recommended):**
- `unboxing_01.mp4` - Unboxing footage
- `application_01.mp4` - Application/installation footage
- `ice_01.mp4` - Ice/skating footage
- `product_01.mp4` - Product close-ups
- `before_01.mp4` - Before shots
- `after_01.mp4` - After shots

The tool automatically categorizes clips based on filenames for better template matching.

#### Step 2: Generate Videos

1. Select number of videos to generate (1-50)
2. (Optional) Choose a specific format or leave as "Random"
3. Click "Generate Videos"
4. Wait for processing (typically 1-3 minutes per video)

#### Video Format Templates

The tool includes 8 built-in templates:

1. **Static Hook** - Simple text hook + b-roll compilation
2. **Step-by-Step** - "5 Steps to Install" tutorial format
3. **Before/After** - Transformation showcase
4. **Quick Tip** - Short punchy tips with overlays
5. **Product Showcase** - Feature highlights
6. **Satisfying Compilation** - ASMR-style application footage
7. **POV Format** - First-person perspective
8. **Comparison** - Compare with alternatives

### Static Ad Generation

#### Step 1: Upload Product Photos

1. Go to the "Static Ads" tab
2. Click the upload zone or drag & drop images
3. Supported formats: JPG, PNG

**Photo Tips:**
- Use high-resolution images (1080px+)
- Include variety: close-ups, action shots, lifestyle
- Clean backgrounds work best

#### Step 2: Generate Ads

1. Select number of ads to generate (1-50)
2. Choose ad size:
   - Instagram Square (1080x1080)
   - Instagram Story (1080x1920)
   - Instagram Feed (1080x1350)
   - Facebook Feed (1200x1200)
   - TikTok (1080x1920)
3. Click "Generate Static Ads"
4. Wait for processing (typically 1-5 seconds per ad)

#### Ad Layouts

The tool includes 6 layout templates:
- Bold Headline Top
- Side by Side
- Minimal Center
- Feature Grid
- Before After
- Hero Image

#### Copy Variations

The tool automatically generates unique copy combinations using:
- 15+ headline variations
- 13+ subheadline options
- 12+ CTA variations
- 7+ body copy options
- 5 color schemes

---

## Using the API

The tool provides a REST API for programmatic access.

### API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

### Example API Calls

#### Generate a Single Video
```bash
curl -X POST "http://localhost:8000/api/video/generate" \
  -H "Content-Type: application/json" \
  -d '{"count": 1, "format_id": "static_hook"}'
```

#### Generate 10 Videos
```bash
curl -X POST "http://localhost:8000/api/video/generate" \
  -H "Content-Type: application/json" \
  -d '{"count": 10}'
```

#### Generate 10 Instagram Story Ads
```bash
curl -X POST "http://localhost:8000/api/ads/generate" \
  -H "Content-Type: application/json" \
  -d '{"count": 10, "ad_size": "instagram_story"}'
```

#### List Generated Videos
```bash
curl "http://localhost:8000/api/video/list"
```

#### Get Statistics
```bash
curl "http://localhost:8000/api/stats"
```

---

## Using Python Scripts Directly

### Video Generation Script

```python
from backend.video_processor import VideoProcessor

# Initialize processor
processor = VideoProcessor()

# Generate a single video with random format and hook
video_path = processor.generate_video()
print(f"Generated: {video_path}")

# Generate with specific format
video_path = processor.generate_video(
    format_id="step_by_step",
    hook_id="hook_001"
)

# Generate batch of 10 videos
videos = processor.generate_batch(count=10)
print(f"Generated {len(videos)} videos")

# List available formats
formats = processor.list_available_formats()
for fmt in formats:
    print(f"- {fmt['name']}: {fmt['description']}")

# List available hooks
hooks = processor.list_available_hooks()
for hook in hooks:
    print(f"- {hook['text']}")
```

### Static Ad Generation Script

```python
from backend.static_ad_generator import StaticAdGenerator

# Initialize generator
generator = StaticAdGenerator()

# Generate a single ad
ad_path = generator.generate_ad(
    ad_size="instagram_square",
    layout_id="layout_01",
    color_scheme="Ice Blue"
)
print(f"Generated: {ad_path}")

# Generate batch of 10 ads
ads = generator.generate_batch(
    count=10,
    ad_size="instagram_story"
)
print(f"Generated {len(ads)} ads")

# List available layouts
layouts = generator.list_available_layouts()
for layout in layouts:
    print(f"- {layout['name']}")

# List color schemes
schemes = generator.list_color_schemes()
for scheme in schemes:
    print(f"- {scheme}")
```

---

## Customization

### Adding Custom Hooks

Edit `backend/templates/hooks.json`:

```json
{
  "hooks": [
    {
      "id": "hook_custom_001",
      "text": "Your custom hook text here",
      "duration": 2.0,
      "style": "bold_center"
    }
  ]
}
```

**Styles:**
- `bold_center` - Large, centered, bold text
- `top_left` - Upper left corner
- `bottom_center` - Bottom center
- `minimal` - Simple, clean style

### Adding Custom Copy

Edit `backend/templates/copy_templates.json`:

Add to `headlines`, `subheadlines`, `ctas`, or `body_copy` arrays.

### Adding Custom Color Schemes

Edit `backend/templates/copy_templates.json`:

```json
{
  "color_schemes": [
    {
      "name": "Your Scheme",
      "primary": "#HEX",
      "secondary": "#HEX",
      "accent": "#HEX",
      "text": "#HEX",
      "background": "#HEX"
    }
  ]
}
```

---

## Tips for Best Results

### Video Generation

1. **Upload Variety**: Include different types of footage (unboxing, application, ice shots)
2. **Name Files**: Use descriptive filenames for better categorization
3. **Quality**: Use 1080p or higher resolution clips
4. **Duration**: 3-10 second clips work best
5. **Lighting**: Well-lit footage produces better results
6. **Batch Generate**: Create 10-20 variations to test different combinations

### Static Ad Generation

1. **High Resolution**: Use images 1080px or larger
2. **Clean Backgrounds**: Simple backgrounds work better for overlays
3. **Multiple Photos**: Upload variety for more diverse results
4. **Test Sizes**: Generate for multiple platforms (IG, FB, TikTok)
5. **A/B Testing**: Generate 10+ variations to find winners

### A/B Testing Strategy

1. Generate 20-30 video variations
2. Generate 20-30 static ad variations
3. Upload to Facebook Ads Manager or TikTok Ads
4. Let each variation spend $5-10
5. Scale the winners
6. Generate more variations of winning formats

---

## Troubleshooting

### "No video clips found"
- Ensure you've uploaded videos to `uploads/broll/`
- Check file extensions (.mp4, .mov, .avi)

### "FFmpeg not found"
- Install FFmpeg (see installation section)
- Ensure FFmpeg is in your system PATH

### Videos are too long/short
- Edit `backend/templates/formats.json` to adjust `total_duration`
- Edit individual segment durations

### Text doesn't fit on screen
- Edit font sizes in `backend/video_processor.py`
- Shorten hook text in `backend/templates/hooks.json`

### Low quality output
- Increase the FPS in `backend/video_processor.py` (default: 30)
- Use higher resolution source clips

### Server won't start
- Check if port 8000 is already in use
- Try changing the port in `backend/app.py`

---

## Advanced Usage

### Batch Processing Script

Create a script to generate large batches:

```python
from backend.video_processor import VideoProcessor
from backend.static_ad_generator import StaticAdGenerator

# Generate 50 videos
processor = VideoProcessor()
videos = processor.generate_batch(50)

# Generate 50 ads across different sizes
generator = StaticAdGenerator()
sizes = ["instagram_square", "instagram_story", "tiktok"]
for size in sizes:
    ads = generator.generate_batch(count=20, ad_size=size)
```

### Automated Upload to Social Media

You can integrate with social media APIs to auto-upload:
- Facebook Graph API
- Instagram Graph API
- TikTok API

Example workflow:
1. Generate videos with this tool
2. Use `requests` library to upload via API
3. Schedule posts using platform scheduling features

---

## Support

For issues or questions:
- Check the troubleshooting section
- Review API docs at `/docs`
- Check server logs for error messages

---

## Performance Tips

- **Hardware**: More RAM = faster processing
- **Parallel Processing**: Run multiple instances on different ports
- **Storage**: Use SSD for faster read/write
- **Batch Size**: Generate 10-20 at a time for optimal performance
