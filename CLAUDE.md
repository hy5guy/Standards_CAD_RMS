## Enhanced CLAUDE.md for AI Agents

Here's an improved version that combines Gemini's structure with the technical accuracy from our deep dive:

---

# Claude.md — CAD/RMS Data Quality System AI Agent Protocol

**Version:** 1.3.4  
**Last Updated:** 2026-02-04  
**Purpose:** Context and operational guidelines for AI agents working on this codebase

---

## 🚨 CRITICAL UPDATE - 2026-02-04

### Emergency Status: Dashboard Data Quality Crisis

**IMMEDIATE PRIORITY:** Phase 1 - Dashboard Data Fix (2 hours)
- **Problem:** Dashboard showing invalid HowReported values (`hackensack`, `ppp`, `u`, `Phone/911`, etc.)
- **Root Cause:** CAD baseline was consolidated but NOT normalized (ESRI polishing step skipped)
- **Solution:** Re-run `enhanced_esri_output_generator.py` with updated mappings
- **Status:** ✅ Mappings added (HACKENSACK, PHONE/911), ready to execute

**SECONDARY PRIORITY:** Phase 2 - Repository Consolidation (3-4 hours, execute tomorrow)
- **Plan:** See `CURSOR_AI_CONSOLIDATION_GUIDE.md` in this directory
- **Status:** 60% complete (CAD/, RMS/, CAD_RMS/ structure exists, unified_data_dictionary/ needs archival)

### 4 Critical Decisions Made (Authority for AI Agents)

1. **Which mapping format is authoritative?**
   - **ANSWER: A (with additions) - CAD_RMS v2.0 (2025-12-30) + dashboard validation fixes**
   - Rationale: Most recent, includes multi-column matching, 280 lines comprehensive
   - Location: `enhanced_esri_output_generator.py` HOW_REPORTED_MAPPING (lines 137-299)

2. **How to handle -PD_BCI_01 suffixed files?**
   - **ANSWER: A - Archive all (scripts reference non-suffixed versions)**
   - Rationale: Non-suffixed are actively maintained (v1.3.2), PD_BCI are frozen (v0.2.1)
   - Action: Move to `archive/PD_BCI_01_versions/`

3. **When to do comprehensive validation?**
   - **ANSWER: B - Consolidate first, THEN comprehensive validation**
   - Rationale: Need single dataset to validate; validation reveals gaps in normalization
   - Workflow: Consolidate → Validate → Fix mappings → Re-polish → Validate again

4. **How thorough should schema validation be?**
   - **ANSWER: A - Quick review of critical fields only**
   - Rationale: Dashboard is live with issues; fix critical fields (HowReported, Disposition, Incident) first
   - Defer: Comprehensive vendor documentation review and stakeholder workshops

**⚠️ DO NOT START PHASE 2 UNTIL PHASE 1 COMPLETE AND DASHBOARD VALIDATED**

---

## 🎯 Mission & Critical Constraints

### Primary Objectives
1. **Production Dashboard Integrity:** Support ArcGIS Pro "Calls for Service" dashboard with clean, normalized data
2. **Data Quality:** Maintain 99.9% field completeness, 100% domain compliance in ESRI outputs
3. **Single Source of Truth:** Consolidate fragmented standards into unified, maintainable structure

### High-Stakes Context
- **Active Production System:** 724,794 CAD records (2019-2026) feeding live dashboard
- **Zero Downtime Tolerance:** Dashboard updates must not introduce bad data
- **Geographic Impact:** Data drives police resource allocation decisions
- **Compliance Requirements:** Case number format (YY-NNNNNN) must preserve leading zeros

---

## 🏗️ Repository Architecture

### Current Active Repositories (DO NOT ARCHIVE)

```
02_ETL_Scripts/
├── cad_rms_data_quality/              # THIS REPO - Quality validation & consolidation
│   ├── config/                        # Configuration files
│   │   ├── schemas.yaml               # Points to 09_Reference/Standards
│   │   ├── validation_rules.yaml      # Domain validation rules
│   │   └── consolidation_sources.yaml # CAD/RMS source file registry
│   ├── consolidate_cad_2019_2026.py   # Production consolidation script
│   ├── monthly_validation/scripts/    # CAD/RMS monthly validators
│   └── shared/utils/                  # Shared utilities
│
└── CAD_Data_Cleaning_Engine/          # CRITICAL - Normalization engine
    └── scripts/
        └── enhanced_esri_output_generator.py  # 🔥 AUTHORITATIVE normalization logic
            # Lines 137-297: HOW_REPORTED_MAPPING (280 entries)
            # This is the SINGLE SOURCE OF TRUTH for field normalization
```

