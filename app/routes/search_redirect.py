# search_redirect.py
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import RedirectResponse
from typing import Optional
import os

router = APIRouter()

AFF_TAGS = {
    "us": os.getenv("AMAZON_ASSOCIATE_TAG_US", ""),
    "uk": os.getenv("AMAZON_ASSOCIATE_TAG_UK", ""),
    "br": os.getenv("AMAZON_ASSOCIATE_TAG_BR", ""),
    "de": os.getenv("AMAZON_ASSOCIATE_TAG_DE", ""),
    "ca": os.getenv("AMAZON_ASSOCIATE_TAG_CA", ""),
    # add others...
}

DOMAIN_MAP = {
    "us": "https://www.amazon.com/s",
    "uk": "https://www.amazon.co.uk/s",
    "br": "https://www.amazon.com.br/s",
    "de": "https://www.amazon.de/s",
    "ca": "https://www.amazon.ca/s",
    # add others...
}


@router.get("/api/search")
def amazon_search(q: str = Query(..., min_length=1), market: str = Query("us")):
    market = market.lower()
    if market not in DOMAIN_MAP:
        raise HTTPException(400, "Unknown market")
    base = DOMAIN_MAP[market]
    tag = AFF_TAGS.get(market, "")
    if tag:
        redirect_url = f"{base}?k={q.replace(' ', '+')}&tag={tag}"
    else:
        redirect_url = f"{base}?k={q.replace(' ', '+')}"
    return RedirectResponse(url=redirect_url)
