# 🎬 Naruto What If Bangla Shorts - Automated Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Daily%20Automation-green.svg)](https://github.com/features/actions)

**একটি সম্পূর্ণ স্বয়ংক্রিয় বাংলা YouTube Shorts পাইপলাইন** — নারুটো "What If" কাহিনীর জন্য AI স্ক্রিপ্ট, ভয়েসওভার, ইমেজ জেনারেশন, ভিডিও কম্পোজিশন এবং আপলোড।

## ✨ বৈশিষ্ট্য

| ফিচার | বিবরণ |
|----------|-------------|
| 🤖 **AI স্ক্রিপ্ট জেনারেশন** | Groq/Ollama দিয়ে বাংলা "What If" স্ক্রিপ্ট + দৃশ্য ব্রেকডাউন |
| 🎙️ **বাংলা TTS** | Microsoft Edge-TTS (`bn-IN-TanishaaNeural`) দিয়ে প্রাকৃতিক ভয়েসওভার |
| 🎨 **AI ইমেজ জেনারেশন** | Pollinations.ai (Sana/Flux) দিয়ে দৃশ্য-ভিত্তিক অ্যানিমে স্টাইল ইমেজ |
| 🎬 **শর্টস ভিডিও কম্পোজিশন** | 9:16 (1080x1920), ট্রানজিশন, BGM, SFX, কেন বার্নস ইফেক্ট |
| 🖼️ **থাম্বনেইল** | বাংলা টেক্সট সাপোর্ট, নারুটো থিম, 9:16 ফরম্যাট |
| 📤 **ইউটিউব আপলোড** | বাংলা মেটাডেটা, #Shorts ট্যাগ, পাবলিক/প্রাইভেট |
| ⏰ **দৈনিক অটোমেশন** | GitHub Actions ক্রন (সন্ধ্যা ৭টা BST / ১৩:০০ UTC) |
| 💰 **শূন্য খরচ** | সব টুল এবং API সম্পূর্ণ ফ্রি |

## 🚀 কুইক স্টার্ট

### পূর্বশর্ত
- Python 3.11+
- FFmpeg
- Git

### ইনস্টলেশন

```bash
# রিপোজিটরি ক্লোন করুন
git clone https://github.com/mdkamrul71639-blip/naruto-whatif-bangla.git
cd naruto-whatif-bangla

# পাইথন ডিপেন্ডেন্সি ইনস্টল করুন
pip install -r requirements.txt

# FFmpeg ইনস্টল করুন (Ubuntu/Debian)
sudo apt install ffmpeg fonts-noto-bengali

# এনভায়রনমেন্ট ফাইল তৈরি করুন
cp .env.example .env
# .env ফাইলটি এডিট করে আপনার API কীগুলো যোগ করুন
```

### কনফিগারেশন

**.env ফাইলে নিচের কীগুলো সেট করুন:**

