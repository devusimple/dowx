from __future__ import annotations

import asyncio

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from adapters.youtube import get_direct_url, get_info

app = FastAPI(title="dowx")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class InfoRequest(BaseModel):
    url: str


class DownloadRequest(BaseModel):
    url: str
    format_id: str


@app.post("/api/info")
async def api_info(req: InfoRequest):
    try:
        video = await asyncio.to_thread(get_info, req.url)
        return {
            "title": video.title,
            "duration": video.duration,
            "thumbnail": video.thumbnail,
            "formats": [
                {
                    "format_id": f.format_id,
                    "ext": f.ext,
                    "resolution": f.resolution,
                    "filesize": f.filesize,
                    "vcodec": f.vcodec,
                    "acodec": f.acodec,
                }
                for f in video.formats
            ],
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


async def _stream_download(url: str, format_id: str):
    direct_url = await asyncio.to_thread(get_direct_url, url, format_id)
    if not direct_url:
        raise HTTPException(status_code=404, detail="format not found")

    client = httpx.AsyncClient()
    resp = await client.get(direct_url, follow_redirects=True)
    resp.raise_for_status()

    headers = {
        "Content-Disposition": f'attachment; filename="{format_id}.mp4"',
    }
    content_length = resp.headers.get("content-length")
    if content_length:
        headers["Content-Length"] = content_length

    return StreamingResponse(
        resp.aiter_bytes(),
        media_type=resp.headers.get("content-type", "video/mp4"),
        headers=headers,
    )


@app.post("/api/download")
async def api_download(req: DownloadRequest):
    try:
        return await _stream_download(req.url, req.format_id)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/api/download")
async def api_download_get(url: str = Query(...), format_id: str = Query(...)):
    try:
        return await _stream_download(url, format_id)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
