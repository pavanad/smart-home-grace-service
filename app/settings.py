# -*- coding: utf-8 -*-

"""
FastAPI settings for API service project.
"""

import os

# Project details
TITLE = "API - Grace Service"
DESCRIPTION = "API for the Grace Service"
QUERY_SUMMARY = (
    "Submit a question to the API and get an answer or a action based in the tools."
)

# Agent details
MODEL_NAME = "gemini-pro"

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
