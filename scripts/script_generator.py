#!/usr/bin/env python3
"""
Script Generator Module
Generates Bangla Naruto What If video scripts with scene breakdown for AI image generation
"""

import os
import json
from typing import Dict, Optional, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try importing LLM libraries
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("⚠️  Ollama not installed. Install with: pip install ollama")

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("⚠️  Groq not installed. Install with: pip install groq")


class ScriptGenerator:
    """Generate Bangla video scripts with scene breakdown for AI image generation"""

    def __init__(self):
        self.use_ollama = os.getenv('USE_OLLAMA', 'true').lower() == 'true'
        self.ollama_model = os.getenv('OLLAMA_MODEL', 'llama3.1:8b')
        self.groq_model = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        # OpenRouter (fallback / alternative to Groq - works from any region)
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        self.openrouter_model = os.getenv(
            'OPENROUTER_MODEL',
            'google/gemma-4-31b-it:free'
        )

    def generate_script(self, topic: str, duration: int = 60) -> Dict[str, str]:
        """
        Generate a Bangla Naruto What If video script with scene breakdown

        Args:
            topic: The Naruto What If topic
            duration: Target duration in seconds (default: 60 for Shorts)

        Returns:
            Dictionary containing title, script, scenes, image_prompts, and metadata
        """

        prompt = self._create_prompt(topic, duration)

        # Use Ollama if available and configured
        if self.use_ollama and OLLAMA_AVAILABLE:
            return self._generate_with_ollama(prompt, topic)

        # Use Groq if key is set
        elif GROQ_AVAILABLE and self.groq_api_key:
            return self._generate_with_groq(prompt, topic)

        # Fallback: OpenRouter (free tier available, works in all regions)
        elif self.openrouter_api_key:
            return self._generate_with_openrouter(prompt, topic)

        else:
            raise RuntimeError(
                "No LLM backend available. Set OPENROUTER_API_KEY or GROQ_API_KEY "
                "in .env / GitHub Secrets."
            )

    def _create_prompt(self, topic: str, duration: int) -> str:
        """Create the prompt for Bangla script generation with scene breakdown"""

        words_estimate = duration * 2.5  # Average speaking rate: 150 words/minute
        num_scenes = max(5, duration // 10)  # ~10 seconds per scene for Shorts

        prompt = f"""তুমি একজন বাংলা ইউটিউব স্ক্রিপ্ট লেখক। নিচের "What If" টপিকের উপর {duration}-সেকেন্ডের একটি YouTube Shorts ভিডিওর স্ক্রিপ্ট লেখ।

টপিক: {topic}

আবশ্যকতা:
- লক্ষ্য দৈর্ঘ্য: প্রায় {int(words_estimate)} শব্দ
- ভাষা: বাংলা (সহজ, কথোপকথন স্ট্রিম)
- ফরম্যাট: YouTube Shorts (৯:১৬, দ্রুত গতি, হুক-ভিত্তিক)
- দৃশ্য সংখ্যা: {num_scenes}টি দৃশ্য (প্রতিটি ৮-১২ সেকেন্ড)

কাঠামো:
১. HUK (প্রথম ৩ সেকেন্ড): দর্শককে আকর্ষণ করার জন্য একটি প্রশ্ন বা বল্ড স্টেটমেন্ট
২. MAIN CONTENT ({duration-6} সেকেন্ড): {num_scenes}টি দৃশ্যে মূল কাহিনী বলুন
৩. CALL-TO-ACTION (শেষ ৩ সেকেন্ড): লাইক, সাবস্ক্রাইব, কমেন্ট উদ্দীপনা

শৈলী নির্দেশনা:
- কথোপকথনমূলক এবং আকর্ষণীয় টোন
- ছোট, বেসিমো বাক্য
- "তুমি" দিয়ে দর্শককে সরাসরি উজ্জীবন করুন
- প্রতিটি দৃশ্যের জন্য AI ইমেজ প্রম্পট দিন (ইংরেজিতে)
- রিটোরিক্যাল প্রশ্ন ব্যবহার করুন
- শেষ দৃশ্যে একটি উন্মুক্ত প্রশ্ন দিয়ে কমেন্ট চালান

আউটপুট ফরম্যাট (ঠিক এইভাবে লিখুন):

TITLE: [আকর্ষণীয় বাংলা ভিডিও টাইটেল]

SCRIPT:
[তুমি একখানা প্রবাহমান বাংলা স্ক্রিপ্ট লিখবে যা বুলে পড়লে সহজ লাগবে]

SCENES:
SCENE 1: [দৃশ্যের বাংলা বর্ণনা] | IMAGE_PROMPT: [AI ইমেজ জেনারেশনের জন্য বিস্তারিত ইংরেজি প্রম্পট, এনিমে স্টাইল, নারুটো আর্টস্টাইল]
SCENE 2: [দৃশ্যের বাংলা বর্ণনা] | IMAGE_PROMPT: [AI ইমেজ জেনারেশনের জন্য বিস্তারিত ইংরেজি প্রম্পট, এনিমে স্টাইল, নারুটো আর্টস্টাইল]
SCENE 3: [দৃশ্যের বাংলা বর্ণনা] | IMAGE_PROMPT: [AI ইমেজ জেনারেশনের জন্য বিস্তারিত ইংরেজি প্রম্পট, এনিমে স্টাইল, নারুটো আর্টস্টাইল]
...

TAGS: [৫-৮টি প্রাসঙ্গিক ট্যাগ, কমা দিয়ে আলাদা করুন]

দ্রষ্টব্য: টাইমস্ট্যাম্প, ন্যারেটর নোট বা অতিরিক্ত ব্যাখ্যা দেবেন না। শুধু বলা শব্দ এবং দৃশ্য বিবরণ লিখুন।"""

        return prompt

    def _generate_with_ollama(self, prompt: str, topic: str) -> Dict[str, str]:
        """Generate script using local Ollama"""

        print(f"🤖 Generating Bangla script with Ollama ({self.ollama_model})...")

        try:
            response = ollama.chat(
                model=self.ollama_model,
                messages=[
                    {
                        'role': 'system',
                        'content': 'তুমি একজন বিশেষজ্ঞ বাংলা ইউটিউব স্ক্রিপ্ট লেখক। নারুটো "What If" শর্টস ভিডিওর জন্য আকর্ষণীয়, দ্রুত গতির স্ক্রিপ্ট লিখে দাও যাতে AI ইমেজ জেনারেশন জন্য দৃশ্যগুলো স্পষ্ট হয়।'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            )

            content = response['message']['content']
            return self._parse_script_response(content, topic)

        except Exception as e:
            raise RuntimeError(f"Ollama generation failed: {str(e)}")

    def _generate_with_openrouter(self, prompt: str, topic: str) -> Dict[str, str]:
        """Generate script using OpenRouter API (works from any region, free tier)"""

        import requests

        print(f"🤖 Generating Bangla script with OpenRouter ({self.openrouter_model})...")

        if not self.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY not set in environment variables")

        try:
            import time as _time

            response = None
            last_err = None
            # Retry with backoff for rate limits (429) / transient errors
            for attempt in range(5):
                try:
                    response = requests.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.openrouter_api_key}",
                            "Content-Type": "application/json",
                        },
                        json={
                            "model": self.openrouter_model,
                            "messages": [
                                {
                                    "role": "system",
                                    "content": "তুমি একজন বিশেষজ্ঞ বাংলা ইউটিউব স্ক্রিপ্ট লেখক। নারুটো \"What If\" শর্টস ভিডিওর জন্য আকর্ষণীয়, দ্রুত গতির স্ক্রিপ্ট লিখে দাও যাতে AI ইমেজ জেনারেশন জন্য দৃশ্যগুলো স্পষ্ট হয়।"
                                },
                                {
                                    "role": "user",
                                    "content": prompt
                                }
                            ],
                            "temperature": 0.7,
                            "max_tokens": 2048
                        },
                        timeout=120
                    )
                    response.raise_for_status()
                    break
                except requests.exceptions.RequestException as req_err:
                    last_err = req_err
                    status = getattr(req_err.response, 'status_code', None)
                    # Retry on 429 (rate limit) and 5xx; fail fast on 401/404
                    if status in (429, 500, 502, 503, 504) and attempt < 4:
                        wait = 15 * (attempt + 1)
                        print(f"⏳ OpenRouter {status}, retrying in {wait}s (attempt {attempt+2}/5)...")
                        _time.sleep(wait)
                        continue
                    raise

            data = response.json()

            content = data["choices"][0]["message"]["content"]
            return self._parse_script_response(content, topic)

        except Exception as e:
            # OpenRouter failed (rate limit / invalid key) - fall back to free Pollinations text API
            print(f"⚠️  OpenRouter failed ({str(e)[:100]}), falling back to Pollinations.ai text API...")
            return self._generate_with_pollinations(prompt, topic)

    def _generate_with_pollinations(self, prompt: str, topic: str) -> Dict[str, str]:
        """Generate script using Pollinations.ai text API (free, no API key needed)"""

        import requests
        import time as _time

        print(f"🤖 Generating Bangla script with Pollinations.ai (free, no key)...")

        response = None
        # Retry with backoff for rate limits
        for attempt in range(5):
            try:
                response = requests.post(
                    "https://text.pollinations.ai/openai",
                    headers={"Content-Type": "application/json"},
                    json={
                        "model": "openai",
                        "messages": [
                            {
                                "role": "system",
                                "content": "তুমি একজন বিশেষজ্ঞ বাংলা ইউটিউব স্ক্রিপ্ট লেখক। নারুটো \"What If\" শর্টস ভিডিওর জন্য আকর্ষণীয়, দ্রুত গতির স্ক্রিপ্ট লিখে দাও যাতে AI ইমেজ জেনারেশন জন্য দৃশ্যগুলো স্পষ্ট হয়।"
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": 0.7,
                        "max_tokens": 2048
                    },
                    timeout=180
                )
                response.raise_for_status()
                break
            except requests.exceptions.RequestException as req_err:
                status = getattr(req_err.response, 'status_code', None)
                if status in (429, 500, 502, 503, 504) and attempt < 4:
                    wait = 20 * (attempt + 1)
                    print(f"⏳ Pollinations {status}, retrying in {wait}s (attempt {attempt+2}/5)...")
                    _time.sleep(wait)
                    continue
                raise

        data = response.json()
        content = data["choices"][0]["message"]["content"]
        return self._parse_script_response(content, topic)

    def _generate_with_groq(self, prompt: str, topic: str) -> Dict[str, str]:
        """Generate script using Groq API"""

        print(f"🤖 Generating Bangla script with Groq ({self.groq_model})....")

        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY not set in environment variables")

        try:
            client = Groq(api_key=self.groq_api_key)

            response = client.chat.completions.create(
                model=self.groq_model,
                messages=[
                    {
                        "role": "system",
                        "content": "তুমি একজন বিশেষজ্ঞ বাংলা ইউটিউব স্ক্রিপ্ট লেখক। নারুটো \"What If\" শর্টস ভিডিওর জন্য আকর্ষণীয়, দ্রুত গতির স্ক্রিপ্ট লিখে দাও যাতে AI ইমেজ জেনারেশন জন্য দৃশ্যগুলো স্পষ্ট হয়।"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2048
            )

            content = response.choices[0].message.content
            return self._parse_script_response(content, topic)

        except Exception as e:
            raise RuntimeError(f"Groq generation failed: {str(e)}")

    def _parse_script_response(self, content: str, topic: str) -> Dict[str, str]:
        """Parse the LLM response into structured components with scenes and image prompts"""

        # Extract title
        title = topic
        if "TITLE:" in content:
            title_line = content.split("TITLE:")[1].split("\n")[0].strip()
            if title_line:
                title = title_line

        # Extract script
        script = ""
        if "SCRIPT:" in content and "SCENES:" in content:
            script = content.split("SCRIPT:")[1].split("SCENES:")[0].strip()
        elif "SCRIPT:" in content:
            script = content.split("SCRIPT:")[1].strip()

        # Extract scenes and image prompts
        scenes = []
        image_prompts = []
        if "SCENES:" in content:
            scenes_section = content.split("SCENES:")[1].split("TAGS:")[0] if "TAGS:" in content else content.split("SCENES:")[1]
            scene_lines = [line.strip() for line in scenes_section.strip().split("\n") if line.strip().startswith("SCENE")]
            for scene_line in scene_lines:
                if "| IMAGE_PROMPT:" in scene_line:
                    desc_part = scene_line.split("| IMAGE_PROMPT:")[0]
                    prompt_part = scene_line.split("| IMAGE_PROMPT:")[1]
                    scene_desc = desc_part.replace("SCENE 1:", "").replace("SCENE 2:", "").replace("SCENE 3:", "").replace("SCENE 4:", "").replace("SCENE 5:", "").replace("SCENE 6:", "").replace("SCENE 7:", "").replace("SCENE 8:", "").replace("SCENE 9:", "").replace("SCENE 10:", "").strip()
                    scenes.append(scene_desc)
                    image_prompts.append(prompt_part.strip())
                else:
                    # Fallback if format is different
                    scenes.append(scene_line)

        # Extract tags
        tags = []
        if "TAGS:" in content:
            tags_line = content.split("TAGS:")[1].strip()
            tags = [tag.strip() for tag in tags_line.split(",")]

        # If no tags, generate from topic
        if not tags:
            tags = ["নারুটো", "what if", "অ্যানিমে", "শর্টস", "বাংলা", "নিনজা"][:8]

        return {
            "title": title,
            "script": script,
            "scenes": scenes,
            "image_prompts": image_prompts,
            "tags": tags[:8],
            "topic": topic,
            "word_count": len(script.split())
        }


def main():
    """Test the script generator"""

    # Load a topic from config
    try:
        with open('config/topics.json', 'r') as f:
            topics_data = json.load(f)
            topic_obj = topics_data['topics'][0]
            topic = topic_obj['title']
    except:
        topic = os.getenv('DEFAULT_TOPIC', 'What If Naruto Had the Sharingan?')

    # Generate script
    generator = ScriptGenerator()
    result = generator.generate_script(topic)

    # Display results
    print("\n" + "="*60)
    print(f"📝 TITLE: {result['title']}")
    print("="*60)
    print(f"\n{result['script']}\n")
    print("="*60)
    print(f"🎬 SCENES ({len(result['scenes'])}):")
    for i, (scene, prompt) in enumerate(zip(result['scenes'], result['image_prompts']), 1):
        print(f"  Scene {i}: {scene}")
        print(f"  Prompt: {prompt[:80]}...")
    print("="*60)
    print(f"🏷️  TAGS: {', '.join(result['tags'])}")
    print(f"📊 Word Count: {result['word_count']}")
    print("="*60)

    # Save to file
    output_dir = os.getenv('OUTPUT_DIR', 'output')
    os.makedirs(output_dir, exist_ok=True)

    with open(f'{output_dir}/script.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Script saved to {output_dir}/script.json")


if __name__ == "__main__":
    main()