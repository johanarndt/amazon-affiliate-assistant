from pydantic import BaseModel
from typing import List, Optional

class ProductOut(BaseModel):
    id: int
    market: str
    asin: str
    title: str
    brand: str
    price: float
    currency: str
    rating: float
    reviews_count: int
    images: List[str]
    url: str
    class Config:
        from_attributes = True

class SalesPageOut(BaseModel):
    id: int
    market: str
    language: str
    html: str
    affiliate_link: str
    product: ProductOut
    class Config:
        from_attributes = True

class CreateSalesPageIn(BaseModel):
    product_id: int
    language: str = "en"
    affiliate_link: Optional[str] = ""

class SchedulePostsIn(BaseModel):
    sales_page_id: int
    markets: List[str]
    platforms: List[str]
    languages: List[str]

class ChatIn(BaseModel):
    message: str

class ChatOut(BaseModel):
    reply: str
