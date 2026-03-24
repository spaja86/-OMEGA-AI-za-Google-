"""
OMEGA AI za Google — evolucijski sistem.

Implementira evolucijski AI loop koji kontinuirano unapređuje OMEGA AI
parametre i strategije pretrage ka beskonačnosti.

Evolucijski ciklus:
    1. Evaluacija trenutnih parametara
    2. Selekcija najuspješnijih strategija
    3. Mutacija i rekombinacija parametara
    4. Nova generacija → ponoviti beskonačno
"""

from __future__ import annotations

import json
import math
import os
import random
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

from omega_ai import config


@dataclass
class EvolutionStrategy:
    """Jedna evolucijska strategija sa parametrima i ocjenom uspješnosti."""

    strategy_id: str
    generation: int
    mutation_rate: float
    expand_queries: bool
    top_k_results: int
    summary_max_chars: int
    fitness: float = 0.0
    query_count: int = 0
    total_relevance: float = 0.0

    def average_relevance(self) -> float:
        """Prosječna relevantnost ove strategije."""
        if self.query_count == 0:
            return 0.0
        return self.total_relevance / self.query_count

    def update_fitness(self, relevance_score: float) -> None:
        """Ažurira fitness na temelju novog bodovnog rezultata."""
        self.query_count += 1
        self.total_relevance += relevance_score
        # Fitness = prosječna relevantnost s penalom za premali broj testiranja
        confidence = 1.0 - math.exp(-self.query_count / 5.0)
        self.fitness = self.average_relevance() * confidence


@dataclass
class EvolutionMemory:
    """Trajna memorija evolucijskog procesa."""

    generation: int = 0
    total_queries: int = 0
    total_cycles: int = 0
    avg_relevance_score: float = 0.0
    best_fitness_ever: float = 0.0
    strategies: List[Dict[str, Any]] = field(default_factory=list)
    history: List[Dict[str, Any]] = field(default_factory=list)


