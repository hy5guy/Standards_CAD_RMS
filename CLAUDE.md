# CLAUDE.md -- Standards Repository AI Agent Protocol

**Version:** 2.0.0
**Last Updated:** 2026-04-10
**Purpose:** Context and operational guidelines for AI agents working on this codebase

---

## What This Repository Is

This is the **Standards** repository (`09_Reference/Standards/`) -- the central, authoritative source for CAD/RMS data standards, schemas, field mappings, and normalization rules used by the Hackensack Police Department's data quality infrastructure.

- **GitHub:** `hy5guy/Standards_CAD_RMS`
- **License:** MIT
- **Standards Version:** 3.0.0 (see `VERSION` file)
- **Maintainer:** R. A. Carucci

This repo does **not** contain the ETL pipeline scripts themselves. Those live in sibling repositories under `02_ETL_Scripts/` (specifically `cad_rms_data_quality/` and `CAD_Data_Cleaning_Engine/`). This repo provides the schemas, mappings, and reference data those pipelines consume.

---

## High-Stakes Context

- **Active Production System:** 724,794 CAD records (2019-2026) feeding a live ArcGIS Pro "Calls for Service" dashboard
- **Zero Downtime Tolerance:** Schema or mapping changes here propagate to normalization scripts and dashboard output
- **Geographic Impact:** Data drives police resource allocation decisions
- **Compliance:** Case number format (YY-NNNNNN) must preserve leading zeros

---

## Repository Structure

```
Standards_CAD_RMS/                         # Root (= 09_Reference/Standards/)
|
|-- CAD_RMS/                               # SINGLE SOURCE OF TRUTH for cross-system schemas
|   |-- DataDictionary/current/schema/     # All canonical schemas (9 files)
|   |   |-- canonical_schema.json          #   Unified field dictionary (100+ fields)
|   |   |-- cad_fields_schema_latest.json  #   CAD export field schema
|   |   |-- rms_fields_schema_latest.json  #   RMS export field schema
|   |   |-- transformation_spec.json       #   ETL transformation rules
|   |   |-- cad_rms_schema_registry.yaml   #   Schema registry + domain values (v1.1.0)
|   |   |-- cad_to_rms_field_map.json      #   v2.0 enhanced field mapping
|   |   |-- rms_to_cad_field_map.json      #   v2.0 enhanced field mapping
|   |   |-- multi_column_matching_strategy.md
|   |   +-- README.md
|   |-- DataDictionary/scripts/            # Schema bootstrap/init scripts
|   +-- mappings/                          # Normalization maps + field mapping rules
|       |-- how_reported_normalization_map.json   # 140 entries -> 12 targets
|       |-- disposition_normalization_map.json    # 55 entries -> 20 targets
|       |-- cad_field_map_latest.json
|       |-- rms_field_map_latest.json
|       |-- cad_to_rms_mapping.csv / rms_to_cad_mapping.csv
|       |-- cad_rms_merge_policy_latest.json
|       +-- mapping_rules.md
|
|-- CAD/                                   # CAD-specific standards
|   |-- DataDictionary/current/schema/     #   cad_export_field_definitions.md
|   |-- DataDictionary/archive/            #   Retired v1.0 field maps
|   +-- SCRPA/                             #   Assignment_Master_V2.csv, cad_data_quality_report.md
|
|-- RMS/                                   # RMS-specific standards
|   |-- DataDictionary/current/schema/     #   rms_export_field_definitions.md (29 fields, 8 groups)
|   +-- SCRPA/                             #   SCRPA_7Day_Data_Dictionary.md, rms_data_quality_report.md
|
|-- Clery/                                 # Clery Act compliance standards
|   +-- DataDictionary/current/
|       |-- schema/                        #   clery_crime_definitions.json, clery_geography_definitions.json
|       |-- mappings/                      #   nibrs_to_clery_map.json
|       +-- institutions/                  #   institution_clery_geography_index.json
|
|-- NIBRS/                                 # NIBRS offense standards
|   +-- DataDictionary/current/
|       |-- schema/                        #   nibrs_offense_definitions.md, ucr_offense_classification.json
|       +-- mappings/                      #   rms_to_nibrs_offense_map.json
|
|-- Personnel/                             # Personnel/Assignment Master schema
|   |-- Assignment_Master_SCHEMA.md        #   Human-readable (25 columns)
|   +-- assignment_master.schema.json      #   Machine-readable JSON Schema
|
|-- Processed_Exports/                     # Dashboard CSV outputs (regenerated monthly)
|   |-- response_time/                     #   Monthly response time metrics
|   |-- Drone/                             #   DFR activity/performance
|   |-- detectives/                        #   Case dispositions, clearance rates
|   |-- arrests/, Benchmark/, chief/, ...  #   20 unit-specific subdirectories
|   +-- (99 CSV files total across all subdirs)
|
|-- mappings/                              # Call type classification system
|   |-- call_type_category_mapping.json    #   Programmatic lookup (649 entries)
|   +-- call_types_*.csv                   #   11 category-specific CSV files
|
|-- config/                                # ETL configuration
|   +-- response_time_filters.json         #   Response Time ETL filtering rules
|
|-- scripts/                               # Utility scripts
|   |-- sync_udd_shim.py                   #   Keep UDD shim in sync with CAD_RMS canonical
|   |-- shim_sync_manifest.json            #   Manifest for sync script (4 file pairs)
|   |-- extraction/
|   |   +-- extract_narrative_fields.py    #   RMS narrative field extractor (462 lines)
|   +-- validation/
|       +-- validate_rms_export.py         #   RMS export validator (407 lines)
|
|-- unified_data_dictionary/               # COMPATIBILITY SHIM ONLY
|   +-- schemas/                           #   4 files mirrored from CAD_RMS canonical
|       |-- canonical_schema.json          #   (identical to CAD_RMS copy)
|       |-- cad_fields_schema_latest.json
|       |-- rms_fields_schema_latest.json
|       +-- transformation_spec.json
|
|-- data/samples/rms/                      # Sample/test data
|-- docs/                                  # All documentation (see Documentation section)
|-- archive/                               # Retired content (637+ files, see Archive section)
|
|-- VERSION                                # Machine-readable: "3.0.0"
|-- README.md                              # Repository overview and canonical file locations
|-- CHANGELOG.md                           # Full version history since v0.3.0
|-- CLAUDE.md                              # This file
|-- SUMMARY.md                             # Current state summary
|-- SCHEMA_FILES_SUMMARY.md                # Schema file inventory
|-- CallType_Categories_latest.csv         # Latest call type reference (649 entries)
|-- extract_narrative_fields.py            # Root copy of extraction script
|-- validate_rms_export.py                 # Root copy of validation script
|-- sample_rms_export.csv                  # Sample RMS data for testing
|-- requirements.txt                       # Python deps (pandas, python-dateutil)
|-- next_suggestions.yaml                  # Future improvement task backlog
|-- Standards.code-workspace               # VS Code workspace config
|-- LICENSE                                # MIT
+-- .gitignore                             # OS noise, Office temp, Python/Node/IDE artifacts
```

