# Standards Repository Rationalization Manifest

**Date:** 2026-03-17
**Version:** v3.0.0
**Executed by:** Claude Opus 4.6

---

## Summary

Comprehensive repository rationalization consolidating fragmented schemas, mappings, and documentation into a clean structure with `CAD_RMS/DataDictionary/current/schema/` as the single source of truth.

## Operations Performed

### Phase 2: Promotions (COPY)

| Source | Destination |
|--------|------------|
| `unified_data_dictionary/schemas/canonical_schema.json` | `CAD_RMS/DataDictionary/current/schema/canonical_schema.json` |
| `unified_data_dictionary/schemas/cad_fields_schema_latest.json` | `CAD_RMS/DataDictionary/current/schema/cad_fields_schema_latest.json` |
| `unified_data_dictionary/schemas/rms_fields_schema_latest.json` | `CAD_RMS/DataDictionary/current/schema/rms_fields_schema_latest.json` |
| `unified_data_dictionary/schemas/transformation_spec.json` | `CAD_RMS/DataDictionary/current/schema/transformation_spec.json` |
| `unified_data_dictionary/schemas/cad_rms_schema_registry.yaml` | `CAD_RMS/DataDictionary/current/schema/cad_rms_schema_registry.yaml` |
| `unified_data_dictionary/mappings/` (12 non-PD_BCI files) | `CAD_RMS/mappings/` |

### Phase 2: Doc Relocations (MOVE)

| Source | Destination |
|--------|------------|
| 10 AI handoff docs (OPUS_*, CURSOR_*, CONTEXT_*, etc.) | `docs/ai_handoff/` |
| 6 crisis docs from `CAD/DataDictionary/current/` | `docs/data_quality/` |
| 2 ResponseTime docs | `docs/response_time/` |

### Phase 3: Archives (MOVE)

| Source | Destination | Count |
|--------|------------|-------|
| -PD_BCI_01 files across repository | `archive/PD_BCI_01_versions/` | 64 files |
| `schemas/udd/*` | `archive/schemas_udd_20260317/` | 6 files |
| `mappings/field_mappings/*` | `archive/mappings_field_mappings_20260317/` | 12 files |
| `CAD/.../schema/cad_to_rms_field_map.json`, `rms_to_cad_field_map.json` | `CAD/DataDictionary/archive/` | 2 files |
| Root data dict/reference files | `archive/root_loose_files_20260317/` | 10 files |
| Root planning docs | `archive/completed_planning/` | 7 files |
| Directory tree snapshots | `archive/directory_trees/` | 6 files |
| UDD bulk (everything except schemas/ shim) | `archive/unified_data_dictionary_20260317/` | 25 items |
| `image/` | `docs/image/` | 1 dir |
| `task_templates/` | `docs/task_templates/` | 1 dir |
| `templates/udd/README.md` | `archive/root_loose_files_20260317/` | 1 file |

### Phase 3: Deletes

| Path | Reason |
|------|--------|
| `RMS/DataDictionary/CHANGELOG (1).md` | OneDrive sync artifact |
| `RMS/DataDictionary/README (1).md` | OneDrive sync artifact |
| `RMS/DataDictionary/SUMMARY (1).md` | OneDrive sync artifact |
| `RMS/SCRPA/rms_data_quality_report (1).md` | OneDrive sync artifact |
| `FBI_UCR/` | Empty placeholder |
| `StateReporting/` | Empty placeholder |
| `tools/` | Empty placeholder |
| `templates/` | Empty after content archived |
| `schemas/` | Empty after content archived |

### Phase 5: Documentation Updates

| File | Change |
|------|--------|
| `CLAUDE.md` | Updated architecture, consolidation status, path resolution, version history |
| `README.md` | New directory structure, canonical locations table, shim note |
| `CHANGELOG.md` | Added v3.0.0 rationalization entry |
| `SUMMARY.md` | New structure reflecting v3.0.0 |
| `SCHEMA_FILES_SUMMARY.md` | Updated canonical paths, deprecated paths, shim documentation |
| `schemas.yaml` (external) | Updated `field_rules` path, version to v3.0.0 |

## Validation Results

- All schemas.yaml paths resolve: PASS
- mapping_rules.md in CAD_RMS/mappings/: PASS
- No PD_BCI_01 files outside archive: PASS (0 found)
- No "(1)" sync artifacts in active dirs: PASS (7 remain in archive/ — acceptable)
- transformation_spec.json uses "FullAddress" in both locations: PASS
- Shim files byte-identical to CAD_RMS canonical: PASS (all 4)
- Empty placeholders removed: PASS

## Git Commits

1. `c295bf9` - Checkpoint before Standards rationalization 2026-03-17
2. `243ea98` - Phase 2: Promote schemas/mappings to CAD_RMS, organize documentation
3. `b32026f` - Phase 3: Archive duplicates, PD_BCI_01 files, and slim UDD to shim
4. (Phase 5 commit pending)

## Rollback

To revert all changes: `git reset --hard c295bf9`
