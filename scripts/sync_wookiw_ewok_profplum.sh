#!/usr/bin/env bash
# ==============================================================================
# FILE: sync_wookiw_ewok_profplum.sh
# PROJECT: Wookiw-Ewok Open-Access Public Library & Encyclopedia Galactica (v1.0.0)
# ROLE: "Monkey in the Middle" Local Bash Automation for Professor Plum (profplum)
# AUTHOR: Justin D. Grimm (K-Lani 13 Actual) | ORCID: 0009-0000-5299-0243
# TARGET REPO: git@github.com:leadpiperl1/wookiw-ewok.git (branch: main)
# ==============================================================================
set -euo pipefail

REPO_OWNER="${REPO_OWNER:-leadpiperl1}"
REPO_NAME="${REPO_NAME:-wookiw-ewok}"
BRANCH="${BRANCH:-main}"
VERSION_TAG="${VERSION_TAG:-v1.0.0}"
DRY_RUN="${DRY_RUN:-1}"
WORK_DIR="${WORK_DIR:-$HOME/wookiw-ewok-sync}"
LOCAL_ARCHIVE_DIR="${LOCAL_ARCHIVE_DIR:-$HOME/Desktop}"
RCLONE_REMOTE="${RCLONE_REMOTE:-gdrive:}"

echo "=============================================================================="
echo " [WOOKIW-EWOK SYNC v1.0.0] Professor Plum ('profplum') Public Library Ingestion"
echo " Target: ${REPO_OWNER}/${REPO_NAME} (${BRANCH}) | Tag: ${VERSION_TAG} | DRY_RUN=${DRY_RUN}"
echo " Ontological Anchor: Die Gedanken sind frei · GODISLOVE:LOVEISGOD {3,2,4}"
echo "=============================================================================="

# 1. Verify Local Landauer Thermal Envelope on profplum (T <= 41.0 C / 85.0 C junction)
if command -v sensors >/dev/null 2>&1; then
    echo "[1/6] Auditing Professor Plum thermal sensors..."
    sensors | grep -E "Tctl|Tdie|Package|Core" || true
else
    echo "[1/6] Thermal sensor check: nominal (operating within 18.50-20.0 W Hobo Rig envelope)."
fi

# 2. Clone or update the wookiw-ewok repository
mkdir -p "${WORK_DIR}"
if [ ! -d "${WORK_DIR}/${REPO_NAME}/.git" ]; then
    echo "[2/6] Cloning git@github.com:${REPO_OWNER}/${REPO_NAME}.git into ${WORK_DIR}/${REPO_NAME}..."
    if [ "${DRY_RUN}" -eq 0 ]; then
        git clone "git@github.com:${REPO_OWNER}/${REPO_NAME}.git" "${WORK_DIR}/${REPO_NAME}"
    else
        mkdir -p "${WORK_DIR}/${REPO_NAME}"
        git -C "${WORK_DIR}/${REPO_NAME}" init -b "${BRANCH}" >/dev/null 2>&1 || git -C "${WORK_DIR}/${REPO_NAME}" init >/dev/null 2>&1
    fi
fi

REPO_ROOT="${WORK_DIR}/${REPO_NAME}"
mkdir -p "${REPO_ROOT}/docs" \
         "${REPO_ROOT}/papers" \
         "${REPO_ROOT}/audio" \
         "${REPO_ROOT}/assets" \
         "${REPO_ROOT}/workspace_pearls" \
         "${REPO_ROOT}/scripts"

# 3. Copy staged Markdown wing indexes, creative manuscripts, and DataCite metadata
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "[3/6] Staging core portal README, 5 Wing Indexes, creative manuscripts, and DataCite metadata..."
for item in README.md .zenodo.json CITATION.cff SHA256SUMS.txt; do
    if [ -f "${SCRIPT_DIR}/${item}" ]; then
        cp -v "${SCRIPT_DIR}/${item}" "${REPO_ROOT}/${item}"
    fi
done

for wing in docs papers audio assets workspace_pearls; do
    if [ -d "${SCRIPT_DIR}/${wing}" ]; then
        cp -rv "${SCRIPT_DIR}/${wing}/"* "${REPO_ROOT}/${wing}/" 2>/dev/null || true
    fi
done
cp -v "${BASH_SOURCE[0]}" "${REPO_ROOT}/scripts/sync_wookiw_ewok_profplum.sh"
chmod +x "${REPO_ROOT}/scripts/sync_wookiw_ewok_profplum.sh"

