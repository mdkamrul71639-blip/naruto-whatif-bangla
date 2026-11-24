#!/usr/bin/env python3
"""
Visuals Generator Module
Generates AI images for each scene using Pollinations.ai (free, no API key required)
"""

import os
import json
import time
import urllib.parse
import requests
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AIImageGenerator:
    """Generate images for each scene using Pollinations.ai free API"""

    def __init__(self):
        self.output_dir = os.getenv('OUTPUT_DIR', 'output')
        self.model = os.getenv('IMAGE_MODEL', 'sana')  # sana, flux, turbo, dreamshaper
        self.width = int(os.getenv('IMAGE_WIDTH', '1080'))
        self.height = int(os.getenv('IMAGE_HEIGHT', '1920'))  # Shorts 9:16
        self.nologo = os.getenv('IMAGE_NOLOGO', 'true').lower() == 'true'

        # Pollinations.ai API endpoint
        self.base_url = "https://image.pollinations.ai/prompt/"

    def _build_image_url(self, prompt: str, seed: str = "") -> str:
        """Build the Pollinations.ai image generation URL"""
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"{self.base_url}{encoded_prompt}?width={self.width}&height={self.height}&nologo={str(self.nologo).lower()}"
        if seed:
            url += f"&seed={seed}"
        return url

    def generate_image(
        self,
        prompt: str,
        filename: str,
        subfolder: str = "images",
        seed: str = ""
    ) -> str:
        """
        Generate an image from prompt using Pollinations.ai

        Args:
            prompt: Image generation prompt (English, detailed)
            filename: Output filename
            subfolder: Subfolder in output directory (default: images)
            seed: Optional seed for reproducible results

        Returns:
            Path to generated image file
        """

        print(f"🎨 Generating AI image: {filename}")
        print(f"   Prompt: {prompt[:100]}...")

        # Create output directory
        output_path = Path(self.output_dir) / subfolder
        output_path.mkdir(parents=True, exist_ok=True)

        filepath = output_path / filename

        url = self._build_image_url(prompt, seed)

        try:
            response = requests.get(url, stream=True, timeout=180)
            response.raise_for_status()

            # Download with progress
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\r   Progress: {progress:.1f}%", end='', flush=True)

            print(f"\n✅ Image saved to: {filepath}")
            return str(filepath)

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to generate image: {str(e)}")

    def generate_images_for_scenes(self, script_data: Dict = None) -> List[str]:
        """
        Generate images for all scenes from script data

        Args:
            script_data: Dictionary containing script, scenes, and image_prompts

        Returns:
            List of generated image file paths
        """

        # Load script if not provided
        if script_data is None:
            script_path = f"{self.output_dir}/script.json"
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    script_data = json.load(f)
            except FileNotFoundError:
                raise FileNotFoundError(f"Script file not found: {script_path}")

        image_prompts = script_data.get('image_prompts', [])
        scenes = script_data.get('scenes', [])

        if not image_prompts:
            # Fallback: create prompts from scenes
            print("⚠️  No image_prompts found, creating from scenes...")
            image_prompts = []
            for scene in scenes:
                prompt = f"Anime style, Naruto artstyle, {scene}, highly detailed, vibrant colors, cinematic lighting, 9:16 aspect ratio"
                image_prompts.append(prompt)

        print(f"\n🎨 Generating {len(image_prompts)} AI images for scenes...")

        downloaded_files = []

        for idx, prompt in enumerate(image_prompts):
            # Enhance prompt for Naruto anime style
            enhanced_prompt = self._enhance_prompt(prompt)

            filename = f"scene_{idx+1:02d}.jpg"

            try:
                filepath = self.generate_image(enhanced_prompt, filename)
                downloaded_files.append(filepath)

                # Rate limiting - be nice to the free API
                time.sleep(2)

            except Exception as e:
                print(f"⚠️  Failed to generate {filename}: {str(e)}")
                continue

        # Save metadata
        visuals_metadata = {
            "generated_files": downloaded_files,
            "prompts_used": image_prompts,
            "total_images": len(downloaded_files),
            "model": self.model,
            "resolution": f"{self.width}x{self.height}"
        }

        with open(f'{self.output_dir}/visuals_metadata.json', 'w', encoding='utf-8') as f:
            json.dump(visuals_metadata, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Generated {len(downloaded_files)} AI images")

        return downloaded_files

    def _enhance_prompt(self, prompt: str) -> str:
        """Enhance prompt for better Naruto anime style results"""
        # Add style modifiers if not present
        style_keywords = [
            "anime style", "Naruto artstyle", "cel shaded",
            "vibrant colors", "detailed", "cinematic lighting",
            "masterpiece", "high quality", "9:16 aspect ratio"
        ]

        # Check which style keywords are missing
        prompt_lower = prompt.lower()
        missing_styles = [kw for kw in style_keywords if kw not in prompt_lower]

        if missing_styles:
            enhanced = f"{prompt}, {', '.join(missing_styles[:4])}"
        else:
            enhanced = prompt

        return enhanced


def main():
    """Test the AI image generator"""

    try:
        generator = AIImageGenerator()

        # Try to generate based on existing script, or use default
        output_dir = os.getenv('OUTPUT_DIR', 'output')
        script_path = f"{output_dir}/script.json"

        if os.path.exists(script_path):
            print(f"📄 Using script from: {script_path}\n")
            image_files = generator.generate_images_for_scenes()
        else:
            print("⚠️  No script found. Generating sample images...\n")

            # Sample Naruto What If prompts
            sample_prompts = [
                "Naruto as child awakening Sharingan during Nine-Tails attack, red eyes with tomoe, anime style, Naruto artstyle, dramatic lighting",
                "Naruto training with Kakashi as Uchiha mentor, Chidori practice, forest background, anime style, vibrant colors",
                "Naruto vs Sasuke both with Sharingan, different ideals, epic battle, manga panels style, dynamic pose",
                "Naruto using Mangekyou Sharingan to protect village, Susanoo formation, golden aura, cinematic lighting",
                "Hokage Naruto with Eternal Mangekyou, peace achieved, sunset over Konoha, detailed background, masterpiece"
            ]

            image_files = []
            for idx, prompt in enumerate(sample_prompts):
                filename = f"sample_scene_{idx+1}.jpg"
                filepath = generator.generate_image(prompt, filename)
                image_files.append(filepath)
                time.sleep(2)

        print("\n" + "="*60)
        print("✅ AI Image generation complete!")
        print("="*60)
        print(f"📁 Total images generated: {len(image_files)}")
        for f in image_files:
            print(f"   • {f}")
        print("="*60)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise


if __name__ == "__main__":
    main()