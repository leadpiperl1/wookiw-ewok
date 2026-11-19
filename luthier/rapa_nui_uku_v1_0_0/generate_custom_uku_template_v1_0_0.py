#!/usr/bin/env python3
"""
generate_custom_uku_template_v1_0_0.py
Parametric caliper-driven 1:1 shop SVG & Mersenne-Taylor tension sheet generator for profplum.
Once you measure your exact nut-to-Fret-6 span (--d06-mm), circular rabbet (--rabbet-mm),
clear cavity bore (--bore-mm), and nut width (--nut-mm) with calipers, run:
  python3 generate_custom_uku_template_v1_0_0.py --d06-mm 158.2 --rabbet-mm 140.0 --bore-mm 120.0 --nut-mm 47.5
and print the output HTML from Firefox/Chromium at 100% / Actual Size (US Letter).
"""

import argparse
import math

MM_TO_PT = 72.0 / 25.4
RHO_NYLON = 1140.0
RHO_PVDF = 1780.0
N_TO_LBF = 0.2248089431


def pt(mm: float) -> float:
    return mm * MM_TO_PT


def midi_hz(m: int) -> float:
    return 440.0 * (2.0 ** ((m - 69) / 12.0))


def build_custom_html(d06_mm: float, rabbet_mm: float, bore_mm: float, nut_mm: float, bridge_comp_mm: float) -> str:
    factor = 2.0 + math.sqrt(2.0)
    L_mm = d06_mm * factor
    L_m = L_mm * 1e-3
    saddle_mm = L_mm + bridge_comp_mm
    frets = [L_mm * (1.0 - 2.0 ** (-n / 12.0)) for n in range(1, 7)]

    vw, vh = pt(180.0), pt(195.0)
    cx, cy = 80.0, 96.0
    r_cut = rabbet_mm / 2.0
    r_bore = bore_mm / 2.0

    # Compute Schedule A & Schedule C dynamically at custom L_m
    def t_lbf(d_mm: float, rho: float, m: int) -> float:
        mu = rho * math.pi * ((d_mm * 1e-3) / 2.0) ** 2
        return 4.0 * mu * (L_m ** 2) * (midi_hz(m) ** 2) * N_TO_LBF

    rows_a = [
        ("4 (Top Pair)", "E4–E4", "Nylon 0.50 mm (25 lb)", 2 * t_lbf(0.50, RHO_NYLON, 64)),
        ("3 (Inner High)", "A4–A4", "Nylon 0.38 mm (15 lb)", 2 * t_lbf(0.38, RHO_NYLON, 69)),
        ("2 (Inner Mid)", "D4–D4", "Nylon 0.55 mm (30 lb)", 2 * t_lbf(0.55, RHO_NYLON, 62)),
        ("1 (Bot Pair)", "F#4–F#4", "Nylon 0.45 mm (20 lb)", 2 * t_lbf(0.45, RHO_NYLON, 66)),
    ]
    tot_a = sum(x[3] for x in rows_a)

    rows_c = [
        ("5 (Bass P4)", "A3", "PVDF 0.67 mm (45 lb)", t_lbf(0.67, RHO_PVDF, 57)),
        ("4 (Low-Mid P4)", "D4", "PVDF 0.50 mm (30 lb)", t_lbf(0.50, RHO_PVDF, 62)),
        ("3 (Center P4)", "G4", "PVDF 0.38 mm (17 lb)", t_lbf(0.38, RHO_PVDF, 67)),
        ("2 (Treble P4)", "C5", "Nylon 0.35 mm (12 lb)", t_lbf(0.35, RHO_NYLON, 72)),
        ("1 (High P4)", "F5", "Nylon 0.26 mm (8 lb)", t_lbf(0.26, RHO_NYLON, 77)),
    ]
    tot_c = sum(x[3] for x in rows_c)

    fret_str = " &middot; ".join(f"F{i}: <strong>{fv:.2f} mm</strong>" for i, fv in enumerate(frets, 1))
    tr_a = "".join(f"<tr><td>{c}</td><td>{n}</td><td>{g}</td><td style='text-align:right'>{v:.2f} lb</td></tr>" for c, n, g, v in rows_a)
    tr_c = "".join(f"<tr><td>{c}</td><td>{n}</td><td>{g}</td><td style='text-align:right'>{v:.2f} lb</td></tr>" for c, n, g, v in rows_c)

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Custom Rapa Nui Uku 1:1 Template (L = {L_mm:.1f} mm)</title>
<style>
  @page {{ size: letter portrait; margin: 12mm 15mm; }}
  body {{ font-family: 'DejaVu Sans', sans-serif; font-size: 10pt; color: #0f172a; margin: 0; }}
  h1 {{ font-size: 15pt; color: #1b365d; margin: 0 0 4px 0; }}
  .page-break {{ page-break-after: always; break-after: page; }}
  table {{ width: 100%; border-collapse: collapse; margin: 8px 0 14px 0; }}
  th, td {{ border-bottom: 1px solid #cbd5e1; padding: 5px 7px; text-align: left; }}
  th {{ background: #1b365d; color: #fff; }}
</style></head><body>
<div class="page-break">
  <h1>Custom Rapa Nui Uku 1:1 Shop Template (Ø {rabbet_mm:.1f} mm Cut / L = {L_mm:.1f} mm)</h1>
  <p style="margin:0 0 6px 0;">Print at <strong>100% / Actual Size</strong>. Verify 150.0 mm bar with calipers before cutting.</p>
  <svg width="180mm" height="195mm" viewBox="0 0 {vw:.3f} {vh:.3f}" xmlns="http://www.w3.org/2000/svg">
    <rect x="{pt(0.2):.2f}" y="{pt(0.2):.2f}" width="{pt(179.6):.2f}" height="{pt(194.6):.2f}" fill="none" stroke="#94a3b8" stroke-width="0.7"/>
    <line x1="{pt(15):.2f}" y1="{pt(9):.2f}" x2="{pt(165):.2f}" y2="{pt(9):.2f}" stroke="#0f172a" stroke-width="1.1"/>
    <line x1="{pt(15):.2f}" y1="{pt(9):.2f}" x2="{pt(15):.2f}" y2="{pt(13):.2f}" stroke="#0f172a" stroke-width="1.0"/>
    <line x1="{pt(165):.2f}" y1="{pt(9):.2f}" x2="{pt(165):.2f}" y2="{pt(13):.2f}" stroke="#0f172a" stroke-width="1.0"/>
    <text font-size="9" x="{pt(90):.2f}" y="{pt(6):.2f}" text-anchor="middle" font-weight="bold">150.0 mm Caliper Verification Bar</text>
    <circle cx="{pt(cx):.2f}" cy="{pt(cy):.2f}" r="{pt(r_cut):.3f}" fill="none" stroke="#0f172a" stroke-width="1.6"/>
    <circle cx="{pt(cx):.2f}" cy="{pt(cy):.2f}" r="{pt(r_bore):.3f}" fill="none" stroke="#b45309" stroke-width="1.2" stroke-dasharray="7 4"/>
    <rect x="{pt(cx-36):.2f}" y="{pt(cy+8):.2f}" width="{pt(72):.2f}" height="{pt(6):.2f}" fill="none" stroke="#1b365d" stroke-width="1.1"/>
    <text font-size="9.5" x="{pt(cx):.2f}" y="{pt(cy-6):.2f}" text-anchor="middle" font-weight="bold">Ø {rabbet_mm:.1f} mm Outer Cut / Ø {bore_mm:.1f} mm Clear Bore</text>
    <rect x="{pt(8):.2f}" y="{pt(178):.2f}" width="{pt(nut_mm):.3f}" height="{pt(5.5):.2f}" fill="none" stroke="#0f172a" stroke-width="1.3"/>
    <text font-size="8.8" x="{pt(8):.2f}" y="{pt(175.5):.2f}" font-weight="bold">1:1 Nut Blank ({nut_mm:.1f} × 5.5 mm)</text>
  </svg>
</div>
<h2>Calibrated Scale &amp; Mersenne-Taylor Tension Summary</h2>
<p><strong>Measured D<sub>0&rarr;6</sub>:</strong> {d06_mm:.2f} mm &rarr; <strong>Scale Length L:</strong> {L_mm:.2f} mm ({L_mm/25.4:.2f}&quot;) &rarr; <strong>Compensated Bridge Saddle:</strong> {saddle_mm:.2f} mm</p>
<p><strong>Ideal 12-TET Frets 1–6:</strong> {fret_str}</p>
<h3>Schedule A: Baritone-Tahitian 8-String (E4–A4–D4–F#4) — Total {tot_a:.2f} lb</h3>
<table><tr><th>Course</th><th>Pitch</th><th>Line Gauge</th><th style="text-align:right">Course Load</th></tr>{tr_a}</table>
<h3>Schedule C: Sovereign 5-String All-Fourths (A3–D4–G4–C5–F5) — Total {tot_c:.2f} lb</h3>
<table><tr><th>Course</th><th>Pitch</th><th>Line Gauge</th><th style="text-align:right">String Load</th></tr>{tr_c}</table>
</body></html>"""


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate custom 1:1 Rapa Nui uku shop template")
    ap.add_argument("--d06-mm", type=float, default=158.16, help="Measured nut-to-Fret-6 distance in mm")
    ap.add_argument("--rabbet-mm", type=float, default=140.0, help="Outer soundboard rabbet diameter in mm")
    ap.add_argument("--bore-mm", type=float, default=120.0, help="Inner clear cavity bore diameter in mm")
    ap.add_argument("--nut-mm", type=float, default=47.5, help="Nut width in mm")
    ap.add_argument("--comp-mm", type=float, default=1.8, help="Bridge saddle compensation in mm")
    ap.add_argument("--out", default="custom_rapa_nui_template.html", help="Output HTML path")
    args = ap.parse_args()
    html = build_custom_html(args.d06_mm, args.rabbet_mm, args.bore_mm, args.nut_mm, args.comp_mm)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"Wrote {args.out} (L = {args.d06_mm * (2 + math.sqrt(2)):.2f} mm)")


if __name__ == "__main__":
    main()