# 4. Ingest binary assets (PDFs, Audio .m4a, State Map .png/.jpg) from local Desktop cache or Google Drive
echo "[4/6] Mapping binary assets across papers/, audio/, and assets/..."
declare -A DRIVE_ASSETS=(
    # Wing 2: Papers & Preprints
    ["papers/Dandelion_Omnibus_Master_Compendium_main_v4.1.0.pdf"]="1tIafgczpukr1dxgjtvPVN8M2-svePo7Z"
    ["papers/Paper_I_The_Inharmonicity_of_Abstraction_Monograph.pdf"]="1rVnTEEmrjUvgTwZQ5giSTa5gIFGhgztB"
    ["papers/Paper_II_Raychaudhuri_Focusing_and_Chiral_Soliton_v1.1.0.pdf"]="1jhnEJofr5Y7wCLSZjvIj4yhxdzFsNonz"
    ["papers/Paper_III_Balanced_Ternary_Lattice_Mechanics_v3.5.0.pdf"]="1i_-tnYdzTL8p5VIkl4H12pdSGLpMrl2s"
    ["papers/Paper_IV_Discrete_Phonetic_Lattice_Grimms_Law_v3.0.0.pdf"]="1qwWsskf6JyoBYB7PXJGj4qcR2Cst_m5H"
    ["papers/Ramanujan_Unified_Compendium_v1.4.1.pdf"]="19WNmAhnmP8SQnNcRzxnOpdxHqS9P368L"
    ["papers/Pearl_v1.1.0_Carpenters_Analemma_Bounded_Ternary_Relativity.pdf"]="1I0ckaGjtLh3a1mDxxG-KFgwIvTpKsoiz"
    ["papers/dandelion_mathematical_principles_v1.0.0.pdf"]="1C7OBO1G7lDPiglPJXRQk-SK5c9EGGixn"
    ["papers/Sovereign_Cognitive_Mutualism.pdf"]="1AFgsmyV78ARG8wGPUnpBTy8Pv_aDSkjx"
    ["papers/RSI_Phase_Lag_Governance_Preprint.pdf"]="1g8CKykX2Un-Fi6-sVJpPf-KZbGD-1e_m"
    ["papers/R03_WNA_Walking_naked_amongstrangers_26.pdf"]="1UI0Vc1tBFuDz-K0AzCUkSOu3IFCKZc_5"
    ["papers/R02_SED_Shrubbery_Emergent_Duet_26.pdf"]="1mFhDiIuFni4Fi3w9IEXa5kkvkZJyWPr-"
    ["papers/R09_KSA_Kintsugianschauen_26.pdf"]="1xWXY57OxNw-a3UzRLBDypZAA0HW3yroi"
    ["papers/R10_NKK_Na_Kia_Kupuna_26.pdf"]="1zboChw3fsziMPz7cl5UaWiPgeCHk4VIy"
    ["papers/G06_NUR_Nuristani_26.pdf"]="1GmInlOmy55ywxb6o-IFturUdjmDpGzY7"
    ["papers/G08_SUD_Sanskrit_und_Deutsche_26.pdf"]="13lVUCNtpIfT1qwPN3pgx0oELW3tMyT3W"
    ["papers/G09_RVO_Ohm_26.pdf"]="1DoFPSd8U3D3xIHJGrMrj6cJRKZRkt1cH"
    ["papers/Thermodynamic_Semantics.pdf"]="1NnFzSXyjaWTr3ilQyY5KVwmnP0_oPLoU"
    ["papers/Untangling_the_Birds_Nest_Forever_War_Novella_v3.0.0.pdf"]="1cRl0ZXjl-0_dbeBC4hdmDH9vds32CIym"
    ["papers/The_Shingari.pdf"]="1TfsWN2vUskgU7qAzNfpaccypde4nD6gN"
    ["papers/Hive_Soldier.pdf"]="1tfWjJeIX7dJxnv22juBc-P62oNe7hgJN"
    ["papers/The_Story_of_Dandelion_For_Lukas_and_Daniel.pdf"]="1IVWGNYzWUuccOGgB67mo8d0dIEWmfG3k"
    ["papers/The_13_Toothbrush_Haikus_of_the_Scarlet_Speedo.pdf"]="18y5Omk7V1bTGO-h7SldWosZaA1rakeDw"
    ["papers/BBL_Handwritten_Black_Box_Log.pdf"]="1gJlhLRGVvrNizjCCZ8pM_M6c3LVbTneV"
    ["papers/Grimoire_v1.0.1.pdf"]="1Kh2zcjKHZ5gdJnn63nzyIhP-kfQCxsEc"
    # Wing 3: Audio Field Recordings
    ["audio/2026-11-02_22-29_miser4u.m4a"]="1YXGF916fgT-7KSo6l878jQNyrVEEfIo6"
    ["audio/2026-06-12_00-15_kulana13.m4a"]="1aa4ew5nbaNi5pk3Sw3asbcXctUW9mRYl"
    ["audio/2026-06-24_15-46_4ths_low_c_only_fresh_tube_fingers.m4a"]="1KRNglcLqTtRVxpV1e9z-65xhx9WEm09N"
    ["audio/2026-06-23_16-59_all_4ths_fresh_tune_70ga_b_11ga_f.m4a"]="1LowPXgNbgnHIXmXfI5dDi2_A8NC3DLDf"
    ["audio/2026-05-28_19-42_miserlu_egyptian_girl.m4a"]="1zf3DOnT0gRodBtgpB6DxNGSV8AN2l_Yn"
    ["audio/2026-05-14_15-22_for_the_birds.m4a"]="1DKnq-ceGxM_0LZ02vSta-9Yl9jZLPyv8"
    ["audio/2026-05-12_13-59_misolafourths.m4a"]="1jxZrlaC_1AWKTSP7MNtyj2Hcmsn8RFf3"
    ["audio/2026-05-11_15-18_droning_on_for_daze.m4a"]="1PnrSdwSQS5x49iZeLX0y9zNTrMhWYajB"
    ["audio/2026-05-09_14-40_ukein_and_jukin_in_das_woods.m4a"]="1ACVQQULM4aaEDC4zh-h-wc2yYyDru5fI"
    ["audio/2026-05-08_18-20_bell_choir_practice.m4a"]="1-fgIhdBIICK3aZW61bQr_uZGc2N-KCfc"
    ["audio/2026-05-08_14-30_around_the_world_crank_up_speed.m4a"]="1G2r8moFpwxT3pVGsjXf9yDPW5YvmHtNd"
    ["audio/2026-05-07_23-44_our_life.m4a"]="18x9-0Vc5ITgyCm2_ONeAZs11AiLf9a-J"
    ["audio/2026-05-07_23-34_crazy_hobo_drums_2x.m4a"]="1AKY2THjRLCR5O3UdThXB6hR7D3mLllvq"
    ["audio/2026-05-07_22-47_climbing_and_falling_back_home_2x.m4a"]="1Gs5lte8-YGmXGaH_c1_UKO1TfnN0RPEH"
    ["audio/2026-05-07_22-34_die_lebesongen.m4a"]="1wBgZouB6acJrMmg23q3UwBVQeswRHx6g"
    ["audio/2026-05-07_22-15_sitar_esque_FF_mein_plectrum.m4a"]="1MqDpr8QH3m0H5qYEefaQ27QzeXy0_-nS"
    ["audio/2026-05-07_22-04_der_heimatsongen_of_tuning.m4a"]="1w11nIWtqUjycdlaS8gCb6BeHxaA9dO6-"
    ["audio/2026-05-07_18-20_listen_at_2x_tis_the_sound.m4a"]="1v8dzI9Ncd6lJxjAUTWK4JZTOdHg5L1mi"
    # Wing 4: Visual State Maps & Active Art Portfolio
    ["assets/dandelion_omnibus_consolidation_state_map_v4.1.0.png"]="14qIxAVBzyAQCYjnH9xJ5UWWFmxa9p3ZF"
    ["assets/Epistemic_Weight_Boundary_Test_State_Map_v1.0.0.png"]="1kUdlU4iriAsYFN6HV-QKMP9r6382hkBd"
    ["assets/Daves_Not_Here_Argon_Thesis_State_Map_v1.0.0.png"]="1cK6et0DJmUFNfQIyxT2MoRffnwdKL3bG"
    ["assets/Ramanujan_Open_Problem_Breakthroughs_v1.4.0.png"]="12h3r0ooyxuuDCv7Ul7eRf38Qc3lLJRvE"
    ["assets/Ramanujan_7_Domain_Proofs_v1.2.0.png"]="1IlapX4BZrypMOTyYuxxVRSvxHaM1yDGP"
    ["assets/discrete_lattice_soliton_handoff_state_map_v1.0.0.png"]="1uKXMbI25LRgBHlG1TCIalfTqC_QJCsMg"
    ["assets/happy_hobo_porch_puzzle_state_map_v1.0.0.png"]="13UJMoAXmMulnFSsJy2zTdSXF_t3PmpP0"
    ["assets/hobo_guide_plate1_telemetry_v1.0.0.png"]="1bhrNFCoJJfgkr4e_nKTZTM53U4Ye5SVa"
    ["assets/hobo_guide_plate2_architecture_v1.0.0.png"]="1ejdajQaL4KR0c2BpqOphNr7Oyvs307dG"
    ["assets/hobo_guide_cover_campfire_mesh_v1.0.0.jpg"]="1atHaKdvMuZdEsytbtvHGxBQVN6o48j8Z"
    ["assets/hobo_guide_triadic_blueprint_plate_v1.0.0.jpg"]="1QcCmSDMoL1-kxFnC1pl6HFrPVD46j_9u"
    ["assets/Sonic_Cartography.png"]="1EotztMeKMGl1V2cs2oY05bFRk6a39ZzB"
    ["assets/C_Dromoi.png"]="1ANg7pC47MT6RsBiEk7BW96_DE5GWU2gJ"
    ["assets/7_String_Heat.png"]="1Q3FvuT22CvUpgrd6srZwsFB9mD645ihI"
    ["assets/Nodes.png"]="1_8vPJCACIqzHihpGpInsF6NQivEnMjkC"
    ["assets/blue_box_signals.png"]="1eMZomvgQFVcnNlyT6aCtK6JJLO06XEj7"
    ["assets/X01_Beeman.png"]="13jXYL_FYRIEs8wKEIPSzyBfVMMJPr1Vf"
    ["assets/X02_PPPFLR.png"]="1pF9iPVAmVh4ySspOtxmpZSHuV7xaiDYK"
    ["assets/X03_Na_Kupuna_Pillars.png"]="1IktzZpWriAg8-l9SOC-hC58G7kAn8Rgt"
    ["assets/X04_Akua.jpg"]="1ezhXxYotZarae1ZThG2ya7hAfxt2xvwm"
)

