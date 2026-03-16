# Schema Files Summary - CAD-RMS Integration

**Date**: 2025-12-30  
**Purpose**: Summary of all schema, mapping, and definition files created for CAD-RMS integration

---

## File Locations

All files have been created and/or copied to the appropriate directories under:
```
C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\
```

---

## Primary Locations

### 1. CAD-RMS Cross-System Mapping Schemas

**Directory**: `CAD_RMS/DataDictionary/current/schema/`

- **`cad_to_rms_field_map.json`** (v2.0)
  - Enhanced CAD-to-RMS mapping with multi-column matching strategies
  - Includes primary key matching and 3 alternative matching strategies
  - Confidence scoring and audit fields

- **`rms_to_cad_field_map.json`** (v2.0)
  - Enhanced RMS-to-CAD mapping (mirror of CAD-to-RMS)
  - Same multi-column matching strategies

- **`multi_column_matching_strategy.md`**
  - Comprehensive guide to multi-column matching
  - Implementation examples and workflow
  - Quality assurance procedures

- **`README.md`**
  - Documentation for the schema directory
  - Version history and usage guidelines

### 2. RMS Field Definitions

**Directory**: `RMS/DataDictionary/current/schema/`

- **`rms_export_field_definitions.md`** (v1.0 - Root-level comprehensive documentation)
  - Comprehensive RMS schema documentation (29 fields, grouped by 8 functional categories)
  - Field names, types, formats, regex patterns, validation rules
  - Mapping logic and CAD integration notes
  - Multi-column matching strategy usage
  - Narrative extraction hints for suspect descriptions, vehicle details, property info, and M.O.

- **`README.md`**
  - Documentation for RMS schema directory

### 3. Unified Schemas (Promoted from UDD - 2026-03-17)

**Directory**: `CAD_RMS/DataDictionary/current/schema/`

- **`canonical_schema.json`** (v1.0.0) - Unified CAD/RMS field dictionary (100+ fields)
- **`cad_fields_schema_latest.json`** (v1.0) - CAD export field schema
- **`rms_fields_schema_latest.json`** (v1.0) - RMS export field schema
- **`transformation_spec.json`** (v1.0.0) - ETL transformation rules (uses "FullAddress"/"Zone")
- **`cad_rms_schema_registry.yaml`** (v2.0) - Schema registry with canonical HowReported domain values

### 3b. Legacy CAD Mapping Schemas (ARCHIVED 2026-03-17)

**Directory**: `CAD/DataDictionary/archive/`

- v1.0 field maps archived (superseded by CAD_RMS v2.0)

### 4. Summary Documentation

**Directory**: `CAD_RMS/DataDictionary/`

- **`SCHEMA_ENHANCEMENT_SUMMARY.md`**
  - Comprehensive summary of all enhancements
  - File locations, features, benefits
  - Integration guidance and next steps

---

## Compatibility Shim (schemas.yaml backward compatibility)

**Directory**: `unified_data_dictionary/schemas/`

> **Note (2026-03-17)**: Following repository rationalization, `unified_data_dictionary/` has been
> slimmed to a 4-file compatibility shim. Bulk content archived to `archive/unified_data_dictionary_20260317/`.
> Mapping pointer files promoted to `CAD_RMS/mappings/`.

These 4 files are referenced by `02_ETL_Scripts/cad_rms_data_quality/config/schemas.yaml`:
- `canonical_schema.json` - identical to `CAD_RMS/DataDictionary/current/schema/canonical_schema.json`
- `cad_fields_schema_latest.json` - identical to `CAD_RMS/DataDictionary/current/schema/cad_fields_schema_latest.json`
- `rms_fields_schema_latest.json` - identical to `CAD_RMS/DataDictionary/current/schema/rms_fields_schema_latest.json`
- `transformation_spec.json` - identical to `CAD_RMS/DataDictionary/current/schema/transformation_spec.json`

**Do not modify these files directly.** Update the CAD_RMS canonical copy and re-sync the shim.

---

## File Summary Table