### Canonical Standards Location (v3.0.0 - Rationalized 2026-03-17)

```
09_Reference/Standards/                    # External authoritative schemas
├── CAD/DataDictionary/current/schema/     # CAD-specific: cad_export_field_definitions.md
├── RMS/DataDictionary/current/schema/     # RMS-specific: rms_export_field_definitions.md
├── Clery/DataDictionary/current/          # Clery Act: crime definitions, geography
├── NIBRS/DataDictionary/current/          # NIBRS: offense definitions, RMS-to-NIBRS map
├── Personnel/                             # Assignment Master schema
│
├── CAD_RMS/                               # 🎯 SINGLE SOURCE OF TRUTH
│   ├── DataDictionary/current/schema/     # ALL cross-system schemas:
│   │   ├── canonical_schema.json          #   Unified field dictionary (100+ fields)
│   │   ├── cad_fields_schema_latest.json  #   CAD export field schema
│   │   ├── rms_fields_schema_latest.json  #   RMS export field schema
│   │   ├── transformation_spec.json       #   ETL transformation rules
│   │   ├── cad_rms_schema_registry.yaml   #   Schema registry + domain values
│   │   ├── cad_to_rms_field_map.json      #   v2.0 (2025-12-30) - 280 lines
│   │   ├── rms_to_cad_field_map.json      #   v2.0 (2025-12-30) - 258 lines
│   │   └── multi_column_matching_strategy.md
│   └── mappings/                          # Field mapping rules, CSVs, policies
│
├── unified_data_dictionary/schemas/       # ⚠️ COMPATIBILITY SHIM ONLY
│   # 4 files for schemas.yaml backward compatibility
│   # Identical copies of CAD_RMS canonical versions
│   # Do NOT modify — update CAD_RMS copy and re-sync
│
└── archive/                               # All retired content (preserve-first)
```

### Processed Data Location

```
13_PROCESSED_DATA/ESRI_Polished/
├── base/
│   └── CAD_ESRI_Polished_Baseline.xlsx         # Dashboard data source
│       # 724,794 records | 559,202 unique cases
│       # Date range: 2019-01-01 to 2026-01-30
└── manifest.json                               # Latest file pointer
```

---

## ⚖️ Decision Logic & Version Authority

### When Multiple Versions Exist

**Field Mappings:**
- ✅ **AUTHORITATIVE:** `CAD_RMS/DataDictionary/current/schema/` (v2.0, 2025-12-30)
- ✅ **PROMOTED:** `CAD_RMS/mappings/` (mapping rules, field maps, CSVs — promoted from UDD)
- ❌ **ARCHIVED:** `CAD/DataDictionary/archive/` (v1.0 maps, archived 2026-03-17)
- ❌ **ARCHIVED:** `archive/mappings_field_mappings_20260317/` (v1.0 copies)

**Rationale:** v2.0 includes multi-column matching strategy and comprehensive edge case handling

**Normalization Rules:**
- ✅ **AUTHORITATIVE:** `CAD_Data_Cleaning_Engine/scripts/enhanced_esri_output_generator.py`
  - `HOW_REPORTED_MAPPING` (lines 137-297): 280 entries including typos, abbreviations, concatenations
  - `DISPOSITION_MAPPING`: 100+ disposition variants → 20 standard values
  - Advanced normalization functions for unmapped values

**Python Package Versions:**
- ✅ **AUTHORITATIVE:** `cad_rms_data_quality/pyproject.toml` (v1.3.2)
- ⚠️ **IGNORE:** Any `-PD_BCI_01` suffixed files (artifacts from initial AI setup session)

### Path Resolution Priority

1. **Check `config/schemas.yaml` first** - Contains canonical path mappings
2. **Relative paths from project root** - Preferred for portability
3. **Config.yaml variables** - For external Standards directory
4. **Never hardcode absolute paths** - Breaks on different machines

