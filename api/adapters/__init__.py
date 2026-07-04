from dataclasses import dataclass


@dataclass
class Format:
    format_id: str
    ext: str | None
    resolution: str | None
    filesize: int | None
    vcodec: str | None
    acodec: str | None


@dataclass
class VideoInfo:
    title: str
    duration: float | None
    thumbnail: str | None
    formats: list[Format]
