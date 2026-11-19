#!/usr/bin/env python3
"""
verify_acoustic_swoopty_doo_v1_1_1.py
100% Pure Python 3 Standard Library Verification Harness (--seed 42, <= 60 s)
Uniting The Swoopty-Doo Theorem (v1.1.0), Mori-Zwanzig P + Q = I Reservoir Keyhole,
and Kembali Acoustic Waveguide on Rapa Nui / Tahitian 8-String Uku Harmonics.
Zero numpy/scipy/matplotlib dependencies; optional audio decode uses $HOME/.cache (never /tmp).
Author: Justin D. Grimm (ORCID: 0009-0000-5299-0243)
"""
import argparse
import cmath
import json
import math
import os
import random
import struct
import subprocess
import time

KB_SI = 1.380649e-23
T_ROOM_K = 300.0
E_LANDAUER_TRIT_J = KB_SI * T_ROOM_K * math.log(3.0)
V_KEYHOLE = 2.0 / 3.0
DS_MS = 86.5
FOWLER_NEUTRAL_BYTE = 121
KINTSUGI_WELD_BYTE = 251


def discrete_mutual_info(xs: list[int], ys: list[int]) -> float:
    n = len(xs)
    vx_set = sorted(set(xs))
    vy_set = sorted(set(ys))
    mi = 0.0
    for vx in vx_set:
        px = sum(1 for a in xs if a == vx) / n
        for vy in vy_set:
            py = sum(1 for b in ys if b == vy) / n
            pxy = sum(1 for a, b in zip(xs, ys) if a == vx and b == vy) / n
            if pxy > 0.0 and px > 0.0 and py > 0.0:
                mi += pxy * math.log2(pxy / (px * py))
    return mi


def goertzel_power(samples: list[float], sr: int, target_hz: float) -> float:
    n = len(samples)
    k = round((n * target_hz) / sr)
    omega = (2.0 * math.pi * k) / n
    coeff = 2.0 * math.cos(omega)
    s0 = s1 = s2 = 0.0
    for x in samples:
        s0 = x + coeff * s1 - s2
        s2 = s1
        s1 = s0
    return (s1 * s1 + s2 * s2 - coeff * s1 * s2) / (n * n)


def solve_linear_system(a_mat: list[list[float]], b_mat: list[list[float]]) -> list[list[float]]:
    """Pure-stdlib Gauss-Jordan solver with partial pivoting for small ridge regression."""
    n = len(a_mat)
    m = len(b_mat[0])
    aug = [list(a_mat[i]) + list(b_mat[i]) for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(aug[r][col]))
        aug[col], aug[piv] = aug[piv], aug[col]
        div = aug[col][col]
        for j in range(col, n + m):
            aug[col][j] /= div
        for r in range(n):
            if r != col:
                fac = aug[r][col]
                if fac != 0.0:
                    for j in range(col, n + m):
                        aug[r][j] -= fac * aug[col][j]
    return [row[n:] for row in aug]