| File | Canonical Location | Pointer in unified_data_dictionary | Purpose |
|------|-------------------|-----------------------------------|---------|
| `cad_to_rms_field_map.json` (v2.0) | `CAD_RMS/DataDictionary/current/schema/` | `mappings/cad_to_rms_field_map_v2_enhanced.md` | Enhanced CAD-to-RMS mapping schema |
| `rms_to_cad_field_map.json` (v2.0) | `CAD_RMS/DataDictionary/current/schema/` | `mappings/rms_to_cad_field_map_v2_enhanced.md` | Enhanced RMS-to-CAD mapping schema |
| `multi_column_matching_strategy.md` | `CAD_RMS/DataDictionary/current/schema/` | `mappings/multi_column_matching_strategy_POINTER.md` | Multi-column matching guide |
| `rms_export_field_definitions.md` | `RMS/DataDictionary/current/schema/` | `docs/rms_export_field_definitions_POINTER.md` | RMS field definitions |
| `canonical_schema.json` (v1.0.0) | `CAD_RMS/DataDictionary/current/schema/` | `unified_data_dictionary/schemas/` (shim) | Unified field dictionary |
| `cad_fields_schema_latest.json` | `CAD_RMS/DataDictionary/current/schema/` | `unified_data_dictionary/schemas/` (shim) | CAD export field schema |
| `rms_fields_schema_latest.json` | `CAD_RMS/DataDictionary/current/schema/` | `unified_data_dictionary/schemas/` (shim) | RMS export field schema |
| `transformation_spec.json` | `CAD_RMS/DataDictionary/current/schema/` | `unified_data_dictionary/schemas/` (shim) | ETL transformation rules |
| `cad_rms_schema_registry.yaml` | `CAD_RMS/DataDictionary/current/schema/` | N/A | Schema registry with domain values |
| `SCHEMA_ENHANCEMENT_SUMMARY.md` | `CAD_RMS/DataDictionary/` | N/A | Enhancement summary |
| `README.md` (CAD-RMS) | `CAD_RMS/DataDictionary/current/schema/` | N/A | Schema directory documentation |
| `README.md` (RMS) | `RMS/DataDictionary/current/schema/` | N/A | RMS schema directory documentation |

---

## Usage Recommendations

### For New Development

Use the enhanced v2.0 schemas located in:
- `CAD_RMS/DataDictionary/current/schema/cad_to_rms_field_map.json`
- `CAD_RMS/DataDictionary/current/schema/rms_to_cad_field_map.json`

These schemas include:
- Multi-column matching strategies
- Confidence scoring
- Enhanced audit fields

### For Backward Compatibility

The legacy v1.0 schemas have been archived to `CAD/DataDictionary/archive/` (2026-03-17). Use the v2.0 schemas in `CAD_RMS/DataDictionary/current/schema/` for all new and existing code.

### For Reference

- **RMS field definitions**: `rms_export_field_definitions.md` (v1.0 - Comprehensive with 29 fields, validation rules, and mapping logic)
- **CAD field definitions**: `CAD/DataDictionary/current/schema/cad_export_field_definitions.md`
- **Matching strategy guide**: `multi_column_matching_strategy.md`

---

## Related Files

### Existing Documentation

- **CAD Field Definitions**: `CAD/DataDictionary/current/schema/cad_export_field_definitions.md`
- **Mapping Rules**: `CAD_RMS/mappings/mapping_rules.md`
- **RMS Field Map**: `CAD_RMS/mappings/rms_field_map_latest.json`
- **CAD Field Map**: `CAD_RMS/mappings/cad_field_map_latest.json`

---

## Maintenance Notes

- All files use consistent naming conventions
- Version numbers are included in schema files (v1.0 vs v2.0)
- Legacy schemas are maintained for backward compatibility
- **Canonical locations** are established in CAD_RMS/ and RMS/ DataDictionary folders
- **Pointer files** in unified_data_dictionary reference canonical locations (no duplicates)
- All JSON files are valid and lint-free

---

## Change Log

| Date | Changes |
|------|---------|
| 2025-12-30 | Initial file creation and organization |
| 2025-12-30 | Enhanced schemas (v2.0) created with multi-column matching |
| 2025-12-30 | RMS field definitions document created |
| 2025-12-30 | Files copied to unified_data_dictionary directory |
| 2026-01-15 | Repository restructuring: duplicates replaced with pointer files |
| 2026-03-17 | Repository rationalization: schemas promoted to CAD_RMS, UDD slimmed to shim, v1.0 maps archived |
