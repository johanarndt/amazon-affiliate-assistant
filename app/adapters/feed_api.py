# app/adapters/feed_api.py
from fastapi import APIRouter, Response, HTTPException
from xml.etree.ElementTree import Element, SubElement, tostring
from datetime import datetime
from app.adapters.affiliate_config import MARKET_MAP, affiliate_tag_for_market, DEFAULT_MARKETS
import html

router = APIRouter(prefix="/api/feeds", tags=["feeds"])

def make_item(title, link, description, guid, pub_date):
    item = Element("item")
    t = SubElement(item, "title"); t.text = title
    l = SubElement(item, "link"); l.text = link
    d = SubElement(item, "description"); d.text = description
    g = SubElement(item, "guid"); g.text = guid
    p = SubElement(item, "pubDate"); p.text = pub_date
    return item

@router.get("/{market}/top10.xml", response_class=Response)
def feeds_top10_xml(market: str):
    m = market.upper()
    if m not in DEFAULT_MARKETS:
        raise HTTPException(status_code=400, detail=f"Unknown market: {market}")

    base = MARKET_MAP[m]["base"]
    tag = affiliate_tag_for_market(m)

    # Build envelope
    rss = Element("rss", version="2.0")
    channel = SubElement(rss, "channel")
    title = SubElement(channel, "title"); title.text = f"Top 10 Deals - {m}"
    desc = SubElement(channel, "description"); desc.text = f"Auto-generated top 10 for {m}"
    link = SubElement(channel, "link"); link.text = base

    # Create 10 placeholder items (replace with real product extraction later)
    now = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    for i in range(1, 11):
        item_title = f"Sample Product {i} ({m})"
        product_path = f"/gp/product/sample-{i}"
        href = base + product_path
        if tag:
            sep = "&" if "?" in href else "?"
            href = href + sep + "tag=" + html.escape(tag)
        desc_text = f"Short description for Sample Product {i} in market {m}."
        guid = f"{m}-sample-{i}"
        item = make_item(item_title, href, desc_text, guid, now)
        channel.append(item)

    xml_bytes = tostring(rss, encoding="utf-8")
    return Response(content=xml_bytes, media_type="application/rss+xml; charset=utf-8")

@router.get("/{market}")
def feeds_json(market: str):
    # JSON variation useful for debugging
    m = market.upper()
    if m not in DEFAULT_MARKETS:
        raise HTTPException(status_code=400, detail=f"Unknown market: {market}")

    base = MARKET_MAP[m]["base"]
    tag = affiliate_tag_for_market(m)

    items = []
    for i in range(1, 11):
        title = f"Sample Product {i} ({m})"
        link = base + f"/gp/product/sample-{i}"
        if tag:
            link += ("&" if "?" in link else "?") + f"tag={tag}"
        items.append({"rank": i, "title": title, "link": link, "price_usd": f"{20+i}.99"})
    return {"market": m, "items": items}
