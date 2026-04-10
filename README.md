# Standards Repository

Central repository for CAD/RMS data standards, schemas, and field mappings.

## Repository Layout (v3.0.0 - Rationalized 2026-03-17)

```
Standards/
├── CAD/                        # CAD-specific standards
│   ├── DataDictionary/
│   │   ├── current/schema/     # cad_export_field_definitions.md
│   │   └── archive/            # Retired v1.0 field maps
│   └── SCRPA/                  # Assignment_Master_V2.csv, cad_data_quality_report.md
├── CAD_RMS/                    # CANONICAL unified standards (source of truth)
│   ├── DataDictionary/
│   │   └── current/schema/     # ALL cross-system schemas + mappings (v2.0)
│   └── mappings/               # Normalization maps, field mapping rules, CSVs
├── RMS/                        # RMS-specific standards
│   ├── DataDictionary/
│   │   └── current/schema/     # rms_export_field_definitions.md (29 fields)
│   └── SCRPA/                  # SCRPA_7Day_Data_Dictionary.md, rms_data_quality_report.md
├── Clery/                      # Clery Act crime statistics (v1.1.0)
│   ├── DataDictionary/current/ # Crime definitions, geography, NIBRS-to-Clery map
│   └── scripts/                # extract_clery_geography_from_arcgis.py
├── NIBRS/                      # NIBRS offense standards (81 offenses, FBI 2023.0)
│   └── DataDictionary/current/ # Offense definitions, RMS-to-NIBRS mapping
├── Personnel/                  # Personnel/Assignment Master schema (25 columns)
├── Processed_Exports/          # Dashboard CSV outputs (20 unit subdirs, ~99 CSVs)
│   ├── response_time/          # Monthly response time metrics
│   ├── Drone/                  # DFR activity/performance
│   ├── detectives/             # Case dispositions, clearance rates
│   └── ...                     # arrests, Benchmark, chief, esu, remu, stacp, etc.
├── config/                     # ETL configuration files
│   └── response_time_filters.json
├── data/samples/               # Sample/test data
├── mappings/                   # Call type category CSVs and JSON lookup (649 entries)
├── scripts/                    # Utility scripts
│   ├── sync_udd_shim.py        # Keep UDD shim in sync with CAD_RMS canonical
│   ├── extraction/              # extract_narrative_fields.py
│   └── validation/              # validate_rms_export.py
├── docs/                       # All documentation
│   ├── ai_handoff/             # AI session handoff documents (11 files)
│   ├── chat_logs/              # Development chat logs (14 topics)
│   ├── data_quality/           # Data quality crisis/fix docs
│   ├── merge/                  # Repository merge documentation
│   ├── response_time/          # Response time data dictionaries
│   ├── image/                  # Images and diagrams
│   └── task_templates/         # Task management templates
├── .claude/                    # Claude Code configuration
│   ├── hooks/session-start.sh  # Session start: shim drift check, git status
│   └── settings.json           # Hook registration
├── VERSION                     # Machine-readable version (3.0.0) for runtime checks
├── unified_data_dictionary/    # COMPATIBILITY SHIM ONLY (4 files for schemas.yaml)
│   └── schemas/                # canonical_schema, cad/rms_fields_schema, transformation_spec
└── archive/                    # All retired/archived content (637+ files)
    ├── PD_BCI_01_versions/     # Frozen v0.2.1 files from initial AI setup
    ├── unified_data_dictionary_20260317/  # UDD bulk content
    ├── schemas_udd_20260317/   # Older duplicate schemas
    ├── mappings_field_mappings_20260317/  # v1.0 field mappings
    ├── root_loose_files_20260317/  # Relocated root-level files
    ├── completed_planning/     # Finished merge/planning docs
    ├── directory_trees/        # Historical tree snapshots
    ├── legacy_copies/          # Legacy file versions
    └── merged_residue/         # Merge artifacts
```

## Canonical File Locations

| File | Canonical Location |
|------|-------------------|
| `canonical_schema.json` | `CAD_RMS/DataDictionary/current/schema/` |
| `cad_fields_schema_latest.json` | `CAD_RMS/DataDictionary/current/schema/` |
| `rms_fields_schema_latest.json` | `CAD_RMS/DataDictionary/current/schema/` |
| `transformation_spec.json` | `CAD_RMS/DataDictionary/current/schema/` |
| `cad_rms_schema_registry.yaml` | `CAD_RMS/DataDictionary/current/schema/` |
| `cad_to_rms_field_map.json` (v2.0) | `CAD_RMS/DataDictionary/current/schema/` |
| `rms_to_cad_field_map.json` (v2.0) | `CAD_RMS/DataDictionary/current/schema/` |
| `multi_column_matching_strategy.md` | `CAD_RMS/DataDictionary/current/schema/` |
| `mapping_rules.md` | `CAD_RMS/mappings/` |
| `rms_export_field_definitions.md` | `RMS/DataDictionary/current/schema/` |
| `cad_export_field_definitions.md` | `CAD/DataDictionary/current/schema/` |
| `clery_crime_definitions.json` | `Clery/DataDictionary/current/schema/` |
| `nibrs_to_clery_map.json` | `Clery/DataDictionary/current/mappings/` |

