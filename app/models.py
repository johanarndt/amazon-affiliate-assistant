from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    market = Column(String, index=True)  # US/UK/CA
    asin = Column(String, index=True)
    title = Column(String)
    brand = Column(String)
    price = Column(Float)
    currency = Column(String, default="USD")
    rating = Column(Float)
    reviews_count = Column(Integer)
    images = Column(JSON)  # list[str]
    url = Column(String)
    fetched_at = Column(DateTime, default=datetime.utcnow)

    sales_pages = relationship("SalesPage", back_populates="product")

class SalesPage(Base):
    __tablename__ = "sales_pages"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    market = Column(String, index=True)
    language = Column(String, default="en")
    html = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    affiliate_link = Column(String, default="")

    product = relationship("Product", back_populates="sales_pages")

class ScheduledPost(Base):
    __tablename__ = "scheduled_posts"
    id = Column(Integer, primary_key=True, index=True)
    market = Column(String, index=True)
    platform = Column(String)  # facebook/x/instagram/pinterest/tiktok
    language = Column(String, default="en")
    content = Column(Text)
    sales_page_id = Column(Integer, ForeignKey("sales_pages.id"))
    scheduled_for = Column(DateTime, index=True)
    sent = Column(Boolean, default=False)
    result = Column(Text, default="")

class ChatLog(Base):
    __tablename__ = "chat_logs"
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)  # user/assistant/system
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
