"""
services.py
Minimal service layer for Amazon Affiliate Assistant
"""

from app.adapters.llm_adapter import GroqLLM

llm_engine = GroqLLM()