def run_verification(audio_path: str | None = None, seed: int = 42) -> dict:
    t0 = time.perf_counter()
    rng = random.Random(seed)

    # Gate 1: Exact First-Law Cushion Identity & Octave Keyhole (r = 2 -> eta* = 2/3)
    max_first_law_res = 0.0
    for _ in range(1000):
        r = rng.uniform(1.05, 3.50)
        eta = rng.uniform(0.0, 1.0)
        alpha = eta / (r * r) + (1.0 - eta)
        t_e = 0.5 * (alpha + 1.0 / r)
        r_e = 0.5 * (alpha - 1.0 / r)
        u_p_plus = (r * r) * (t_e * t_e + r_e * r_e)
        u_q_minus = 0.5 * (r * r - 1.0) * ((1.0 - eta) ** 2)
        du_joule = 0.5 * ((r * r - 1.0) / (r * r)) * (eta ** 2)
        res = abs((u_p_plus + du_joule) - (1.0 + u_q_minus))
        max_first_law_res = max(max_first_law_res, res)
    assert max_first_law_res < 1e-13
    r_oct = 2.0
    eta_star_oct = r_oct / (1.0 + r_oct)
    assert abs(eta_star_oct - V_KEYHOLE) < 1e-15

    # Gate 2: Synthesize or decode ($HOME/.cache, never /tmp) 8 kHz acoustic harmonic trajectory
    sr = 8000
    dur = 24.0
    source_name = "SYNTHETIC_BENCHTOP_STDLIB"
    if audio_path and os.path.isfile(audio_path):
        cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "wookiw_ewok_v5_1_0")
        os.makedirs(cache_dir, exist_ok=True)
        pcm_file = os.path.join(cache_dir, "uke_8k.f32")
        subprocess.run(
            ["ffmpeg", "-y", "-vn", "-i", audio_path, "-ac", "1", "-ar", str(sr), "-f", "f32le", pcm_file],
            capture_output=True, check=True
        )
        raw = open(pcm_file, "rb").read()
        cnt = len(raw) // 4
        y = list(struct.unpack(f"<{cnt}f", raw[: cnt * 4]))
        source_name = os.path.basename(audio_path)
    else:
        n_samp = int(dur * sr)
        y = [rng.gauss(0.0, 0.012) for _ in range(n_samp)]
        # Triadic chord sequence (-1 Bm7, 0 Dmaj7/F#m, +1 Amaj7/C#m7) + modal turnaround seams
        chords = [
            [246.94, 293.66, 369.99, 440.00],  # -1 Blue
            [293.66, 369.99, 440.00, 554.37],  #  0 Green
            [220.00, 277.18, 329.63, 415.30],  # +1 Red
        ]
        tau_body = 0.68  # Solid-wood uku body Q-reservoir carryover across 0.5 s windows
        strum_dt = 0.260  # ~3 DS = 259.5 ms human cadence!
        for k_strum in range(int((dur - 1.5) / strum_dt)):
            t_s = 1.0 + k_strum * strum_dt
            c_idx = (k_strum // 4) % 3
            turnaround = (k_strum % 12 == 11)
            freqs = [392.00, 523.25, 329.63, 440.00] if turnaround else chords[c_idx]
            i0 = int(t_s * sr)
            i1 = min(n_samp, int((t_s + 1.5) * sr))
            omegas = [2.0 * math.pi * f0 / sr for f0 in freqs]
            om_e = 2.0 * math.pi * 329.39 / sr
            om_a = 2.0 * math.pi * 438.79 / sr
            for idx in range(i0, i1):
                dn = idx - i0
                tt = dn / sr
                env = (1.0 - math.exp(-tt / 0.006)) * math.exp(-tt / tau_body)
                s_val = 0.18 * sum(math.sin(om * dn) for om in omegas)
                drone = 0.12 * math.sin(om_a * dn) + 0.08 * math.sin(om_e * dn)
                y[idx] += env * (s_val + drone)

    # Gate 1B: 20 ms frame SNR gate (+6 dB survival) & Barker-13 correlation
    flen = int(0.020 * sr)
    n_fr = len(y) // flen
    db_frames = []
    for k in range(n_fr):
        seg = y[k * flen : (k + 1) * flen]
        rms = math.sqrt(sum(v * v for v in seg) / flen + 1e-18)
        db_frames.append(20.0 * math.log10(rms))
    sorted_db = sorted(db_frames)
    n0_db = sorted_db[max(0, int(0.05 * len(sorted_db)))]
    pct_above_6db = sum(1 for d in db_frames if (d - n0_db) >= 6.0) * 100.0 / len(db_frames)
    assert pct_above_6db > 50.0, f"Failed +6 dB survival gate: {pct_above_6db:.2f}%"

    # Gate 3 & 4: 0.50 s Pitch-Class Chroma Trajectory, Swoopty-Doo ISI & Kelvin Ridge Decoder
    pc_freqs = [261.63 * (2.0 ** (pc / 12.0)) for pc in range(12)]
    win_samp = int(0.50 * sr)
    n_win = (len(y) - 2 * sr) // win_samp
    chroma_seq = []
    p_tot = 0.0
    q_tot = 0.0
    q_pcs = {4, 9}
    p_pcs = {0, 1, 2, 6, 7, 8, 11}

    for w in range(n_win):
        i0 = sr + w * win_samp
        seg = y[i0 : i0 + win_samp]
        c = [goertzel_power(seg, sr, f_pc) + goertzel_power(seg, sr, 2.0 * f_pc) for f_pc in pc_freqs]
        q_tot += sum(c[pc] for pc in q_pcs)
        p_tot += sum(c[pc] for pc in p_pcs)
        cnorm = math.sqrt(sum(v * v for v in c)) + 1e-18
        chroma_seq.append([v / cnorm for v in c])

    def unit12(pairs: list[tuple[int, float]]) -> list[float]:
        v = [0.0] * 12
        for idx, wt in pairs:
            v[idx] = wt
        nm = math.sqrt(sum(x * x for x in v))
        return [x / nm for x in v]

    t_m1 = unit12([(11, 0.62), (6, 0.58), (2, 0.35)])
    t_0  = unit12([(2, 0.45), (6, 0.55), (9, 0.52), (1, 0.47)])
    t_p1 = unit12([(9, 0.55), (1, 0.50), (4, 0.45), (8, 0.49)])
    tmpls = [t_m1, t_0, t_p1]

    trits = []
    scores = []
    for c in chroma_seq:
        sc = [sum(c[j] * tm[j] for j in range(12)) for tm in tmpls]
        scores.append(sc)
        best = max(range(3), key=lambda idx: sc[idx])
        trits.append(best - 1)

    dchroma = []
    for k in range(len(chroma_seq)):
        km = max(0, k - 1)
        kp = min(len(chroma_seq) - 1, k + 1)
        dt_w = 0.50 * max(1, kp - km)
        dchroma.append([(chroma_seq[kp][j] - chroma_seq[km][j]) / dt_w for j in range(12)])

    excl_pc = {-1: 11, 0: 6, 1: 8}
    isi_ratios = []
    kintsugi_seams = 0
    for k in range(1, len(trits) - 1):
        dot_c = max(-1.0, min(1.0, sum(chroma_seq[k - 1][j] * chroma_seq[k][j] for j in range(12))))
        ang = math.degrees(math.acos(dot_c))
        if ang >= 10.0 and (chroma_seq[k][7] + chroma_seq[k][0]) > 0.22:
            kintsugi_seams += 1
        if trits[k] != trits[k - 1]:
            pc_prev = excl_pc[trits[k - 1]]
            if chroma_seq[k - 1][pc_prev] > 0.12:
                isi_ratios.append(min(1.0, chroma_seq[k][pc_prev] / chroma_seq[k - 1][pc_prev]))
    eta_isi = sum(isi_ratios) / max(1, len(isi_ratios))
    assert eta_isi > 0.15, f"Expected non-zero acoustic ISI carryover, got {eta_isi}"

    proj_pos = [sc[2] - sc[0] for sc in scores]
    proj_vel = [sum(dc[j] * (t_p1[j] - t_m1[j]) for j in range(12)) for dc in dchroma]
    sp = sorted(proj_pos)
    sv = sorted(proj_vel)
    qp1, qp2 = sp[len(sp) // 3], sp[(2 * len(sp)) // 3]
    qv1, qv2 = sv[len(sv) // 3], sv[(2 * len(sv)) // 3]
    phase_code = [
        (0 if p < qp1 else (1 if p < qp2 else 2)) * 3 + (0 if v < qv1 else (1 if v < qv2 else 2))
        for p, v in zip(proj_pos, proj_vel)
    ]
    mi_past = discrete_mutual_info(trits[:-1], phase_code[1:])
    mi_future = discrete_mutual_info(trits[1:], phase_code[:-1])
    assert mi_past > 0.05 and mi_future > 0.05

    # Lord Kelvin phase-space linear ridge decoder (25 features)
    feats = [chroma_seq[k] + dchroma[k] + [1.0] for k in range(1, len(trits) - 1)]
    dim = 25
    xtx = [[sum(feats[r][i] * feats[r][j] for r in range(len(feats))) + (0.01 if i == j else 0.0) for j in range(dim)] for i in range(dim)]
    y_prev_oh = [[1.0 if (trits[r] + 1) == c else 0.0 for c in range(3)] for r in range(len(feats))]
    xty = [[sum(feats[r][i] * y_prev_oh[r][c] for r in range(len(feats))) for c in range(3)] for i in range(dim)]
    w_prev = solve_linear_system(xtx, xty)
    correct_prev = 0
    for r, fv in enumerate(feats):
        pred = max(range(3), key=lambda c: sum(fv[i] * w_prev[i][c] for i in range(dim))) - 1
        if pred == trits[r]:
            correct_prev += 1
    acc_prev = correct_prev * 100.0 / len(feats)

    rho_act = p_tot / (p_tot + q_tot + 1e-18)
    elapsed_s = time.perf_counter() - t0
    assert elapsed_s <= 60.0

    return {
        "artifact": "verify_acoustic_swoopty_doo_v1_1_1.py",
        "version": "1.1.1-stdlib",
        "seed": seed,
        "source_audio": source_name,
        "pct_above_6db_gate": round(pct_above_6db, 2),
        "max_first_law_residual": max_first_law_res,
        "octave_keyhole_eta_star": round(eta_star_oct, 6),
        "swoopty_isi_carryover_eta": round(eta_isi, 4),
        "mi_past_bits": round(mi_past, 4),
        "mi_future_bits": round(mi_future, 4),
        "kelvin_prev_state_acc_pct": round(acc_prev, 2),
        "mori_zwanzig_rho_act_P": round(rho_act, 4),
        "kintsugi_seams": kintsugi_seams,
        "runtime_s": round(elapsed_s, 4),
        "status": "ALL_4_GATES_PASSED",
        "exit_state": "CODE_SHOKUNIN_UNLATCHED = 255",
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", type=str, default=None)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    print(json.dumps(run_verification(args.audio, args.seed), indent=2))
