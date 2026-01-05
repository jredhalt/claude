#!/usr/bin/env python3
"""
Example Usage Script
Demonstrates how to use the Skateskins Ad Generator programmatically
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from video_processor import VideoProcessor
from static_ad_generator import StaticAdGenerator


def main():
    print("=" * 60)
    print("Skateskins Ad Generator - Example Usage")
    print("=" * 60)
    print()

    # Initialize processors
    video_processor = VideoProcessor()
    ad_generator = StaticAdGenerator()

    # Check for uploaded content
    clips = video_processor.get_broll_clips()
    photos = ad_generator.get_product_photos()

    print(f"📹 B-Roll Clips Found: {len(clips)}")
    print(f"📸 Product Photos Found: {len(photos)}")
    print()

    if len(clips) == 0:
        print("⚠️  No b-roll clips found!")
        print("   Upload video clips to 'uploads/broll/' to generate videos")
        print()
    else:
        print("Available Video Formats:")
        formats = video_processor.list_available_formats()
        for i, fmt in enumerate(formats, 1):
            print(f"  {i}. {fmt['name']}")
            print(f"     {fmt['description']}")
        print()

        print("Available Hooks (first 5):")
        hooks = video_processor.list_available_hooks()[:5]
        for i, hook in enumerate(hooks, 1):
            print(f"  {i}. {hook['text']}")
        print()

        # Example: Generate a single video
        choice = input("Generate a sample video? (y/n): ").lower()
        if choice == 'y':
            print("\n🎬 Generating video...")
            try:
                video_path = video_processor.generate_video()
                print(f"✅ Video generated: {video_path}")
            except Exception as e:
                print(f"❌ Error: {e}")

    if len(photos) == 0:
        print("\n⚠️  No product photos found!")
        print("   Upload photos to 'uploads/photos/' to generate ads")
        print()
    else:
        print("\nAvailable Ad Layouts:")
        layouts = ad_generator.list_available_layouts()
        for i, layout in enumerate(layouts, 1):
            print(f"  {i}. {layout['name']}")
        print()

        print("Available Color Schemes:")
        schemes = ad_generator.list_color_schemes()
        for i, scheme in enumerate(schemes, 1):
            print(f"  {i}. {scheme}")
        print()

        # Example: Generate a static ad
        choice = input("Generate a sample ad? (y/n): ").lower()
        if choice == 'y':
            print("\n🎨 Generating static ad...")
            try:
                ad_path = ad_generator.generate_ad(ad_size="instagram_square")
                print(f"✅ Ad generated: {ad_path}")
            except Exception as e:
                print(f"❌ Error: {e}")

    print("\n" + "=" * 60)
    print("Examples of Batch Generation:")
    print("=" * 60)
    print()
    print("# Generate 10 random videos:")
    print("videos = video_processor.generate_batch(10)")
    print()
    print("# Generate 20 Instagram Story ads:")
    print("ads = ad_generator.generate_batch(20, ad_size='instagram_story')")
    print()
    print("# Generate video with specific format:")
    print("video = video_processor.generate_video(")
    print("    format_id='step_by_step',")
    print("    hook_id='hook_001'")
    print(")")
    print()
    print("For more examples, see USAGE_GUIDE.md")
    print("=" * 60)


if __name__ == "__main__":
    main()
