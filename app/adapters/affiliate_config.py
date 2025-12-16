# app/adapters/affiliate_config.py
# small helper: market -> store base URLs and env tag keys

import os

MARKET_MAP = {
    "US": {"base": "https://www.amazon.com", "tag_env": "AMAZON_ASSOCIATE_TAG_US"},
    "UK": {"base": "https://www.amazon.co.uk", "tag_env": "AMAZON_ASSOCIATE_TAG_UK"},
    "CA": {"base": "https://www.amazon.ca", "tag_env": "AMAZON_ASSOCIATE_TAG_CA"},
    "AU": {"base": "https://www.amazon.com.au", "tag_env": "AMAZON_ASSOCIATE_TAG_AU"},
    "IN": {"base": "https://www.amazon.in", "tag_env": "AMAZON_ASSOCIATE_TAG_IN"},
    "JP": {"base": "https://www.amazon.co.jp", "tag_env": "AMAZON_ASSOCIATE_TAG_JP"},
    "DE": {"base": "https://www.amazon.de", "tag_env": "AMAZON_ASSOCIATE_TAG_DE"},
    "FR": {"base": "https://www.amazon.fr", "tag_env": "AMAZON_ASSOCIATE_TAG_FR"},
    "ES": {"base": "https://www.amazon.es", "tag_env": "AMAZON_ASSOCIATE_TAG_ES"},
    "IT": {"base": "https://www.amazon.it", "tag_env": "AMAZON_ASSOCIATE_TAG_IT"},
    "NL": {"base": "https://www.amazon.nl", "tag_env": "AMAZON_ASSOCIATE_TAG_NL"},
    "BR": {"base": "https://www.amazon.com.br", "tag_env": "AMAZON_ASSOCIATE_TAG_BR"},
    "MX": {"base": "https://www.amazon.com.mx", "tag_env": "AMAZON_ASSOCIATE_TAG_MX"},
    "SG": {"base": "https://www.amazon.sg", "tag_env": "AMAZON_ASSOCIATE_TAG_SG"},
    "AE": {"base": "https://www.amazon.ae", "tag_env": "AMAZON_ASSOCIATE_TAG_AE"},
}

DEFAULT_MARKETS = list(MARKET_MAP.keys())

def affiliate_tag_for_market(market: str) -> str:
    m = market.upper()
    if m not in MARKET_MAP:
        return ""
    key = MARKET_MAP[m]["tag_env"]
    return os.getenv(key, "") or ""
