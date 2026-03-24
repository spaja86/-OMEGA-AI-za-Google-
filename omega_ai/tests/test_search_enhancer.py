"""
Testovi za OMEGA AI search enhancer modul.
"""

import unittest

from omega_ai.search_enhancer import SearchEnhancer


class TestSearchEnhancer(unittest.TestCase):
    def setUp(self):
        self.enhancer = SearchEnhancer()

    def test_mock_search_returns_results(self):
        results = self.enhancer.search("AI")
        self.assertGreater(len(results), 0)

    def test_mock_search_results_ranked(self):
        results = self.enhancer.search("machine learning")
        scores = [r.relevance_score for r in results]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_search_no_expand(self):
        results = self.enhancer.search("google", expand=False)
        self.assertIsInstance(results, list)

    def test_search_num_limit(self):
        results = self.enhancer.search("test", num=2)
        self.assertLessEqual(len(results), 2)

    def test_result_has_rank(self):
        results = self.enhancer.search("technology")
        for r in results:
            self.assertGreater(r.rank, 0)

    def test_result_has_ai_summary(self):
        results = self.enhancer.search("quantum computing")
        for r in results:
            self.assertIsNotNone(r.ai_summary)


if __name__ == "__main__":
    unittest.main()