---

## Key Concepts

### Single Source of Truth

`CAD_RMS/DataDictionary/current/schema/` is the authoritative location for all cross-system schemas. Everything else either derives from or points to files here.

### Compatibility Shim

`unified_data_dictionary/schemas/` contains 4 files that are identical copies of CAD_RMS originals. These exist for backward compatibility with `02_ETL_Scripts/cad_rms_data_quality/config/schemas.yaml`. **Never edit the shim directly** -- update the CAD_RMS canonical copy and run `python scripts/sync_udd_shim.py` to propagate changes.

### Normalization Mappings

Two JSON files in `CAD_RMS/mappings/` define how raw field values are normalized:
- `how_reported_normalization_map.json`: 140 raw values -> 12 canonical targets (9-1-1, Phone, Walk-In, Self-Initiated, Radio, eMail, Mail, Other - See Notes, Fax, Teletype, Virtual Patrol, Canceled Call)
- `disposition_normalization_map.json`: 55 raw values -> 20 canonical targets

These are loaded at runtime by the external `enhanced_esri_output_generator.py` script.

### Call Type Classification

649 call types mapped to 11 ESRI standard categories with response types (Emergency, Urgent, Routine). Primary reference: `CallType_Categories_latest.csv`. Programmatic lookup: `mappings/call_type_category_mapping.json`.

### Multi-Column Matching (v2.0)

When primary key matching (`ReportNumberNew` <-> `Case Number`) fails, three alternative strategies are available:
1. Temporal + Address Match (confidence >= 0.85)
2. Officer + Temporal Match (confidence >= 0.80)
3. Address + Zone + Approximate Date Match (confidence >= 0.75)

Defined in `CAD_RMS/DataDictionary/current/schema/cad_to_rms_field_map.json` and `rms_to_cad_field_map.json`.

---

## Version Authority & Decision Rules

### When Multiple Versions Exist

| What | Authoritative Location | Do NOT Use |
|------|----------------------|------------|
| Cross-system schemas | `CAD_RMS/DataDictionary/current/schema/` | `unified_data_dictionary/schemas/` (shim only) |
| Normalization maps | `CAD_RMS/mappings/*.json` | Hardcoded dicts in Python scripts |
| Field mappings (v2.0) | `CAD_RMS/DataDictionary/current/schema/` | `archive/mappings_field_mappings_20260317/` |
| Call type reference | `CallType_Categories_latest.csv` | Any backup/timestamped copy |
| `-PD_BCI_01` suffixed files | **Ignore entirely** | `archive/PD_BCI_01_versions/` (frozen v0.2.1 artifacts) |

