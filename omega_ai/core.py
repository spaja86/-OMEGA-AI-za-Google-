"""
OMEGA AI za Google — glavni motor.

OmegaAI je centralni objekt koji integrira sve komponente:
- SearchEnhancer: poboljšana Google pretraga
- EvolutionEngine: evolucijski AI loop
- QueryExpander: proširivanje upita
"""

from __future__ import annotations

from typing import List, Optional

from omega_ai import config
from omega_ai.evolution import EvolutionEngine
from omega_ai.result_ranker import SearchResult
from omega_ai.search_enhancer import SearchEnhancer


class OmegaAI:
    """Centralni OMEGA AI objekat koji evolvira Google ka beskonačnosti.

    Primjer upotrebe::

        omega = OmegaAI()
        results = omega.search("kvantno računarstvo")
        for r in results:
            print(r.title, r.relevance_score)

        # Ručno pokretanje evolucijskog ciklusa
        omega.evolution.run_cycle()

        # Statistika
        stats = omega.evolution.get_stats()
        print(f"Generacija: {stats['generation']}")
    """

    VERSION = "1.0.0"
    OMEGA_AI_URL = config.OMEGA_AI_URL

    def __init__(
        self,
        memory_file: Optional[str] = None,
    ) -> None:
        """Inicijalizira OMEGA AI.

        Args:
            memory_file: Putanja do datoteke za čuvanje evolucijske memorije.
        """
        self.evolution = EvolutionEngine(memory_file=memory_file)
        self._enhancer = SearchEnhancer()

    def search(
        self,
        query: str,
        *,
        num: Optional[int] = None,
        auto_evolve: bool = False,
    ) -> List[SearchResult]:
        """Izvodi poboljšanu Google pretragu i bilježi rezultat u evoluciju.

        Args:
            query: Korisnički upit.
            num: Željeni broj rezultata.
            auto_evolve: Ako True, pokreće evolucijski ciklus po svakom upitu.

        Returns:
            Rangirana lista SearchResult objekata.
        """
        strategy = self.evolution.current_strategy
        results = self._enhancer.search(
            query,
            expand=strategy.expand_queries,
            num=num,
        )

        # Bilježi prosječnu relevantnost ovog upita u evolucijsku memoriju
        if results:
            avg_relevance = sum(r.relevance_score for r in results) / len(results)
            self.evolution.record_query_result(avg_relevance)

        if auto_evolve:
            self.evolution.run_cycle()

        return results

    def __repr__(self) -> str:
        stats = self.evolution.get_stats()
        return (
            f"OmegaAI(version={self.VERSION}, "
            f"generation={stats['generation']}, "
            f"queries={stats['total_queries']})"
        )
