# feed_api.py
from fastapi import APIRouter, HTTPException, Response
from pathlib import Path
from typing import Optional

router = APIRouter()

FEEDS_DIR = Path(__file__).resolve().parents[2] / "feeds"

@router.get("/api/feeds/{market}/{category}.xml", response_class=Response)
def serve_feed_file(market: str, category: str):
    f = FEEDS_DIR / market / f"{category}.xml"
    if not f.exists():
        raise HTTPException(status_code=404, detail="Feed not found")
    content = f.read_text(encoding="utf-8")
    return Response(content=content, media_type="application/rss+xml")

@router.get("/api/feeds/{market}", response_class=Response)
def serve_market_top10(market: str):
    f = FEEDS_DIR / market / "top10.xml"
    if not f.exists():
        raise HTTPException(status_code=404, detail="Feed not found")
    content = f.read_text(encoding="utf-8")
    return Response(content=content, media_type="application/rss+xml")

@router.get("/api/sitemap.xml", response_class=Response)
def serve_sitemap():
    f = FEEDS_DIR / "sitemap.xml"
    if not f.exists():
        raise HTTPException(status_code=404, detail="Sitemap not found")
    return Response(content=f.read_text(encoding="utf-8"), media_type="application/xml")
