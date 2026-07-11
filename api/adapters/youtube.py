from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path

import yt_dlp

from . import Format, VideoInfo

_SOURCE_COOKIES = Path(__file__).resolve().parent.parent.parent / "cookies.txt"
_COOKIES_FILE: str | None = None

if _SOURCE_COOKIES.exists():
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    shutil.copy2(str(_SOURCE_COOKIES), tmp.name)
    _COOKIES_FILE = tmp.name

_ydl_opts = {
    "quiet": True,
    "no_warnings": True,
}
if _COOKIES_FILE:
    _ydl_opts["cookiefile"] = _COOKIES_FILE


def _parse_formats(raw: dict) -> list[Format]:
    return [
        Format(
            format_id=f["format_id"],
            ext=f.get("ext"),
            resolution=f.get("resolution") or f"{f.get('height', '')}p" or None,
            filesize=f.get("filesize") or f.get("filesize_approx"),
            vcodec=f.get("vcodec"),
            acodec=f.get("acodec"),
        )
        for f in raw.get("formats", [])
        if f.get("url")
    ]


def get_info(url: str) -> VideoInfo | tuple[str, list[VideoInfo]]:
    with yt_dlp.YoutubeDL(_ydl_opts) as ydl:
        raw = ydl.extract_info(url, download=False)

    if "entries" in raw:
        videos = [
            VideoInfo(
                title=entry.get("title", ""),
                duration=entry.get("duration"),
                thumbnail=entry.get("thumbnail"),
                formats=_parse_formats(entry),
            )
            for entry in raw["entries"]
            if entry is not None
        ]
        return raw.get("title", "Untitled Playlist"), videos

    return VideoInfo(
        title=raw.get("title", ""),
        duration=raw.get("duration"),
        thumbnail=raw.get("thumbnail"),
        formats=_parse_formats(raw),
    )


def get_direct_url(url: str, format_id: str) -> str | None:
    with yt_dlp.YoutubeDL(_ydl_opts) as ydl:
        raw = ydl.extract_info(url, download=False)

    entries = raw.get("entries")
    if entries:
        for entry in entries:
            if entry is None:
                continue
            for f in entry.get("formats", []):
                if f.get("format_id") == format_id:
                    return f.get("url")
        return None

    for f in raw.get("formats", []):
        if f.get("format_id") == format_id:
            return f.get("url")
    return None
