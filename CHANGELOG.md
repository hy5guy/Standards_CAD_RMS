# Changelog

All notable changes to this Standards folder (structure and key artifacts) will be documented here.

## [v3.1.0] - 2026-04-10

### Documentation Refresh & Session Tooling

#### Standards Audit Phases 1-3 Complete (2026-04-09)
- **Normalization maps extracted** from hardcoded Python dicts to standalone JSON in `CAD_RMS/mappings/`:
  - `how_reported_normalization_map.json` (140 entries -> 12 canonical targets)
  - `disposition_normalization_map.json` (55 entries -> 20 canonical targets)
- **Schema registry updated** to v1.1.0: HowReported enum expanded 6 -> 12 canonical values; Walk-in corrected to Walk-In
- **transformation_spec.json** field name discrepancies fixed (TimeOfCall, Hour_Calc, PDZone/Zone)
- **Shim sync tooling added**: `scripts/sync_udd_shim.py` + `scripts/shim_sync_manifest.json`
- Full audit trail: `docs/ai_handoff/Phase1_Standards_Audit.md`

#### Documentation Updates (2026-04-10)
- **CLAUDE.md rewritten** (v2.0.0): accurate repo-centric documentation replacing stale cross-repo references
- **README.md updated**: added missing directories (SCRPA, Processed_Exports, scripts, .claude), removed hardcoded Windows paths
- **SUMMARY.md modernized**: replaced stale v1.0-v1.2.2 "Recent Enhancements" with current milestone summary
- **SCHEMA_FILES_SUMMARY.md updated**: corrected date header, added normalization maps section, updated schema registry version to v1.1.0

#### Session Start Hook Added
- `.claude/hooks/session-start.sh`: runs on Claude Code web session start
  - Installs Python dependencies from `requirements.txt`
  - Displays Standards VERSION
  - Runs `sync_udd_shim.py --dry-run` for shim drift detection
  - Reports git branch and uncommitted changes
- `.claude/settings.json`: registers SessionStart hook

---

## [v3.0.0] - 2026-03-17

### Repository Rationalization

Comprehensive consolidation and cleanup of the Standards repository. Reduced root-level clutter from 50+ files to ~12 essential files. Established `CAD_RMS/DataDictionary/current/schema/` as the single source of truth for all cross-system schemas and mappings.

#### Schema Consolidation
- **Promoted 5 schemas** from `unified_data_dictionary/schemas/` to `CAD_RMS/DataDictionary/current/schema/`: `canonical_schema.json`, `cad_fields_schema_latest.json`, `rms_fields_schema_latest.json`, `transformation_spec.json`, `cad_rms_schema_registry.yaml`
- **Promoted 12 mapping files** from `unified_data_dictionary/mappings/` to `CAD_RMS/mappings/`
- **Created compatibility shim**: `unified_data_dictionary/schemas/` retains 4 files for `schemas.yaml` backward compatibility

#### Archives Created
- `archive/PD_BCI_01_versions/` - 64 frozen v0.2.1 files from initial AI setup session
- `archive/schemas_udd_20260317/` - 6 older/duplicate schema files from `schemas/udd/`
- `archive/mappings_field_mappings_20260317/` - 12 v1.0 field mapping files
- `archive/unified_data_dictionary_20260317/` - UDD bulk content (docs, scripts, src, tests, etc.)
- `archive/root_loose_files_20260317/` - 10 root-level data dict/reference files
- `archive/completed_planning/` - 7 completed planning/merge docs
- `archive/directory_trees/` - 6 historical tree snapshots

#### Cleanup
- **Deleted** 4 OneDrive "(1)" sync artifacts from `RMS/`
- **Removed** empty placeholder directories: `FBI_UCR/`, `StateReporting/`, `tools/`
- **Archived** v1.0 field maps from `CAD/DataDictionary/current/schema/` (superseded by CAD_RMS v2.0)
- **Moved** `image/` to `docs/image/`, `task_templates/` to `docs/task_templates/`

#### Documentation Reorganized
- **10 AI handoff docs** (OPUS_*, CURSOR_*, CONTEXT_*) moved to `docs/ai_handoff/`
- **6 data quality crisis docs** moved from `CAD/DataDictionary/current/` to `docs/data_quality/`
- **2 ResponseTime docs** moved to `docs/response_time/`

#### Breaking Changes for Consumers
- `mappings/field_mappings/mapping_rules.md` moved to `CAD_RMS/mappings/mapping_rules.md` - update `schemas.yaml` `field_rules` path
- `schemas/udd/` directory removed (contents archived)
- `unified_data_dictionary/` slimmed to 4-file schemas-only shim

---

## [v2.0.0] - 2026-01-15

### Repository Restructuring

Major cleanup and reorganization of the Standards repository.

#### Changes

**Nested Git Repository Removed**
- Removed nested `.git/` from `unified_data_dictionary/`
- Repository now has single `.git/` at root
- Backup of nested git saved to `archive/legacy_copies/udd_git_backup/`

