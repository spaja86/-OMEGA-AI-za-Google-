"""
OMEGA AI za Google — query expander modul.

Proširuje korisničke upite kako bi Google pretraga dala relevantnije rezultate.
"""

from __future__ import annotations

import re
from typing import List


# Sinonimi i proširenja za česte koncepte (statički rječnik kao fallback)
_STATIC_EXPANSIONS: dict[str, List[str]] = {
    "ai": ["artificial intelligence", "machine learning", "deep learning"],
    "ml": ["machine learning", "neural network", "AI"],
    "quantum": ["quantum computing", "qubit", "superposition"],
    "google": ["Google Search", "Google AI", "Alphabet"],
    "beskonačnost": ["infinity", "unlimited", "infinite"],
}


def expand_query(query: str, extra_terms: List[str] | None = None) -> str:
    """Vraća proširenu verziju upita.

    Args:
        query: Originalni korisnički upit.
        extra_terms: Dodatni pojmovi koji se dodaju na upit.

    Returns:
        Prošireni upit kao string.
    """
    tokens = query.lower().split()
    additions: List[str] = []

    for token in tokens:
        clean = re.sub(r"[^a-zčćšđž]", "", token)
        if clean in _STATIC_EXPANSIONS:
            additions.extend(_STATIC_EXPANSIONS[clean])

    if extra_terms:
        additions.extend(extra_terms)

    # Deduplikacija, zadržava redosljed
    seen: set[str] = set(query.lower().split())
    unique_additions: List[str] = []
    for term in additions:
        if term.lower() not in seen:
            seen.add(term.lower())
            unique_additions.append(term)

    if unique_additions:
        return query + " " + " ".join(unique_additions)
    return query


def suggest_related_queries(query: str, n: int = 3) -> List[str]:
    """Generira listu srodnih upita na temelju originalnog.

    Args:
        query: Originalni upit.
        n: Broj srodnih upita za generisanje.

    Returns:
        Lista srodnih upita.
    """
    templates = [
        "{query} tutorial",
        "{query} examples 2024",
        "{query} best practices",
        "how does {query} work",
        "{query} vs alternatives",
        "latest research {query}",
        "{query} future trends",
    ]
    related = [t.format(query=query) for t in templates[:n]]
    return related
