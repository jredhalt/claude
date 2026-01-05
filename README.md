# Skateskins Video Compilation & Ad Generator

An automated tool for generating infinite variations of video ads and static image ads from b-roll footage and product photos.

## Features

### Video Compilation
- Upload b-roll footage (unboxing, application, ice shots)
- Generate unlimited unique video combinations
- Multiple format templates:
  - Static text hooks
  - Step-by-step tutorials ("5 Steps to Install Your Skateskins")
  - Before/After showcases
  - Quick tips format
  - Product highlight reels
- Automatic text overlay variations
- Optimized for TikTok and Instagram Reels

### Static Photo Ads
- Upload product photos and inspiration ads
- Generate 10+ variations at a time
- AI-powered copy generation
- Multiple graphic layouts
- Different color schemes and text placements

## Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install FFmpeg (required for video processing)
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# macOS:
brew install ffmpeg

# Windows:
# Download from https://ffmpeg.org/download.html
```

## Usage

### Start the Server
```bash
python backend/app.py
```

### Access the Web Interface
Open http://localhost:8000 in your browser

### Generate Videos
1. Upload your b-roll clips to the `uploads/broll/` folder
2. Select a template format (or generate random variations)
3. Click "Generate Videos" and specify how many variations you want
4. Download generated videos from `output/videos/`

### Generate Static Ads
1. Upload product photos to `uploads/photos/`
2. (Optional) Upload inspiration ads to `uploads/inspiration/`
3. Click "Generate Static Ads"
4. Download generated ads from `output/static_ads/`

## Project Structure

```
skateskins-video-tool/
├── backend/
│   ├── app.py                    # FastAPI server
│   ├── video_processor.py        # Video compilation engine
│   ├── static_ad_generator.py    # Photo ad generator
│   ├── templates/                # Video format templates
│   │   ├── hooks.json           # Text hook variations
│   │   ├── formats.json         # Video format templates
│   │   └── copy_templates.json  # Static ad copy templates
│   └── utils/
│       ├── text_overlay.py      # Text rendering utilities
│       └── ai_generator.py      # AI copy generation
├── frontend/
│   ├── index.html               # Web interface
│   └── style.css
├── uploads/
│   ├── broll/                   # User uploaded video clips
│   ├── photos/                  # Product photos
│   └── inspiration/             # Inspiration static ads
├── output/
│   ├── videos/                  # Generated video ads
│   └── static_ads/              # Generated photo ads
├── requirements.txt
└── README.md
```

## Template Formats

The tool includes several built-in video formats:

1. **Static Hook**: Simple text overlay at the start
2. **Step-by-Step**: Numbered steps (e.g., "5 Steps to Install")
3. **Before/After**: Comparison format
4. **Quick Tip**: Short, punchy advice format
5. **Product Showcase**: Feature highlights

## Customization

Edit template files in `backend/templates/` to customize:
- Text hooks and CTAs
- Video formats and structures
- Static ad copy variations
- Font styles and colors

## Requirements

- Python 3.8+
- FFmpeg
- 2GB+ RAM for video processing
- Storage space for video output