**Archive Structure Created**
- New `archive/` directory with subdirectories:
  - `packages/` - Packaging artifacts (Standards.7z moved here)
  - `legacy_copies/` - Legacy file versions
  - `removed_duplicates/` - Duplicate files removed during cleanup
- See `archive/README.md` for retention policy

**Duplicate Files Resolved**
- `CallType_Categories_backup_20260109_214115.csv` removed (duplicate of latest)
- Canonical locations established for mapping files:
  - `CAD_RMS/DataDictionary/current/schema/` for cad_to_rms, rms_to_cad mappings
  - `RMS/DataDictionary/current/schema/` for rms_export_field_definitions.md
- Pointer files added in `unified_data_dictionary/` pointing to canonical locations

**Legacy Files Archived**
- Root-level legacy mapping files moved to `archive/legacy_copies/`:
  - `cad_to_rms_field_map.json` (older version)
  - `rms_to_cad_field_map.json` (older version)
  - `multi_column_matching_strategy.md` (older version)

**Chatlog Structure Flattened**
- 9 nested chatlog folders flattened from `chunked/<topic>/<timestamp>_<topic>/` to `chunked/<timestamp>_<topic>/`

**unified_data_dictionary Integrated**
- Content from previously nested repository now part of main repo

---

## [v1.2.2] - 2026-01-14

### Added
- **Response Time Filter Configuration**
  - New config directory: `config/`
  - Added `config/response_time_filters.json` - JSON configuration for Response Time ETL filtering rules
  - Configuration includes:
    - How Reported exclusions (Self-Initiated)
    - Category_Type exclusions (4 categories: Regulatory/Ordinance, Admin/Support, Investigations, Community Engagement)
    - Specific incident exclusions (41 incidents)
    - Inclusion overrides (14 incidents kept despite category exclusion)
  - Source: `Master_Automation/config/response_time_filters.json`
  - Used by: `02_ETL_Scripts/Response_Times/response_time_monthly_generator.py` (v2.0.0)

---

## [v1.2.1] - 2026-01-09

### Added
- **Backup Strategy for CallType_Categories.csv**
  - Timestamped backups created in both CallTypes directory and Standards directory
  - Backup script: `scripts/backup_calltype_categories.py` (in Year-End Report project)
  - Backups created: `CallType_Categories_backup_YYYYMMDD_HHMMSS.csv`
  - "Latest" copy maintained in Standards directory: `CallType_Categories_latest.csv`
  - Backup locations:
    - Primary: `09_Reference/Classifications/CallTypes/` (same directory as source)
    - Secondary: `09_Reference/Standards/` (centralized reference location)

### Updated
- **Documentation** - Updated category counts in README.md and call_type_category_mapping.md to reflect actual counts (122 Admin/Support, 201 Criminal Incidents, 85 Public Safety, etc.)

## [v1.2.0] - 2026-01-08

### Fixed
- **Standardized to 11 ESRI Categories Only**
  - Fixed category mapping: All entries now use only the 11 ESRI standard categories
  - Mapped non-standard categories to ESRI standard:
    - "Miscellaneous" → "Public Safety and Welfare" (14 entries)
    - "Uncategorized" → "Public Safety and Welfare" (4 entries)
    - "Criminal Investigation" → "Criminal Incidents" (39 entries)
    - "Patrol and Prevention" → "Public Safety and Welfare" (8 entries)
    - "Community Engagement and Services" → "Community Engagement" (2 entries)
  - Total categories reduced from 16 to 11 (ESRI standard)
  - **ESRI Standard Categories** (11 total):
    1. Administrative and Support
    2. Assistance and Mutual Aid
    3. Community Engagement
    4. Criminal Incidents
    5. Emergency Response
    6. Investigations and Follow-Ups
    7. Juvenile-Related Incidents
    8. Public Safety and Welfare
    9. Regulatory and Ordinance
    10. Special Operations and Tactical
    11. Traffic and Motor Vehicle

### Added
- **Added 9 Remaining Unmatched Types from 2023 RMS Processing**
  - Missing Person- Return → Investigations and Follow-Ups
  - Motor Vehicle Theft → Criminal Incidents
  - Duty to Warn-E.D.P. → Public Safety and Welfare
  - FERPO/TERPO → Emergency Response
  - Handle With Care → Emergency Response
  - Medical Emergency → Public Safety and Welfare
  - Evidence Delivery / Retrieval → Investigations and Follow-Ups
  - (Child Safety Seat Installation...) → Community Engagement
  - Invasion of Privacy → Criminal Incidents
  - Total entries: 649 (up from 640)

## [v1.1.0] - 2026-01-08

### Updated
- **Call Type to Category Type Mapping System - Single Source of Truth**
  - Primary reference file renamed: `CallType_Categories_.csv` → `CallType_Categories.csv` (removed underscore)
  - Now includes `Incident_Norm` column for normalized incident type matching
  - Total entries increased from 516 to 640 entries
  - Added missing entries from archive file
  - Updated E.D.P. mappings: All E.D.P. variations (E.D.P., EDP, edp, e.d.p., etc.) now map to "Mental Health Incident"
    - Category: "Public Safety and Welfare"
    - Response: "Emergency"
    - Incident_Norm: "Mental Health Incident"
  - Format: Incident, Incident_Norm, Category_Type, Response_Type
  - **Single Source of Truth**: This file is now the authoritative reference for all Call Type classifications
  - Location: `09_Reference/Classifications/CallTypes/CallType_Categories.csv`

