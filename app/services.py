"""
services.py
Minimal service layer for Amazon Affiliate Assistant
"""

import os

llm_engine = None

if os.getenv("ENABLE_LLM", "false").lower() == "true":
    from app.adapters.llm_adapter import LocalTemplateLLM
    llm_engine = LocalTemplateLLM()


# -------------------------------
# LLM ENGINE (REQUIRED BY backend)
# -------------------------------

# Create a single global LLM engine
llm_engine = LocalTemplateLLM()

# -------------------------------
# Feed placeholder
# -------------------------------

def fetch_feed_for_market(market: str):
    """
    Placeholder feed provider.
    Your frontend loads XML feeds directly, so this backend
    just returns a confirmation payload.
    """
    return {
        "status": "ok",
        "market": market,
        "message": "Feed adapter active"
    }

# -------------------------------
# Search placeholder
# -------------------------------

def search_redirect(query: str):
    """
    Placeholder search redirect handler.
    Your frontend handles the actual Amazon search URL redirects.
    """
    return {
        "status": "ok",
        "query": query,
        "message": "Search redirect adapter active"
    }
