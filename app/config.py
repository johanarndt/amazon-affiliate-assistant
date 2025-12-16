import os
from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "dev")
APP_TIMEZONE = os.getenv("APP_TIMEZONE", "Africa/Johannesburg")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")

# Amazon
AMAZON_PAAPI_ACCESS_KEY = os.getenv("AMAZON_PAAPI_ACCESS_KEY", "")
AMAZON_PAAPI_SECRET_KEY = os.getenv("AMAZON_PAAPI_SECRET_KEY", "")
AMAZON_ASSOCIATE_TAGS = {
    "US": os.getenv("AMAZON_ASSOCIATE_TAG_US", ""),
    "UK": os.getenv("AMAZON_ASSOCIATE_TAG_UK", ""),
    "CA": os.getenv("AMAZON_ASSOCIATE_TAG_CA", ""),
}

# LLM
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Social
FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", "")
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN", "")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
PINTEREST_ACCESS_TOKEN = os.getenv("PINTEREST_ACCESS_TOKEN", "")
TIKTOK_ACCESS_TOKEN = os.getenv("TIKTOK_ACCESS_TOKEN", "")

# Scheduler hours (CSV of ints)
def parse_hours(v, default):
    try:
        return [int(x) for x in (v or "").split(",") if x.strip() != ""]
    except Exception:
        return default

POST_HOURS = {
    "US": parse_hours(os.getenv("POST_HOURS_US", ""), [10, 19]),
    "UK": parse_hours(os.getenv("POST_HOURS_UK", ""), [11, 20]),
    "CA": parse_hours(os.getenv("POST_HOURS_CA", ""), [10, 19]),
}

# Adapters (toggle here)
USE_MOCK_AMAZON = True if not AMAZON_PAAPI_ACCESS_KEY else False
USE_MOCK_SOCIAL = True if not any([FACEBOOK_PAGE_ACCESS_TOKEN, X_BEARER_TOKEN, INSTAGRAM_ACCESS_TOKEN, PINTEREST_ACCESS_TOKEN, TIKTOK_ACCESS_TOKEN]) else False
USE_MOCK_LLM = True if not OPENAI_API_KEY else False
DEFAULT_MARKETS = ["US", "UK", "CA"]