1. **GROQ_API_KEY** (প্রয়োজনীয়) - [console.groq.com](https://console.groq.com) থেকে ফ্রি API কী নিন
2. **YOUTUBE_CLIENT_SECRETS** - Google Cloud Console থেকে OAuth client_secret.json-এর পুরো JSON
3. **YOUTUBE_TOKEN_PICKLE** - প্রথমবার লোকালি `python scripts/upload.py` চালিয়ে অথরাইজ করুন, তারপর `base64 config/token.pickle` আউটপুটটি এখানে দিন

### ব্যবহার

```bash
# সম্পূর্ণ পাইপলাইন চালান (আপলোড সহ)
python main.py

# শুধু ভিডিও বানান (আপলোড ছাড়া)
python main.py --no-upload

# নির্দিষ্ট টপিক দিয়ে চালান
python main.py --topic "What If Naruto Joined the Akatsuki?"

# পৃথক কম্পোনেন্ট চালান
python scripts/script_generator.py
python scripts/voiceover.py
python scripts/visuals.py
python scripts/compose.py
python scripts/thumbnails.py
python scripts/upload.py
```

## 📁 প্রজেক্ট স্ট্রাকচার

```
naruto-whatif-bangla/
├── scripts/
│   ├── script_generator.py    # বাংলা স্ক্রিপ্ট + দৃশ্য ব্রেকডাউন
│   ├── voiceover.py           # Edge-TTS বাংলা ভয়েসওভার
│   ├── visuals.py             # Pollinations.ai ইমেজ জেনারেশন
│   ├── thumbnails.py          # বাংলা থাম্বনেইল (9:16)
│   ├── compose.py             # শর্টস ভিডিও কম্পোজিশন (ট্রানজিশন, BGM, SFX)
│   └── upload.py              # ইউটিউব শর্টস আপলোড
├── config/
│   └── topics.json            # নারুটো What If টপিক লিস্ট (রোটেশন সহ)
├── .github/workflows/
│   └── auto-video.yml         # GitHub Actions ডেইলি ক্রন (১৩:০০ UTC)
├── main.py                    # পাইপলাইন অর্কেস্ট্রেটর
├── requirements.txt           # পাইথন ডিপেন্ডেন্সি
├── .env.example               # এনভায়রনমেন্ট টেমপ্লেট
└── README.md                  # এই ফাইল
```

## 🔧 টপিক কনফিগারেশন

`config/topics.json` ফাইলে নারুটো "What If" টপিকগুলো রয়েছে। প্রতিটি টপিকের সাথে আছে:
- `title` - ভিডিওর টাইটেল
- `keywords` - সার্চ কীওয়ার্ড
- `description` - সংক্ষিপ্ত বর্ণনা
- `visual_queries` - ইমেজ জেনারেশনের জন্য কোয়েরি
- `scenes` - দৃশ্যের বিস্তারিত বর্ণনা (LLM-কে গাইড করার জন্য)

```json
{
  "topics": [
    {
      "title": "What If Naruto Had the Sharingan?",
      "keywords": ["naruto", "sharingan", "uchiha", "what if"],
      "description": "Naruto awakens the Sharingan instead of Kurama's power",
      "visual_queries": ["naruto sharingan", "uchiha eyes", "anime eyes", "ninja battle"],
      "scenes": [
        "Naruto as a child awakening Sharingan during the Nine-Tails attack",
        "Naruto training with Kakashi as his Uchiha mentor",
        "Naruto vs Sasuke - both with Sharingan, different ideals",
        "Naruto using Mangekyou Sharingan to protect the village",
        "Hokage Naruto with Eternal Mangekyou, peace achieved differently"
      ]
    }
  ],
  "rotation_strategy": "sequential",
  "last_used_index": 0
}
```

পাইপলাইন প্রতিদিন পরবর্তী টপিকে রোটেট করবে (`last_used_index` আপডেট করে)।

## 🤖 GitHub Actions অটোমেশন

### সেটআপ

1. **রিপোজিটরি পুশ করুন:**
```bash
git push -u origin main
```

2. **GitHub Secrets যোগ করুন** (Settings → Secrets and variables → Actions):

| Secret Name | বিবরণ | কিভাবে পাবেন |
|---|---|---|
| `GROQ_API_KEY` | Groq API কী | [console.groq.com](https://console.groq.com) |
| `YOUTUBE_CLIENT_SECRETS` | OAuth credentials | `client_secrets.json`-এর পুরো JSON কন্টেন্ট |
| `YOUTUBE_TOKEN_PICKLE` | Refresh token | `base64 config/token.pickle` আউটপুট |

3. **শিডিউল কনফিগার করুন** (`.github/workflows/auto-video.yml`):
```yaml
on:
  schedule:
    - cron: '0 13 * * *'  # Daily at 13:00 UTC = 7:00 PM BST
```

### ম্যানুয়াল ট্রিগার
1. Actions ট্যাবে যান
2. "Naruto What If Bangla Shorts - Daily Automation" সিলেক্ট করুন
3. "Run workflow" ক্লিক করুন
4. ঐচ্ছিক: কাস্টম টপিক বা `--no-upload` দিন

## 💰 খরচ বিশ্লেষণ

| কম্পোনেন্ট | টুল | খরচ |
|---|---|---|
| স্ক্রিপ্ট জেনারেশন | Groq / Ollama | $০ |
| টেক্সট-টু-স্পিচ | Edge-TTS | $০ |
| AI ইমেজ জেনারেশন | Pollinations.ai | $০ |
| ভিডিও এডিটিং | MoviePy + FFmpeg | $০ |
| থাম্বনেইল | Pillow | $০ |
| ইউটিউব আপলোড | YouTube Data API v3 | $০ |
| অটোমেশন | GitHub Actions | $০ (২,০০০ মিনিট/মাস ফ্রি) |
| **মোট** | | **$০/মাস** |

**ফ্রি টিয়ার লিমিট:**
- Pollinations.ai: অনলিমিটেড (রেট লিমিট সহ)
- YouTube: ১০,০০০ কোটা ইউনিট/দিন (~১০০ আপলোড)
- GitHub Actions: ২,০০০ মিনিট/মাস
- Groq: খুব উদার লিমিট

## 📊 পাইপলাইন পারফরম্যান্স

- **গড় পাইপলাইন সময়**: ৫-১০ মিনিট/ভিডিও
- **ভিডিও কোয়ালিটি**: 1080x1920 (9:16), 30 FPS
- **অডিও কোয়ালিটি**: হাই-ফিডেলিটি বাংলা TTS
- **ফাইল সাইজ**: ~১৫-৩০ MB প্রতি শর্টস

## 🛠️ অ্যাডভান্সড কাস্টমাইজেশন

### কাস্টম স্ক্রিপ্ট টেমপ্লেট
`scripts/script_generator.py`-এ `_create_prompt` মেথড এডিট করুন।

### ভিডিও ট্রানজিশন ও ইফেক্ট
`scripts/compose.py`-এ `_add_ken_burns`, `TRANSITION_DURATION`, `BGM_VOLUME` এডিট করুন।

### থাম্বনেইল কাস্টমাইজেশন
`scripts/thumbnails.py`-এ রঙ, ফন্ট, নারুটো এলিমেন্ট পরিবর্তন করুন।

### BGM/SFX যোগ করুন
`output/bgm/` ও `output/sfx/` ফোল্ডারে রয়েলটি-ফ্রি অডিও ফাইল রাখুন।

## 🔍 ট্রাবলশুটিং

| সমস্যা | সমাধান |
|---------|----------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| `FFmpeg not found` | `sudo apt install ffmpeg` / `brew install ffmpeg` |
| `GROQ_API_KEY not found` | `.env` ফাইলে কী সেট করুন |
| `YouTube authentication failed` | `config/token.pickle` মুছে `python scripts/upload.py` আবার চালান |
| `Bangla font not found` | `sudo apt install fonts-noto-bengali` |
| `Pollinations.ai rate limited` | `IMAGE_MODEL=flux` বা `turbo` ব্যবহার করুন |

## 📚 ডকুমেন্টেশন

- [Quick Start Guide](QUICKSTART.md) - ১০ মিনিটে সেটআপ
- [Architecture Overview](ARCHITECTURE.md) - টেকনিক্যাল ডিটেইলস
- [Setup Summary](SETUP_SUMMARY.md) - সম্পূর্ণ ওভারভিউ

## 🤝 অবদান

কন্ট্রিবিউশন স্বাগতম! Pull Request জমা দিন।

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 লাইসেন্স

MIT License - বিস্তারিতের জন্য [LICENSE](LICENSE) ফাইলটি দেখুন।

## 🙏 স্বীকৃতি

- [Groq](https://groq.com/) - দ্রুত LLM API
- [Pollinations.ai](https://pollinations.ai/) - ফ্রি AI ইমেজ জেনারেশন
- [Edge-TTS](https://github.com/rany2/edge-tts) - মাইক্রোসফ্ট বাংলা TTS
- [MoviePy](https://zulko.github.io/moviepy/) - ভিডিও এডিটিং
- [YouTube Data API](https://developers.google.com/youtube/v3) - ভিডিও আপলোড
- [GitHub Actions](https://github.com/features/actions) - ফ্রি CI/CD

## ⭐ সাপোর্ট

এই প্রজেক্টটি উপকারী লাগলে ⭐ দিন!

## 📧 যোগাযোগ

- GitHub Issues: [Create an issue](https://github.com/mdkamrul71639-blip/naruto-whatif-bangla/issues)
- Discussions: [Join the discussion](https://github.com/mdkamrul71639-blip/naruto-whatif-bangla/discussions)

---

**Made with ❤️ using 100% free and open-source tools for Bangla Naruto fans!**