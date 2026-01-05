"""
FastAPI Backend Server
Main application server for Skateskins video and ad generator
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import shutil
from pathlib import Path
import uvicorn

from video_processor import VideoProcessor
from static_ad_generator import StaticAdGenerator

# Initialize FastAPI app
app = FastAPI(
    title="Skateskins Ad Generator API",
    description="Generate infinite video and static ad variations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize processors
video_processor = VideoProcessor()
ad_generator = StaticAdGenerator()

# Ensure directories exist
Path("uploads/broll").mkdir(parents=True, exist_ok=True)
Path("uploads/photos").mkdir(parents=True, exist_ok=True)
Path("output/videos").mkdir(parents=True, exist_ok=True)
Path("output/static_ads").mkdir(parents=True, exist_ok=True)

# Mount static files and output directories
app.mount("/output", StaticFiles(directory="output"), name="output")


# Pydantic models
class VideoGenerationRequest(BaseModel):
    count: int = 1
    format_id: Optional[str] = None
    hook_id: Optional[str] = None


class StaticAdGenerationRequest(BaseModel):
    count: int = 10
    ad_size: str = "instagram_square"
    layout_id: Optional[str] = None
    color_scheme: Optional[str] = None


class GenerationStatus(BaseModel):
    status: str
    message: str
    generated_files: List[str] = []


# Root endpoint - serve the web interface
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main web interface"""
    html_path = Path("frontend/index.html")
    if html_path.exists():
        return HTMLResponse(content=html_path.read_text())
    return HTMLResponse(content="<h1>Skateskins Ad Generator</h1><p>Frontend not found. See /docs for API.</p>")


# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Skateskins Ad Generator"}


# Video endpoints
@app.get("/api/video/formats")
async def get_video_formats():
    """Get all available video format templates"""
    return {"formats": video_processor.list_available_formats()}


@app.get("/api/video/hooks")
async def get_video_hooks():
    """Get all available hook texts"""
    return {"hooks": video_processor.list_available_hooks()}


@app.get("/api/video/clips")
async def get_uploaded_clips():
    """Get list of uploaded b-roll clips"""
    clips = video_processor.get_broll_clips()
    categorized = video_processor.categorize_clips(clips)

    return {
        "total_clips": len(clips),
        "clips": [str(clip.name) for clip in clips],
        "categories": {
            category: [str(clip.name) for clip in clips_list]
            for category, clips_list in categorized.items()
        }
    }


@app.post("/api/video/upload")
async def upload_video_clip(file: UploadFile = File(...)):
    """Upload a b-roll video clip"""
    try:
        # Save uploaded file
        upload_path = Path("uploads/broll") / file.filename
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "status": "success",
            "message": f"Uploaded {file.filename}",
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/video/generate")
async def generate_video(request: VideoGenerationRequest, background_tasks: BackgroundTasks):
    """Generate video ad(s)"""
    try:
        if request.count == 1:
            # Generate single video synchronously
            video_path = video_processor.generate_video(
                format_id=request.format_id,
                hook_id=request.hook_id
            )
            return {
                "status": "success",
                "message": "Video generated successfully",
                "generated_files": [video_path]
            }
        else:
            # Generate batch
            generated_videos = video_processor.generate_batch(request.count)
            return {
                "status": "success",
                "message": f"Generated {len(generated_videos)} videos",
                "generated_files": generated_videos
            }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/video/list")
async def list_generated_videos():
    """List all generated video files"""
    video_dir = Path("output/videos")
    videos = list(video_dir.glob("*.mp4"))

    return {
        "count": len(videos),
        "videos": [
            {
                "filename": video.name,
                "path": f"/output/videos/{video.name}",
                "size_mb": round(video.stat().st_size / (1024 * 1024), 2)
            }
            for video in sorted(videos, key=lambda x: x.stat().st_mtime, reverse=True)
        ]
    }


