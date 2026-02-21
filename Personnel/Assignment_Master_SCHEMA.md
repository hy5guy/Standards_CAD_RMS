# Assignment_Master_V3_FINAL.xlsx Schema Documentation (V2)

**File:** `Assignment_Master_V3_FINAL.xlsx`
**Location:** `09_Reference/Personnel/`
**Sheet Name:** `Assignment_Master_V2` *(kept for backward compatibility with automation scripts)*
**Table Name:** `Assignment_Master_V2` *(Excel table object)*
**Created:** 2026-02-04
**Last Updated:** 2026-02-21
**Record Count:** 166 personnel records *(was 168 — 6 duplicate PEO rows deleted; 4 probationary officers added via POSS merge)*

---

## Purpose

This is the **single source of truth** for Hackensack Police Department personnel data. Used for:
- Validating officer assignments in CAD/E-Ticket data
- Personnel drift detection (new hires, retirements, reassignments)
- Report attribution and bureau-level summons classification
- Power BI visual enrichment (bureau, team, rank, display name)

---

## Column Change Summary (V1 → V2)

Dataset reduced from **42 columns → 25 columns**.

**Columns Removed:**
`DEP_CHIEF`, `WG5`, `POSS_CONTRACT_TYPE` *(renamed)*, `Proposed 4-Digit Format` *(renamed)*, `Conflict Resolution` *(renamed)*, `Special Notes` *(renamed then deleted)*, 10 `*_seniority` columns, 2 `*_workgroup` columns, 4 empty columns (`FullName`, `Status`, `Badge`, `Notes`)

**Columns Renamed:**

| Old Name | New Name |
|----------|----------|
| `POSS_CONTRACT_TYPE` | `CONTRACT_TYPE` |
| `Proposed 4-Digit Format` | `STANDARD_NAME` |
| `Conflict Resolution` | `CONFLICT_RESOLUTION` |

**New Columns Added:**

| Column | Type | Description |
|--------|------|-------------|
| `CODE` | TEXT | Short unique lookup ID (e.g., `JA386`) |
| `WORKING_GROUP` | TEXT | Contract group — often mirrors `CONTRACT_TYPE` |

---

## Full 25-Column Schema

| # | Column | Type | Nulls | Description | Example |
|---|--------|------|-------|-------------|---------|
| 1 | `REF_NUMBER` | INT | ~5 | Internal reference/sort number | `0` |
| 2 | `FULL_NAME` | TEXT | 0 | Composite: `{TITLE} {FIRST} {LAST} {BADGE}` | `P.O. JANN ABERDE 386` |
| 3 | `TITLE` | TEXT | 0 | Job title abbreviation (functional role) | `P.O.` |
| 4 | `FIRST_NAME` | TEXT | 0 | First name | `JANN` |
| 5 | `LAST_NAME` | TEXT | 0 | Last name | `ABERDE` |
| 6 | `BADGE_NUMBER` | TEXT | ~10 | Numeric badge — blank for unbadged civilians | `386` |
| 7 | `PADDED_BADGE_NUMBER` | TEXT | 0 | 4-digit zero-padded; `0000` for unbadged | `0386` |
| 8 | `TEAM` | TEXT | 0 | Squad-level assignment (from POSS) | `PLT A Squad 1` |
| 9 | `WG1` | TEXT | ~12 | Division level | `OPERATIONS DIVISION` |
| 10 | `WG2` | TEXT | ~12 | Bureau / section level | `PATROL DIVISION` |
| 11 | `WG3` | TEXT | ~60 | Sub-unit or role | `PLATOON A` |
| 12 | `WG4` | TEXT | ~100 | Squad code — patrol only | `A1` |
| 13 | `CONTRACT_TYPE` | TEXT | ~20 | Bargaining unit | `PBA LOCAL 9 (12 HOUR)` |
| 14 | `STANDARD_NAME` | TEXT | 0 | Display name — `F. LAST #BADGE` (20 = `REQUIRES_MANUAL_MAPPING`) | `J. ABERDE #0386` |
| 15 | `CONFLICT_RESOLUTION` | TEXT | ~50 | YES / NO flag | `NO` |
| 16 | `CODE` | TEXT | ~15 | Short lookup ID | `JA386` |
| 17 | `WORKING_GROUP` | TEXT | ~30 | Contract group | `PBA LOCAL 9 (12 HOUR)` |
| 18 | `DOB` | DATE | ~60 | Date of birth — stored as Excel serial number | `12/07/1997` |
| 19 | `JOINED_SERVICE` | DATE | ~30 | Service start date — Excel serial number | `03/10/2025` |
| 20 | `SGT` | DATE | ~140 | Sergeant promotion date | *(null for most)* |
| 21 | `LT` | DATE | ~150 | Lieutenant promotion date | *(null for most)* |
| 22 | `CAPT` | DATE | ~160 | Captain promotion date | *(null for most)* |
| 23 | `CHIEF` | DATE | ~165 | Chief promotion date | *(null for most)* |
| 24 | `STATUS` | TEXT | 0 | `ACTIVE` or `INACTIVE` | `ACTIVE` |
| 25 | `RANK` | TEXT | 0 | Standardized rank abbreviation — 100% populated | `P.O.` |

