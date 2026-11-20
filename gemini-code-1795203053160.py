import numpy as np
from scipy.signal import hilbert

def perceptual_invariants(X, t, freqs=None):
    """
    Domain-agnostic structural probes over raw sensor manifolds.
    Returns pure dimensionless signatures without physical priors.
    """
    probes = {}

    # 1. Chromatic Dispersion Shear (2D frequency-time grids: Form V)
    if X.ndim == 2 and freqs is not None:
        # Maximize temporal kurtosis over inverse-square shear parameter kappa
        kappas = np.linspace(0, 1e3, 200)
        scores = []
        for k in kappas:
            shifts = np.round(k * (freqs ** -2)).astype(int)
            aligned = np.array([np.roll(row, -s) for row, s in zip(X, shifts)])
            profile = aligned.mean(axis=0)
            scores.append(np.mean((profile - profile.mean())**4) / (np.var(profile)**2 + 1e-30))
        probes["shear_kurtosis_peak"] = (kappas[np.argmax(scores)], max(scores))

    # 2. Clock-Lattice Autocorrelation Excess (1D continuous streams: Form VII)
    if X.ndim == 1:
        x0 = X - np.mean(X)
        acf = np.correlate(x0, x0, mode="full")[len(x0)-1:]
        acf /= (acf[0] + 1e-30)
        probes["acf_profile"] = acf

        # 3. Time-Reversal Asymmetry / Sawtooth Index (Form VIII)
        dx = np.diff(X)
        probes["time_asymmetry"] = np.mean(dx**3) / (np.var(dx)**1.5 + 1e-30)

        # 4. Analytic Envelope & Instantaneous Phase / Hilbert Symmetry (Forms VI, IX)
        z = hilbert(x0)
        probes["phase_coherence"] = np.abs(np.mean(np.exp(1j * np.angle(z))))

    return probes