# Static ad endpoints
@app.get("/api/ads/layouts")
async def get_ad_layouts():
    """Get all available ad layout templates"""
    return {"layouts": ad_generator.list_available_layouts()}


@app.get("/api/ads/colors")
async def get_color_schemes():
    """Get all available color schemes"""
    return {"color_schemes": ad_generator.list_color_schemes()}


@app.get("/api/ads/photos")
async def get_uploaded_photos():
    """Get list of uploaded product photos"""
    photos = ad_generator.get_product_photos()

    return {
        "total_photos": len(photos),
        "photos": [str(photo.name) for photo in photos]
    }


@app.post("/api/ads/upload")
async def upload_product_photo(file: UploadFile = File(...)):
    """Upload a product photo"""
    try:
        # Save uploaded file
        upload_path = Path("uploads/photos") / file.filename
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "status": "success",
            "message": f"Uploaded {file.filename}",
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/ads/generate")
async def generate_static_ad(request: StaticAdGenerationRequest):
    """Generate static photo ad(s)"""
    try:
        if request.count == 1:
            # Generate single ad
            ad_path = ad_generator.generate_ad(
                layout_id=request.layout_id,
                ad_size=request.ad_size,
                color_scheme=request.color_scheme
            )
            return {
                "status": "success",
                "message": "Ad generated successfully",
                "generated_files": [ad_path]
            }
        else:
            # Generate batch
            generated_ads = ad_generator.generate_batch(
                count=request.count,
                ad_size=request.ad_size
            )
            return {
                "status": "success",
                "message": f"Generated {len(generated_ads)} ads",
                "generated_files": generated_ads
            }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/ads/list")
async def list_generated_ads():
    """List all generated static ad files"""
    ads_dir = Path("output/static_ads")
    ads = list(ads_dir.glob("*.png")) + list(ads_dir.glob("*.jpg"))

    return {
        "count": len(ads),
        "ads": [
            {
                "filename": ad.name,
                "path": f"/output/static_ads/{ad.name}",
                "size_kb": round(ad.stat().st_size / 1024, 2)
            }
            for ad in sorted(ads, key=lambda x: x.stat().st_mtime, reverse=True)
        ]
    }


# Utility endpoints
@app.delete("/api/cleanup")
async def cleanup_generated_files():
    """Delete all generated files (videos and ads)"""
    try:
        # Clean videos
        video_dir = Path("output/videos")
        video_count = 0
        for video in video_dir.glob("*.mp4"):
            video.unlink()
            video_count += 1

        # Clean ads
        ads_dir = Path("output/static_ads")
        ad_count = 0
        for ad in list(ads_dir.glob("*.png")) + list(ads_dir.glob("*.jpg")):
            ad.unlink()
            ad_count += 1

        return {
            "status": "success",
            "message": f"Deleted {video_count} videos and {ad_count} ads"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_statistics():
    """Get overall statistics"""
    clips = video_processor.get_broll_clips()
    photos = ad_generator.get_product_photos()

    video_dir = Path("output/videos")
    videos = list(video_dir.glob("*.mp4"))

    ads_dir = Path("output/static_ads")
    ads = list(ads_dir.glob("*.png")) + list(ads_dir.glob("*.jpg"))

    return {
        "uploads": {
            "broll_clips": len(clips),
            "product_photos": len(photos)
        },
        "generated": {
            "videos": len(videos),
            "static_ads": len(ads)
        },
        "templates": {
            "video_formats": len(video_processor.formats),
            "hooks": len(video_processor.hooks),
            "ad_layouts": len(ad_generator.templates["layouts"]),
            "color_schemes": len(ad_generator.templates["color_schemes"])
        }
    }


if __name__ == "__main__":
    print("=" * 60)
    print("Skateskins Ad Generator Server")
    print("=" * 60)
    print("\n🚀 Starting server...")
    print("📍 Access the app at: http://localhost:8000")
    print("📚 API documentation: http://localhost:8000/docs")
    print("\n" + "=" * 60)

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