---

## Valid STATUS Values

| Value | Description |
|-------|-------------|
| `ACTIVE` | Currently employed |
| `INACTIVE` | Retired, transferred, or on extended leave |

**Note:** Currently 1 INACTIVE record — F. LORENZO.

---

## Valid RANK Values (14 values)

| Rank | Description | Standardized From |
|------|-------------|-------------------|
| `P.O.` | Police Officer (also used for Detectives) | — |
| `SGT.` | Sergeant | `Sgt.`, `Sgt. ` (trailing space) |
| `LT.` | Lieutenant | `Lt.` |
| `CAPT.` | Captain | `Captain` |
| `CHIEF` | Chief of Police | `Chief ` (trailing space) |
| `SPO II` | Special Police Officer Class II | `SLEO2` |
| `SPO III` | Special Police Officer Class III | `SLEO3` |
| `C.O.` | Communications Officer | *(NEW in V2)* |
| `CLK` | Clerk | — |
| `PEO` | Parking Enforcement Officer | — |
| `DPW` | Dept of Public Works | — |
| `TM` | Traffic Monitor | — |
| `PLA` | Police Liaison Assistant | — |
| `HCOP` | Community Oriented Policing | *(NEW in V2)* |

> **IMPORTANT — TITLE vs RANK distinction:**
> `TITLE` = functional role (e.g., `DET.`, `HCOP`); `RANK` = civil service rank.
> Detectives have `TITLE = DET.` but `RANK = P.O.`

---

## Valid TITLE Values (15 values)

`P.O.`, `SGT.`, `LT.`, `CAPT.`, `CHIEF`, `DET.` *(rank = P.O.)*, `SPO II`, `SPO III`, `C.O.`, `CLK`, `PEO`, `DPW`, `TM`, `PLA`, `HCOP`

---

## Valid TEAM Values (37 values)

**Patrol (14):**
`PLT A Squad 1`, `PLT A Squad 2`, `PLT A Squad 3`, `PLT A Squad 4`,
`PLT B Squad 1`, `PLT B Squad 2`, `PLT B Squad 3`, `PLT B Squad 4`,
`PLT A TC`, `PLT B TC`, `PLT A DESK`, `PLT B DESK`, `PATROL`, `Probationary PO`

**Investigative (5):**
`Detective/Juv Bureau`, `Crime Suppression Bureau`, `School Threat Bureau`,
`SCHOOL THREAT ASSESSMENT & CRIME PREVENTION`, `SPO III`

**Operations & Support (12):**
`Emergency Services Unit`, `Communications Unit`, `Records & Evidence`, `Traffic Bureau`,
`TRAFFIC`, `Training Unit`, `Safe Streets Operations`, `Housing`, `HCOP`,
`Community Outreach`, `Parking Enforcement`, `Parking Lot Attendant`

**Admin (4):**
`Operations Division`, `Division Commanders`, `Office of Police Chief`, `Internal Affairs Unit`

**Civilian (2):**
`DPW`, `Traffic Maintenance`

---

## Valid CONTRACT_TYPE Values (9 values)

