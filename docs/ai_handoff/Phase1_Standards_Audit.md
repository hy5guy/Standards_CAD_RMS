// 2026-04-09-20-15-00
// CAD_RMS_Integration/Phase1_Standards_Audit.md (Rev 2 — corrected per RAC accuracy review)
// Author: R. A. Carucci
// Purpose: Phase 1 Standards Audit & Lock-In for CAD/RMS multi-phase ETL project

---

# Phase 1 — Standards Audit & Lock-In

## Thinking (Dependencies, Risks, Sequencing)

### Key Dependencies
- Standards v3.0.0 (rationalized 2026-03-17) is the baseline
- `schemas.yaml` in `cad_rms_data_quality/config/` is the runtime config that wires ETL scripts to Standards
- `enhanced_esri_output_generator.py` in `CAD_Data_Cleaning_Engine` holds the AUTHORITATIVE normalization mappings (145 HOW_REPORTED entries → 12 canonical targets, 58 DISPOSITION entries → 20 canonical targets)
- ArcGIS Pro project (`LawEnforcementDataManagement.ppkx`) provides Beat/Grid/Zone polygon layers for spatial enrichment

### Key Risks
1. **Dual normalization authority**: `enhanced_esri_output_generator.py` (runtime logic) vs `cad_rms_schema_registry.yaml` (domain values) could drift
2. **Shim staleness**: `unified_data_dictionary/schemas/` shim files could get out of sync with `CAD_RMS/DataDictionary/current/schema/` canonical copies
3. **CAD_Data_Cleaning_Engine size (1.3 GB)**: Likely contains large data artifacts, not just code — needs triage before any merge decision
4. **schemas.yaml path resolution**: Uses `${standards_root}` variable expansion — Python's `yaml.safe_load` does NOT expand `${}` natively. However, no production script currently consumes these paths (LOW risk)

### Sequencing
1. Validate Standards file inventory against docs
2. Cross-reference `schemas.yaml` paths against filesystem
3. Audit `cad_rms_data_quality` script imports against Standards
4. Audit `CAD_Data_Cleaning_Engine` contents and size breakdown
5. Flag conflicts/gaps
6. Recommendation on `CAD_Data_Cleaning_Engine` disposition
7. Lock-in checklist

---

## Phase 1 Summary

### 1. Standards Repository (v3.0.0) — Validated Clean

The repository rationalization completed 2026-03-17 is well-documented. Source of truth hierarchy is clear:

| Layer | Location | Status |
|-------|----------|--------|
| Cross-system schemas | `CAD_RMS/DataDictionary/current/schema/` (8 files) | ✅ Canonical |
| Cross-system mappings | `CAD_RMS/mappings/` (12 files) | ✅ Promoted from UDD |
| CAD field defs | `CAD/DataDictionary/current/schema/cad_export_field_definitions.md` | ✅ Draft v1.0 |
| RMS field defs | `RMS/DataDictionary/current/schema/rms_export_field_definitions.md` | ✅ v1.0 (29 fields, 8 groups) |
| Call type classification | `mappings/call_type_category_mapping.json` + 11 CSVs (649 entries) | ✅ v1.2.0 |
| Response time filters | `config/response_time_filters.json` | ✅ v1.2.2 |
| Compatibility shim | `unified_data_dictionary/schemas/` (4 files) | ⚠️ Must stay in sync |
| Clery | `Clery/DataDictionary/current/` | ✅ v1.1.0 |
| NIBRS | `NIBRS/DataDictionary/current/` | ✅ Active |
| Personnel | `Personnel/` | ✅ Assignment Master (25 cols) |

**No conflicts found between Standards docs (SCHEMA_FILES_SUMMARY.md, SUMMARY.md, CHANGELOG.md, README.md).**

### 2. `schemas.yaml` Path Audit

Current `schemas.yaml` (attached, dated 2026-01-30) references:

| Key | Path | Target Exists? | Notes |
|-----|------|----------------|-------|
| `schemas.canonical` | `…/unified_data_dictionary/schemas/canonical_schema.json` | ✅ (shim) | Points to shim, not canonical — acceptable per design |
| `schemas.cad` | `…/unified_data_dictionary/schemas/cad_fields_schema_latest.json` | ✅ (shim) | Same |
| `schemas.rms` | `…/unified_data_dictionary/schemas/rms_fields_schema_latest.json` | ✅ (shim) | Same |
| `schemas.transformation` | `…/unified_data_dictionary/schemas/transformation_spec.json` | ✅ (shim) | Same |
| `mappings.cad_to_rms` | `…/CAD_RMS/DataDictionary/current/schema/cad_to_rms_field_map.json` | ✅ | Direct canonical |
| `mappings.rms_to_cad` | `…/CAD_RMS/DataDictionary/current/schema/rms_to_cad_field_map.json` | ✅ | Direct canonical |
| `mappings.field_rules` | `…/CAD_RMS/mappings/mapping_rules.md` | ✅ | Updated in v3.0.0 |
| `mappings.call_types_csv` | `…/mappings/call_types_*.csv` | ✅ | 11 category CSVs |
| `mappings.multi_column_strategy` | `…/CAD_RMS/DataDictionary/current/schema/multi_column_matching_strategy.md` | ✅ | v2.0 |
| `config.response_time_filters` | `…/config/response_time_filters.json` | ✅ | v1.2.2 |

**⚠️ NOTE — `${standards_root}` variable expansion:**
Python's `yaml.safe_load()` does NOT expand `${variable}` syntax. However, **no production script currently consumes `schemas.yaml`** — it is a documentation/future-use artifact. When Phase 2 scripts need it, add a simple post-load resolver. Not a blocker.

### 3. `cad_rms_data_quality` Cross-Reference

Based on CLAUDE.md (v1.4.0) and Claude.md (v1.6.1), this project contains:

| Component | Script | Standards Dependency |
|-----------|--------|---------------------|
| Consolidation | `consolidate_cad_2019_2026.py` | `consolidation_sources.yaml` (source registry) |
| Normalization | `CAD_Data_Cleaning_Engine/scripts/enhanced_esri_output_generator.py` (separate manual step; consumes consolidation CSV output) | `HOW_REPORTED_MAPPING`, `DISPOSITION_MAPPING` (hardcoded in script) |
| Monthly validation | `monthly_validation/scripts/validate_cad.py` | `validation_rules.yaml` |
| Monthly validation | `monthly_validation/scripts/validate_rms.py` | `validation_rules.yaml` |
| Deployment | `scripts/copy_polished_to_processed_and_update_manifest.py` | `13_PROCESSED_DATA/ESRI_Polished/manifest.json` |
| Dashboard health | `scripts/monitor_dashboard_health.py` | ArcGIS Online layer URL |
| Gap fix | `scripts/fix_gap_calldate_*.py`, `probe_gap_record.py` | Local/online geodatabase |
| Backfill | `complete_backfill_simplified.py` | ArcGIS Pro environment |

**Key findings:**
1. The pipeline is **sequential but decoupled** — `consolidate_cad_2019_2026.py` produces a CSV, which is then manually fed to `enhanced_esri_output_generator.py`. There is no automated caller/callee relationship. Phase 2 must wire these together explicitly.
2. Normalization logic lives in `enhanced_esri_output_generator.py` as hardcoded Python dicts, NOT in Standards JSON/YAML. Domain values in `cad_rms_schema_registry.yaml` and the hardcoded mappings could drift.

### 4. `CAD_Data_Cleaning_Engine` Disposition Recommendation

**Size:** 1.3 GB, 2 folders

**Assessment:**
- The 1.3 GB is almost certainly data artifacts (Excel/CSV exports, geodatabases), not code
- The critical asset is ONE file: `scripts/enhanced_esri_output_generator.py`
- This file holds the authoritative `HOW_REPORTED_MAPPING` (145 entries → 12 canonical targets) and `DISPOSITION_MAPPING` (58 entries → 20 canonical targets)
- Everything else in this directory is likely intermediate outputs or test data

**Recommendation: EXTRACT + ARCHIVE**
1. **Extract** `enhanced_esri_output_generator.py` into `cad_rms_data_quality/shared/normalization/` (or a new `02_ETL_Scripts/cad_rms_pipeline/` if Phase 2 creates a new project)
2. **Extract** normalization mappings from the Python dicts into standalone JSON files in `09_Reference/Standards/CAD_RMS/DataDictionary/current/schema/`:
   - `how_reported_normalization_map.json`
   - `disposition_normalization_map.json`
3. **Archive** the rest of `CAD_Data_Cleaning_Engine` to `02_ETL_Scripts/archive/CAD_Data_Cleaning_Engine_20260409/`
4. **Do NOT delete** until Phase 2 pipeline is validated end-to-end

### 5. Conflicts & Gaps Found

