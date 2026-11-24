#!/usr/bin/env python3
"""
Thumbnail Generator Module - Shorts Edition
Creates eye-catching YouTube Shorts thumbnails with Bangla text support
"""

import os
import json
from pathlib import Path
from typing import Tuple, Optional, Dict
from dotenv import load_dotenv

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️  Pillow not installed. Install with: pip install Pillow")

# Load environment variables
load_dotenv()


class ThumbnailGenerator:
    """Generate YouTube Shorts thumbnails with Bangla text"""

    # YouTube Shorts thumbnail recommended size (9:16 aspect ratio)
    THUMBNAIL_SIZE = (1080, 1920)

    def __init__(self):
        if not PIL_AVAILABLE:
            raise RuntimeError("Pillow is required. Install with: pip install Pillow")

        self.output_dir = os.getenv('OUTPUT_DIR', 'output')
        self.thumbnail_dir = Path(self.output_dir) / 'thumbnails'
        self.thumbnail_dir.mkdir(parents=True, exist_ok=True)

        # Bangla font path
        self.bangla_font = self._get_bangla_font()

    def create_thumbnail(
        self,
        title: str,
        background_image: Optional[str] = None,
        background_color: Tuple[int, int, int] = (15, 15, 35),
        text_color: Tuple[int, int, int] = (255, 255, 255),
        accent_color: Tuple[int, int, int] = (255, 100, 100),  # Naruto red/orange
        output_filename: str = "thumbnail.jpg"
    ) -> str:
        """
        Create a YouTube Shorts thumbnail with Bangla text

        Args:
            title: Video title text (Bangla)
            background_image: Path to background image (optional)
            background_color: RGB color for solid background if no image
            text_color: RGB color for title text
            accent_color: RGB color for accent elements (Naruto theme)
            output_filename: Output filename

        Returns:
            Path to generated thumbnail
        """

        print(f"🎨 Creating Shorts thumbnail...")

        # Create base image
        if background_image and os.path.exists(background_image):
            thumbnail = self._create_from_image(background_image)
        else:
            thumbnail = self._create_gradient_background(background_color, accent_color)

        # Add title text (Bangla)
        thumbnail = self._add_bangla_title_text(thumbnail, title, text_color, accent_color)

        # Add Naruto-themed decorative elements
        thumbnail = self._add_naruto_elements(thumbnail, accent_color)

        # Add visual polish
        thumbnail = self._add_visual_polish(thumbnail)

        # Save thumbnail
        output_path = self.thumbnail_dir / output_filename
        thumbnail.save(output_path, "JPEG", quality=95, optimize=True)

        print(f"✅ Thumbnail saved to: {output_path}")

        return str(output_path)

    def _create_from_image(self, image_path: str) -> Image.Image:
        """Create thumbnail from existing image"""

        img = Image.open(image_path)

        # Resize to thumbnail dimensions (fill)
        img = img.resize(self.THUMBNAIL_SIZE, Image.Resampling.LANCZOS)

        # Apply slight darkening for text readability
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.5)

        # Add slight blur to background
        img = img.filter(ImageFilter.GaussianBlur(radius=3))

        return img

    def _create_gradient_background(
        self,
        base_color: Tuple[int, int, int],
        accent_color: Tuple[int, int, int]
    ) -> Image.Image:
        """Create a gradient background with Naruto theme"""

        width, height = self.THUMBNAIL_SIZE
        img = Image.new('RGB', self.THUMBNAIL_SIZE)
        draw = ImageDraw.Draw(img)

        # Create vertical gradient with Naruto colors
        # Dark blue/purple to orange/red (Naruto theme)
        for y in range(height):
            ratio = y / height

            # Multi-stop gradient
            if ratio < 0.3:
                # Top: Dark blue (night)
                r = int(base_color[0] + (20 - base_color[0]) * (ratio / 0.3))
                g = int(base_color[1] + (15 - base_color[1]) * (ratio / 0.3))
                b = int(base_color[2] + (50 - base_color[2]) * (ratio / 0.3))
            elif ratio < 0.7:
                # Middle: Purple/transition
                mid_ratio = (ratio - 0.3) / 0.4
                r = int(20 + (accent_color[0] - 20) * mid_ratio)
                g = int(15 + (accent_color[1] - 15) * mid_ratio)
                b = int(50 + (accent_color[2] - 50) * mid_ratio)
            else:
                # Bottom: Orange/red (Naruto)
                bot_ratio = (ratio - 0.7) / 0.3
                r = int(accent_color[0] + (255 - accent_color[0]) * bot_ratio)
                g = int(accent_color[1] + (80 - accent_color[1]) * bot_ratio)
                b = int(accent_color[2] + (0 - accent_color[2]) * bot_ratio)

            draw.line([(0, y), (width, y)], fill=(r, g, b))

        return img

    def _add_bangla_title_text(
        self,
        img: Image.Image,
        title: str,
        text_color: Tuple[int, int, int],
        accent_color: Tuple[int, int, int]
    ) -> Image.Image:
        """Add Bangla title text to thumbnail"""

        draw = ImageDraw.Draw(img)
        width, height = img.size

        # Load Bangla font
        try:
            if self.bangla_font:
                # Try different sizes
                font_size = 72
                font = ImageFont.truetype(self.bangla_font, font_size)
            else:
                font = ImageFont.load_default()
                print("⚠️  Using default font. Install Noto Sans Bengali for better Bangla rendering.")
        except Exception as e:
            print(f"⚠️  Font loading failed: {e}, using default")
            font = ImageFont.load_default()

        # Clean title - remove any English "What If" prefix if present
        clean_title = title.replace("What If", "").replace("what if", "").strip()

        # Split title into multiple lines for vertical layout
        words = clean_title.split()
        lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)

            # Check if line is too long
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] > width * 0.85:
                if len(current_line) > 1:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(test_line)
                    current_line = []

        if current_line:
            lines.append(' '.join(current_line))

        # Limit to 4 lines for Shorts thumbnail
        lines = lines[:4]

        # Calculate total text height
        line_height = 95
        total_height = len(lines) * line_height

        # Starting Y position (upper third for Shorts)
        y = height // 4

        # Draw each line with shadow and outline
        for line in lines:
            # Get text bounding box
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]

            # Center horizontally
            x = (width - text_width) // 2

            # Draw shadow (multiple layers for depth)
            shadow_offsets = [(4, 4), (3, 3), (2, 2)]
            for i, (sx, sy) in enumerate(shadow_offsets):
                alpha = 180 - i * 40
                draw.text(
                    (x + sx, y + sy),
                    line,
                    font=font,
                    fill=(0, 0, 0, alpha)
                )

            # Draw main text
            draw.text((x, y), line, font=font, fill=text_color)

            # Add subtle glow effect
            glow_font = ImageFont.truetype(self.bangla_font, font_size + 4) if self.bangla_font else font
            draw.text((x, y), line, font=glow_font, fill=accent_color + (50,))

            y += line_height

        return img

    def _add_naruto_elements(self, img: Image.Image, accent_color: Tuple[int, int, int]) -> Image.Image:
        """Add Naruto-themed decorative elements"""

        draw = ImageDraw.Draw(img)
        width, height = img.size

        # Add Sharingan-like circles at corners
        circle_positions = [
            (width * 0.08, height * 0.15),  # Top-left
            (width * 0.92, height * 0.15),  # Top-right
            (width * 0.08, height * 0.85),  # Bottom-left
            (width * 0.92, height * 0.85),  # Bottom-right
        ]

        for cx, cy in circle_positions:
            radius = 35
            # Outer ring
            draw.ellipse(
                [(cx - radius, cy - radius), (cx + radius, cy + radius)],
                outline=accent_color,
                width=3
            )
            # Inner circle
            inner_radius = 20
            draw.ellipse(
                [(cx - inner_radius, cy - inner_radius), (cx + inner_radius, cy + inner_radius)],
                fill=accent_color
            )
            # Center dot (tombe-like)
            dot_radius = 8
            draw.ellipse(
                [(cx - dot_radius, cy - dot_radius), (cx + dot_radius, cy + dot_radius)],
                fill=(0, 0, 0)
            )

        # Add "Shorts" badge at bottom
        badge_y = height - 120
        badge_height = 60
        badge_width = 200
        badge_x = (width - badge_width) // 2

        # Badge background
        draw.rounded_rectangle(
            [(badge_x, badge_y), (badge_x + badge_width, badge_y + badge_height)],
            radius=30,
            fill=accent_color
        )

        # Badge text
        try:
            badge_font = ImageFont.truetype(self.bangla_font, 28) if self.bangla_font else ImageFont.load_default()
        except:
            badge_font = ImageFont.load_default()

        badge_text = "SHORTS"
        bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        text_x = badge_x + (badge_width - text_w) // 2
        text_y = badge_y + (badge_height - text_h) // 2

        draw.text((text_x, text_y), badge_text, font=badge_font, fill=(255, 255, 255))

        return img

    def _add_visual_polish(self, img: Image.Image) -> Image.Image:
        """Add final visual polish to thumbnail"""

        # Increase contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.25)

        # Increase saturation
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.15)

        # Slight sharpening
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

        return img

    def create_from_script(self, script_data: Dict = None) -> str:
        """
        Create thumbnail from script data

        Args:
            script_data: Dictionary containing script and metadata

        Returns:
            Path to generated thumbnail
        """

        # Load script if not provided
        if script_data is None:
            script_path = f"{self.output_dir}/script.json"
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    script_data = json.load(f)
            except FileNotFoundError:
                raise FileNotFoundError(f"Script file not found: {script_path}")

        title = script_data.get('title', 'নারুটো What If')

        # Try to use first generated image as background
        background_image = None
        try:
            images_dir = Path(self.output_dir) / 'images'
            if images_dir.exists():
                image_files = list(images_dir.glob('*.jpg')) + list(images_dir.glob('*.png'))
                if image_files:
                    # Use first generated scene image
                    background_image = str(image_files[0])
        except:
            pass

        # Generate thumbnail
        thumbnail_path = self.create_thumbnail(
            title=title,
            background_image=background_image,
            output_filename="shorts_thumbnail.jpg"
        )

        # Save metadata
        thumbnail_metadata = {
            "thumbnail_path": thumbnail_path,
            "title": title
        }

        with open(f'{self.output_dir}/thumbnail_metadata.json', 'w', encoding='utf-8') as f:
            json.dump(thumbnail_metadata, f, indent=2, ensure_ascii=False)

        return thumbnail_path

    def _get_bangla_font(self) -> Optional[str]:
        """Get path to Bangla-compatible font"""
        # Common Bangla font paths
        font_paths = [
            "/usr/share/fonts/truetype/noto/NotoSansBengali-Bold.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansBengali-Regular.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "C:\\Windows\\Fonts\\NotoSansBengali-Bold.ttf",
            "C:\\Windows\\Fonts\\NotoSansBengali-Regular.ttf",
            "C:\\Windows\\Fonts\\vrinda.ttf",  # Windows built-in Bangla font
            "/System/Library/Fonts/NotoSansBengali-Bold.ttf",
        ]

        for font_path in font_paths:
            if os.path.exists(font_path):
                return font_path

        return None


def main():
    """Test the thumbnail generator"""

    try:
        generator = ThumbnailGenerator()

        # Try to use existing script
        output_dir = os.getenv('OUTPUT_DIR', 'output')
        script_path = f"{output_dir}/script.json"

        if os.path.exists(script_path):
            print(f"📄 Using script from: {script_path}\n")
            thumbnail_path = generator.create_from_script()
        else:
            print("⚠️  No script found. Creating sample thumbnail...\n")

            # Create sample thumbnail
            thumbnail_path = generator.create_thumbnail(
                title="নারুটো শেয়ারিংগ্যান পেলে কী হতো?",
                output_filename="sample_thumbnail.jpg"
            )

        print("\n" + "="*60)
        print("✅ Thumbnail generation complete!")
        print("="*60)
        print(f"📁 Thumbnail saved to: {thumbnail_path}")
        print("="*60)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise


if __name__ == "__main__":
    main()