---

## 🔥 Critical Files & Their Purposes

### Never Modify Without Understanding Impact

| File | Purpose | Breaking This Affects |
|------|---------|----------------------|
| `CAD_Data_Cleaning_Engine/scripts/enhanced_esri_output_generator.py` | Field normalization for ESRI | Dashboard data quality |
| `13_PROCESSED_DATA/ESRI_Polished/base/CAD_ESRI_Polished_Baseline.xlsx` | Dashboard data source | Live production dashboard |
| `config/consolidation_sources.yaml` | Source file registry | Consolidation script execution |
| `config/validation_rules.yaml` | Domain validation rules | Monthly validation scoring |
| `09_Reference/Standards/CAD_RMS/DataDictionary/current/schemas/canonical_schema.json` | Master field definitions | Cross-system validation |

### Workflow-Critical Scripts

```python
# Consolidation workflow
consolidate_cad_2019_2026.py              # Step 1: Merge yearly + monthly files
→ CAD_Data_Cleaning_Engine/scripts/enhanced_esri_output_generator.py  # Step 2: Normalize & polish
→ scripts/copy_polished_to_processed_and_update_manifest.py           # Step 3: Deploy to 13_PROCESSED_DATA

# Monthly validation workflow
monthly_validation/scripts/validate_cad.py   # Validate new CAD exports
monthly_validation/scripts/validate_rms.py   # Validate new RMS exports
```

---

## 🧪 Validation Commands & Smoke Tests

### Pre-Deployment Validation

```powershell
# 1. Verify schema paths resolve
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\cad_rms_data_quality"
python -c "import yaml; print(yaml.safe_load(open('config/schemas.yaml')))"

# 2. Test normalization mapping loads
cd "..\CAD_Data_Cleaning_Engine"
python -c "from scripts.enhanced_esri_output_generator import HOW_REPORTED_MAPPING; print(f'Loaded {len(HOW_REPORTED_MAPPING)} mappings')"
# Expected output: Loaded 280 mappings (or higher if new mappings added)

# 3. Check for deprecated paths in codebase
Get-ChildItem -Recurse -Include *.py,*.yaml,*.bat,*.ps1 | Select-String "unified_data_dictionary" | Where-Object {$_.Line -notmatch "^#"}
# Should return ZERO results (or only comments)

# 4. Validate baseline file integrity
python scripts/verify_baseline.py
# Expected: Record count = 724794, No NaN dates, HowReported has only valid values
```

### Data Quality Validation

```python
# Quick HowReported domain check (after polishing)
import pandas as pd

df = pd.read_excel('13_PROCESSED_DATA/ESRI_Polished/base/CAD_ESRI_Polished_Baseline.xlsx')

valid_values = ['9-1-1', 'Phone', 'Walk-In', 'Self-Initiated', 'Radio', 
                'eMail', 'Mail', 'Other - See Notes', 'Fax', 'Teletype',
                'Virtual Patrol', 'Canceled Call']

invalid = df[~df['How Reported'].isin(valid_values)]['How Reported'].unique()
print(f"Invalid values: {len(invalid)}")
if len(invalid) > 0:
    print("❌ VALIDATION FAILED - Dashboard will show bad data")
    print(invalid)
else:
    print("✅ All HowReported values normalized correctly")
```

### Critical Field Completeness Check

```python
# Dashboard-critical fields must be ≥99% complete
critical_fields = ['ReportNumberNew', 'Incident', 'Time of Call', 
                   'FullAddress2', 'PDZone', 'How Reported', 'Disposition']

for field in critical_fields:
    completeness = (df[field].notna().sum() / len(df)) * 100
    status = "✅" if completeness >= 99.0 else "❌"
    print(f"{status} {field}: {completeness:.2f}%")
```

---

## 🚨 Common Pitfalls & How to Avoid Them

### Pitfall 1: Case Number Format Corruption

**Problem:** Excel converts `26-000001` to `26000001` (numeric), losing format  
**Solution:** Always force `ReportNumberNew` to string dtype on load:
```python
df = pd.read_excel(file, dtype={'ReportNumberNew': str})
# Then normalize: "26000001.0" → "26-000001"
```

