#!/usr/bin/env python3
"""
Voiceover Generator Module
Converts Bangla text scripts to natural-sounding speech using Edge-TTS
"""

import os
import asyncio
import json
from pathlib import Path
from dotenv import load_dotenv

try:
    from edge_tts import Communicate, list_voices
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False
    print("⚠️  edge-tts not installed. Install with: pip install edge-tts")

# Load environment variables
load_dotenv()


class VoiceoverGenerator:
    """Generate Bangla voiceovers using Edge-TTS"""

    def __init__(self):
        if not EDGE_TTS_AVAILABLE:
            raise RuntimeError("edge-tts is required. Install with: pip install edge-tts")

        # Default to Bangla voice
        self.voice = os.getenv('TTS_VOICE', 'bn-IN-TanishaaNeural')
        self.output_dir = os.getenv('OUTPUT_DIR', 'output')

    async def generate_voiceover(
        self,
        text: str,
        output_filename: str = "voiceover.mp3",
        rate: str = "+0%",
        volume: str = "+0%",
        pitch: str = "+0Hz"
    ) -> str:
        """
        Generate voiceover from Bangla text

        Args:
            text: The script text to convert to speech
            output_filename: Output filename (default: voiceover.mp3)
            rate: Speech rate adjustment (e.g., "+10%" for faster, "-10%" for slower)
            volume: Volume adjustment (e.g., "+50%" for louder)
            pitch: Pitch adjustment (e.g., "+5Hz" for higher pitch)

        Returns:
            Path to the generated audio file
        """

        print(f"🎙️  Generating Bangla voiceover with voice: {self.voice}")

        # Ensure output directory exists
        audio_dir = Path(self.output_dir) / 'audio'
        audio_dir.mkdir(parents=True, exist_ok=True)

        output_path = audio_dir / output_filename

        try:
            # Create communicate instance
            communicate = Communicate(
                text=text,
                voice=self.voice,
                rate=rate,
                volume=volume,
                pitch=pitch
            )

            # Save audio
            await communicate.save(str(output_path))

            print(f"✅ Voiceover saved to: {output_path}")
            print(f"📏 Text length: {len(text)} characters")

            return str(output_path)

        except Exception as e:
            raise RuntimeError(f"Failed to generate voiceover: {str(e)}")

    async def get_available_voices(self, language: str = "bn") -> list:
        """
        Get list of available Bangla voices

        Args:
            language: Language code (default: "bn" for Bangla)

        Returns:
            List of voice dictionaries
        """

        voices = await list_voices()
        filtered_voices = [
            v for v in voices
            if v["Locale"].startswith(language)
        ]

        return filtered_voices

    def display_voice_options(self):
        """Display available Bangla voice options"""

        print("\n🎤 Popular Bangla Voice Options:")
        print("-" * 60)

        popular_voices = [
            ("bn-IN-TanishaaNeural", "Natural female (India)", "Best for: Storytelling, narration"),
            ("bn-IN-BashkarNeural", "Natural male (India)", "Best for: Deep narration, documentaries"),
            ("bn-BD-PradeepNeural", "Natural male (Bangladesh)", "Best for: Local content, news style"),
            ("bn-BD-NabanitaNeural", "Natural female (Bangladesh)", "Best for: Friendly, casual content"),
        ]

        for voice_id, description, best_for in popular_voices:
            print(f"• {voice_id}")
            print(f"  {description}")
            print(f"  {best_for}\n")


async def generate_from_script_file(script_path: str = None) -> str:
    """
    Generate voiceover from a saved script file

    Args:
        script_path: Path to script.json file

    Returns:
        Path to generated audio file
    """

    if script_path is None:
        output_dir = os.getenv('OUTPUT_DIR', 'output')
        script_path = f"{output_dir}/script.json"

    # Load script
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            script_data = json.load(f)

        text = script_data.get('script', '')

        if not text:
            raise ValueError("No script text found in file")

    except FileNotFoundError:
        raise FileNotFoundError(f"Script file not found: {script_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in script file: {script_path}")

    # Generate voiceover
    generator = VoiceoverGenerator()
    audio_path = await generator.generate_voiceover(text)

    # Save metadata
    audio_metadata = {
        "audio_path": audio_path,
        "voice": generator.voice,
        "text_length": len(text),
        "script_file": script_path
    }

    output_dir = os.getenv('OUTPUT_DIR', 'output')
    with open(f'{output_dir}/audio_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(audio_metadata, f, indent=2, ensure_ascii=False)

    return audio_path


def main():
    """Main function for testing"""

    # Test with a sample script or load from file
    script_path = None

    # Try to load from saved script
    output_dir = os.getenv('OUTPUT_DIR', 'output')
    test_script_path = f"{output_dir}/script.json"

    if os.path.exists(test_script_path):
        print(f"📄 Found existing script at {test_script_path}")
        script_path = test_script_path
    else:
        print("⚠️  No script found. Generating sample Bangla voiceover...")

        # Create sample Bangla script
        sample_text = """\
হে বন্ধুরা! আজ আমরা কথা বলব নারুটোর সম্পর্কে একটাু আশ্চর্য কল্পনা। 
ক्या होगा যদি নারুটো শেয়ারিংগ্যান পেতো? সেটা তার জীবন কীভাবে বদলে দিত? 
চলুন জানি!
প্রথমেই, নারুটো ছোটবেলায় নাইন-টেইলস আক্রমণের সময় শেয়ারিংগ্যান জাগ্রত করত। 
তার চোখে লাল টোমোই ঘুরতে শুরু করত! 
তারপর কাকাশি তার উচিহা মেন্টর হয়ে তাকে প্রশিক্ষণ দিত। 
সাসুকে আর নারুটো - দুজনেই শেয়ারিংগ্যান ধারক, কিন্তু আদর্শ ভিন্ন। 
মাঙ্গেক্যো শেয়ারিংগ্যান দিয়ে নারুটো গ্রাম রক্ষা করত! 
অंतত হোকাগে নারুটো, ইটারন্যাল মাঙ্গেক্যো দিয়ে শান্তি প্রতিষ্ঠা করত। 
তুমি কী ভাব? কমেন্টে লিখে দাও! লাইক ও সাবস্ক্রাইব করতে ভুলো না!
"""

        # Save sample script
        os.makedirs(output_dir, exist_ok=True)
        sample_data = {
            "title": "What If Naruto Had Sharingan?",
            "script": sample_text.strip(),
            "tags": ["নারুটো", "শেয়ারিংগ্যান", "what if", "অ্যানিমে"]
        }

        with open(test_script_path, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, indent=2, ensure_ascii=False)

        script_path = test_script_path

    # Generate voiceover
    audio_path = asyncio.run(generate_from_script_file(script_path))

    print(f"\n✅ Voiceover generation complete!")
    print(f"📁 Audio file: {audio_path}")

    # Display voice options for reference
    generator = VoiceoverGenerator()
    generator.display_voice_options()


if __name__ == "__main__":
    main()