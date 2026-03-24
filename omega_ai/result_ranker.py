"""
OMEGA AI za Google — result ranker modul.

AI bodovanje i rangiranje rezultata pretrage prema relevantnosti.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import List


@dataclass
class SearchResult:
    """Predstavlja jedan obogaćen rezultat pretrage."""

    title: str
    url: str
    snippet: str
    relevance_score: float = 0.0
    ai_summary: str = ""
    keywords: List[str] = field(default_factory=list)
    rank: int = 0


def _keyword_overlap(text: str, query: str) -> float:
    """Računa TF-IDF-like overlap između teksta i upita."""
    query_tokens = set(re.sub(r"[^\w\s]", "", query.lower()).split())
    text_tokens = re.sub(r"[^\w\s]", "", text.lower()).split()
    if not query_tokens or not text_tokens:
        return 0.0
    matches = sum(1 for t in text_tokens if t in query_tokens)
    # Normalizacija logaritmom kako bi veći dokumenti ne bili automatski bolji
    return matches / (1 + math.log(1 + len(text_tokens)))


def score_result(result: SearchResult, query: str) -> float:
    """Izračunava relevancijsku ocjenu za jedan rezultat.

    Kombinira:
    - Preklapanje ključnih riječi u naslovu (veća težina)
    - Preklapanje ključnih riječi u snippetu
    - Bonus za HTTPS
    - Bonus za dužinu snippeta (više informacija = bolje)

    Args:
        result: Rezultat pretrage.
        query: Originalni upit.

    Returns:
        Float ocjena u rasponu [0, 1].
    """
    title_score = _keyword_overlap(result.title, query) * 2.0
    snippet_score = _keyword_overlap(result.snippet, query)
    https_bonus = 0.1 if result.url.startswith("https") else 0.0
    length_bonus = min(len(result.snippet) / 500.0, 0.2)

    raw = title_score + snippet_score + https_bonus + length_bonus
    # Sigmoid normalizacija u [0, 1]
    normalized = 1.0 / (1.0 + math.exp(-raw + 1.5))
    return round(normalized, 4)


def rank_results(results: List[SearchResult], query: str) -> List[SearchResult]:
    """Boduje i rangira listu rezultata.

    Args:
        results: Lista rezultata pretrage.
        query: Upit prema kojemu se rangira.

    Returns:
        Rangirana lista rezultata (od najboljeg prema najlošijem).
    """
    for result in results:
        result.relevance_score = score_result(result, query)
        # Kratki AI summary — ekstrakt najrelevantnijih rečenica iz snippeta
        result.ai_summary = _extract_summary(result.snippet, query)
        result.keywords = _extract_keywords(result.snippet + " " + result.title)

    ranked = sorted(results, key=lambda r: r.relevance_score, reverse=True)
    for idx, result in enumerate(ranked):
        result.rank = idx + 1
    return ranked


def _extract_summary(text: str, query: str, max_chars: int = 200) -> str:
    """Vraća kratki summary ekstrakcijom najrelevantnijih rečenica."""
    if not text:
        return ""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    query_tokens = set(re.sub(r"[^\w\s]", "", query.lower()).split())
    scored = []
    for s in sentences:
        overlap = sum(1 for t in s.lower().split() if t in query_tokens)
        scored.append((overlap, s))
    scored.sort(key=lambda x: x[0], reverse=True)
    summary = " ".join(s for _, s in scored[:2])
    return summary[:max_chars].strip()


def _extract_keywords(text: str, top_n: int = 5) -> List[str]:
    """Izvlači top N ključnih riječi iz teksta."""
    # Ukloni stop words (osnovna lista)
    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
        "for", "of", "with", "by", "from", "is", "it", "this", "that",
        "was", "are", "be", "as", "at", "so", "we", "he", "she", "they",
        "i", "you", "his", "her", "its", "our", "your", "their",
    }
    tokens = re.sub(r"[^\w\s]", "", text.lower()).split()
    freq: dict[str, int] = {}
    for t in tokens:
        if t not in stop_words and len(t) > 2:
            freq[t] = freq.get(t, 0) + 1
    sorted_tokens = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [t for t, _ in sorted_tokens[:top_n]]
