"""
Static Ad Generator Module
Creates image-based ads with various layouts and copy combinations
"""

import os
import json
import random
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import textwrap


class StaticAdGenerator:
    def __init__(
        self,
        photos_dir: str = "uploads/photos",
        output_dir: str = "output/static_ads"
    ):
        self.photos_dir = Path(photos_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load copy templates
        self.templates = self._load_json("backend/templates/copy_templates.json")

        # Standard ad sizes
        self.ad_sizes = {
            "instagram_square": (1080, 1080),
            "instagram_story": (1080, 1920),
            "instagram_feed": (1080, 1350),
            "facebook_feed": (1200, 1200),
            "tiktok": (1080, 1920)
        }

    def _load_json(self, filepath: str) -> Dict:
        """Load JSON template file"""
        with open(filepath, 'r') as f:
            return json.load(f)

    def get_product_photos(self) -> List[Path]:
        """Get all product photos from uploads directory"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
        photos = []

        for ext in image_extensions:
            photos.extend(self.photos_dir.glob(f"*{ext}"))

        return sorted(photos)

    def get_font(self, size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
        """
        Get a font object. Falls back to default if custom fonts not available.
        """
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "C:\\Windows\\Fonts\\arial.ttf",
        ]

        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, size)
                except:
                    pass

        # Fallback to default
        return ImageFont.load_default()

    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def add_text_with_background(
        self,
        draw: ImageDraw.Draw,
        text: str,
        position: Tuple[int, int],
        font: ImageFont.FreeTypeFont,
        text_color: Tuple[int, int, int],
        bg_color: Optional[Tuple[int, int, int, int]] = None,
        padding: int = 20,
        max_width: int = None
    ):
        """Add text with optional background rectangle"""
        # Wrap text if max_width specified
        if max_width:
            avg_char_width = font.getlength("A")
            chars_per_line = int(max_width / avg_char_width)
            text = "\n".join(textwrap.wrap(text, width=chars_per_line))

        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Draw background if specified
        if bg_color:
            bg_box = [
                position[0] - padding,
                position[1] - padding,
                position[0] + text_width + padding,
                position[1] + text_height + padding
            ]
            draw.rectangle(bg_box, fill=bg_color)

        # Draw text
        draw.text(position, text, font=font, fill=text_color)

        return (text_width, text_height)

    def create_gradient_background(
        self,
        size: Tuple[int, int],
        color1: Tuple[int, int, int],
        color2: Tuple[int, int, int]
    ) -> Image.Image:
        """Create a gradient background"""
        base = Image.new('RGB', size, color1)
        top = Image.new('RGB', size, color2)

        mask = Image.new('L', size)
        mask_data = []
        for y in range(size[1]):
            mask_data.extend([int(255 * (y / size[1]))] * size[0])
        mask.putdata(mask_data)

        base.paste(top, (0, 0), mask)
        return base

    def process_product_image(
        self,
        image_path: Path,
        target_size: Tuple[int, int],
        position: str = "center",
        size_percent: int = 70
    ) -> Image.Image:
        """Process and position product image"""
        img = Image.open(image_path)

        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Calculate new size
        aspect = img.width / img.height
        target_aspect = target_size[0] / target_size[1]

        if aspect > target_aspect:
            new_width = int(target_size[0] * (size_percent / 100))
            new_height = int(new_width / aspect)
        else:
            new_height = int(target_size[1] * (size_percent / 100))
            new_width = int(new_height * aspect)

        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Create canvas
        canvas = Image.new('RGB', target_size, (255, 255, 255))

        # Position image
        if position == "center":
            x = (target_size[0] - new_width) // 2
            y = (target_size[1] - new_height) // 2
        elif position == "left":
            x = 50
            y = (target_size[1] - new_height) // 2
        elif position == "right":
            x = target_size[0] - new_width - 50
            y = (target_size[1] - new_height) // 2
        else:
            x, y = 0, 0

        canvas.paste(img, (x, y))
        return canvas

    def generate_ad(
        self,
        layout_id: Optional[str] = None,
        ad_size: str = "instagram_square",
        color_scheme: Optional[str] = None,
        headline: Optional[str] = None,
        subheadline: Optional[str] = None,
        cta: Optional[str] = None,
        product_images: Optional[List[Path]] = None,
        output_filename: Optional[str] = None
    ) -> str:
        """
        Generate a single static ad

        Args:
            layout_id: Layout template ID
            ad_size: Size preset key
            color_scheme: Color scheme name
            headline: Custom headline (random if None)
            subheadline: Custom subheadline (random if None)
            cta: Custom CTA (random if None)
            product_images: List of product image paths
            output_filename: Custom output filename

        Returns:
            Path to generated ad image
        """
        # Get product images
        if not product_images:
            all_photos = self.get_product_photos()
            if not all_photos:
                raise ValueError("No product photos found in uploads directory")
            product_images = [random.choice(all_photos)]

        # Select random elements if not specified
        layout = random.choice(self.templates["layouts"]) if not layout_id else \
            next((l for l in self.templates["layouts"] if l["id"] == layout_id), self.templates["layouts"][0])

        color_data = random.choice(self.templates["color_schemes"]) if not color_scheme else \
            next((c for c in self.templates["color_schemes"] if c["name"] == color_scheme), self.templates["color_schemes"][0])

        headline_text = headline or random.choice(self.templates["headlines"])
        subheadline_text = subheadline or random.choice(self.templates["subheadlines"])
        cta_text = cta or random.choice(self.templates["ctas"])

        # Get canvas size
        canvas_size = self.ad_sizes.get(ad_size, self.ad_sizes["instagram_square"])

        # Convert hex colors to RGB
        colors = {
            "primary": self.hex_to_rgb(color_data["primary"]),
            "secondary": self.hex_to_rgb(color_data["secondary"]),
            "accent": self.hex_to_rgb(color_data["accent"]),
            "text": self.hex_to_rgb(color_data["text"]),
            "background": self.hex_to_rgb(color_data["background"])
        }

        # Create base image
        if random.random() < 0.3:  # 30% chance of gradient
            img = self.create_gradient_background(
                canvas_size,
                colors["background"],
                colors["secondary"]
            )
        else:
            img = Image.new('RGB', canvas_size, colors["background"])

        draw = ImageDraw.Draw(img, 'RGBA')

        # Get fonts
        font_headline = self.get_font(80, bold=True)
        font_subheadline = self.get_font(40)
        font_cta = self.get_font(50, bold=True)

        # Layout rendering based on layout type
        layout_name = layout["name"]

        if layout_name == "Bold Headline Top":
            # Headline at top
            self.add_text_with_background(
                draw,
                headline_text,
                (50, 100),
                font_headline,
                colors["text"],
                bg_color=(*colors["primary"], 230),
                padding=30,
                max_width=canvas_size[0] - 100
            )

            # Product image in center
            product_img = self.process_product_image(
                product_images[0],
                canvas_size,
                "center",
                70
            )
            img.paste(product_img, (0, int(canvas_size[1] * 0.15)))

            # Subheadline
            self.add_text_with_background(
                draw,
                subheadline_text,
                (50, int(canvas_size[1] * 0.65)),
                font_subheadline,
                colors["text"],
                max_width=canvas_size[0] - 100
            )

            # CTA button
            cta_width = 400
            cta_height = 100
            cta_x = (canvas_size[0] - cta_width) // 2
            cta_y = canvas_size[1] - 150

            draw.rounded_rectangle(
                [cta_x, cta_y, cta_x + cta_width, cta_y + cta_height],
                radius=15,
                fill=colors["accent"]
            )

            cta_bbox = draw.textbbox((0, 0), cta_text, font=font_cta)
            cta_text_width = cta_bbox[2] - cta_bbox[0]
            cta_text_height = cta_bbox[3] - cta_bbox[1]

            draw.text(
                (cta_x + (cta_width - cta_text_width) // 2,
                 cta_y + (cta_height - cta_text_height) // 2),
                cta_text,
                font=font_cta,
                fill=(255, 255, 255)
            )

        elif layout_name == "Side by Side":
            # Product image on left half
            left_img = self.process_product_image(
                product_images[0],
                (canvas_size[0] // 2, canvas_size[1]),
                "center",
                80
            )
            img.paste(left_img, (0, 0))

            # Text on right half
            right_x = canvas_size[0] // 2 + 50
            self.add_text_with_background(
                draw,
                headline_text,
                (right_x, 150),
                font_headline,
                colors["text"],
                max_width=canvas_size[0] // 2 - 100
            )

            self.add_text_with_background(
                draw,
                subheadline_text,
                (right_x, 400),
                font_subheadline,
                colors["text"],
                max_width=canvas_size[0] // 2 - 100
            )

            # CTA button on right
            cta_width = 300
            cta_height = 80
            cta_x = right_x
            cta_y = canvas_size[1] - 200

            draw.rounded_rectangle(
                [cta_x, cta_y, cta_x + cta_width, cta_y + cta_height],
                radius=12,
                fill=colors["accent"]
            )

            cta_bbox = draw.textbbox((0, 0), cta_text, font=font_cta)
            cta_text_width = cta_bbox[2] - cta_bbox[0]
            cta_text_height = cta_bbox[3] - cta_bbox[1]

            draw.text(
                (cta_x + (cta_width - cta_text_width) // 2,
                 cta_y + (cta_height - cta_text_height) // 2),
                cta_text,
                font=font_cta,
                fill=(255, 255, 255)
            )

        elif layout_name == "Minimal Center":
            # Full-size product image
            product_img = self.process_product_image(
                product_images[0],
                canvas_size,
                "center",
                90
            )
            img.paste(product_img, (0, 0))

            # Headline overlay at top
            self.add_text_with_background(
                draw,
                headline_text,
                (50, 80),
                font_headline,
                (255, 255, 255),
                bg_color=(0, 0, 0, 200),
                padding=30,
                max_width=canvas_size[0] - 100
            )

            # CTA at bottom
            cta_width = canvas_size[0] - 100
            cta_height = 100
            cta_x = 50
            cta_y = canvas_size[1] - 150

            draw.rounded_rectangle(
                [cta_x, cta_y, cta_x + cta_width, cta_y + cta_height],
                radius=15,
                fill=(*colors["accent"], 240)
            )

            cta_bbox = draw.textbbox((0, 0), cta_text, font=font_cta)
            cta_text_width = cta_bbox[2] - cta_bbox[0]
            cta_text_height = cta_bbox[3] - cta_bbox[1]

            draw.text(
                (cta_x + (cta_width - cta_text_width) // 2,
                 cta_y + (cta_height - cta_text_height) // 2),
                cta_text,
                font=font_cta,
                fill=(255, 255, 255)
            )

        else:
            # Default simple layout
            # Headline at top
            self.add_text_with_background(
                draw,
                headline_text,
                (50, 100),
                font_headline,
                colors["text"],
                max_width=canvas_size[0] - 100
            )

            # Product image
            product_img = self.process_product_image(
                product_images[0],
                canvas_size,
                "center",
                60
            )
            img.paste(product_img, (0, int(canvas_size[1] * 0.25)))

            # CTA
            cta_width = 350
            cta_height = 90
            cta_x = (canvas_size[0] - cta_width) // 2
            cta_y = canvas_size[1] - 150

            draw.rounded_rectangle(
                [cta_x, cta_y, cta_x + cta_width, cta_y + cta_height],
                radius=15,
                fill=colors["accent"]
            )

            cta_bbox = draw.textbbox((0, 0), cta_text, font=font_cta)
            cta_text_width = cta_bbox[2] - cta_bbox[0]
            cta_text_height = cta_bbox[3] - cta_bbox[1]

            draw.text(
                (cta_x + (cta_width - cta_text_width) // 2,
                 cta_y + (cta_height - cta_text_height) // 2),
                cta_text,
                font=font_cta,
                fill=(255, 255, 255)
            )

        # Generate output filename
        if not output_filename:
            output_filename = f"skateskins_ad_{layout['id']}_{color_data['name'].replace(' ', '_')}_{random.randint(1000, 9999)}.png"

        output_path = self.output_dir / output_filename

        # Save image
        img.save(str(output_path), quality=95, optimize=True)

        return str(output_path)

    def generate_batch(self, count: int = 10, ad_size: str = "instagram_square") -> List[str]:
        """Generate multiple unique ad variations"""
        generated_ads = []

        for i in range(count):
            print(f"Generating ad {i + 1}/{count}...")
            try:
                ad_path = self.generate_ad(ad_size=ad_size)
                generated_ads.append(ad_path)
                print(f"✓ Generated: {ad_path}")
            except Exception as e:
                print(f"✗ Error generating ad {i + 1}: {str(e)}")

        return generated_ads

    def list_available_layouts(self) -> List[Dict]:
        """Return list of available layouts"""
        return [
            {
                "id": layout["id"],
                "name": layout["name"]
            }
            for layout in self.templates["layouts"]
        ]

    def list_color_schemes(self) -> List[str]:
        """Return list of available color schemes"""
        return [scheme["name"] for scheme in self.templates["color_schemes"]]


if __name__ == "__main__":
    # Test the static ad generator
    generator = StaticAdGenerator()

    print("Available layouts:")
    for layout in generator.list_available_layouts():
        print(f"  - {layout['name']}")

    print("\nAvailable color schemes:")
    for scheme in generator.list_color_schemes():
        print(f"  - {scheme}")

    print("\nTo generate ads, use:")
    print("  generator.generate_ad()  # Single ad")
    print("  generator.generate_batch(10)  # 10 ads")
