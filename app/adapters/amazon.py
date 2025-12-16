from typing import List, Dict, Any
import random, time

class AmazonClientBase:
    def top_products(self, market: str, k: int = 10) -> List[Dict[str, Any]]:
        raise NotImplementedError
    def reviews_for(self, market: str, asin: str, k: int = 30) -> List[str]:
        raise NotImplementedError
    def affiliate_url(self, market: str, asin: str, associate_tag: str) -> str:
        return f"https://www.amazon.{ 'com' if market=='US' else ('co.uk' if market=='UK' else 'ca') }/dp/{asin}?tag={associate_tag or 'yourtag-20'}"

class AmazonClientMock(AmazonClientBase):
    def top_products(self, market: str, k: int = 10) -> List[Dict[str, Any]]:
        # Deterministic-ish fake data
        suffix = {'US':'com','UK':'co.uk','CA':'ca'}[market]
        out = []
        for i in range(k):
            asin = f"M{market}{i:03d}"
            price = round(random.uniform(99, 1499), 2)
            out.append({
                "market": market,
                "asin": asin,
                "title": f"ProMax {market} Gadget {i}",
                "brand": "AcmeTech",
                "price": price,
                "currency": "USD" if market=="US" else ("GBP" if market=="UK" else "CAD"),
                "rating": round(random.uniform(3.8, 4.8), 1),
                "reviews_count": random.randint(120, 12000),
                "images": [f"https://picsum.photos/seed/{asin}-{n}/600/600" for n in range(3)],
                "url": f"https://www.amazon.{suffix}/dp/{asin}"
            })
        return out

    def reviews_for(self, market: str, asin: str, k: int = 30) -> List[str]:
        random.seed(hash(asin) % (2**32))
        samples = [
            "Sturdy build and premium feel.",
            "Battery lasts all day with heavy use.",
            "Setup was plug-and-play; super easy.",
            "Customer support resolved my issue quickly.",
            "Picture quality is crisp and bright.",
            "Sound could be louder but acceptable.",
            "Great value for the price point.",
            "Packaging was excellent; arrived safe.",
            "Manual could be clearer but YouTube helps.",
            "Exceeded expectations for performance.",
        ]
        return [random.choice(samples) for _ in range(k)]

class AmazonClientPAAPI(AmazonClientBase):
    # Stub for real PA-API integration
    def __init__(self, access_key: str, secret_key: str, associate_tag: str):
        self.access_key = access_key
        self.secret_key = secret_key
        self.associate_tag_default = associate_tag

    def top_products(self, market: str, k: int = 10) -> List[Dict[str, Any]]:
        # TODO: Implement search in BestSellers or BrowseNodes via PA-API 5.0
        raise NotImplementedError("PA-API integration not implemented in starter. Use mock or add your key and implement here.")

    def reviews_for(self, market: str, asin: str, k: int = 30) -> List[str]:
        # Amazon public reviews are not in PA-API; you must build a compliant pipeline.
        raise NotImplementedError("Fetching reviews requires a compliant method. Keep using mock in this starter.")