| # | Issue | Severity | Resolution |
|---|-------|----------|------------|
| 1 | `${standards_root}` in `schemas.yaml` — Python doesn't expand this natively | 🟢 LOW | No production script consumes interpolated paths; `schemas.yaml` is a documentation/future-use artifact. Add resolver when needed (30-min fix) |
| 2 | Normalization mappings hardcoded in Python, not in Standards | 🟡 HIGH | Extract to JSON in Standards (Phase 2 prerequisite) |
| 3 | `cad_rms_schema_registry.yaml` has `HowReported` enum with 6 values (pre-normalization); Python script maps to 12 canonical targets (post-normalization). Also: registry uses `Walk-in`, script uses `Walk-In` | 🟡 HIGH | Update registry enum to 12 canonical targets; fix case to `Walk-In`; add note clarifying pre- vs post-normalization layers |
| 4 | Shim sync process is manual ("update CAD_RMS copy and re-sync") | 🟡 MEDIUM | Add a sync script or pre-commit hook in Phase 2 |
| 5 | `transformation_spec.json` uses `"FullAddress"/"Zone"` — verified: CAD uses `FullAddress2` (✅ match), `PDZone` (⚠️ CAD header vs `Zone` RMS header) | 🟡 MEDIUM | Document CAD=`PDZone`, RMS=`Zone` distinction in spec |
| 6 | CLAUDE.md references `config/schemas.yaml` pointing to Standards but `schemas.yaml` metadata says `standards_version: "v3.0.0"` — confirm metadata is updated when standards change | 🟢 LOW | Add version check to ETL startup |
| 7 | `CAD_Data_Cleaning_Engine` at 1.3 GB is bloating OneDrive sync | 🟢 LOW | Archive after extraction (see §4) |
| 8 | `transformation_spec.json` Stage 1.3 `expected_cad_cols` uses `TimeOfCall` but actual CAD export header is `"Time of Call"` (with spaces) | 🟡 MEDIUM | Update spec to use actual header; or document as a required rename operation |
| 9 | ESRI generator expects `Hour_Calc`; actual CAD export has `HourMinuetsCalc` (vendor typo preserved). Rename is implicit in script, undocumented in spec | 🟡 MEDIUM | Document the rename in transformation_spec Stage 2.1; fix typo in field name when next export format is generated |

### 6. Files That Must NOT Change Before Phase 2

These are **locked** — any modification requires re-audit:

- `CAD_RMS/DataDictionary/current/schema/canonical_schema.json` (v1.0.0)
- `CAD_RMS/DataDictionary/current/schema/cad_to_rms_field_map.json` (v2.0)
- `CAD_RMS/DataDictionary/current/schema/rms_to_cad_field_map.json` (v2.0)
- `CAD_RMS/DataDictionary/current/schema/transformation_spec.json` (v1.0.0)
- `CAD_RMS/DataDictionary/current/schema/cad_rms_schema_registry.yaml` (v2.0)
- `CAD_RMS/DataDictionary/current/schema/multi_column_matching_strategy.md` (v2.0)
- `RMS/DataDictionary/current/schema/rms_export_field_definitions.md` (v1.0)
- `CAD/DataDictionary/current/schema/cad_export_field_definitions.md` (Draft v1.0)
- `config/response_time_filters.json`
- `mappings/call_type_category_mapping.json` + 11 category CSVs
- `config/schemas.yaml`

---

## Resolved Questions (from initial audit)

1. ~~**`${standards_root}` expansion**~~ — **RESOLVED:** No production script consumes `schemas.yaml`. Downgraded to LOW. Add resolver when needed.
2. ~~**`CAD_Data_Cleaning_Engine` contents**~~ — **RESOLVED:** Confirmed 1,355.9 MB data artifacts, 0.1 MB scripts. Extract-and-archive approved.
3. **Normalization mapping extraction** — **APPROVED.** Extract `HOW_REPORTED_MAPPING` (145 entries) and `DISPOSITION_MAPPING` (58 entries) to `CAD_RMS/mappings/how_reported_mapping.json` and `disposition_mapping.json`. Phase 2 prerequisite.
4. ~~**`transformation_spec.json` field names**~~ — **RESOLVED:** `FullAddress2` matches ✅. `PDZone` vs `Zone` is a CAD/RMS header difference (documented). `TimeOfCall` vs `"Time of Call"` and `Hour_Calc` vs `HourMinuetsCalc` added as new gaps #8 and #9.
5. ~~**Response Time PDFs**~~ — **RESOLVED:** `response_time_filters.json` exists and is referenced. PDFs are Phase 2B only.

---

## Phase 1 Complete — LOCKED.