### Path Resolution Priority

1. Check canonical locations listed in the table above
2. Use relative paths from repo root for portability
3. Never hardcode absolute paths (breaks across machines)

---

## External Consumers

This repo is consumed by scripts in sibling repositories. Understanding these relationships is essential:

```
This Repo (Standards)                    External Consumers
========================                 ============================
CAD_RMS/mappings/*.json          --->    CAD_Data_Cleaning_Engine/scripts/enhanced_esri_output_generator.py
                                           (loads normalization maps at runtime)

unified_data_dictionary/schemas/ --->    cad_rms_data_quality/config/schemas.yaml
                                           (references shim paths via ${standards_root})

config/response_time_filters.json --->   Response_Times/response_time_monthly_generator.py
                                           (filtering rules for response time ETL)

CallType_Categories_latest.csv   --->    Various ETL scripts for incident classification
```

### External Data Pipeline (for context)

```
Raw CAD Exports (Excel)
    |
    v
consolidate_cad_2019_2026.py          # EXTERNAL: merges yearly + monthly files
    |
    v
enhanced_esri_output_generator.py      # EXTERNAL: normalizes using THIS repo's mappings
    |
    v
CAD_ESRI_POLISHED_[timestamp].xlsx     # EXTERNAL: 724K records, normalized
    |
    v
ArcGIS Pro Dashboard (Production)
```

---

## Scripts in This Repo

### `scripts/sync_udd_shim.py`
Keeps the 4 UDD shim files in sync with their CAD_RMS canonical sources. Uses SHA-256 hash comparison.
```bash
python scripts/sync_udd_shim.py            # sync
python scripts/sync_udd_shim.py --dry-run  # report only
```

### `scripts/extraction/extract_narrative_fields.py` (also at root)
Extracts structured data (suspect descriptions, vehicle info, property, M.O.) from RMS Narrative fields using regex pattern matching. 462 lines.
```bash
python extract_narrative_fields.py input.csv [output.csv]
```

### `scripts/validation/validate_rms_export.py` (also at root)
Validates RMS export CSV files against field definitions. Generates HTML reports. 407 lines.
```bash
python validate_rms_export.py input.csv [report.html]
```

---

## Documentation Map

```
docs/
|-- ai_handoff/              # AI session handoff documents (11 files)
|   |-- Phase1_Standards_Audit.md      # Full audit record for Phases 1-3
|   |-- CURSOR_AI_CONSOLIDATION_GUIDE.md
|   |-- OPUS_*.md                      # Claude/Opus session briefings
|   +-- CONTEXT_SUMMARY_AI_HANDOFF.md
|
|-- data_quality/            # Data quality crisis documentation (6 files)
|   |-- CRITICAL_DATA_QUALITY_ALERT.md
|   |-- HOW_REPORTED_FIX_SUMMARY.md
|   +-- EXECUTIVE_SUMMARY.md
|
|-- merge/                   # Repository merge/rationalization docs (24 files)
|   |-- RATIONALIZATION_MANIFEST_20260317.md  # Full audit trail
|   +-- STANDARDS_RATIONALIZATION_PROMPT_OPTIMIZED.md
|
|-- response_time/           # Response time data dictionaries
|   |-- ResponseTime_AllMetrics_DataDictionary.json
|   +-- ResponseTime_AllMetrics_DataDictionary.md
|
|-- chat_logs/               # Development session transcripts (14 topic dirs)
|-- image/                   # Screenshots and diagrams
|-- html/                    # Generated HTML reports
|-- task_templates/          # Task management (kanban, audit CSVs)
+-- call_type_category_mapping.md  # Human-readable call type breakdown
```

---

## Archive Structure

The `archive/` directory (637+ files) contains retired content organized by date and category. **Never delete archive contents.** Key subdirectories:

| Directory | Files | Contents |
|-----------|-------|----------|
| `PD_BCI_01_versions/` | 66 | Frozen v0.2.1 files from initial AI setup |
| `unified_data_dictionary_20260317/` | 282 | UDD bulk content (docs, scripts, src, tests) |
| `legacy_copies/` | 228 | Legacy file versions + UDD git backup |
| `mappings_field_mappings_20260317/` | 12 | v1.0 field mappings (superseded by v2.0) |
| `root_loose_files_20260317/` | 11 | Relocated root-level files |
| `completed_planning/` | 7 | Finished merge/planning docs |
| `directory_trees/` | 6 | Historical tree snapshots |
| `schemas_udd_20260317/` | 6 | Older duplicate schemas |
| `merged_residue/` | 14 | Merge artifacts |
| `schema_drafts/` | 3 | Draft schemas |