| Value | Description |
|-------|-------------|
| `PBA LOCAL 9 (12 HOUR)` | 12-hour patrol shifts |
| `PBA LOCAL 9 (8 HOUR)` | 8-hour specialized shifts |
| `PBA LOCAL 9A` | Supervisors (SGT.+) |
| `SLEO2` | Special LEO contract Class II |
| `SLEO3` | Special LEO contract Class III |
| `SLEO4` | Special LEO contract Class IV |
| `CIVILIAN DISPATCHERS` | Communications Unit |
| `PARKING ENFORCEMENT OFF` | PEO personnel |
| `WHITE COLLAR CONTRACT` | Civilian admin |

---

## Valid WG4 Values (8 codes)

`A1`, `A2`, `A3`, `A4` — Platoon A Squads 1–4
`B1`, `B2`, `B3`, `B4` — Platoon B Squads 1–4

> Only populated for patrol division officers. Null for all other assignments.

---

## FULL_NAME Format

**Old format (V1):** Last, First MI — e.g., `Smith, John P`

**New format (V2):** `{TITLE} {FIRST_NAME} {LAST_NAME} {BADGE_NUMBER}`
- Example (badged): `P.O. JANN ABERDE 386`
- Example (unbadged civilian): `CLK MADDALENA CANDELA`

---

## Usage in Validation

```python
import pandas as pd

# Load from Excel (canonical source)
personnel = pd.read_excel('Assignment_Master_V3_FINAL.xlsx', sheet_name='Assignment_Master_V2')

# Build validation sets
VALID_BADGE_NUMBERS = set(
    personnel.loc[personnel['PADDED_BADGE_NUMBER'] != '0000', 'BADGE_NUMBER']
    .dropna().astype(str)
)
VALID_TEAMS = set(personnel['TEAM'].dropna().unique())
VALID_RANKS = {
    'P.O.', 'SGT.', 'LT.', 'CAPT.', 'CHIEF',
    'SPO II', 'SPO III', 'C.O.', 'CLK', 'PEO', 'DPW', 'TM', 'PLA', 'HCOP'
}

def validate_unit(value):
    if pd.isna(value):
        return True, None
    if value not in VALID_TEAMS:
        return False, f'Unknown unit: {value}'
    return True, None

# Active and sworn filters
active_officers = personnel[personnel['STATUS'] == 'ACTIVE']
sworn_ranks = {'P.O.', 'SGT.', 'LT.', 'CAPT.', 'CHIEF', 'SPO II', 'SPO III'}
sworn_officers = personnel[personnel['RANK'].isin(sworn_ranks)]
```

---

## Data Quality Notes

- **RANK populated:** 100% — 28 blanks filled from TITLE in Turn 10; all values standardized
- **Trailing spaces:** RESOLVED — `Sgt. ` → `SGT.`, `Chief ` → `CHIEF`, etc.
- **STANDARD_NAME gaps:** 20 records flagged `REQUIRES_MANUAL_MAPPING`
- **Badge format:** PEOs use 4-digit badges (2008, 2013, 2025, 2027, 2030); sworn officers use ≤3 digits zero-padded to 4; unbadged = `0000`
- **FULL_NAME format:** Uses `TITLE FIRST LAST BADGE` — NOT `Last, First MI`
- **TITLE vs RANK:** Detectives → `TITLE = DET.` / `RANK = P.O.`; known exception: WANDA RIVERA `FULL_NAME` shows `P.O.` but actual rank is `SGT.`
- **WG2 typo:** `RECODS AND EVIDENCE MANAGEMENT` — missing `R` — carry forward until bulk correction
- **Date storage:** `DOB`, `JOINED_SERVICE`, and all promotion date columns stored as Excel serial numbers

---

## Trim Candidates (Future Cleanup)

| Column | Issue | Nulls |
|--------|-------|-------|
| `WG4` | Patrol only — ~100 nulls for non-patrol | ~100 |
| `CONFLICT_RESOLUTION` | Could be derived; sparse | ~50 |
| `CODE` | Computable from initials + badge; some gaps | ~15 |
| `WORKING_GROUP` | Often mirrors `CONTRACT_TYPE`; may be redundant | ~30 |
| `STANDARD_NAME` | 20 records still `REQUIRES_MANUAL_MAPPING` | 0 (flagged) |

---

## Drift Detection

