PYTHON ?= python3
CACHE_DIR ?= $(HOME)/.cache/wookiw_ewok_v5_1_0

.PHONY: all verify clean

all: verify

verify:
	@mkdir -p $(CACHE_DIR)
	$(PYTHON) benchmarks/verify_gaia_beat_pretty_noise_v1_0_0.py --seed 42 > $(CACHE_DIR)/gaia_beat_receipt.json
	$(PYTHON) luthier/rapa_nui_uku_v1_0_0/verify_rapa_nui_uku_luthier_v1_0_0.py --seed 42 > $(CACHE_DIR)/rapa_nui_receipt.json
	$(PYTHON) benchmarks/verify_acoustic_swoopty_doo_v1_1_1.py --seed 42 > $(CACHE_DIR)/swoopty_doo_receipt.json
	env -u BASH_ENV bash "$(CURDIR)/scripts/audit_wfx_loot.sh" "$(CURDIR)"

clean:
	rm -rf "$(CACHE_DIR)"
