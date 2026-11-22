"""First-hand check of the PR #2 prototype shadow, on the original code.

Usage:
  git show origin/anthology:gemini-code-1795203041292.py > /tmp/probe_original.py
  python3 -I -B audits/2026-11-22/checks/check_probe_shadow.py /tmp/probe_original.py

The claim under test (AUDIT-007R): the original probe_window reports
near-perfect coupling for two independent linear drifts, while staying
near zero for independent white noise. Exit 0 means the shadow
reproduces on the original artifact.
"""
import importlib.util
import sys

import numpy as np


def main(path):
    spec = importlib.util.spec_from_file_location("probe_original", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    rng = np.random.default_rng(7)
    t = np.arange(900.0)
    drifts = mod.probe_window({
        "a": 0.01 * t + rng.normal(0, 0.05, 900),
        "b": -0.013 * t + rng.normal(0, 0.05, 900),
    })
    noise = mod.probe_window({
        "a": rng.normal(0, 1, 900),
        "b": rng.normal(0, 1, 900),
    })
    lock_drift = drifts["cross_modal_coupling"][("a", "b")]["manifold_lock"]
    lock_noise = noise["cross_modal_coupling"][("a", "b")]["manifold_lock"]
    print(f"independent drifts lock: {lock_drift:.4f}")
    print(f"independent noise lock:  {lock_noise:.4f}")
    if not (lock_drift > 0.9 and lock_noise < 0.1):
        raise SystemExit("FAIL: shadow did not reproduce as audited")
    print("prototype shadow reproduced on original code: OK")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(sys.argv[1])
