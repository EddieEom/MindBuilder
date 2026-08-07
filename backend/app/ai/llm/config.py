import os

from dotenv import load_dotenv

load_dotenv()

# ==========================================================
# OpenRouter
# ==========================================================

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_BASE_URL = os.getenv(
    "OPENROUTER_BASE_URL",
    "https://openrouter.ai/api/v1",
)

MODEL_NAME = os.getenv(
    "OPENROUTER_MODEL",
    "nvidia/nemotron-3-ultra-550b-a55b:free",
)

# ==========================================================
# Retry
# ==========================================================

MAX_RETRY = 3

RETRY_DELAY = 1

# ==========================================================
# Generation Profile
# ==========================================================

DEFAULT_PROFILE = "default"

LLM_PROFILES = {

    "default": {

        "temperature": 0.3,

        "top_p": 0.9,

        "max_tokens": 1200,

    },

    "recommendation": {

        "temperature": 0.4,

        "top_p": 0.9,

        "max_tokens": 1800,

    },

    "growth": {

        "temperature": 0.35,

        "top_p": 0.9,

        "max_tokens": 1500,

    },

    "identity": {

        "temperature": 0.30,

        "top_p": 0.90,

        "max_tokens": 1500,

    },

    "lifemap": {

        "temperature": 0.40,

        "top_p": 0.95,

        "max_tokens": 2000,

    },

}