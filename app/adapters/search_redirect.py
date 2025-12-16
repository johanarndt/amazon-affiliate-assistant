
# app/adapters/search_redirect.py
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from app.adapters.affiliate_config import MARKET_MAP, affiliate_tag_for_market, DEFAULT_MARKETS
from urllib.parse import quote_plus

router = APIRouter(prefix="/api/search", tags=["search"])

@router.get("/")
def search_url(q: str = Query(..., min_length=1, description="Search query"),
               market: str = Query("US", description="Market code, e.g. US,UK,CA")):
    m = market.upper()
    if m not in DEFAULT_MARKETS:
        raise HTTPException(status_code=400, detail=f"Unknown market: {market}")

    base = MARKET_MAP[m]["base"]
    tag = affiliate_tag_for_market(m)
    # Build Amazon search URL
    qs = quote_plus(q)
    url = f"{base}/s?k={qs}"
    if tag:
        sep = "&" if "?" in url else "?"
        url += sep + f"tag={tag}"
    return {"query": q, "market": m, "redirect_url": url}

@router.get("/redirect")
def search_redirect(q: str = Query(..., min_length=1), market: str = Query("US")):
    m = market.upper()
    if m not in DEFAULT_MARKETS:
        raise HTTPException(status_code=400, detail=f"Unknown market: {market}")
    base = MARKET_MAP[m]["base"]
    tag = affiliate_tag_for_market(m)
    url = f"{base}/s?k={quote_plus(q)}"
    if tag:
        url += ("&" if "?" in url else "?") + f"tag={tag}"
    return RedirectResponse(url)
