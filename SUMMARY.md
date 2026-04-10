# Summary (current state)

## Repository Structure (v3.0.0 - Rationalized 2026-03-17)

This repository contains a single `.git/` at the root level. The `unified_data_dictionary/` folder has been slimmed to a 4-file compatibility shim; bulk content archived.

### Source of Truth: `CAD_RMS/DataDictionary/current/schema/`

All cross-system schemas and mappings are now consolidated here:

| File | Version | Purpose |
|------|---------|---------|
| `canonical_schema.json` | v1.0.0 | Unified CAD/RMS field dictionary |
| `cad_fields_schema_latest.json` | v1.0 | CAD export field schema |
| `rms_fields_schema_latest.json` | v1.0 | RMS export field schema |
| `transformation_spec.json` | v1.0.0 | ETL transformation rules |
| `cad_rms_schema_registry.yaml` | v2.0 | Schema registry with domain values |
| `cad_to_rms_field_map.json` | v2.0 | Enhanced CAD-to-RMS mapping (280 lines) |
| `rms_to_cad_field_map.json` | v2.0 | Enhanced RMS-to-CAD mapping |
| `multi_column_matching_strategy.md` | v2.0 | Multi-column matching guide |

### Domain-Specific Standards

| Domain | Location | Key Files |
|--------|----------|-----------|
| CAD | `CAD/DataDictionary/current/schema/` | `cad_export_field_definitions.md` |
| RMS | `RMS/DataDictionary/current/schema/` | `rms_export_field_definitions.md` (29 fields, 8 groups) |
| Clery | `Clery/DataDictionary/current/` | Crime definitions, geography, NIBRS-to-Clery map |
| NIBRS | `NIBRS/DataDictionary/current/` | Offense definitions, RMS-to-NIBRS mapping |
| Personnel | `Personnel/` | Assignment Master schema (25 columns) |

### Compatibility Shim

`unified_data_dictionary/schemas/` contains 4 files referenced by `02_ETL_Scripts/cad_rms_data_quality/config/schemas.yaml`. These are identical copies of the CAD_RMS canonical versions. Do not modify — update the CAD_RMS copy and re-sync.

### Archive

The `archive/` directory contains retired content organized by date and category. Key subdirectories: `PD_BCI_01_versions/`, `unified_data_dictionary_20260317/`, `schemas_udd_20260317/`, `mappings_field_mappings_20260317/`, `legacy_copies/`, `merged_residue/`.

## What Exists Now

- **CAD** - `cad_export_field_definitions.md` (Draft v1.0, finalized 2025-12-30)
- **RMS** - `rms_export_field_definitions.md` (29 fields, 8 functional groups)
- **Cross-system** - 9 files in `CAD_RMS/DataDictionary/current/schema/` + 15 mapping files in `CAD_RMS/mappings/`
- **Normalization maps** - `how_reported_normalization_map.json` (140 entries), `disposition_normalization_map.json` (55 entries)
- **Call Type Classification** - 649 entries, 11 ESRI categories, JSON + CSV + per-category files
- **Processed Exports** - 20 unit subdirectories, ~99 monthly dashboard CSVs
- **ETL Configuration** - `config/response_time_filters.json`
- **Utility Scripts** - `sync_udd_shim.py`, `extract_narrative_fields.py`, `validate_rms_export.py`
- **Documentation** - Organized under `docs/` (ai_handoff, chat_logs, data_quality, merge, response_time, image, task_templates)
- **CI/Hooks** - `.claude/hooks/session-start.sh` (shim drift detection, git status on session start)

## Recent Milestones

### Standards Audit Phases 1-3 Complete (2026-04-09)

All 9 audit gaps resolved. See `docs/ai_handoff/Phase1_Standards_Audit.md`.

- Normalization mappings extracted from hardcoded Python dicts to standalone JSON in `CAD_RMS/mappings/`
- Schema registry HowReported enum expanded 6 to 12 canonical values; Walk-in corrected to Walk-In
- `transformation_spec.json` field name discrepancies fixed (TimeOfCall, Hour_Calc, PDZone/Zone)
- Shim sync script added (`scripts/sync_udd_shim.py` + `scripts/shim_sync_manifest.json`)

### Repository Rationalization v3.0.0 (2026-03-17)

- All schemas promoted to `CAD_RMS/DataDictionary/current/schema/`
- `unified_data_dictionary/` slimmed to 4-file compatibility shim
- 64 PD_BCI_01 files archived; root clutter reduced from 50+ to ~12 essential files
- `schemas.yaml` shim paths validated and functional

### Call Type Classification v1.2.0 (2026-01-08)

- 649 entries across 11 ESRI standard categories, 3 response types
- Primary reference: `CallType_Categories_latest.csv`
- Per-category CSVs in `mappings/`, JSON lookup in `mappings/call_type_category_mapping.json`
