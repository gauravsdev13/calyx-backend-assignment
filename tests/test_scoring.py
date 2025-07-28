import unittest
from app.utils import sigmoid_score


class TestScoring(unittest.TestCase):

    def test_midpoint_score(self):
        score = sigmoid_score(50)
        self.assertAlmostEqual(score, 50.0, delta=0.5)

    def test_high_score(self):
        score = sigmoid_score(100)
        self.assertGreater(score, 95)

    def test_low_score(self):
        score = sigmoid_score(0)
        self.assertLess(score, 10)


if __name__ == "__main__":
    unittest.main()
