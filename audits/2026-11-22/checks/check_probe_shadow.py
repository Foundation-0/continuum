"""First-hand check of the PR #2 prototype shadow, on the original code.

Needs numpy and scipy (the loaded prototype imports scipy.signal.hilbert).
Under python -I those packages must be on the isolated interpreter path;
user-site installs are hidden. This audit ran numpy 2.5.4 and scipy 1.18.1.

Usage:
  probe=$(mktemp)
  git show origin/anthology:gemini-code-1795203041292.py > "$probe"
  python3 -I -B audits/2026-11-22/checks/check_probe_shadow.py "$probe"

The claim under test (AUDIT-007R): the original probe_window reports
near-perfect coupling for two independent linear drifts, while staying
near zero for independent white noise. Exit 0 means the shadow
reproduces on the original artifact.
"""
import importlib.util
import sys

try:
    import numpy as np
except ImportError as exc:
    raise SystemExit(
        "check_probe_shadow.py needs numpy and scipy; under python -I "
        "install them on the isolated interpreter path (user-site is hidden)."
    ) from exc


def main(path):
    spec = importlib.util.spec_from_file_location("probe_original", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"could not load prototype from {path}")
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except ImportError as exc:
        raise SystemExit(
            "the loaded prototype needs numpy and scipy; under python -I "
            "install them on the isolated interpreter path (user-site is hidden)."
        ) from exc
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
