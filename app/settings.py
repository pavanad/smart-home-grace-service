# -*- coding: utf-8 -*-

"""
FastAPI settings for API service project.
"""

import logging
import os
from pathlib import Path

import yaml

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

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# cameras
def get_list_cameras():
    logger = logging.getLogger(__name__)
    filename = f"{BASE_DIR}/app/cameras.yml"
    try:
        with open(filename, "r") as f:
            data = yaml.safe_load(f)
            logger.info(f"Loaded cameras from '{filename}'.")
            return data.get("cameras", [])
    except FileNotFoundError:
        logger.error(f"File '{filename}' not found.")
        return []
    except Exception as e:
        logger.error(f"Error loading YAML file '{filename}': {e}")
        return []
