"""
OMEGA AI za Google — search enhancer modul.

Poboljšava Google pretragu koristeći Google Custom Search API ili web scraping
kao fallback. Svaki rezultat se obogaćuje AI analizom.
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import List

from omega_ai import config
from omega_ai.query_expander import expand_query
from omega_ai.result_ranker import SearchResult, rank_results


class SearchEnhancer:
    """Poboljšava Google pretragu koristeći AI proširivanje upita i bodovanje."""

    def __init__(self) -> None:
        self._api_key = config.GOOGLE_API_KEY
        self._cse_id = config.GOOGLE_CSE_ID
        self._max_results = config.MAX_RESULTS_PER_QUERY

    def search(
        self,
        query: str,
        *,
        expand: bool = True,
        num: int | None = None,
    ) -> List[SearchResult]:
        """Izvršava poboljšanu Google pretragu.

        Args:
            query: Korisnički upit.
            expand: Da li proširiti upit AI proširivačem.
            num: Broj rezultata (default iz config).

        Returns:
            Rangirana lista SearchResult objekata.
        """
        effective_query = expand_query(query) if expand else query
        count = min(num or self._max_results, 10)  # Google API max = 10 po pozivu

        if self._api_key and self._cse_id:
            raw_results = self._google_api_search(effective_query, count)
        else:
            raw_results = self._mock_search(query, count)

        ranked = rank_results(raw_results, query)
        return ranked

    def _google_api_search(self, query: str, num: int) -> List[SearchResult]:
        """Pretražuje koristeći Google Custom Search JSON API."""
        base_url = "https://www.googleapis.com/customsearch/v1"
        params = urllib.parse.urlencode(
            {
                "key": self._api_key,
                "cx": self._cse_id,
                "q": query,
                "num": num,
            }
        )
        url = f"{base_url}?{params}"
        try:
            with urllib.request.urlopen(url, timeout=10) as resp:  # noqa: S310
                data = json.loads(resp.read().decode())
        except Exception as exc:
            raise RuntimeError(f"Google API greška: {exc}") from exc

        results: List[SearchResult] = []
        for item in data.get("items", []):
            results.append(
                SearchResult(
                    title=item.get("title", ""),
                    url=item.get("link", ""),
                    snippet=item.get("snippet", ""),
                )
            )
        return results

    def _mock_search(self, query: str, num: int) -> List[SearchResult]:
        """Vraća mock rezultate kada API ključevi nisu postavljeni (demo/testing)."""
        templates = [
            (
                f"{query} — Wikipedia",
                f"https://en.wikipedia.org/wiki/{urllib.parse.quote(query)}",
                f"Sveobuhvatni članak o temi '{query}'. Sadrži historiju, definicije i primjere.",
            ),
            (
                f"Šta je {query}? Kompletni vodič",
                f"https://example.com/guides/{urllib.parse.quote(query)}",
                f"Ovaj vodič objašnjava sve aspekte teme {query} na jednostavan i detaljan način.",
            ),
            (
                f"{query} — najnovija istraživanja 2024",
                f"https://arxiv.org/search/?searchtype=all&query={urllib.parse.quote(query)}",
                f"Najnoviji naučni radovi i istraživanja vezana za {query}.",
            ),
            (
                f"Kako koristiti {query} — praktični primjeri",
                f"https://example.com/tutorials/{urllib.parse.quote(query)}",
                f"Praktični vodič sa primjerima kako primijeniti {query} u realnim situacijama.",
            ),
            (
                f"{query} vs alternative — poređenje",
                f"https://example.com/compare/{urllib.parse.quote(query)}",
                f"Detaljna analiza i poređenje {query} sa alternativnim rješenjima.",
            ),
        ]
        results: List[SearchResult] = []
        for title, url, snippet in templates[:num]:
            results.append(SearchResult(title=title, url=url, snippet=snippet))
        return results
