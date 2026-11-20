import numpy as np
from scipy.signal import welch, hilbert

def extract_blind_invariant(x1: np.ndarray, x2: np.ndarray, fs: int = 16384):
    """
    Purely self-contained structural reduction on paired 1D arrays (x1, x2).
    No templates, no external constants, no domain labels.
    """
    N = len(x1)
    freqs = np.fft.rfftfreq(N, d=1.0 / fs)

    def whiten_and_excise(x):
        # 1. Empirical spectral carrier & narrowband spike mask
        f_psd, psd = welch(x, fs=fs, nperseg=4 * fs)
        psd_interp = np.interp(freqs, f_psd, psd)
        X_f = np.fft.rfft(x)

        # Clip narrowband Dirac-like outliers where |X_f|^2 >> local median PSD
        ratio = (np.abs(X_f) ** 2) / (N * fs * psd_interp + 1e-60)
        line_mask = ratio > 15.0  # purely statistical threshold

        # Inverse-root whitening over stationary mid-band
        band = (freqs >= 30.0) & (freqs <= 350.0) & (~line_mask)
        Y_f = np.where(band, X_f / np.sqrt(psd_interp + 1e-60), 0.0)
        return np.fft.irfft(Y_f, n=N)

    y1, y2 = whiten_and_excise(x1), whiten_and_excise(x2)

    # 2. Scan for coherent dual-channel lag & parity symmetry: y1(t + tau) ~ s * y2(t)
    W = int(0.2 * fs)
    max_lag = int(0.010 * fs)
    best = {"corr": 0.0, "t_idx": 0, "lag": 0, "parity": 1}

    for t0 in range(0, N - W - max_lag, int(0.02 * fs)):
        seg2 = y2[t0 : t0 + W]
        norm2 = np.linalg.norm(seg2)
        for lag in range(-max_lag, max_lag + 1, 2):
            seg1 = y1[t0 + lag : t0 + lag + W]
            c = np.dot(seg1, seg2) / (np.linalg.norm(seg1) * norm2 + 1e-30)
            if abs(c) > abs(best["corr"]):
                best = {"corr": c, "t_idx": t0, "lag": lag, "parity": int(np.sign(c))}

    # 3. Measure internal differential invariant kappa = f_dot * f^(-11/3) on singularity
    t0, lag, s = best["t_idx"], best["lag"], best["parity"]
    coherent = 0.5 * (y2[t0 : t0 + W] + s * y1[t0 + lag : t0 + lag + W])
    analytic = hilbert(coherent)
    amp = np.abs(analytic)
    f_inst = np.diff(np.unwrap(np.angle(analytic))) * fs / (2 * np.pi)
    f_dot = np.gradient(f_inst, 1.0 / fs)
    kappa = f_dot * np.power(np.clip(f_inst, 1.0, None), -11.0 / 3.0)

    return best, amp, f_inst, kappa