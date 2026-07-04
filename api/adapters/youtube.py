from __future__ import annotations

import yt_dlp

from . import Format, VideoInfo

_ydl_opts = {"quiet": True, "no_warnings": True}


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
