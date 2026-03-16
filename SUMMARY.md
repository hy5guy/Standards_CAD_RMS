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

## What exists now

- **CAD** - `cad_export_field_definitions.md` (Draft v1.0, finalized 2025-12-30)
- **RMS** - `rms_export_field_definitions.md` (29 fields, 8 functional groups)
- **Cross-system** - 8 files in `CAD_RMS/DataDictionary/current/schema/` + 12 mapping files in `CAD_RMS/mappings/`
- **Call Type Classification** - 649 entries, 11 ESRI categories, JSON + CSV + per-category files
- **ETL Configuration** - `config/response_time_filters.json`
- **Documentation** - Organized under `docs/` (ai_handoff, chat_logs, data_quality, merge, response_time, image, task_templates)

## Recent Enhancements

### 🚀 Response Time Filter Configuration v1.2.2 (2026-01-14)

**ETL Configuration Added**
- New `config/` directory created for ETL configuration files
- Added `config/response_time_filters.json` - JSON configuration for Response Time ETL filtering rules
- Used by Response Time Monthly Generator script (v2.0.0)
- Configuration includes:
  - How Reported exclusions (Self-Initiated)
  - Category_Type exclusions (4 categories)
  - Specific incident exclusions (41 incidents)
  - Inclusion overrides (14 incidents kept despite category exclusion)

### 🚀 Call Type to Category Type Mapping v1.2.1 (2026-01-09)

**Backup Strategy Added**
- Timestamped backups created automatically in both CallTypes directory and Standards directory
- Backup script available: `scripts/backup_calltype_categories.py`
- "Latest" copy maintained in Standards directory for quick access

### 🚀 Call Type to Category Type Mapping v1.2.0 (2026-01-08)

**Category Standardization Complete**
- All categories standardized to 11 ESRI standard categories only
- Non-standard categories mapped to ESRI equivalents
- Added 9 remaining unmatched types (total now 649 entries)

### 🚀 Call Type to Category Type Mapping v1.0 (2026-01-08)

**Call Type Classification System - Added**
- **Primary Reference File**: `CallType_Categories.csv` (649 entries) - ESRI standardized classification - **Single Source of Truth**
  - Location: `09_Reference/Classifications/CallTypes/CallType_Categories.csv`
  - Format: Incident, Incident_Norm, Category_Type, Response_Type
  - Includes Incident_Norm column for normalized matching
  - E.D.P. variations (E.D.P., EDP, edp, etc.) all map to "Mental Health Incident"
  - **11 ESRI Standard Categories Only**: All non-standard categories have been mapped to ESRI standard
  - 11 standardized categories (Administrative and Support, Assistance and Mutual Aid, Community Engagement, Criminal Incidents, Emergency Response, Investigations and Follow-Ups, Juvenile-Related Incidents, Public Safety and Welfare, Regulatory and Ordinance, Special Operations and Tactical, Traffic and Motor Vehicle)
  - 3 Response Types (Emergency, Urgent, Routine)
- **Documentation**: `docs/call_type_category_mapping.md` - Complete breakdown of all Call Types by Category Type
- **Category-Specific Files**: 11 CSV files in `mappings/call_types_*.csv` for targeted script loading
- **JSON Mapping**: `mappings/call_type_category_mapping.json` - Programmatic lookup dictionaries
  - `call_type_to_category`: Quick category lookup
  - `call_type_to_response`: Response type lookup
  - `category_to_call_types`: All call types per category
- **Purpose**: Streamline knowledge base with script-referenceable files for RMS Incident Type classification and filtering

### 🚀 Schema Documentation v0.3.0 (2025-12-30)

**CAD Export Field Definitions - Finalized (Draft v1.0)**
- Comprehensive CAD export field definitions and validation rules
- Field-by-field documentation with export header to standard name mapping
- Validation rules, formats, and allowed values for all CAD export fields (ReportNumberNew, Incident, HowReported, temporal fields, location fields, etc.)
- Temporal field derivation logic and standard naming conventions
- Cross-referenced with RMS field definitions for integration

**RMS Export Field Definitions - Added (v1.0)**
- Comprehensive RMS export schema documentation
  - 29 documented fields across 8 functional categories
  - Groups: Incident Identification, Temporal, Incident Classification, Location, Incident Details, Property, Vehicle, Personnel, Case Management
  - Each field includes validation rules, format patterns, CAD mapping references, and multi-column matching strategy usage
  - Special narrative extraction logic for deriving suspect descriptions, vehicle details, property information, and M.O.
  - Integrated with `rms_to_cad_field_map_v2_enhanced.json` and multi-column matching strategies
  - Data quality validation rules summary organized by field group