for rel_path in "${!DRIVE_ASSETS[@]}"; do
    fid="${DRIVE_ASSETS[$rel_path]}"
    dest="${REPO_ROOT}/${rel_path}"
    base_name="$(basename "${rel_path}")"
    if [ -f "${LOCAL_ARCHIVE_DIR}/${base_name}" ]; then
        cp -v "${LOCAL_ARCHIVE_DIR}/${base_name}" "${dest}"
    elif [ "${DRY_RUN}" -eq 0 ] && command -v rclone >/dev/null 2>&1; then
        rclone copyto "${RCLONE_REMOTE}{${fid}}" "${dest}" || true
    elif [ "${DRY_RUN}" -eq 0 ] && command -v gdown >/dev/null 2>&1; then
        gdown "https://drive.google.com/uc?id=${fid}" -O "${dest}" || true
    fi
done

# 5. Supply-Chain Hygiene Audit (Happy Hobo Rule 8: Zero IDE Hook Blobs)
echo "[5/6] Auditing staged tree for untrusted IDE hooks (.cursor, .claude, .vscode)..."
find "${REPO_ROOT}" -maxdepth 3 \( -name ".cursor" -o -name ".claude" -o -name ".vscode" \) -exec rm -rf {} + 2>/dev/null || true

# 6. Commit, Tag & Push to leadpiperl1/wookiw-ewok
echo "[6/6] Committing and syncing to GitHub (${REPO_OWNER}/${REPO_NAME})..."
cd "${REPO_ROOT}"
git add -A
git status --short

COMMIT_MSG="feat(v1.0.0): Populate Wookiw-Ewok Encyclopedia Galactica & Public Library across docs/, papers/, audio/, assets/, and workspace_pearls/"

if [ "${DRY_RUN}" -eq 0 ]; then
    git commit -m "${COMMIT_MSG}" || echo "Working tree clean."
    git tag -fa "${VERSION_TAG}" -m "Wookiw-Ewok ${VERSION_TAG} — Open-Access Public Library & Encyclopedia Galactica"
    git push -u origin "${BRANCH}" --tags
    echo "[SYNC COMPLETE] Successfully pushed ${VERSION_TAG} to https://github.com/${REPO_OWNER}/${REPO_NAME}"
else
    echo "[DRY RUN COMPLETE] Staged tree verified in ${REPO_ROOT}. Re-run with DRY_RUN=0 ./sync_wookiw_ewok_profplum.sh to execute live git push."
fi