**Note:** `unified_data_dictionary/schemas/` is a 4-file compatibility shim for `02_ETL_Scripts/cad_rms_data_quality/config/schemas.yaml`. The canonical copies live in `CAD_RMS/DataDictionary/current/schema/`.

## Archive Policy

Files in `archive/` are retained indefinitely for reference. See `archive/README.md` for details.

---

## CAD-RMS Cross-System Mapping Schema

This repository contains enhanced mapping schemas and strategies for integrating CAD (Computer-Aided Dispatch) and RMS (Records Management System) data.

## Files

### Core Mapping Schemas

- **`cad_to_rms_field_map.json`** (v2.0) - Enhanced CAD-to-RMS field mapping with multi-column matching strategies
- **`rms_to_cad_field_map.json`** (v2.0) - Enhanced RMS-to-CAD field mapping with multi-column matching strategies

### Documentation

- **`multi_column_matching_strategy.md`** - Comprehensive guide to multi-column matching strategies for confident record linking
- **`rms_export_field_definitions.md`** - Comprehensive RMS field definitions with validation rules, formats, and mapping notes (29 fields across 8 functional groups)
- **`docs/call_type_category_mapping.md`** - Complete Call Type to Category Type mapping documentation (649 call types across 11 categories, ESRI standard)

## Version 2.0 Enhancements

The enhanced mapping schemas (v2.0) include:

1. **Multi-Column Matching Strategies**: Three alternative matching strategies beyond primary key matching:
   - Temporal + Address Match (confidence threshold: 0.85)
   - Officer + Temporal Match (confidence threshold: 0.80)
   - Address + Zone + Approximate Date Match (confidence threshold: 0.75)

2. **Confidence Scoring**: Each match includes a confidence score (0.0 to 1.0) indicating match quality

3. **Match Strategy Tracking**: Audit fields track which matching strategy was used for each record

4. **Enhanced Audit Fields**: Additional metadata fields for match quality analysis and troubleshooting

## Usage

### Primary Key Matching

The primary join key (`ReportNumberNew` ↔ `Case Number`) should be used first for exact matching. The enhanced schemas maintain backward compatibility with primary key matching.

### Alternative Matching Strategies

When primary key matching fails or confidence is low, the alternative matching strategies can be applied according to the workflow defined in `multi_column_matching_strategy.md`.

### Backward Compatibility

The enhanced schemas are backward compatible with v1.0 schemas. Existing code that uses primary key matching will continue to work. Alternative matching strategies are additive enhancements.

## Related Documentation

- **CAD Field Definitions**: `CAD/DataDictionary/current/schema/cad_export_field_definitions.md`
- **RMS Field Definitions**: `rms_export_field_definitions.md` (comprehensive v1.0 with 29 fields organized into 8 functional groups)
- **Call Type Classification**: `docs/call_type_category_mapping.md` (527 call types mapped to 11 ESRI categories with response types)
- **Mapping Rules**: `CAD_RMS/mappings/mapping_rules.md`

## Call Type Classification System

The Standards folder now includes a comprehensive Call Type to Category Type mapping system for RMS Incident Type classification:

- **Primary Reference**: `09_Reference/Classifications/CallTypes/CallType_Categories.csv` (649 entries, with Incident_Norm column, 11 ESRI standard categories only)
- **Documentation**: `docs/call_type_category_mapping.md` - Human-readable breakdown by category
- **Category Files**: `mappings/call_types_*.csv` - 11 category-specific CSV files for targeted loading
- **JSON Mapping**: `mappings/call_type_category_mapping.json` - Programmatic lookup dictionaries

**Usage Example:**
```python
import pandas as pd
from pathlib import Path

# Load standard reference (from repo root)
df = pd.read_csv("CallType_Categories_latest.csv")

# Or load specific category
criminal_incidents = pd.read_csv("mappings/call_types_criminal_incidents.csv")

# Or use JSON for quick lookups
import json
with open("mappings/call_type_category_mapping.json", "r") as f:
    mapping = json.load(f)
category = mapping['call_type_to_category']['Domestic Dispute']  # Returns: 'Criminal Incidents'
```

**Categories (11 total):**
1. Administrative and Support (122 call types)
2. Assistance and Mutual Aid (21 call types)
3. Community Engagement (20 call types)
4. Criminal Incidents (201 call types)
5. Emergency Response (33 call types)
6. Investigations and Follow-Ups (44 call types)
7. Juvenile-Related Incidents (16 call types)
8. Public Safety and Welfare (85 call types)
9. Regulatory and Ordinance (31 call types)
10. Special Operations and Tactical (19 call types)
11. Traffic and Motor Vehicle (57 call types)

**Note:** The reference file includes an `Incident_Norm` column for normalized incident type matching, with E.D.P. variations (E.D.P., EDP, edp, etc.) all mapping to "Mental Health Incident".

## Schema Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-15 | Initial mapping schema with primary key matching |
| 2.0 | 2025-12-30 | Added multi-column matching strategies, confidence scoring, enhanced audit fields |
