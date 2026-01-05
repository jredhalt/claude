"""
Video Processor Module
Handles video compilation, text overlays, and clip composition
"""

import os
import json
import random
from pathlib import Path
from typing import List, Dict, Any, Optional
from moviepy.editor import (
    VideoFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
    ColorClip
)
from moviepy.video.fx import resize, speedx
import numpy as np


class VideoProcessor:
    def __init__(self, uploads_dir: str = "uploads/broll", output_dir: str = "output/videos"):
        self.uploads_dir = Path(uploads_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load templates
        self.hooks = self._load_json("backend/templates/hooks.json")["hooks"]
        self.formats = self._load_json("backend/templates/formats.json")["formats"]

        # Video settings for social media
        self.target_width = 1080
        self.target_height = 1920  # 9:16 vertical format
        self.fps = 30

    def _load_json(self, filepath: str) -> Dict:
        """Load JSON template file"""
        with open(filepath, 'r') as f:
            return json.load(f)

    def get_broll_clips(self) -> List[Path]:
        """Get all video files from uploads directory"""
        video_extensions = ['.mp4', '.mov', '.avi', '.MP4', '.MOV']
        clips = []

        for ext in video_extensions:
            clips.extend(self.uploads_dir.glob(f"*{ext}"))

        return sorted(clips)

    def categorize_clips(self, clips: List[Path]) -> Dict[str, List[Path]]:
        """
        Categorize clips based on filename keywords
        Expected naming: unboxing_01.mp4, application_01.mp4, ice_01.mp4, etc.
        """
        categories = {
            "unboxing": [],
            "application": [],
            "ice_shots": [],
            "product": [],
            "before": [],
            "after": [],
            "general": []
        }

        for clip in clips:
            filename_lower = clip.stem.lower()

            if any(word in filename_lower for word in ["unbox", "opening", "package"]):
                categories["unboxing"].append(clip)
            elif any(word in filename_lower for word in ["apply", "install", "peel", "stick"]):
                categories["application"].append(clip)
            elif any(word in filename_lower for word in ["ice", "rink", "skating", "hockey"]):
                categories["ice_shots"].append(clip)
            elif any(word in filename_lower for word in ["product", "closeup", "detail"]):
                categories["product"].append(clip)
            elif "before" in filename_lower:
                categories["before"].append(clip)
            elif "after" in filename_lower:
                categories["after"].append(clip)
            else:
                categories["general"].append(clip)

        return categories

    def create_text_clip(
        self,
        text: str,
        duration: float,
        style: str = "bold_center",
        size: tuple = None
    ) -> CompositeVideoClip:
        """
        Create a text overlay clip

        Styles: bold_center, top_left, bottom_center, minimal
        """
        if size is None:
            size = (self.target_width, self.target_height)

        # Style configurations
        style_configs = {
            "bold_center": {
                "fontsize": 70,
                "color": "white",
                "font": "Arial-Bold",
                "stroke_color": "black",
                "stroke_width": 3,
                "method": "caption",
                "size": (size[0] - 100, None),
                "align": "center"
            },
            "top_left": {
                "fontsize": 50,
                "color": "white",
                "font": "Arial-Bold",
                "stroke_color": "black",
                "stroke_width": 2,
                "method": "label"
            },
            "bottom_center": {
                "fontsize": 60,
                "color": "white",
                "font": "Arial-Bold",
                "stroke_color": "black",
                "stroke_width": 2,
                "method": "caption",
                "size": (size[0] - 100, None),
                "align": "center"
            },
            "minimal": {
                "fontsize": 45,
                "color": "white",
                "font": "Arial",
                "method": "label"
            }
        }

        config = style_configs.get(style, style_configs["bold_center"])

        # Create text clip
        txt_clip = TextClip(
            text,
            fontsize=config["fontsize"],
            color=config["color"],
            font=config.get("font", "Arial"),
            stroke_color=config.get("stroke_color"),
            stroke_width=config.get("stroke_width", 0),
            method=config["method"],
            size=config.get("size")
        ).set_duration(duration)

        # Create background
        bg = ColorClip(size=size, color=(0, 0, 0)).set_duration(duration)

        # Position text based on style
        if style == "top_left":
            txt_clip = txt_clip.set_position((50, 100))
        elif style == "bottom_center":
            txt_clip = txt_clip.set_position(("center", size[1] - 200))
        else:  # center
            txt_clip = txt_clip.set_position("center")

        return CompositeVideoClip([bg, txt_clip])

    def process_clip(
        self,
        clip_path: Path,
        duration: float = None,
        apply_effects: bool = False
    ) -> VideoFileClip:
        """Load and process a video clip"""
        clip = VideoFileClip(str(clip_path))

        # Resize to target dimensions (9:16 vertical)
        clip = clip.resize((self.target_width, self.target_height))

        # Apply duration if specified
        if duration and clip.duration > duration:
            # Random start time for variety
            max_start = max(0, clip.duration - duration)
            start_time = random.uniform(0, max_start)
            clip = clip.subclip(start_time, start_time + duration)
        elif duration and clip.duration < duration:
            # Loop if too short
            times_to_loop = int(np.ceil(duration / clip.duration))
            clip = concatenate_videoclips([clip] * times_to_loop).subclip(0, duration)

        # Apply effects if requested
        if apply_effects:
            # Randomly apply slow motion to some clips
            if random.random() < 0.3:
                clip = clip.fx(speedx, 0.7)

        return clip

    def generate_video(
        self,
        format_id: Optional[str] = None,
        hook_id: Optional[str] = None,
        output_filename: Optional[str] = None
    ) -> str:
        """
        Generate a single video based on format and hook

        Args:
            format_id: ID of the format template (random if None)
            hook_id: ID of the hook (random if None)
            output_filename: Custom output filename (auto-generated if None)

        Returns:
            Path to generated video file
        """
        # Get all available clips
        all_clips = self.get_broll_clips()
        if not all_clips:
            raise ValueError("No video clips found in uploads directory")

        categorized_clips = self.categorize_clips(all_clips)

        # Select format and hook
        video_format = random.choice(self.formats) if not format_id else \
            next((f for f in self.formats if f["id"] == format_id), self.formats[0])

        selected_hook = random.choice(self.hooks) if not hook_id else \
            next((h for h in self.hooks if h["id"] == hook_id), self.hooks[0])

        # Build video sequence
        clips_sequence = []

        for segment in video_format["structure"]:
            seg_type = segment["type"]

            if seg_type == "text_overlay":
                # Use hook text or custom text
                if segment.get("source") == "hook":
                    text = selected_hook["text"]
                    duration = selected_hook["duration"]
                    style = selected_hook.get("style", "bold_center")
                else:
                    text = segment.get("text", "")
                    duration = segment.get("duration", 2.0)
                    style = segment.get("style", "bold_center")

                text_clip = self.create_text_clip(text, duration, style)
                clips_sequence.append(text_clip)

            elif seg_type == "broll_compilation":
                # Random compilation of clips
                min_clips = segment.get("min_clips", 3)
                max_clips = segment.get("max_clips", 5)
                num_clips = random.randint(min_clips, max_clips)

                clip_duration_range = segment.get("clip_duration", [2, 4])
                category = segment.get("category")

                # Select clips from category or all
                if category and categorized_clips.get(category):
                    available_clips = categorized_clips[category]
                else:
                    available_clips = all_clips

                selected_clips = random.sample(
                    available_clips,
                    min(num_clips, len(available_clips))
                )

                for clip_path in selected_clips:
                    duration = random.uniform(*clip_duration_range)
                    apply_fx = segment.get("slow_mo", False)
                    clip = self.process_clip(clip_path, duration, apply_fx)
                    clips_sequence.append(clip)

            elif seg_type in ["step", "feature", "tip_overlay"]:
                # Text overlay on b-roll
                step_text = segment.get("text", "")
                if seg_type == "step":
                    step_text = f"{segment.get('number', '')}. {step_text}"

                duration = segment.get("duration", 3.0)
                category = segment.get("broll")

                # Get appropriate b-roll
                if category and categorized_clips.get(category):
                    clip_path = random.choice(categorized_clips[category])
                else:
                    clip_path = random.choice(all_clips)

                broll_clip = self.process_clip(clip_path, duration)
                text_clip = TextClip(
                    step_text,
                    fontsize=60,
                    color="white",
                    font="Arial-Bold",
                    stroke_color="black",
                    stroke_width=3,
                    method="caption",
                    size=(self.target_width - 100, None),
                    align="center"
                ).set_duration(duration).set_position(("center", 100))

                composite = CompositeVideoClip([broll_clip, text_clip])
                clips_sequence.append(composite)

            elif seg_type == "broll":
                # Single b-roll clip
                category = segment.get("category")
                duration = segment.get("duration", 3.0)

                if category and categorized_clips.get(category):
                    clip_path = random.choice(categorized_clips[category])
                else:
                    clip_path = random.choice(all_clips)

                clip = self.process_clip(clip_path, duration)
                clips_sequence.append(clip)

            elif seg_type == "cta":
                # Call to action
                text = segment.get("text", "Get yours now!")
                duration = segment.get("duration", 2.0)
                cta_clip = self.create_text_clip(text, duration, "bold_center")
                clips_sequence.append(cta_clip)

        # Concatenate all clips
        final_video = concatenate_videoclips(clips_sequence, method="compose")

        # Generate output filename
        if not output_filename:
            output_filename = f"skateskins_{video_format['id']}_{selected_hook['id']}_{random.randint(1000, 9999)}.mp4"

        output_path = self.output_dir / output_filename

        # Export video
        final_video.write_videofile(
            str(output_path),
            fps=self.fps,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
            preset="medium",
            threads=4
        )

        # Clean up
        final_video.close()
        for clip in clips_sequence:
            clip.close()

        return str(output_path)

    def generate_batch(self, count: int = 10) -> List[str]:
        """Generate multiple unique video variations"""
        generated_videos = []

        for i in range(count):
            print(f"Generating video {i + 1}/{count}...")
            try:
                video_path = self.generate_video()
                generated_videos.append(video_path)
                print(f"✓ Generated: {video_path}")
            except Exception as e:
                print(f"✗ Error generating video {i + 1}: {str(e)}")

        return generated_videos

    def list_available_formats(self) -> List[Dict]:
        """Return list of available video formats"""
        return [
            {
                "id": fmt["id"],
                "name": fmt["name"],
                "description": fmt["description"]
            }
            for fmt in self.formats
        ]

    def list_available_hooks(self) -> List[Dict]:
        """Return list of available hooks"""
        return [
            {
                "id": hook["id"],
                "text": hook["text"]
            }
            for hook in self.hooks
        ]


if __name__ == "__main__":
    # Test the video processor
    processor = VideoProcessor()

    print("Available formats:")
    for fmt in processor.list_available_formats():
        print(f"  - {fmt['name']}: {fmt['description']}")

    print("\nAvailable hooks:")
    for hook in processor.list_available_hooks()[:5]:
        print(f"  - {hook['text']}")

    print("\nTo generate videos, use:")
    print("  processor.generate_video()  # Single video")
    print("  processor.generate_batch(10)  # 10 videos")