**Validation:** `validate_cad.py` and `validate_rms.py` do this automatically (v1.2.6+)

### Pitfall 2: Skipping Normalization

**Problem:** Consolidation produces valid CSV, but ESRI baseline has raw typos  
**Reality Check:** `consolidate_cad_2019_2026.py` does NOT normalize - it only merges files  
**Solution:** Always run `enhanced_esri_output_generator.py` after consolidation

**Pipeline:**
```
consolidate_cad_2019_2026.py          # Merges files → raw CSV
↓
enhanced_esri_output_generator.py     # Normalizes fields → polished Excel
↓
Dashboard consumes polished Excel     # Shows clean data
```

### Pitfall 3: Overwriting Baseline Accidentally

**Problem:** Running incremental mode can corrupt baseline if not configured correctly  
**Safe Mode (Recommended):**
```powershell
python consolidate_cad_2019_2026.py --full  # Always rebuild from source
```

**Incremental Mode (Advanced - Use with caution):**
```yaml
# config/consolidation_sources.yaml
incremental:
  enabled: false  # Keep disabled unless you understand deduplication logic
```

### Pitfall 4: Mixing Schema Versions

**Problem:** Script references `unified_data_dictionary/schemas/` but files moved to `CAD_RMS/`  
**Detection:**
```powershell
# Find all references to deprecated paths
Get-ChildItem -Recurse *.py,*.yaml | Select-String "unified_data_dictionary/schemas"
```

**Fix:** Update paths to point to new structure:
```yaml
# config/schemas.yaml
schemas:
  canonical: "${standards_root}/CAD_RMS/DataDictionary/current/schemas/canonical_schema.json"
  cad: "${standards_root}/CAD/DataDictionary/current/schemas/cad_fields_schema_latest.json"
```

---

## 📋 Standards Repository Consolidation Status

### Current State (As of 2026-03-17)

**Repository Rationalization:** COMPLETE
- **v3.0.0** — Full rationalization executed 2026-03-17
- All schemas promoted to `CAD_RMS/DataDictionary/current/schema/`
- `unified_data_dictionary/` slimmed to 4-file compatibility shim
- 64 `-PD_BCI_01` files archived to `archive/PD_BCI_01_versions/`
- Duplicate schemas/mappings archived with date-stamped folders
- Root clutter reduced from 50+ to ~12 essential files
- `schemas.yaml` shim paths validated and functional

**Archive Contents:**
- `archive/PD_BCI_01_versions/` — 64 frozen v0.2.1 files
- `archive/unified_data_dictionary_20260317/` — UDD bulk content
- `archive/schemas_udd_20260317/` — Older duplicate schema copies
- `archive/mappings_field_mappings_20260317/` — v1.0 field mappings
- `archive/root_loose_files_20260317/` — Relocated root-level files
- `archive/completed_planning/` — Finished planning docs
- `archive/directory_trees/` — Historical tree snapshots

**Pending Action:**
- Update `schemas.yaml` `field_rules` path: `mappings/field_mappings/mapping_rules.md` → `CAD_RMS/mappings/mapping_rules.md`

**Related Documentation:**
- 📄 `docs/ai_handoff/CURSOR_AI_CONSOLIDATION_GUIDE.md` — Original consolidation instructions
- 📄 `docs/merge/STANDARDS_RATIONALIZATION_PROMPT_OPTIMIZED.md` — Rationalization governing prompt

---

## 🤖 AI Agent Behavioral Guidelines

### DO: Production-Safe Practices

✅ **Always create git checkpoint before major changes:**
```powershell
git add .
git commit -m "Checkpoint before [operation]"
```

✅ **Test on sample data first:**
```python
# Test normalization on 1000 rows before processing 724K
df_sample = df.head(1000)
# Apply normalization
# Validate results
# Then process full dataset
```

✅ **Provide rollback instructions with every script:**
```powershell
# If this breaks, run:
git reset --hard HEAD
Copy-Item -Recurse "archive/backup_20260204" "restored_folder"
```

✅ **Validate assumptions with data:**
```python
# Don't assume - verify
print(f"HowReported nulls: {df['How Reported'].isna().sum()}")
print(f"Unique values: {df['How Reported'].nunique()}")
```

### DON'T: Dangerous Practices