class EvolutionEngine:
    """Evolutivni motor koji vodi OMEGA AI ka beskonačnosti.

    Parametri koji evolvuiraju:
    - mutation_rate: stopa mutacije za slijedeću generaciju
    - expand_queries: da li proširivati upite
    - top_k_results: koliko top rezultata zadržati
    - summary_max_chars: dužina AI sažetka
    """

    _POPULATION_SIZE = 4

    # Granice mutacije
    _MUTATION_RATE_MIN = 0.01
    _MUTATION_RATE_MAX = 0.5
    _MUTATION_RATE_DELTA = 0.05
    _TOP_K_MIN = 1
    _TOP_K_MAX = 10
    _SUMMARY_CHARS_MIN = 50
    _SUMMARY_CHARS_MAX = 500
    _SUMMARY_CHARS_DELTA = 50

    def __init__(self, memory_file: Optional[str] = None) -> None:
        self._memory_file = memory_file or config.EVOLUTION_MEMORY_FILE
        self._memory = self._load_memory()
        self._population: List[EvolutionStrategy] = self._restore_population()
        if not self._population:
            self._population = self._initialize_population()

    # ------------------------------------------------------------------
    # Javne metode
    # ------------------------------------------------------------------

    @property
    def current_strategy(self) -> EvolutionStrategy:
        """Vraća trenutno najboljу strategiju."""
        return max(self._population, key=lambda s: s.fitness)

    def record_query_result(self, relevance_score: float) -> None:
        """Bilježi rezultat upita u trenutnu strategiju i memoriju.

        Args:
            relevance_score: Ocjena relevantnosti u rasponu [0, 1].
        """
        self._memory.total_queries += 1
        # Ažurira sve strategije (samo aktivnu u praksi, ali tracking za sve)
        self.current_strategy.update_fitness(relevance_score)
        # Ažurira globalnu prosječnu ocjenu
        total = self._memory.total_queries
        prev = self._memory.avg_relevance_score
        self._memory.avg_relevance_score = prev + (relevance_score - prev) / total

        if self.current_strategy.fitness > self._memory.best_fitness_ever:
            self._memory.best_fitness_ever = self.current_strategy.fitness

        self._save_memory()

    def run_cycle(self) -> EvolutionStrategy:
        """Pokreće jedan evolucijski ciklus.

        Returns:
            Nova best strategija nakon evolucije.
        """
        self._memory.generation += 1
        self._memory.total_cycles += 1

        # Selekcija — zadržavamo top half
        sorted_pop = sorted(self._population, key=lambda s: s.fitness, reverse=True)
        survivors = sorted_pop[: self._POPULATION_SIZE // 2]

        # Reprodukcija i mutacija
        offspring: List[EvolutionStrategy] = []
        while len(offspring) < self._POPULATION_SIZE - len(survivors):
            parent_a = random.choice(survivors)
            parent_b = random.choice(survivors)
            child = self._crossover(parent_a, parent_b)
            child = self._mutate(child)
            offspring.append(child)

        self._population = survivors + offspring

        # Bilježi historiju generacije
        self._memory.history.append(
            {
                "generation": self._memory.generation,
                "timestamp": time.time(),
                "best_fitness": self.current_strategy.fitness,
                "avg_fitness": sum(s.fitness for s in self._population)
                / len(self._population),
                "population_size": len(self._population),
            }
        )
        self._save_memory()
        return self.current_strategy

    def get_stats(self) -> Dict[str, Any]:
        """Vraća statistike evolucijskog procesa.

        Returns:
            Rječnik sa statistikama.
        """
        return {
            "generation": self._memory.generation,
            "total_queries": self._memory.total_queries,
            "total_cycles": self._memory.total_cycles,
            "avg_relevance_score": round(self._memory.avg_relevance_score, 4),
            "best_fitness_ever": round(self._memory.best_fitness_ever, 4),
            "current_strategy": {
                "strategy_id": self.current_strategy.strategy_id,
                "fitness": round(self.current_strategy.fitness, 4),
                "mutation_rate": self.current_strategy.mutation_rate,
                "expand_queries": self.current_strategy.expand_queries,
                "top_k_results": self.current_strategy.top_k_results,
            },
            "population_size": len(self._population),
        }

    def reset(self) -> None:
        """Resetuje evolucijsku memoriju na početno stanje."""
        self._memory = EvolutionMemory()
        self._population = self._initialize_population()
        self._save_memory()

    # ------------------------------------------------------------------
    # Interne metode
    # ------------------------------------------------------------------

    def _initialize_population(self) -> List[EvolutionStrategy]:
        """Kreira inicijalnu populaciju strategija."""
        strategies = []
        for i in range(self._POPULATION_SIZE):
            strategies.append(
                EvolutionStrategy(
                    strategy_id=f"gen0_s{i}",
                    generation=0,
                    mutation_rate=0.05 + i * 0.05,
                    expand_queries=i % 2 == 0,
                    top_k_results=3 + i,
                    summary_max_chars=150 + i * 50,
                )
            )
        return strategies

    def _crossover(
        self, parent_a: EvolutionStrategy, parent_b: EvolutionStrategy
    ) -> EvolutionStrategy:
        """Rekombinira parametre dvaju roditelja."""
        gen = self._memory.generation
        return EvolutionStrategy(
            strategy_id=f"gen{gen}_s{random.randint(100, 999)}",
            generation=gen,
            mutation_rate=(parent_a.mutation_rate + parent_b.mutation_rate) / 2,
            expand_queries=random.choice(
                [parent_a.expand_queries, parent_b.expand_queries]
            ),
            top_k_results=random.choice(
                [parent_a.top_k_results, parent_b.top_k_results]
            ),
            summary_max_chars=random.choice(
                [parent_a.summary_max_chars, parent_b.summary_max_chars]
            ),
        )

    def _mutate(self, strategy: EvolutionStrategy) -> EvolutionStrategy:
        """Mutira parametre strategije prema mutation_rate."""
        rate = strategy.mutation_rate
        if random.random() < rate:
            strategy.mutation_rate = max(
                self._MUTATION_RATE_MIN,
                min(self._MUTATION_RATE_MAX, strategy.mutation_rate + random.uniform(-self._MUTATION_RATE_DELTA, self._MUTATION_RATE_DELTA)),
            )
        if random.random() < rate:
            strategy.expand_queries = not strategy.expand_queries
        if random.random() < rate:
            strategy.top_k_results = max(self._TOP_K_MIN, min(self._TOP_K_MAX, strategy.top_k_results + random.randint(-1, 1)))
        if random.random() < rate:
            strategy.summary_max_chars = max(
                self._SUMMARY_CHARS_MIN,
                min(self._SUMMARY_CHARS_MAX, strategy.summary_max_chars + random.randint(-self._SUMMARY_CHARS_DELTA, self._SUMMARY_CHARS_DELTA)),
            )
        return strategy

    def _restore_population(self) -> List[EvolutionStrategy]:
        """Obnavlja populaciju iz sačuvane memorije."""
        restored = []
        for s_dict in self._memory.strategies:
            try:
                restored.append(EvolutionStrategy(**s_dict))
            except (TypeError, KeyError):
                pass
        return restored

    def _load_memory(self) -> EvolutionMemory:
        """Učitava memoriju iz datoteke."""
        if os.path.exists(self._memory_file):
            try:
                with open(self._memory_file, encoding="utf-8") as f:
                    data = json.load(f)
                mem = EvolutionMemory()
                for key, value in data.items():
                    if hasattr(mem, key):
                        setattr(mem, key, value)
                return mem
            except (json.JSONDecodeError, OSError):
                pass
        return EvolutionMemory()

    def _save_memory(self) -> None:
        """Čuva memoriju u datoteku."""
        self._memory.strategies = [asdict(s) for s in self._population]
        try:
            with open(self._memory_file, "w", encoding="utf-8") as f:
                json.dump(asdict(self._memory), f, indent=2, ensure_ascii=False)
        except OSError:
            pass
