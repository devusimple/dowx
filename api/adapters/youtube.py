from __future__ import annotations

import yt_dlp

from . import Format, VideoInfo

_ydl_opts = {"quiet": True, "no_warnings": True}


def get_info(url: str) -> VideoInfo:
    with yt_dlp.YoutubeDL(_ydl_opts) as ydl:
        raw = ydl.extract_info(url, download=False)

    formats = [
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

    return VideoInfo(
        title=raw.get("title", ""),
        duration=raw.get("duration"),
        thumbnail=raw.get("thumbnail"),
        formats=formats,
    )


def get_direct_url(url: str, format_id: str) -> str | None:
    with yt_dlp.YoutubeDL(_ydl_opts) as ydl:
        raw = ydl.extract_info(url, download=False)

    for f in raw.get("formats", []):
        if f.get("format_id") == format_id:
            return f.get("url")
    return None