Monitor for:
1. **New personnel** — Badge numbers in CAD not in master
2. **Inactive personnel** — Active in master, not seen in CAD 90+ days
3. **Unit changes** — Different TEAM assignments vs WG4
4. **Squad reassignments** — WG4 code changes between periods
5. **STANDARD_NAME gaps** — Remaining `REQUIRES_MANUAL_MAPPING` entries

```python
# Badge drift detection
cad_badges = set(cad_data['badge'].astype(str))
master_badges = set(
    personnel.loc[personnel['STATUS'] == 'ACTIVE', 'BADGE_NUMBER']
    .dropna().astype(str)
)
new_personnel = cad_badges - master_badges       # In CAD but not in master
missing_from_cad = master_badges - cad_badges    # In master but not in CAD 90+ days
```

---

## Maintenance Procedures

### Adding New Personnel
1. Add row with minimum: `FULL_NAME`, `TITLE`, `FIRST_NAME`, `LAST_NAME`, `BADGE_NUMBER`, `PADDED_BADGE_NUMBER`, `TEAM`, `STATUS`, `RANK`
2. Set `STATUS = ACTIVE`
3. Set `PADDED_BADGE_NUMBER` = 4-digit zero-padded string (or `0000` for unbadged)
4. Set `STANDARD_NAME = F. LAST #BADGE` (or `REQUIRES_MANUAL_MAPPING` if uncertain)
5. Set `CODE` = first initial + last initial + badge number (e.g., `JA386`)
6. Add entry to version history below

### Marking Personnel Inactive
1. Set `STATUS = INACTIVE`
2. Do **NOT** delete the row — historical data references must remain valid

### Updating Squad Assignments
1. Update `TEAM` (e.g., `PLT A Squad 2` → `PLT B Squad 1`)
2. Update `WG3` if platoon changed (`PLATOON A` → `PLATOON B`)
3. Update `WG4` squad code (`A2` → `B1`)

---

## Related Files

| File | Status | Purpose |
|------|--------|---------|
| `Assignment_Master_V3_FINAL.xlsx` | **Current canonical** | Excel workbook with data + Claude Log audit trail |
| `Assignment_Master_V2.csv` | Previous (archived) | CSV export — used by active automation scripts |
| `Assignment_Master_V2.xlsx` | Previous (archived) | Prior Excel version |
| `POSS_EMPLOYEE.xlsx` | Source | Turn 9 merge source (138 TEAM updates, 8 CONTRACT_TYPE) |
| `2025_12_29_assigned_shift.csv` | Source | Ground-truth patrol roster (67 records validated in Turn 6) |
| `99_Archive/` | Archive | Historical versions and backups |

---

## Version History

| Date | Version | Changes | Records |
|------|---------|---------|---------|
| 2026-02-04 | v1.0.0 | Schema created, duplicates archived | 168 |
| 2026-02-04 | v1.1.0 | Deleted 6 duplicate PEO rows | 166 |
| 2026-02-04 | v1.2.0 | Formatted seniority dates mm/dd/yyyy | 166 |
| 2026-02-04 | v2.0.0 | **MAJOR**: 42→26 cols; deleted seniority/workgroup/empty cols; renamed cols; flagged STANDARD_NAME | 166 |
| 2026-02-04 | v2.0.1 | Renamed table to `Assignment_Master_V2_Rework` | 166 |
| 2026-02-04 | v2.1.0 | Validated vs patrol roster; identified 29 WG4 mismatches | 166 |
| 2026-02-04 | v2.2.0 | Compared vs POSS_EMPLOYEE; identified 138 TEAM differences | 166 |
| 2026-02-05 | v3.0.0 | **MAJOR**: 138 TEAM updates; 8 CONTRACT_TYPE updates; 2 name fixes; TC/DESK distinction | 166 |
| 2026-02-05 | v3.1.0 | 28 RANK blanks filled from TITLE; all RANK values standardized; SPECIAL_NOTES deleted | 166 |
| 2026-02-05 | v3.2.0 | Deleted PQ sheet; renamed sheet/table to `Assignment_Master_V2`; saved as V3_FINAL | 166 |

---

**Contact:** R. A. Carucci | Hackensack PD CAD/RMS Data Quality System
**Schema Version:** V2 | **Last Updated:** 2026-02-21
