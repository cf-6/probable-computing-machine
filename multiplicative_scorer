from typing import List, Tuple, Dict, Callable, Union, Optional
import math
import numpy as np

# ==============================
# Normalizer implementations
# ==============================
def norm_linear(b: float, b_min: float, b_max: float) -> float:
    if b_max == b_min:
        return 0.
    return (b - b_min) / (b_max - b_min)

def norm_sigmoid(b: float, k: float = 1.0, b0: float = 0.0) -> float:
    return 1.0 / (1.0 + math.exp(-k * (b - b0)))

def norm_rank(b: float, dataset: List[float]) -> float:
    sorted_b = sorted(dataset)
    N = len(sorted_b)
    if N <= 1:
        return 0.0
    rank = sorted_b.index(b) + 1   # from 1
    return (rank - 1) / (N - 1)

def norm_log(b: float, b_min: float, b_max: float) -> float:
    if b_max == b_min:
        return 0.
    num = math.log(1 + b - b_min)
    den = math.log(1 + b_max - b_min)
    return num / den

# ==============================
# Verify factor φ(f)
# ==============================
def phi(f: Union[float,int]) -> float:
    if isinstance(f, float):
        return f
    if isinstance(f, int):
        return 1.0 if f == 1 else 0.0
    raise ValueError("Invalid type for f")

# ==============================
# Single score computation S(...)
# ==============================
def compute_score(
    e: float, b: float, C: float, Y: float, f: Union[float,int],
    normalizer: Callable[..., float],
    normalizer_args: Optional[dict] = None,
) -> float:
    normalizer_args = normalizer_args or {}
    nb = normalizer(b, **normalizer_args)
    pf = phi(f)
    S = e * nb * C * Y * pf
    # Clamp to [0,1]
    return max(0.0, min(1.0, S))

# ==============================
# Batch scoring for candidates
# ==============================
def batch_scores(
    e_list: List[float], 
    b_list: List[float], 
    C_list: List[float], 
    Y_list: List[float], 
    f_list: List[Union[float,int]],
    normalizer: Callable[..., float],
    normalizer_args: Optional[dict] = None,
) -> List[float]:
    scores = []
    for i in range(len(e_list)):
        e, b, C, Y, f = e_list[i], b_list[i], C_list[i], Y_list[i], f_list[i]
        args = dict(normalizer_args or {})
        if 'dataset' in normalizer.__code__.co_varnames:
            args['dataset'] = b_list
        score = compute_score(e, b, C, Y, f, normalizer, args)
        scores.append(score)
    return scores

# ==============================
# Top-K selection by score
# ==============================
def top_k(scores: List[float], K: int) -> List[int]:
    """Return indices of top-K scores"""
    return sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:K]

# ==============================
# Example usage and demonstration
# ==============================
if __name__ == "__main__":
    # Sample data
    e_list = [0.7, 0.9, 1.0, 0.6]
    b_list = [85, 67, 92, 50]
    C_list = [0.8, 1.0, 0.75, 0.9]
    Y_list = [0.95, 0.9, 1.0, 0.85]
    f_list = [1, 1, 0, 0.7]   # mix of binary and continuous

    b_min, b_max = min(b_list), max(b_list)

    # linearly normalized model with continuous f
    scores = batch_scores(
        e_list, b_list, C_list, Y_list, f_list,
        normalizer=norm_linear,
        normalizer_args={'b_min': b_min, 'b_max': b_max}
    )
    print("Scores (linear norm, mixed f):", scores)

    # Sigmoid normalization (k=0.05, center at mean)
    b0 = sum(b_list) / len(b_list)
    sig_scores = batch_scores(
        e_list, b_list, C_list, Y_list, f_list,
        normalizer=norm_sigmoid,
        normalizer_args={'k': 0.05, 'b0': b0}
    )
    print("Scores (sigmoid norm):", sig_scores)

    # Rank normalization
    rank_scores = batch_scores(
        e_list, b_list, C_list, Y_list, f_list,
        normalizer=norm_rank,
        normalizer_args={}
    )
    print("Scores (rank norm):", rank_scores)

    # Top-2 selection
    K = 2
    top2_idx = top_k(scores, K)
    print(f"Top-{K} indices:", top2_idx)
    print(f"Top-{K} scores:", [scores[i] for i in top2_idx])
