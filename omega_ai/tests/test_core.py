"""
Testovi za OMEGA AI core modul.
"""

import unittest


class TestOmegaAICore(unittest.TestCase):
    def setUp(self):
        # Koristimo privremenu datoteku za memoriju kako testovi ne bi zagađivali
        import tempfile
        import os
        tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        tmp.close()
        self._tmpfile = tmp.name
        from omega_ai.core import OmegaAI
        self.omega = OmegaAI(memory_file=self._tmpfile)

    def tearDown(self):
        import os
        if os.path.exists(self._tmpfile):
            os.remove(self._tmpfile)

    def test_version(self):
        self.assertEqual(self.omega.VERSION, "1.0.0")

    def test_omega_ai_url(self):
        self.assertIn("chatgpt.com", self.omega.OMEGA_AI_URL)

    def test_search_returns_results(self):
        results = self.omega.search("kvantno računarstvo")
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

    def test_search_results_have_required_fields(self):
        results = self.omega.search("AI technology")
        for r in results:
            self.assertIsNotNone(r.title)
            self.assertIsNotNone(r.url)
            self.assertIsNotNone(r.snippet)
            self.assertGreaterEqual(r.relevance_score, 0.0)
            self.assertLessEqual(r.relevance_score, 1.0)

    def test_search_results_are_ranked(self):
        results = self.omega.search("machine learning")
        for i in range(len(results) - 1):
            self.assertGreaterEqual(
                results[i].relevance_score, results[i + 1].relevance_score
            )

    def test_search_updates_evolution_stats(self):
        initial_queries = self.omega.evolution.get_stats()["total_queries"]
        self.omega.search("test query")
        updated_queries = self.omega.evolution.get_stats()["total_queries"]
        self.assertEqual(updated_queries, initial_queries + 1)

    def test_repr(self):
        r = repr(self.omega)
        self.assertIn("OmegaAI", r)
        self.assertIn("version=", r)

    def test_auto_evolve(self):
        initial_gen = self.omega.evolution.get_stats()["generation"]
        self.omega.search("test", auto_evolve=True)
        new_gen = self.omega.evolution.get_stats()["generation"]
        self.assertGreater(new_gen, initial_gen)


if __name__ == "__main__":
    unittest.main()
