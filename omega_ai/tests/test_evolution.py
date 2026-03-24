"""
Testovi za OMEGA AI evolution modul.
"""

import json
import os
import tempfile
import unittest

from omega_ai.evolution import EvolutionEngine, EvolutionMemory, EvolutionStrategy


class TestEvolutionEngine(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        tmp.close()
        self._tmpfile = tmp.name
        self.engine = EvolutionEngine(memory_file=self._tmpfile)

    def tearDown(self):
        if os.path.exists(self._tmpfile):
            os.remove(self._tmpfile)

    def test_initial_population(self):
        self.assertGreater(len(self.engine._population), 0)

    def test_current_strategy_is_strategy(self):
        s = self.engine.current_strategy
        self.assertIsInstance(s, EvolutionStrategy)

    def test_record_query_result_increments_count(self):
        initial = self.engine.get_stats()["total_queries"]
        self.engine.record_query_result(0.75)
        self.assertEqual(self.engine.get_stats()["total_queries"], initial + 1)

    def test_run_cycle_increments_generation(self):
        initial_gen = self.engine.get_stats()["generation"]
        self.engine.run_cycle()
        self.assertEqual(self.engine.get_stats()["generation"], initial_gen + 1)

    def test_run_cycle_increments_total_cycles(self):
        initial = self.engine.get_stats()["total_cycles"]
        self.engine.run_cycle()
        self.assertEqual(self.engine.get_stats()["total_cycles"], initial + 1)

    def test_get_stats_keys(self):
        stats = self.engine.get_stats()
        expected_keys = {
            "generation", "total_queries", "total_cycles",
            "avg_relevance_score", "best_fitness_ever",
            "current_strategy", "population_size",
        }
        self.assertTrue(expected_keys.issubset(set(stats.keys())))

    def test_memory_persists_across_instances(self):
        self.engine.record_query_result(0.8)
        self.engine.run_cycle()
        queries_before = self.engine.get_stats()["total_queries"]

        # Novi engine sa istom datotekom
        engine2 = EvolutionEngine(memory_file=self._tmpfile)
        self.assertEqual(engine2.get_stats()["total_queries"], queries_before)

    def test_reset_clears_memory(self):
        self.engine.record_query_result(0.9)
        self.engine.run_cycle()
        self.engine.reset()
        stats = self.engine.get_stats()
        self.assertEqual(stats["generation"], 0)
        self.assertEqual(stats["total_queries"], 0)

    def test_avg_relevance_score_updates(self):
        self.engine.record_query_result(1.0)
        stats = self.engine.get_stats()
        self.assertGreater(stats["avg_relevance_score"], 0.0)

    def test_population_size_stable_after_cycles(self):
        pop_size = self.engine.get_stats()["population_size"]
        for _ in range(5):
            self.engine.run_cycle()
        self.assertEqual(self.engine.get_stats()["population_size"], pop_size)


class TestEvolutionStrategy(unittest.TestCase):
    def _make_strategy(self):
        return EvolutionStrategy(
            strategy_id="test_s0",
            generation=0,
            mutation_rate=0.1,
            expand_queries=True,
            top_k_results=5,
            summary_max_chars=200,
        )

    def test_average_relevance_zero_with_no_queries(self):
        s = self._make_strategy()
        self.assertEqual(s.average_relevance(), 0.0)

    def test_update_fitness_increments_query_count(self):
        s = self._make_strategy()
        s.update_fitness(0.8)
        self.assertEqual(s.query_count, 1)

    def test_update_fitness_tracks_total_relevance(self):
        s = self._make_strategy()
        s.update_fitness(0.6)
        s.update_fitness(0.8)
        self.assertAlmostEqual(s.total_relevance, 1.4)

    def test_fitness_grows_with_good_scores(self):
        s = self._make_strategy()
        for _ in range(10):
            s.update_fitness(1.0)
        self.assertGreater(s.fitness, 0.5)


if __name__ == "__main__":
    unittest.main()
