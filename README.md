# 🎵 YouTube Mixtape Pro-Automator

An end-to-end Python application that transforms a collection of audio files and a single image into a professional, seamless YouTube mixtape with AI-powered transitions and automatic timestamp generation.

## ✨ Features
* **Pro DJ Transitions:** Uses High-Pass/Low-Pass filters and constant power crossfading for seamless song changes.
* **Auto-Metadata:** Generates YouTube-ready descriptions with clickable timestamps (Chapters).
* **High-Speed Rendering:** Uses FFmpeg for ultra-fast image-to-video conversion.
* **Modern UI:** Built with Streamlit for a drag-and-drop user experience.
* **Modular Backend:** Powered by FastAPI for scalable processing.

## 🛠️ Installation

### 1. Prerequisites
Ensure you have **FFmpeg** installed on your system.
* **Windows:** `choco install ffmpeg`
* **Mac:** `brew install ffmpeg`
* **Linux:** `sudo apt install ffmpeg`

### 2. Clone and Setup
```bash
git clone [https://github.com/your-username/youtube-mixtape-pro.git](https://github.com/your-username/youtube-mixtape-pro.git)
cd youtube-mixtape-pro
pip install -r requirements.txt