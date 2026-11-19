# Rapa Nui & Tahitian Ukulele Luthier Bundle (`v1.0.0`)

- **Author:** Justin D. Grimm (`ORCID: 0009-0000-5299-0243`) — Independent Dandelion Substrate Research Group, Gurley, Alabama 35748, USA
- **Workspace Commons Targets:** `013_Die LebeSongen` & `001_Dandelion OS Documentation & Specs`

## Contents
1. `rapa_nui_uku_shop_template_v1.0.0.pdf` — Print-ready 4-page US Letter `1:1` shop cut/slot/drill template & Mersenne-Taylor string-tension schedules (print Page 1 at **100% / Actual Size**).
2. `rapa_nui_tahitian_uku_1027_v1.0.0.jpg` — Primary forensic bench calibration photograph (`1027.jpg`, Rapa Nui 10-peg carved Moai/Tiki uku left vs. Tahitian 8-string ukulele right).
3. `verify_rapa_nui_uku_luthier_v1_0_0.py` — Zero-dependency Python 3 verification suite (`--seed 42`, `< 50 ms`) verifying all 4 photogrammetric, `(2 + sqrt(2))` octave-bisection, PVDF/Nylon Mersenne-Taylor, and `AUD-TRK-09` Acoustic Swoopty-Doo alignment gates.
4. `generate_custom_uku_template_v1_0_0.py` — Parametric CLI generator for `profplum`: enter your exact caliper readings (`--d06-mm`, `--rabbet-mm`, `--bore-mm`, `--nut-mm`) to emit a custom `1:1` printable SVG/HTML template and recalculated tension table.
5. `audit_manifest_v1.0.0.json` — Deterministic verification receipt (`ALL_4_GATES_PASSED = true`).

## Quick-Start on `profplum`
```bash
unzip -o rapa_nui_uku_luthier_bundle_v1.0.0.zip -d ~/dandelion_workspace/rapa_nui_uku_v1_0_0
cd ~/dandelion_workspace/rapa_nui_uku_v1_0_0
python3 verify_rapa_nui_uku_luthier_v1_0_0.py --seed 42

# Regenerate with exact bench caliper measurements:
python3 generate_custom_uku_template_v1_0_0.py --d06-mm 158.5 --rabbet-mm 139.0 --bore-mm 120.0 --nut-mm 47.5 --out bench_exact_template.html
```