---

## Audit Status

### Standards Audit -- Phases 1, 2, 3 Complete (2026-04-09)

All 9 gaps from the Phase 1 audit have been resolved. See `docs/ai_handoff/Phase1_Standards_Audit.md`.

**Key outcomes:**
- Normalization mappings extracted from hardcoded Python dicts to standalone JSON in `CAD_RMS/mappings/`
- Schema registry HowReported enum expanded 6 -> 12 canonical values; Walk-in -> Walk-In
- `transformation_spec.json` field name discrepancies fixed (TimeOfCall, Hour_Calc, PDZone/Zone)
- Shim sync script added (`scripts/sync_udd_shim.py`)

### Standing Decisions

1. **Authoritative mapping format:** CAD_RMS v2.0 (2025-12-30) + normalization JSON files
2. **-PD_BCI_01 suffixed files:** Archived to `archive/PD_BCI_01_versions/`
3. **Validation order:** Consolidate first, THEN validate
4. **Schema validation scope:** Critical fields first (HowReported, Disposition, Incident)

---

## Common Pitfalls

### Case Number Format Corruption
Excel converts `26-000001` to `26000001`. Always force `ReportNumberNew` to string dtype on load:
```python
df = pd.read_excel(file, dtype={'ReportNumberNew': str})
```

### Editing the Shim Instead of Canonical
Never edit `unified_data_dictionary/schemas/` directly. Edit the canonical copy in `CAD_RMS/DataDictionary/current/schema/` and run `python scripts/sync_udd_shim.py`.

### Mixing Schema Versions
If any script references `unified_data_dictionary/schemas/` directly (instead of through the shim mechanism), update it to point to `CAD_RMS/DataDictionary/current/schema/`.

### Stale Normalization Maps
The JSON normalization maps in `CAD_RMS/mappings/` must stay in sync with the external `enhanced_esri_output_generator.py`. If you add a new HowReported value to the schema registry, also add it to `how_reported_normalization_map.json`.

---

## AI Agent Guidelines

### DO

- **Read before editing** -- understand the file's role before modifying it
- **Create a git checkpoint** before major changes: `git add . && git commit -m "Checkpoint before [operation]"`
- **Run the shim sync** after editing any of the 4 canonical schema files
- **Validate assumptions with data** -- check field counts, unique values, null rates
- **Prefer relative paths** from the repo root

### DON'T

- **Never modify files in `archive/`** -- they are frozen historical records
- **Never edit shim files directly** -- always edit the CAD_RMS canonical copy
- **Never hardcode absolute Windows paths** -- use relative paths or config variables
- **Never delete files without archiving** -- this repo uses a preserve-first policy
- **Never assume Excel preserves dtypes** -- always force string for case numbers

### When Proposing Changes

1. State the specific file and line number affected
2. Show before/after snippets
3. Explain impact on downstream consumers (dashboard, ETL scripts)
4. Provide a validation step to verify the change worked
5. Include rollback procedure

---

## Development Setup

### Python Dependencies
```bash
pip install -r requirements.txt  # pandas>=2.0.0, python-dateutil>=2.8.2
```

### Quick Validation
```bash
# Verify shim sync status
python scripts/sync_udd_shim.py --dry-run

# Validate an RMS export
python validate_rms_export.py sample_rms_export.csv
```

---

## Version History

| Version | Date | Key Changes |
|---------|------|-------------|
| 3.0.0 | 2026-03-17 | **RATIONALIZATION:** CAD_RMS is single source of truth, UDD slimmed to 4-file shim, 64 PD_BCI_01 files archived, root reduced to ~12 essential files |
| 2.0.0 | 2026-01-15 | Repository restructuring, nested git removed, archive structure created |
| 1.2.2 | 2026-01-14 | Response time filter configuration added |
| 1.2.0 | 2026-01-08 | Standardized to 11 ESRI categories, added 9 unmatched call types |
| 1.1.0 | 2026-01-08 | Call type mapping system with Incident_Norm column, 640 entries |
| 1.0.0 | 2026-01-08 | Initial call type classification (516 entries, 11 categories) |
| 0.3.0 | 2025-12-30 | RMS export field definitions (29 fields, 8 groups), v2.0 mappings |

See `CHANGELOG.md` for full details.

---

**Last Updated:** 2026-04-10
**CLAUDE.md Version:** 2.0.0
**For AI Agents:** Treat this as your operational manual. When in doubt, refer here first.
