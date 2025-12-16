from typing import Dict

class SocialPosterBase:
    def post(self, platform: str, market: str, language: str, message: str, link: str) -> str:
        raise NotImplementedError

class MockSocialPoster(SocialPosterBase):
    def post(self, platform: str, market: str, language: str, message: str, link: str) -> str:
        return f"[MOCK:{platform}:{market}:{language}] {message} -> {link}"

# Stubs for real APIs
class FacebookPoster(SocialPosterBase):
    def post(self, platform, market, language, message, link):
        # Implement Graph API call here
        return "posted:facebook"

class XPoster(SocialPosterBase):
    def post(self, platform, market, language, message, link):
        # Implement X (Twitter) API v2 here
        return "posted:x"

class InstagramPoster(SocialPosterBase):
    def post(self, platform, market, language, message, link):
        # Implement Instagram Graph API here
        return "posted:instagram"

class PinterestPoster(SocialPosterBase):
    def post(self, platform, market, language, message, link):
        # Implement Pinterest API here
        return "posted:pinterest"

class TikTokPoster(SocialPosterBase):
    def post(self, platform, market, language, message, link):
        # Implement TikTok API here
        return "posted:tiktok"
