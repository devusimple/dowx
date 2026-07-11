<div align="center">
  <img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/yt--dlp-2024+-red?style=for-the-badge" alt="yt-dlp">
  <img src="https://img.shields.io/badge/Vercel-black?style=for-the-badge&logo=vercel&logoColor=white" alt="Vercel">
  <br>
  <img src="https://img.shields.io/github/license/devusimple/dowx?style=flat-square" alt="License">
  <img src="https://img.shields.io/github/last-commit/devusimple/dowx?style=flat-square" alt="Last Commit">
  <img src="https://img.shields.io/github/stars/devusimple/dowx?style=flat-square" alt="Stars">
</div>

<br>

<h1 align="center">🎬 dowx</h1>
<p align="center">
  <strong>A lightweight, serverless video information & download API</strong><br>
  Extract metadata and stream videos from YouTube and 1000+ sites — powered by yt-dlp & FastAPI.
</p>

---

## 📖 Description

**dowx** is a minimal, stateless API that accepts any video URL and returns:

- **Rich metadata** — title, duration, thumbnail, and all available formats (resolution, codecs, file size)
- **Direct video streaming** — proxy-download any format without storing files on disk
- **Playlist support** — fetch all videos in a playlist in one request

Built for serverless deployment (Vercel), it uses **yt-dlp** under the hood to support **1000+ websites** including YouTube, Vimeo, Twitter/X, Instagram, TikTok, Facebook, Twitch, Dailymotion, and many more.

---

## ✨ Features

- ✅ **Single video info** — title, duration, thumbnail, all formats
- ✅ **Playlist support** — full playlist metadata with all videos and formats
- ✅ **Direct download** — stream any format directly to your client
- ✅ **1000+ sites supported** — anything yt-dlp handles
- ✅ **Serverless-ready** — deploy on Vercel with zero config
- ✅ **No database** — fully stateless, no disk writes
- ✅ **CORS enabled** — use from any frontend
- ✅ **Async performance** — non-blocking with thread-pool offloading

---

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- pip

### Local Setup

```bash
# Clone the repository
git clone https://github.com/devusimple/dowx.git
cd dowx

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate    # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn api.main:app --reload
```

The API will be running at **http://localhost:8000**.

---

## ☁️ Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

A `vercel.json` is already configured — no additional setup needed.

---

## 📡 API Documentation

### Base URL

| Local | Production |
|-------|------------|
| `http://localhost:8000` | `https://dowx.vercel.app` |

---

### `GET /`

Welcome message.

**Response:**
```json
{
  "message": "Welcome to the dowx API!"
}
```

---

### `GET /api/health`

Health check.

**Response:**
```json
{
  "status": "ok"
}
```

---

### `POST /api/info`

Get video or playlist metadata.

**Request:**
```json
{
  "url": "https://youtube.com/watch?v=..."
}
```

**Response (single video):**
```json
{
  "title": "Video Title",
  "duration": 245.6,
  "thumbnail": "https://i.ytimg.com/vi/.../hqdefault.jpg",
  "formats": [
    {
      "format_id": "137",
      "ext": "mp4",
      "resolution": "1080p",
      "filesize": 52428800,
      "vcodec": "avc1.640028",
      "acodec": "mp4a.40.2"
    }
  ]
}
```

**Response (playlist):**
```json
{
  "playlist": "Playlist Name",
  "videos": [
    {
      "title": "Video 1",
      "duration": 120.5,
      "thumbnail": "https://...",
      "formats": []
    }
  ]
}
```

---

### `POST /api/download`

Download a video format.

**Request:**
```json
{
  "url": "https://youtube.com/watch?v=...",
  "format_id": "137"
}
```

**Response:** Binary video stream (`Content-Type: video/mp4`)

---

### `GET /api/download`

Same as POST but with query parameters.

```
GET /api/download?url=https://youtube.com/watch?v=...&format_id=137
```

**Response:** Binary video stream

---

## 🧱 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **Video Extraction** | [yt-dlp](https://github.com/yt-dlp/yt-dlp) |
| **Async HTTP** | [httpx](https://www.python-httpx.org/) |
| **Deployment** | [Vercel](https://vercel.com/) |
| **Linting** | [ruff](https://docs.astral.sh/ruff/) |
| **Runtime** | Python 3.13 |

---

## 📁 Project Structure

```
dowx/
├── api/
│   ├── main.py              # FastAPI app with all endpoints
│   └── adapters/
│       ├── __init__.py       # Format & VideoInfo dataclasses
│       └── youtube.py        # yt-dlp integration logic
├── requirements.txt          # Dependencies
├── vercel.json               # Vercel deployment config
└── README.md                 # You are here
```

---

## 👨‍💻 Developer

<div align="center">
  <table>
    <tr>
      <td><strong>Name</strong></td>
      <td><a href="https://github.com/devusimple">Mehedi Hasan</a></td>
    </tr>
    <tr>
      <td><strong>Role</strong></td>
      <td>Owner & Developer</td>
    </tr>
    <tr>
      <td><strong>Website</strong></td>
      <td><a href="https://mehedi-uzzol.vercel.app">mehedi-uzzol.vercel.app</a></td>
    </tr>
    <tr>
      <td><strong>GitHub</strong></td>
      <td><a href="https://github.com/devusimple">@devusimple</a></td>
    </tr>
    <tr>
      <td><strong>Facebook</strong></td>
      <td><a href="https://fb.com/huzzat77">fb/huzzat77</a></td>
    </tr>
    <tr>
      <td><strong>Email</strong></td>
      <td><a href="mailto:huzzat2@gmail.com">huzzat2@gmail.com</a></td>
    </tr>
  </table>
</div>

---

## 📄 License

This project is open source and available under the **MIT License**.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/devusimple">Mehedi Hasan</a>
</p>