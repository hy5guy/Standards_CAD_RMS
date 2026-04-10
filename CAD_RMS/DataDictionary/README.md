# CAD_RMS DataDictionary

This folder stores **cross-system** (CAD ↔ RMS) rules and mappings.

## Layout

- `current/schema/`: cross-system field maps, merge rules, schema registry (JSON/YAML/MD)
- `archive/`: dated snapshots of retired schemas

## Normalization Mappings (in `../mappings/`)

| File | Entries | Targets | Consumer |
|------|---------|---------|----------|
| `how_reported_normalization_map.json` | 140 | 12 canonical values | `enhanced_esri_output_generator.py` (loaded at runtime) |
| `disposition_normalization_map.json` | 55 | 20 canonical values | `enhanced_esri_output_generator.py` (loaded at runtime) |

These JSON files are the **single source of truth** for normalization mappings. The ETL script `CAD_Data_Cleaning_Engine/scripts/enhanced_esri_output_generator.py` loads them via `_load_mapping()` at module import time (no hardcoded dicts).
