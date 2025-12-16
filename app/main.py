# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# existing chat router (you already have this working)
from app.adapters.chat_adapter import router as chat_router

# new routers we just added
from app.adapters.feed_api import router as feed_router
from app.adapters.search_redirect import router as search_router

app = FastAPI(title="Amazon Affiliate Assistant", version="0.1.0")

# CORS (allow your local frontend / systeme.io to call it during development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# health
@app.get("/")
def home():
    return {"status": "ok", "message": "Amazon Affiliate Assistant Backend Running"}

# include routers (they already contain their own prefixes)
app.include_router(chat_router)   # /api/chat/
app.include_router(feed_router)   # /api/feeds/...
app.include_router(search_router) # /api/search/...