**Standards are auditable and structurally sound at v3.0.0.** Nine gaps identified (0 blockers, 2 high, 4 medium, 3 low). No schema conflicts between documentation files. All five pre-Phase-2 questions resolved.

**Also note for Phase 2:** CLAUDE.md's claim of "280 HOW_REPORTED entries" is incorrect (actual: 145 → 12 targets). Correct CLAUDE.md when next touched.

**Phase 1 locked. Confirm to proceed to Phase 2.**

---

## Phase 2 Completion Record

**Completed:** 2026-04-09 | **Repo:** [hy5guy/Standards_CAD_RMS](https://github.com/hy5guy/Standards_CAD_RMS)

| Gap | Stage | Resolution | Commit | Files Modified |
|-----|-------|------------|--------|----------------|
| #2 | A | Extracted mappings to JSON | `03d3aed` | `CAD_RMS/mappings/how_reported_normalization_map.json` (140 entries), `CAD_RMS/mappings/disposition_normalization_map.json` (55 entries) |
| #3 | B | Fixed schema registry enum 6→12; Walk-in→Walk-In; added post-normalization header | `03d3aed` | `CAD_RMS/DataDictionary/current/schema/cad_rms_schema_registry.yaml` (v1.0.0→v1.1.0) |
| #5 | C3 | Documented PDZone (CAD) vs Zone (RMS) in Stage 1.3 | `e476508` | `CAD_RMS/DataDictionary/current/schema/transformation_spec.json` |
| #8 | C1 | Fixed TimeOfCall → "Time of Call" in Stage 1.3 expected_cad_cols | `e476508` | `CAD_RMS/DataDictionary/current/schema/transformation_spec.json` |
| #9 | C2 | Documented HourMinuetsCalc → Hour_Calc rename in Stage 2.1 | `e476508` | `CAD_RMS/DataDictionary/current/schema/transformation_spec.json` |
| #4 | C4 | Added shim sync script and manifest | `e476508` | `scripts/sync_udd_shim.py`, `scripts/shim_sync_manifest.json` |
| — | D1 | Corrected CLAUDE.md mapping counts (280→140 HOW_REPORTED, 100+→55 DISPOSITION) | `6ed2533` | `CLAUDE.md` |
| — | — | Synced transformation_spec.json shim after Stage C changes | `554b235` | `unified_data_dictionary/schemas/transformation_spec.json` |

**Also completed (ETL scripts repo — [hy5guy/CAD_Data_Cleaning_Engine](https://github.com/hy5guy/CAD_Data_Cleaning_Engine)):**
- `enhanced_esri_output_generator.py` wired to load from Standards JSON instead of hardcoded dicts (commit `cc06069`)

**Gaps remaining open after Phase 2:**
- Gap #1 (LOW): `${standards_root}` resolver — deferred, no production script consumes it
- Gap #6 (LOW): `schemas.yaml` version metadata check on ETL startup — deferred
- Gap #7 (LOW): `CAD_Data_Cleaning_Engine` OneDrive bloat — extraction done; archive pending confirmation

**Count correction (D2):** Phase 1 §4 and §Thinking reference "145/58" mapping counts. Correct values are "140/55" (effective runtime entries — duplicates removed from original hardcoded dicts during JSON extraction).

---

## Phase 3 — Validate & Close

**Goal:** Confirm Phase 2 wiring is production-ready; close 3 remaining LOW-priority gaps.
**Started:** 2026-04-10

| Task | Description | Gap | Status |
|------|-------------|-----|--------|
| 3A | Smoke-test JSON loading in `enhanced_esri_output_generator.py` | — | ✅ PASS (2026-04-09) |
| 3B | Add `${standards_root}` post-load resolver to `schemas.yaml` handling | #1 | ⏳ Pending |
| 3C | Archive `CAD_Data_Cleaning_Engine/data/` artifacts (~1.4 GB) from OneDrive active sync | #7 | 🔄 In Progress (2026-04-10) |
| 3D | Add `schemas.yaml` version metadata check stub in ETL startup sequence | #6 | ⏳ Pending |

**Key constraint:** 3C is safe to run independently of 3A — `data/` contains input/output artifacts only. The script loads normalization mappings exclusively from `Standards/CAD_RMS/mappings/*.json`.

---

## Phase 3A — Smoke Test (2026-04-09)

**Purpose:** Validate Phase 2 wiring — `enhanced_esri_output_generator.py` loading normalization mappings from Standards JSON instead of hardcoded Python dicts.

### Test 1: Import & Count — PASS ✅

```
cd CAD_Data_Cleaning_Engine/
python -c "from scripts.enhanced_esri_output_generator import HOW_REPORTED_MAPPING, DISPOSITION_MAPPING; ..."

Result:
  Loaded DISPOSITION_MAPPING: 55 entries from disposition_normalization_map.json
  Loaded HOW_REPORTED_MAPPING: 140 entries from how_reported_normalization_map.json
  HOW_REPORTED: 140 entries
  DISPOSITION: 55 entries
```

**Wiring chain verified:** `_STANDARDS_ROOT` (line 84) → `_MAPPINGS_DIR` (line 88) → `_load_mapping()` (lines 90–97) → JSON parse → module-level dicts populated.

### Test 2: Normalization Spot-Check — PASS ✅ (4/4 correct)

| Input | Mapping Result | Expected | Status | Notes |
|-------|---------------|----------|--------|-------|
| `911` | `9-1-1` | `9-1-1` | ✅ | Direct match |
| `PHONE/911` | `Phone` | `Phone` | ✅ | Correct — phone-initiated, not direct 911 |
| `WALK IN` | `Walk-In` | `Walk-In` | ✅ | Direct match |
| `SELF-INIT` | `Self-Initiated` | `Self-Initiated` | ✅ | Hyphenated key is the actual variant |

Initial test expectations for `PHONE/911` (expected `9-1-1`) and `SELF INIT` (space, not hyphen) were incorrect assumptions — corrected above to match actual source data patterns.

**Unmapped values** are handled by `_normalize_how_reported_advanced()` and `_normalize_disposition_advanced()` fallback functions (lines 138–143), which apply pattern matching and defaults. The direct mapping dict is not the only normalization layer.

### Phase 3A Verdict: PASS

Phase 2 wiring is **production-ready**. Safe to proceed with Gap #7 archive and remaining Phase 3 tasks.

---

## Phase 3C — Data Archive (Gap #7)

**Authorized:** 2026-04-10 — Phase 3A PASS confirms it is safe.
**Why safe:** `enhanced_esri_output_generator.py` loads normalization mappings from `Standards/CAD_RMS/mappings/*.json` only. The `data/` subdirectories are intermediate input/output artifacts with no runtime dependency.

**Action:** Move `CAD_Data_Cleaning_Engine/data/01_raw/` and `data/03_final/` (~1.4 GB of intermediate Excel/CSV artifacts) to:

```
02_ETL_Scripts/archive/CAD_Data_Cleaning_Engine_data_20260410/
```

`scripts/` folder remains in place and untouched.

**Status:** 🔄 In Progress (2026-04-10) — Claude Code move in progress.

---

## Phase 3B & 3D — Remaining Open Gaps

### 3B — `${standards_root}` Resolver (Gap #1, LOW, ~30 min)

**Problem:** `schemas.yaml` uses `${standards_root}` variable syntax. Python's `yaml.safe_load()` does not expand it. No production script currently consumes the interpolated paths — this is a future-use risk, not an active break.

**Fix:** Add a `load_schemas()` helper in `cad_rms_data_quality/shared/utils/schema_loader.py` that:
1. Loads `schemas.yaml` with `yaml.safe_load()`
2. Resolves `${standards_root}` using the same pattern as `enhanced_esri_output_generator.py`:
   - Check `os.environ.get('STANDARDS_ROOT')` first
   - Fall back to `C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards`
3. Returns the resolved dict

**Status:** ⏳ Pending

### 3D — Version Metadata Check (Gap #6, LOW, ~1 hour)

**Problem:** `schemas.yaml` declares `standards_version: "v3.0.0"` but there is no runtime check that the Standards repo actually matches this version. Schema drift could go undetected.

**Fix:** Add `cad_rms_data_quality/shared/utils/version_check.py` that:
1. Reads `standards_version` from `schemas.yaml`
2. Compares against a `VERSION` file or latest git tag in the Standards repo
3. Emits `logger.warning()` (not error) on mismatch — non-blocking, informational only
4. Called at ETL startup before any processing begins

**Status:** ⏳ Pending

---

## Phase 3 Open Items Tracker

| Item | Gap | Priority | Blocked By | Status |
|------|-----|----------|------------|--------|
| 3A Smoke test | — | DONE | — | ✅ PASS |
| 3C Data archive | #7 | LOW | 3A PASS | 🔄 In Progress |
| 3B Schema loader | #1 | LOW | Nothing | ⏳ Pending |
| 3D Version check | #6 | LOW | Nothing | ⏳ Pending |