### Notes
- Old file `CallType_Categories_.csv` removed (replaced by `CallType_Categories.csv`)
- All scripts should reference `CallType_Categories.csv` (without underscore)
- Incident_Norm column enables better fuzzy matching and normalization
- E.D.P. variations are now properly categorized as Mental Health Incidents

## [v1.0.0] - 2026-01-08

### Added
- **Call Type to Category Type Mapping System**
  - Primary reference file: `CallType_Categories_.csv` (516 entries) - ESRI standardized classification
    - Location: `09_Reference/Classifications/CallTypes/CallType_Categories_.csv`
    - Format: Call_Type, Category, Response Type
    - 11 standardized categories based on ESRI classification system
    - 3 Response Types (Emergency, Urgent, Routine)
  - Documentation: `docs/call_type_category_mapping.md`
    - Complete breakdown of all Call Types organized by Category Type
    - Human-readable format with statistics and response type distributions
  - Category-specific CSV files: `mappings/call_types_*.csv` (11 files)
    - One file per category for targeted script loading
    - Files: administrative_and_support, assistance_and_mutual_aid, community_engagement, criminal_incidents, emergency_response, investigations_and_follow-ups, juvenile-related_incidents, public_safety_and_welfare, regulatory_and_ordinance, special_operations_and_tactical, traffic_and_motor_vehicle
  - JSON mapping file: `mappings/call_type_category_mapping.json`
    - Programmatic lookup dictionaries for Python scripts
    - Includes: `call_type_to_category`, `call_type_to_response`, `category_to_call_types`
    - Metadata: total count, categories list, response types list
  - Purpose: Streamline knowledge base with script-referenceable files for RMS Incident Type classification, filtering admin reports vs calls for service, and standardized categorization

### Notes
- All files are script-referenceable and ready for use across ETL projects
- Standardized filename (`CallType_Categories_.csv`) for consistent script references
- ESRI format maintained for compatibility with existing systems

## [v0.3.0] - 2025-12-30

### Added
- **RMS Export Field Definitions** (`rms_export_field_definitions.md`)
  - Comprehensive documentation of 29 RMS export fields
  - Organized into 8 logical groups: Incident Identification, Temporal, Incident Classification, Location, Incident Details, Property, Vehicle, Personnel, and Case Management
  - Each field includes: Export Header, Standard Name, Definition, Source Field, Format/Regex, Logic, Validation Rules, Mapping Notes, and Group classification
  - Special narrative extraction logic for deriving suspect descriptions, vehicle details, property information, and modus operandi (M.O.)
  - Multi-column matching strategy usage summary showing which RMS fields are used in each matching strategy
  - Data quality validation rules summary organized by field group
  - Integration references to `rms_to_cad_field_map_v2_enhanced.json` and `multi_column_matching_strategy.md`

### Enhanced
- **CAD Export Field Definitions** (`CAD/DataDictionary/current/schema/cad_export_field_definitions.md`)
  - Finalized draft v1.0 comprehensive CAD export field definitions and validation rules
  - Cross-referenced with RMS definitions and mapping schemas
  - Standardized field naming conventions and validation patterns
- Updated `README.md` with reference to comprehensive RMS field definitions
- Updated `SUMMARY.md` to reflect new schema documentation
- Enhanced cross-referencing between CAD and RMS schema documentation

## 2025-12-15

- Created CAD/RMS/CAD_RMS `DataDictionary/` scaffolding:
  - `current/schema`, `current/domains`, `current/defaults`
  - `archive`, `templates`, `scripts`
- Added root documentation files:
  - `README.md`, `SUMMARY.md`, `CHANGELOG.md`
- Added per-DataDictionary documentation files:
  - `CAD/DataDictionary/{README.md,SUMMARY.md,CHANGELOG.md}`
  - `RMS/DataDictionary/{README.md,SUMMARY.md,CHANGELOG.md}`
  - `CAD_RMS/DataDictionary/{README.md,SUMMARY.md,CHANGELOG.md}`
- Added bootstrap scaffolding + placement script:
  - `CAD_RMS/DataDictionary/scripts/init_cad_rms_standards.ps1`
- Copied cross-system field maps into the canonical cross-system location:
  - `CAD_RMS/DataDictionary/current/schema/cad_to_rms_field_map.json`
  - `CAD_RMS/DataDictionary/current/schema/rms_to_cad_field_map.json`
- Initialized local Git repository:
  - `.git/` created (branch `main`)
  - `.gitignore` added

## 2025-12-17

- Added CAD export field definitions / validation rules (draft):
  - `CAD/DataDictionary/current/schema/cad_export_field_definitions.md`
- Updated summaries to reference the new CAD definitions document.
