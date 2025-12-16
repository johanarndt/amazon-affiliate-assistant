# feed_generator.py
import os
import json
import html
from datetime import datetime
from pathlib import Path
from typing import List
from dotenv import load_dotenv

load_dotenv()

# Import DB session and models from your project. Adjust if names differ.
try:
    from app.db import SessionLocal
    from app.models import Product, SalesPage
except Exception:
    # Fallback if run standalone for testing (adjust imports to match your project)
    from db import SessionLocal
    from models import Product, SalesPage

from app.adapters.translator import translate_text

# CONFIG --------------------------------------------------------------------
MARKETS = [
    "us", "uk", "ca", "br", "mx",
    "de", "fr", "it", "es", "nl",
    "in", "jp", "au", "sg", "ae"
]

# map market -> language code (for translate_text)
LANG_MAP = {
    "us": "en", "uk": "en", "ca": "en", "au": "en", "in": "en",
    "br": "pt", "mx": "es", "de": "de", "fr": "fr", "it": "it",
    "es": "es", "nl": "nl", "jp": "ja", "sg": "en", "ae": "ar"
}

# Categories to generate feeds for
CATEGORIES = [
    "top10",
    "electronics",
    "home_kitchen",
    "sports_outdoors",
    "beauty_health",
    "fashion",
    "tools_home",
    "toys_kids",
    "pets",
    "office_business",
    "seasonal"
]

# Where to write feeds
BASE = Path(__file__).resolve().parents[2]  # backend/app/adapters -> backend
FEEDS_DIR = BASE / "feeds"
FEEDS_DIR.mkdir(parents=True, exist_ok=True)

# Affiliate tags per market: ensure you set these in .env or here
AFF_TAGS = {
    "us": os.getenv("AMAZON_ASSOCIATE_TAG_US", ""),
    "uk": os.getenv("AMAZON_ASSOCIATE_TAG_UK", ""),
    "ca": os.getenv("AMAZON_ASSOCIATE_TAG_CA", ""),
    "br": os.getenv("AMAZON_ASSOCIATE_TAG_BR", ""),
    "mx": os.getenv("AMAZON_ASSOCIATE_TAG_MX", ""),
    "de": os.getenv("AMAZON_ASSOCIATE_TAG_DE", ""),
    "fr": os.getenv("AMAZON_ASSOCIATE_TAG_FR", ""),
    "it": os.getenv("AMAZON_ASSOCIATE_TAG_IT", ""),
    "es": os.getenv("AMAZON_ASSOCIATE_TAG_ES", ""),
    "nl": os.getenv("AMAZON_ASSOCIATE_TAG_NL", ""),
    "in": os.getenv("AMAZON_ASSOCIATE_TAG_IN", ""),
    "jp": os.getenv("AMAZON_ASSOCIATE_TAG_JP", ""),
    "au": os.getenv("AMAZON_ASSOCIATE_TAG_AU", ""),
    "sg": os.getenv("AMAZON_ASSOCIATE_TAG_SG", ""),
    "ae": os.getenv("AMAZON_ASSOCIATE_TAG_AE", "")
}

# Price currency for schema (we'll use USD as requested)
PRICE_CURRENCY = "USD"

# ---------------------------------------------------------------------------

def _ensure_market_dir(market: str):
    d = FEEDS_DIR / market
    d.mkdir(parents=True, exist_ok=True)
    return d

def _pick_images(product) -> List[str]:
    # try common attribute names; return up to 3 images (strings)
    imgs = []
    if not product:
        return imgs
    for attr in ("images", "image_urls", "image_url", "image"):
        v = getattr(product, attr, None)
        if v:
            if isinstance(v, (list, tuple)):
                imgs.extend(v)
            elif isinstance(v, str):
                # some strings are comma separated
                if "," in v and v.startswith("http"):
                    imgs.extend([x.strip() for x in v.split(",") if x.strip()])
                else:
                    imgs.append(v)
    # dedupe & limit
    out = []
    for u in imgs:
        if u and u not in out:
            out.append(u)
        if len(out) >= 3:
            break
    return out

def _pick_review_highlights(product, limit=3):
    # Attempt to find review text(s). Your Product model may have reviews stored.
    # We try common attributes; otherwise return empty list.
    highlights = []
    if not product:
        return highlights
    # Preferred: product.reviews (list of dicts)
    revs = getattr(product, "reviews", None) or getattr(product, "reviews_list", None) or getattr(product, "reviews_json", None)
    if revs:
        # if string try parse JSON
        if isinstance(revs, str):
            try:
                revs = json.loads(revs)
            except Exception:
                revs = []
        if isinstance(revs, (list, tuple)):
            # pick up to limit reviews with rating >=4 or best available
            rated = []
            for r in revs:
                # r may be dict with rating & text
                rating = None
                text = None
                if isinstance(r, dict):
                    rating = r.get("rating") or r.get("stars")
                    text = r.get("text") or r.get("body") or r.get("review")
                else:
                    text = str(r)
                try:
                    rating = int(rating) if rating is not None else None
                except Exception:
                    rating = None
                rated.append((rating, text))
            # prefer highest rated
            rated_sorted = sorted(rated, key=lambda x: (x[0] or 0), reverse=True)
            for rating, text in rated_sorted[:limit]:
                if text:
                    highlights.append(text)
    # Fallback: product.top_review_text or product.review_excerpt
    if not highlights:
        for attr in ("top_review_text", "review_excerpt", "best_review"):
            v = getattr(product, attr, None)
            if v:
                highlights.append(v)
    # final fallback: empty
    return highlights[:limit]

