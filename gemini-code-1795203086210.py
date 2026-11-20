# Blind rank-collapse detector on coupled array M (shape: C x N)
import numpy as np

def effective_rank_trajectory(M: np.ndarray, win: int = 512, step: int = 128):
    r_eff = []
    for t0 in range(0, M.shape[1] - win, step):
        X = M[:, t0 : t0 + win]
        X = X - X.mean(axis=1, keepdims=True)
        s = np.linalg.svd(X, compute_uv=False)
        p = (s ** 2) / (np.sum(s ** 2) + 1e-30)
        r_eff.append(np.exp(-np.sum(p * np.log(p + 1e-30))))
    return np.array(r_eff)  # sharp trough isolates [2996s, 3036s]