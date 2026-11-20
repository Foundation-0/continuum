import numpy as np
from scipy.signal import hilbert
from scipy.spatial.distance import pdist, squareform
from scipy.sparse.csgraph import minimum_spanning_tree


def takens_embed(x: np.ndarray, dim: int = 5, tau: int = 3) -> np.ndarray:
    """Coordinate-free phase-space reconstruction from a 1D wave."""
    x = (x - np.mean(x)) / (np.std(x) + 1e-12)
    win = (dim - 1) * tau + 1
    return np.lib.stride_tricks.sliding_window_view(x, win)[:, ::tau]


def async_event_lens(x: np.ndarray, delta: float = 0.35) -> np.ndarray:
    """
    Software neuromorphic lens: discards uniform clock ticks, firing only
    when signal amplitude crosses an adaptive threshold, then reconstructs
    strictly from asynchronous gradient events.
    """
    z = (x - np.mean(x)) / (np.std(x) + 1e-12)
    idx, vals = [0], [z[0]]
    last = z[0]
    for i in range(1, len(z)):
        if abs(z[i] - last) >= delta:
            idx.append(i)
            vals.append(z[i])
            last = z[i]
    if idx[-1] != len(z) - 1:
        idx.append(len(z) - 1)
        vals.append(z[-1])
    return np.interp(np.arange(len(z)), idx, vals)


def centered_rbf_kernel(X: np.ndarray) -> np.ndarray:
    """Scale- and rotation-invariant local geometry kernel on a manifold."""
    D = squareform(pdist(X))
    med = np.median(D[D > 0]) + 1e-12
    K = np.exp(-(D ** 2) / (2.0 * med ** 2))
    return K - K.mean(axis=0, keepdims=True) - K.mean(axis=1, keepdims=True) + K.mean()


def manifold_cka(X: np.ndarray, Y: np.ndarray) -> float:
    """
    Centered Kernel Alignment in [0, 1].
    Measures whether two distinct physical channels trace the same
    underlying topological geometry—independent of units or coordinates.
    """
    n = min(len(X), len(Y))
    Kx = centered_rbf_kernel(X[:n])
    Ky = centered_rbf_kernel(Y[:n])
    return float(np.sum(Kx * Ky) / (np.linalg.norm(Kx) * np.linalg.norm(Ky) + 1e-12))


def h0_persistence_entropy(X: np.ndarray) -> float:
    """
    Exact 0-dimensional Vietoris-Rips persistence via Minimum Spanning Tree.
    Quantifies topological fragmentation of the reconstructed attractor.
    """
    D = squareform(pdist(X))
    lifetimes = minimum_spanning_tree(D).data
    p = lifetimes / (np.sum(lifetimes) + 1e-12)
    return float(-np.sum(p * np.log(p + 1e-12)) / np.log(len(p) + 1e-12))


def probe_window(channels: dict[str, np.ndarray], dim: int = 5, tau: int = 3) -> dict:
    """
    Runs observer-cancellation and cross-modal sheaf locking over a synchronized
    multi-sensor window with zero semantic labels.
    """
    names = list(channels.keys())
    manifolds, observer_stability, topo_entropy = {}, {}, {}

    for name, sig in channels.items():
        M_raw = takens_embed(sig, dim=dim, tau=tau)
        # Incompatible observer lenses: (1) clockless async events, (2) pi/2 phase rotation
        M_async = takens_embed(async_event_lens(sig), dim=dim, tau=tau)
        M_phase = takens_embed(np.imag(hilbert(sig)), dim=dim, tau=tau)

        manifolds[name] = M_raw
        observer_stability[name] = 0.5 * (
            manifold_cka(M_raw, M_async) + manifold_cka(M_raw, M_phase)
        )
        topo_entropy[name] = h0_persistence_entropy(M_raw)

    # Cross-modal relational matrix (sheaf consistency across modalities)
    coupling = {}
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            raw_lock = manifold_cka(manifolds[a], manifolds[b])
            # Weight by geometric survival across observer perturbations
            reality_weighted = raw_lock * np.sqrt(
                observer_stability[a] * observer_stability[b]
            )
            coupling[(a, b)] = {
                "manifold_lock": round(raw_lock, 4),
                "observer_invariant_lock": round(reality_weighted, 4),
            }

    return {
        "observer_stability": {k: round(v, 4) for k, v in observer_stability.items()},
        "h0_topo_entropy": {k: round(v, 4) for k, v in topo_entropy.items()},
        "cross_modal_coupling": coupling,
    }