def _clean_text_for_html(s: str) -> str:
    if not s:
        return ""
    # Basic sanitization, keep line breaks
    s = str(s)
    s = html.escape(s)
    s = s.replace("\n", "<br/>")
    return s

def _build_affiliate_link(product_asin: str, market: str, override_affiliate_url: str = None):
    # If the sales page contains affiliate_link, prefer that. Otherwise build a search/asin link.
    tag = AFF_TAGS.get(market, "")
    if override_affiliate_url:
        return override_affiliate_url
    domain_map = {
        "us": "amazon.com",
        "uk": "amazon.co.uk",
        "ca": "amazon.ca",
        "br": "amazon.com.br",
        "mx": "amazon.com.mx",
        "de": "amazon.de",
        "fr": "amazon.fr",
        "it": "amazon.it",
        "es": "amazon.es",
        "nl": "amazon.nl",
        "in": "amazon.in",
        "jp": "amazon.co.jp",
        "au": "amazon.com.au",
        "sg": "amazon.sg",
        "ae": "amazon.ae",
    }
    d = domain_map.get(market, "amazon.com")
    if not product_asin:
        # fallback to homepage
        return f"https://{d}/?tag={tag}" if tag else f"https://{d}/"
    # direct ASIN link (product detail)
    if tag:
        return f"https://{d}/dp/{product_asin}?tag={tag}"
    else:
        return f"https://{d}/dp/{product_asin}"

def _build_item_html(product, sales_page_html, market, lang):
    """
    Return HTML snippet for description with images, review highlights, and JSON-LD schema.
    """
    imgs = _pick_images(product)
    img_tags = ""
    for u in imgs:
        safe_u = html.escape(u)
        img_tags += f'<img src="{safe_u}" alt="{html.escape(getattr(product, "title", ""))}" style="max-width:220px;margin-right:8px;display:inline-block;vertical-align:top"/>'

    # review highlights
    reviews = _pick_review_highlights(product, limit=3)
    reviews_html = ""
    if reviews:
        for r in reviews:
            reviews_html += f'<blockquote style="border-left:3px solid #ddd;padding-left:8px;margin:6px 0">{html.escape(r)}</blockquote>'

    title = getattr(product, "title", None) or getattr(product, "name", "") or "Top Amazon Pick"
    price = getattr(product, "price", None) or ""
    rating = getattr(product, "rating", None) or ""
    review_count = getattr(product, "reviews_count", None) or getattr(product, "review_count", None) or ""

    asin = getattr(product, "asin", None) or getattr(product, "asin_code", None) or getattr(product, "id", None)
    affiliate_link = _build_affiliate_link(asin, market)

    # JSON-LD product schema (price currency = USD per your choice)
    schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": title,
        "image": imgs if imgs else None,
        "description": getattr(product, "short_description", "") or (getattr(product, "description", "") or "")[:250],
        "sku": asin or None,
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": str(rating) if rating else None,
            "reviewCount": str(review_count) if review_count else None
        },
        "offers": {
            "@type": "Offer",
            "url": affiliate_link,
            "priceCurrency": PRICE_CURRENCY,
            # price left blank if not available
            "price": str(price) if price else None,
            "availability": "https://schema.org/InStock"
        }
    }

    # Combine into CDATA HTML
    desc_html = "<div class='feed-item'>"
    desc_html += f"<div class='images'>{img_tags}</div>"
    desc_html += f"<h3>{html.escape(title)}</h3>"
    if price:
        desc_html += f"<p><strong>Price:</strong> {html.escape(str(price))} {PRICE_CURRENCY}</p>"
    if rating:
        desc_html += f"<p><strong>Rating:</strong> {html.escape(str(rating))} / 5 ({html.escape(str(review_count))} reviews)</p>"
    desc_html += f"<div class='summary'>{_clean_text_for_html(sales_page_html)}</div>"
    if reviews_html:
        desc_html += "<div class='reviews'><h4>What customers say:</h4>" + reviews_html + "</div>"
    desc_html += f'<p><a href="{html.escape(affiliate_link)}" style="background:#111;color:#fff;padding:10px 12px;border-radius:6px;text-decoration:none">View on Amazon</a></p>'
    # add JSON-LD
    schema_json = json.dumps(schema, ensure_ascii=False)
    desc_html += f'<script type="application/ld+json">{schema_json}</script>'
    desc_html += "</div>"

    return desc_html, affiliate_link

