#!/usr/bin/env python3
"""
Video Composer Module - Shorts Edition
Combines AI-generated images, audio, BGM, SFX and creates the final Shorts video using MoviePy
"""

import os
import json
import random
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

try:
    from moviepy.editor import (
        VideoFileClip, AudioFileClip, ImageClip, concatenate_videoclips,
        CompositeVideoClip, TextClip, ColorClip, CompositeAudioClip, afx
    )
    from moviepy.video.fx import resize, fadein, fadeout
    import moviepy.video.fx.all as vfx
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    print("⚠️  MoviePy not installed. Install with: pip install moviepy")

# Load environment variables
load_dotenv()


class VideoComposer:
    """Compose final Shorts video from AI images, audio, BGM, and SFX"""

    def __init__(self):
        if not MOVIEPY_AVAILABLE:
            raise RuntimeError("MoviePy is required. Install with: pip install moviepy")

        self.output_dir = os.getenv('OUTPUT_DIR', 'output')
        # Shorts format: 9:16 = 1080x1920
        self.video_width = int(os.getenv('VIDEO_WIDTH', '1080'))
        self.video_height = int(os.getenv('VIDEO_HEIGHT', '1920'))
        self.video_fps = int(os.getenv('VIDEO_FPS', '30'))

        # Transition settings
        self.transition_duration = float(os.getenv('TRANSITION_DURATION', '0.5'))
        self.add_transitions = os.getenv('ADD_TRANSITIONS', 'true').lower() == 'true'

        # Audio settings
        self.bgm_volume = float(os.getenv('BGM_VOLUME', '0.15'))  # Background music volume
        self.sfx_volume = float(os.getenv('SFX_VOLUME', '0.3'))   # Sound effects volume
        self.voice_volume = float(os.getenv('VOICE_VOLUME', '1.0')) # Main voiceover volume

        # BGM/SFX paths (optional)
        self.bgm_dir = Path(self.output_dir) / 'bgm'
        self.sfx_dir = Path(self.output_dir) / 'sfx'

    def create_shorts_video(
        self,
        image_paths: List[str],
        audio_path: str,
        output_filename: str = "final_shorts.mp4",
        bgm_path: Optional[str] = None,
        sfx_paths: Optional[List[str]] = None,
        add_captions: bool = True
    ) -> str:
        """
        Create final Shorts video from images and audio

        Args:
            image_paths: List of AI-generated image file paths
            audio_path: Path to voiceover audio file
            output_filename: Output filename
            bgm_path: Optional background music path
            sfx_paths: Optional list of sound effect paths
            add_captions: Whether to add Bangla captions

        Returns:
            Path to final video file
        """

        print(f"🎬 Creating Shorts video from {len(image_paths)} images...")
        print(f"   Resolution: {self.video_width}x{self.video_height} (9:16)")

        if not image_paths:
            raise ValueError("No image paths provided")

        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        # Load audio to get target duration
        voiceover = AudioFileClip(audio_path)
        target_duration = voiceover.duration
        voiceover = voiceover.volumex(self.voice_volume)

        print(f"🎵 Voiceover duration: {target_duration:.2f} seconds")

        # Load and process images as clips
        clips = self._load_and_process_images(
            image_paths,
            target_duration
        )

        # Concatenate image clips
        print("🔗 Concatenating image clips...")
        final_video = concatenate_videoclips(clips, method="compose")

        # Ensure video matches audio duration
        if final_video.duration > target_duration:
            final_video = final_video.subclip(0, target_duration)
        elif final_video.duration < target_duration:
            # Loop if shorter
            loops_needed = int(target_duration / final_video.duration) + 1
            final_video = concatenate_videoclips([final_video] * loops_needed)
            final_video = final_video.subclip(0, target_duration)

        # Prepare audio tracks
        audio_tracks = [voiceover]

        # Add BGM if provided
        if bgm_path and os.path.exists(bgm_path):
            try:
                bgm = AudioFileClip(bgm_path).volumex(self.bgm_volume)
                # Loop BGM to match video duration
                if bgm.duration < target_duration:
                    loops = int(target_duration / bgm.duration) + 1
                    bgm = concatenate_videoclips([bgm] * loops).subclip(0, target_duration)
                else:
                    bgm = bgm.subclip(0, target_duration)
                audio_tracks.append(bgm)
                print(f"🎵 Added BGM: {Path(bgm_path).name}")
            except Exception as e:
                print(f"⚠️  Failed to add BGM: {str(e)}")

        # Add SFX if provided
        if sfx_paths:
            for sfx_path in sfx_paths:
                if os.path.exists(sfx_path):
                    try:
                        sfx = AudioFileClip(sfx_path).volumex(self.sfx_volume)
                        # Place SFX at random or specific times
                        sfx = sfx.set_start(random.uniform(0, max(0, target_duration - sfx.duration)))
                        audio_tracks.append(sfx)
                        print(f"🔊 Added SFX: {Path(sfx_path).name}")
                    except Exception as e:
                        print(f"⚠️  Failed to add SFX {sfx_path}: {str(e)}")

        # Composite audio
        print("🎵 Compositing audio tracks...")
        final_audio = CompositeAudioClip(audio_tracks)

        # Add audio to video
        final_video = final_video.set_audio(final_audio)

        # Add Bangla captions if requested
        if add_captions:
            final_video = self._add_captions(final_video, audio_path)

        # Export final video
        output_path = Path(self.output_dir) / 'videos' / output_filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"📤 Exporting Shorts video... (this may take a while)")

        final_video.write_videofile(
            str(output_path),
            fps=self.video_fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            threads=4,
            preset='medium',
            ffmpeg_params=['-crf', '23', '-movflags', '+faststart']
        )

        # Clean up
        voiceover.close()
        for clip in clips:
            clip.close()
        final_video.close()
        final_audio.close()

        print(f"✅ Shorts video exported to: {output_path}")

        # Get file size
        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"📊 File size: {file_size_mb:.2f} MB")

        return str(output_path)

    def _load_and_process_images(
        self,
        image_paths: List[str],
        total_duration: float
    ) -> List[ImageClip]:
        """Load and process images as video clips with transitions"""

        clips = []
        duration_per_image = total_duration / len(image_paths)

        print(f"⏱️  Target duration per image: {duration_per_image:.2f} seconds")

        for idx, img_path in enumerate(image_paths):
            if not os.path.exists(img_path):
                print(f"⚠️  Image not found: {img_path}, skipping...")
                continue

            print(f"🖼️  Processing image {idx + 1}/{len(image_paths)}: {Path(img_path).name}")

            # Load image as clip
            clip = ImageClip(img_path, duration=duration_per_image)

            # Resize to Shorts dimensions (1080x1920) maintaining aspect ratio
            clip = self._resize_to_shorts(clip)

            # Add subtle zoom/pan effect (Ken Burns style)
            clip = self._add_ken_burns(clip, duration_per_image)

            # Add transitions
            if self.add_transitions and len(image_paths) > 1:
                if idx > 0:  # Fade in (except first)
                    clip = clip.fx(fadein, self.transition_duration)
                if idx < len(image_paths) - 1:  # Fade out (except last)
                    clip = clip.fx(fadeout, self.transition_duration)

            clips.append(clip)

        return clips

    def _resize_to_shorts(self, clip: ImageClip) -> ImageClip:
        """Resize image to 1080x1920 (9:16) with proper cropping"""
        # Resize to fill height
        clip = clip.fx(resize.resize, height=self.video_height)

        # If wider than target, crop center
        if clip.w > self.video_width:
            x_center = clip.w / 2
            clip = clip.crop(
                x1=x_center - self.video_width/2,
                x2=x_center + self.video_width/2
            )
        # If narrower, pad with black bars (shouldn't happen with AI images)
        elif clip.w < self.video_width:
            pad_width = (self.video_width - clip.w) // 2
            clip = clip.margin(left=pad_width, right=pad_width, color=(0, 0, 0))

        return clip

    def _add_ken_burns(self, clip: ImageClip, duration: float) -> ImageClip:
        """Add subtle zoom/pan animation (Ken Burns effect)"""
        # Random zoom direction
        zoom_factor = 1.0 + random.uniform(0.02, 0.08)  # 2-8% zoom

        def zoom_animation(get_frame, t):
            frame = get_frame(t)
            progress = t / duration
            # Smooth zoom
            scale = 1 + (zoom_factor - 1) * progress
            # Simple scale (MoviePy handles this via resize)
            return frame

        # Apply zoom by resizing over time
        # Note: This is a simplified version; full Ken Burns needs custom transform
        clip = clip.fx(vfx.resize, zoom_factor)

        return clip

    def _add_captions(self, video: VideoFileClip, audio_path: str) -> VideoFileClip:
        """Add Bangla captions/subtitles to video"""
        try:
            # Load script for caption text
            script_path = f"{self.output_dir}/script.json"
            if os.path.exists(script_path):
                with open(script_path, 'r', encoding='utf-8') as f:
                    script_data = json.load(f)

                script_text = script_data.get('script', '')
                if script_text:
                    # Create caption clip
                    caption_clips = self._create_caption_clips(script_text, video.duration)
                    if caption_clips:
                        video = CompositeVideoClip([video] + caption_clips)
                        print("📝 Added Bangla captions")
        except Exception as e:
            print(f"⚠️  Failed to add captions: {str(e)}")

        return video

    def _create_caption_clips(self, script_text: str, video_duration: float) -> List[TextClip]:
        """Create Bangla caption clips from script"""
        # Split script into sentences for captions
        sentences = [s.strip() for s in script_text.split('।') if s.strip()]
        if not sentences:
            sentences = [s.strip() for s in script_text.split('.') if s.strip()]

        caption_clips = []
        time_per_sentence = video_duration / max(len(sentences), 1)

        # Font for Bangla
        font_path = self._get_bangla_font()

        for i, sentence in enumerate(sentences):
            if not sentence:
                continue

            start_time = i * time_per_sentence
            end_time = min((i + 1) * time_per_sentence, video_duration)

            try:
                txt_clip = TextClip(
                    sentence + '।',
                    fontsize=48,
                    color='white',
                    font=font_path,
                    stroke_color='black',
                    stroke_width=2,
                    size=(self.video_width * 0.9, None),
                    method='caption',
                    align='center'
                ).set_position(('center', self.video_height * 0.8)) \
                 .set_start(start_time) \
                 .set_duration(end_time - start_time) \
                 .fx(fadein, 0.3) \
                 .fx(fadeout, 0.3)

                caption_clips.append(txt_clip)
            except Exception as e:
                print(f"⚠️  Failed to create caption for: {sentence[:30]}... Error: {e}")

        return caption_clips

    def _get_bangla_font(self) -> str:
        """Get path to Bangla-compatible font"""
        # Common Bangla font paths
        font_paths = [
            "/usr/share/fonts/truetype/noto/NotoSansBengali-Regular.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansBengali-Bold.ttf",
            "C:\\Windows\\Fonts\\NotoSansBengali-Regular.ttf",
            "C:\\Windows\\Fonts\\vrinda.ttf",  # Windows Bangla font
            "/System/Library/Fonts/NotoSansBengali-Regular.ttf",
        ]

        for font_path in font_paths:
            if os.path.exists(font_path):
                return font_path

        # Fallback
        print("⚠️  No Bangla font found, using default")
        return None

    def create_from_pipeline_output(self) -> str:
        """
        Create Shorts video using outputs from previous pipeline steps
        """

        # Load metadata from previous steps
        try:
            with open(f'{self.output_dir}/visuals_metadata.json', 'r', encoding='utf-8') as f:
                visuals_meta = json.load(f)
                image_paths = visuals_meta.get('generated_files', visuals_meta.get('downloaded_files', []))
        except FileNotFoundError:
            raise FileNotFoundError("Visuals metadata not found. Run visuals.py first.")

        try:
            with open(f'{self.output_dir}/audio_metadata.json', 'r', encoding='utf-8') as f:
                audio_meta = json.load(f)
                audio_path = audio_meta['audio_path']
        except FileNotFoundError:
            raise FileNotFoundError("Audio metadata not found. Run voiceover.py first.")

        # Find BGM/SFX if available
        bgm_path = None
        sfx_paths = []

        if self.bgm_dir.exists():
            bgm_files = list(self.bgm_dir.glob('*.mp3')) + list(self.bgm_dir.glob('*.wav'))
            if bgm_files:
                bgm_path = str(bgm_files[0])  # Use first BGM

        if self.sfx_dir.exists():
            sfx_paths = [str(f) for f in self.sfx_dir.glob('*.mp3')] + \
                        [str(f) for f in self.sfx_dir.glob('*.wav')]

        # Create video
        video_path = self.create_shorts_video(
            image_paths=image_paths,
            audio_path=audio_path,
            bgm_path=bgm_path,
            sfx_paths=sfx_paths[:3] if sfx_paths else None,  # Max 3 SFX
            add_captions=True
        )

        # Save video metadata
        with open(f'{self.output_dir}/script.json', 'r', encoding='utf-8') as f:
            script_data = json.load(f)

        video_metadata = {
            "video_path": video_path,
            "title": script_data.get('title', 'Naruto What If Shorts'),
            "duration": AudioFileClip(audio_path).duration,
            "images_used": len(image_paths),
            "resolution": f"{self.video_width}x{self.video_height}",
            "fps": self.video_fps,
            "format": "Shorts (9:16)"
        }

        with open(f'{self.output_dir}/video_metadata.json', 'w', encoding='utf-8') as f:
            json.dump(video_metadata, f, indent=2, ensure_ascii=False)

        return video_path


def main():
    """Test the video composer"""

    try:
        composer = VideoComposer()

        # Create video from pipeline output
        print("🎬 Starting Shorts video composition...\n")

        video_path = composer.create_from_pipeline_output()

        print("\n" + "="*60)
        print("✅ Shorts video composition complete!")
        print("="*60)
        print(f"📁 Final video: {video_path}")
        print("="*60)

    except FileNotFoundError as e:
        print(f"\n❌ Missing required files: {str(e)}")
        print("\n💡 Make sure to run the pipeline in order:")
        print("   1. python scripts/script_generator.py")
        print("   2. python scripts/voiceover.py")
        print("   3. python scripts/visuals.py")
        print("   4. python scripts/compose.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise


if __name__ == "__main__":
    main()