❌ **Never modify production baseline directly** - Always generate new version  
❌ **Never skip validation after normalization** - Dashboard depends on clean data  
❌ **Never hardcode absolute paths** - Breaks on different machines  
❌ **Never assume Excel preserves dtypes** - Always force string for case numbers  
❌ **Never merge without understanding deduplication** - Risk of data loss  

### Communication Standards

**When proposing changes:**
1. State the **specific file and line number** affected
2. Show **before/after** code snippets
3. Explain **impact on dashboard** if relevant
4. Provide **validation test** to verify change worked
5. Include **rollback procedure**

**When reporting issues:**
1. Exact error message (full traceback)
2. File path and line number
3. Input data characteristics (row count, dtypes, sample values)
4. Expected vs. actual behavior
5. Steps to reproduce

---

## 📚 Key Documentation References

### Internal Documentation
- `README.md` - Project overview, quick start, architecture
- `CHANGELOG.md` - Version history with detailed change notes
- `INCREMENTAL_RUN_GUIDE.md` - Baseline + incremental workflow
- `BASELINE_QUICK_ANSWERS.md` - Common baseline questions
- `outputs/consolidation/CAD_CONSOLIDATION_EXECUTION_GUIDE.txt` - Step-by-step consolidation

### External Standards
- `09_Reference/Standards/README.md` - Standards repository structure
- `09_Reference/Standards/CAD_RMS/DataDictionary/SCHEMA_ENHANCEMENT_SUMMARY.md` - v2.0 improvements
- `09_Reference/Standards/unified_data_dictionary/docs/` - Legacy documentation (being consolidated)

### Quality Reports Reference
- `monthly_validation/reports/latest.json` - Most recent validation metrics
- `consolidation/reports/2026_02_02_baseline_only/` - Baseline validation results

---

## 🔄 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.4.0 | 2026-03-17 | **RATIONALIZATION COMPLETE:** Updated architecture for v3.0.0, CAD_RMS is single source of truth, UDD slimmed to shim, consolidation status updated, deprecated paths removed |
| 1.3.4 | 2026-02-04 | **EMERGENCY UPDATE:** Added dashboard crisis context, 4 critical decisions, Phase 1/2 priorities, updated mapping status |
| 1.3.3 | 2026-02-04 | Added HowReported normalization crisis context, enhanced validation commands |
| 1.3.2 | 2026-02-03 | Baseline generation documentation, enhanced ESRI output workflow |
| 1.2.6 | 2026-02-02 | Incremental run support, ReportNumberNew Excel artifact fix |
| 1.1.0 | 2026-01-31 | Initial consolidation complete, ESRI output operational |

---

## 🎓 Learning Resources for AI Agents

### Understanding the Data Pipeline

```
Raw CAD Exports (Excel)
    ↓
consolidate_cad_2019_2026.py (Merge yearly + monthly)
    ↓
2019_to_2026_01_30_CAD.csv (714K+ records, raw data)
    ↓
enhanced_esri_output_generator.py (Normalize fields, RMS backfill)
    ↓
CAD_ESRI_POLISHED_[timestamp].xlsx (724K records, normalized)
    ↓
13_PROCESSED_DATA/ESRI_Polished/base/ (Deployment)
    ↓
ArcGIS Pro Dashboard (Production)
```

### Critical Normalization Concepts

**Why Normalization Matters:**
- Raw CAD data has 858 incident variants → Normalized to 557
- HowReported has ~30+ typos/abbreviations → Normalized to 12 standard values
- Disposition has 101 variants → Normalized to 20 standard values

**How It Works:**
1. **Direct Mapping:** `'911' → '9-1-1'` (case-insensitive, 280 mappings)
2. **Pattern Matching:** Unmapped values checked for patterns (`'91-1'` contains `'911'`)
3. **Default Fallback:** Unknown values get sensible defaults (`'U' → 'Phone'`)

**Success Metrics:**
- 100% domain compliance (all values in valid set)
- Zero NULL values in HowReported (default applied)
- Dashboard dropdown shows only 12 canonical values

---

**Last Updated:** 2026-02-04  
**Maintained By:** R. A. Carucci  
**For AI Agents:** Treat this as your operational manual - when in doubt, refer here first.

---