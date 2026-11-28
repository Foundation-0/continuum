"""Zero-shared-code checks of headline identities claimed in PR #3.

Nothing here imports repository code. Each check re-derives a claimed
identity from its statement in the synthesis and double-slit reports,
in exact rational arithmetic. Exit code 0 means every check passed.

Run under: python3 -I -B, python3 -I -O -B, python3 -I -B -W error.
No bare asserts: failures raise SystemExit with the failing witness.
"""
from fractions import Fraction as F
import random
import sys


def require(cond, witness):
    if not cond:
        raise SystemExit(f"FAIL: {witness}")


def check_mobius_cross_ratio():
    def q(p, r, c):
        return (r * p + c * (1 - p)) / (r * p + (1 - p))

    def cr(a, b, c, d):
        return ((c - a) * (d - b)) / ((c - b) * (d - a))

    ps = [F(1, 4), F(1, 2), F(3, 4), F(1)]
    base = cr(*ps)
    for r, c in [(F(6), F(1, 4)), (F(6), F(1, 2)), (F(6), F(3, 4)),
                 (F(37, 5), F(2, 11)), (F(3), F(9, 10))]:
        qs = [q(p, r, c) for p in ps]
        require(cr(*qs) == base, f"cross-ratio moved at r={r} c={c}")
        require(q(F(1), r, c) == 1, f"fixed point lost at r={r} c={c}")

    def q_nonmobius(p, c):
        r = 6 + 10 * p
        return (r * p + c * (1 - p)) / (r * p + (1 - p))

    got = cr(*[q_nonmobius(p, F(1, 2)) for p in ps])
    require(got != base, f"non-Mobius control failed to break invariance: {got}")
    print("mobius cross-ratio cancellation: OK")


def check_two_loop():
    def dot(a, b):
        return sum(x * y for x, y in zip(a, b))

    def orthobasis(vecs):
        out = []
        for v in vecs:
            r = list(v)
            for b in out:
                k = dot(r, b) / dot(b, b)
                r = [x - k * y for x, y in zip(r, b)]
            if dot(r, r) != 0:
                out.append(r)
        return out

    def residual(v, ob):
        r = list(v)
        for b in ob:
            k = dot(r, b) / dot(b, b)
            r = [x - k * y for x, y in zip(r, b)]
        return r

    rng = random.Random(20261122)
    trials = boundary = 0
    for _ in range(400):
        n = 5
        phi = [[F(rng.randint(-4, 4)) for _ in range(n)] for _ in range(2)]
        ob = orthobasis(phi)
        if len(ob) < 2:
            continue
        y = [F(rng.randint(-5, 5)) for _ in range(n)]
        a1 = [F(rng.randint(-4, 4)) for _ in range(n)]
        a2 = [F(rng.randint(-4, 4)) for _ in range(n)]
        r_star = residual(y, ob)
        a1_res = residual(a1, ob)
        p1 = [x - z for x, z in zip(a1, a1_res)]
        e1, p1n = dot(a1, r_star), dot(p1, p1)
        if e1 == 0 or p1n == 0:
            continue
        k = e1 / p1n
        r_ad = [x - k * z for x, z in zip(r_star, p1)]
        require(dot(a1, r_ad) == 0, "silencing construction failed")
        require(dot(r_ad, r_ad) == dot(r_star, r_star) + e1 * e1 / p1n,
                "Pythagorean inflation identity failed")
        trials += 1
        e2 = dot(a2, r_star)
        if e2 == 0:
            continue
        rho, kappa = dot(p1, a2) / p1n, e2 / e1
        lhs, rhs = dot(a2, r_ad), e2 * (1 - rho / kappa)
        require(lhs == rhs, "fresh-anchor identity failed")
        require((abs(lhs) < abs(e2)) == (F(0) < rho / kappa < F(2)),
                "phase boundary iff failed")
        boundary += 1
    require(trials > 300 and boundary > 300, f"too few trials: {trials}/{boundary}")
    print(f"two-loop Pythagoras and boundary: OK ({trials} trials)")


def check_fold_curves_and_hadamard():
    for k in [F(1, 3), F(1, 2), F(3, 4), F(2), F(-1, 4)]:
        a = 4 * k / (2 * k * k + 1)
        t = (2 * k * k - 1) / (2 * k * k + 1)
        require(a * a + 2 * t * t == 2, f"Fn->Dn curve failed at k={k}")
    for m in [F(-1, 4), F(1, 4), F(0), F(1, 3), F(2, 5)]:
        a = (1 - 4 * m) / (2 * m * m - m + 1)
        t = (1 - 2 * m * m) / (2 * m * m - m + 1)
        require(a * a - a * t + 2 * t * t == 2, f"F8->E8 curve failed at m={m}")

    h = [[1]]
    while len(h) < 8:
        h = [row + row for row in h] + [row + [-x for x in row] for row in h]

    def matmul(a, b):
        return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
                 for j in range(len(b[0]))] for i in range(len(a))]

    h2 = matmul(h, h)
    require(all(h2[i][j] == (8 if i == j else 0) for i in range(8) for j in range(8)),
            "H8^2 != 8I")
    require(sum(h[i][i] for i in range(8)) == 0, "trace H8 != 0, no 4/4 split")
    print("fold curves and Hadamard stress split: OK")


def check_bregman_cone():
    def d(p, q):  # generator phi(t) = t^3 / 3, per coordinate
        return sum((F(a) ** 3 - F(b) ** 3 - 3 * F(b) ** 2 * (F(a) - F(b))) / 3
                   for a, b in zip(p, q))

    q_star, q_adapt, p = (3, 4, 5), (5, 12, 13), (4, 5, 4)
    require(d(p, q_adapt) == F(3865, 3), f"D(p||q_adapt) = {d(p, q_adapt)}")
    require(d(p, q_star) == F(37, 3), f"D(p||q*) = {d(p, q_star)}")
    require(d(q_star, q_adapt) == 1276, f"D(q*||q_adapt) = {d(q_star, q_adapt)}")
    require(d(p, q_adapt) == d(p, q_star) + d(q_star, q_adapt), "Pythagoras failed")
    print("cubic Bregman cone [3,4,5]->[5,12,13]: OK")


if __name__ == "__main__":
    check_mobius_cross_ratio()
    check_two_loop()
    check_fold_curves_and_hadamard()
    check_bregman_cone()
    print("all independent exact checks passed")
    sys.exit(0)
