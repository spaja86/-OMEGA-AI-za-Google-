"""
OMEGA AI za Google — konfiguracija sustava.
"""

import os

# Google Custom Search API (opciono)
GOOGLE_API_KEY: str = os.environ.get("GOOGLE_API_KEY", "")
GOOGLE_CSE_ID: str = os.environ.get("GOOGLE_CSE_ID", "")

# OpenAI / compatible LLM API (opciono)
OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL: str = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL: str = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

# Evolucija
EVOLUTION_MEMORY_FILE: str = os.environ.get(
    "OMEGA_MEMORY_FILE", "omega_evolution_memory.json"
)
MAX_RESULTS_PER_QUERY: int = int(os.environ.get("MAX_RESULTS_PER_QUERY", "10"))
EVOLUTION_MUTATION_RATE: float = float(os.environ.get("EVOLUTION_MUTATION_RATE", "0.1"))
EVOLUTION_TOP_K: int = int(os.environ.get("EVOLUTION_TOP_K", "5"))

# Referenca
OMEGA_AI_URL: str = "https://chatgpt.com/c/686787a3-1168-8006-8d37-418e3e220e69"
