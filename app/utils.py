# app/utils.py
import math
import hashlib


def sigmoid_score(x: float, k: float = 0.2, x0: float = 50.0) -> float:
    """
    Calculate a normalized sigmoid score.

    Args:
        x (float): The input value to score.
        k (float, optional): Steepness of the curve. Default is 0.2.
        x0 (float, optional): Midpoint of the curve. Default is 50.0.
        scale (float, optional): Maximum score value. Default is 100.0.

    Returns:
        float: The normalized score, rounded to 2 decimal places.
    """
    return round(100 / (1 + math.exp(-k * (x - x0))), 2)


def generate_proof(score: float, timestamp: str, verifier_id: str) -> str:
    combined = f"{score}{timestamp}{verifier_id}".encode()
    return hashlib.sha256(combined).hexdigest()


def score_bucket(score: float) -> str:
    if score <= 50:
        return "0–50"
    elif score <= 75:
        return "51–75"
    else:
        return "76–100"


def category_weight(category: str) -> float:
    weights = {"emissions": 1.05, "water": 1.00, "waste": 0.95}
    return weights.get(category, 1.0)