def generate_feed_for_market_and_category(market: str, category: str):
    """
    Generate a feed XML string for a given market and category.
    Writes to FEEDS_DIR/{market}/{category}.xml
    """
    db = SessionLocal()
    # Market directory
    mdir = _ensure_market_dir(market)

    # Query: collect SalesPage rows for this market and category
    # Assumes SalesPage has .market and .category fields; otherwise we attempt to map Product data
    try:
        if category == "top10":
            pages = db.query(SalesPage).filter(SalesPage.market == market).order_by(SalesPage.created_at.desc()).limit(50).all()
        else:
            # try filter by category first; fall back to name matching
            pages = db.query(SalesPage).filter(SalesPage.market == market, SalesPage.category == category).order_by(SalesPage.created_at.desc()).limit(50).all()
            if not pages:
                # fallback: join product and use product.category or product.browse_node
                pages = db.query(SalesPage).join(Product).filter(SalesPage.market == market).all()
    except Exception as e:
        print("DB query error:", e)
        pages = []

    lang = LANG_MAP.get(market, "en")

    items_xml = []
    # scoring for top10: use reviews_count or created_at; we'll sort by reviews_count desc then created_at
    def score_page(p):
        try:
            pr = db.query(Product).filter(Product.id == p.product_id).first()
            rc = getattr(pr, "reviews_count", 0) or 0
            return (rc, p.created_at)
        except Exception:
            return (0, p.created_at)

    # sort pages for top10
    pages_sorted = sorted(pages, key=score_page, reverse=True)[:50]

    for p in pages_sorted:
        # get product
        product = None
        try:
            product = db.query(Product).filter(Product.id == p.product_id).first()
        except Exception:
            product = None

        # Prepare localized title & html
        original_title = getattr(product, "title", None) or getattr(p, "title", "") or ""
        original_html = getattr(p, "html", None) or getattr(p, "content", None) or getattr(p, "description", "") or ""

        translated_title = translate_text(original_title, lang) if original_title else ""
        translated_html = translate_text(original_html, lang) if original_html else ""

        # if category specific filter: skip if product.category doesn't match (best-effort)
        # Build item html + affiliate link
        desc_html, aff_link = _build_item_html(product, translated_html, market, lang)

        title_safe = html.escape(translated_title or (product.title if product else "Top Amazon pick"))
        # pubDate
        pubDate = (p.created_at if getattr(p, "created_at", None) else datetime.utcnow()).strftime("%a, %d %b %Y %H:%M:%S +0000")

        # Build RSS item block (including CDATA for description)
        item_block = f"""
<item>
  <title>{title_safe}</title>
  <link>{html.escape(aff_link)}</link>
  <description><![CDATA[{desc_html}]]></description>
  <pubDate>{pubDate}</pubDate>
</item>
"""
        items_xml.append(item_block)

    # Build channel
    channel_title = f"Daily Amazon Picks - {market.upper()} - {category}"
    channel_link = f"https://YOUR_PUBLIC_DOMAIN/market/{market}/"  # replace with real domain
    channel_description = f"Daily {category} Amazon picks for {market.upper()} (localized)."

    rss = '<?xml version="1.0" encoding="UTF-8"?>\n'
    rss += '<rss version="2.0">\n'
    rss += '<channel>\n'
    rss += f"<title>{html.escape(channel_title)}</title>\n"
    rss += f"<link>{html.escape(channel_link)}</link>\n"
    rss += f"<description>{html.escape(channel_description)}</description>\n"
    rss += "\n".join(items_xml)
    rss += "\n</channel>\n</rss>\n"

    # Write to file
    out_path = mdir / f"{category}.xml"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(rss)

    print(f"WROTE: {out_path}")
    db.close()
    return out_path

def generate_all_feeds():
    """
    Generate all feeds for all markets & categories.
    Writes files to FEEDS_DIR/{market}/{category}.xml and _top10.xml
    """
    for market in MARKETS:
        for category in CATEGORIES:
            try:
                generate_feed_for_market_and_category(market, category)
            except Exception as e:
                print(f"Error generating feed {market}/{category}: {e}")

    # generate sitemap
    generate_sitemap()

def generate_sitemap():
    """
    Create sitemap.xml referencing market pages and feed files.
    """
    now = datetime.utcnow().strftime("%Y-%m-%d")
    sitemap_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for market in MARKETS:
        sitemap_lines.append("<url>")
        sitemap_lines.append(f"<loc>https://YOUR_PUBLIC_DOMAIN/market/{market}/</loc>")
        sitemap_lines.append(f"<lastmod>{now}</lastmod>")
        sitemap_lines.append("</url>")
        for category in CATEGORIES:
            sitemap_lines.append("<url>")
            sitemap_lines.append(f"<loc>https://YOUR_PUBLIC_DOMAIN/feeds/{market}/{category}.xml</loc>")
            sitemap_lines.append(f"<lastmod>{now}</lastmod>")
            sitemap_lines.append("</url>")
    sitemap_lines.append("</urlset>")
    out = FEEDS_DIR / "sitemap.xml"
    out.write_text("\n".join(sitemap_lines), encoding="utf-8")
    print("WROTE SITEMAP:", out)
    return out
