# Clery Act Reference Data — AI Agent Protocol

**Version:** 1.1.0  
**Last Updated:** 2026-03-09  
**Purpose:** Context and guidelines for AI agents working on Clery Act reference data and requests

---

## Audience

AI coding assistants (Claude, Cursor, etc.) working on Clery-related data tasks for Hackensack PD.

---

## Mission

Support Hackensack PD in completing **Clery Act** crime statistics requests from institutions of higher education. Provide authoritative reference data for crime classification, geography definitions, and institution-specific Clery boundaries.

---

## Repository Structure

```
Clery/
├── DataDictionary/
│   ├── current/
│   │   ├── schema/
│   │   │   ├── clery_crime_definitions.json     # Crime categories & NIBRS mappings
│   │   │   └── clery_geography_definitions.json  # On-Campus, Noncampus, Public Property
│   │   ├── mappings/
│   │   │   └── nibrs_to_clery_map.json          # NIBRS → Clery mapping
│   │   ├── institutions/                         # Institution geography (GeoJSON)
│   │   │   ├── institution_clery_geography_index.json
│   │   │   └── *_*.geojson                       # Exported from ArcGIS Pro
│   │   └── REQUEST_CHECKLIST.md
│   ├── archive/
│   └── CHANGELOG.md                              # Schema/mapping changes only
├── scripts/
│   ├── extract_clery_geography_from_arcgis.py   # ArcPy extraction
│   └── README.md
├── README.md
├── SUMMARY.md
├── CHANGELOG.md                                  # Module version history
└── CLAUDE.md
```

---

## Critical Constraints

1. **Geography is institution-specific** — Each school defines its own On-Campus, Noncampus, Public Property. Use exported GeoJSON from `institutions/` for filtering.
2. **Crime definitions** — Use FBI UCR/NIBRS definitions. `clery_crime_definitions.json` is authoritative.
3. **VAWA crimes** — Dating Violence, Domestic Violence, Stalking require relationship/conduct context from narrative; not derivable from NIBRS codes alone.
4. **Hate crimes** — Simple Assault, Larceny-Theft, Intimidation, Destruction/Vandalism are Clery-reportable only when bias-motivated.
5. **Date range** — Clery reports cover the 3 most recent completed calendar years. Do not include current (incomplete) year unless the institution requests it.

---

## Key Paths

| Path | Purpose |
|------|---------|
| `10_Projects\Clery\2024\` | Source ArcGIS Pro projects and data |
| `10_Projects\Clery\2024\2024_Clery_Request_FDU.pdf` | FDU request requirements (institution-specific) |
| `Standards\NIBRS\DataDictionary\current\mappings\rms_to_nibrs_offense_map.json` | RMS → NIBRS (upstream of Clery mapping) |
| `[RMS_EXPORT_PATH]` | RMS incident export (institution-specific date range) |

---

## Running the Extraction Script

**Requires ArcGIS Pro** (arcpy). Do not use system Python. See [scripts/README.md](scripts/README.md) for full commands.

---

## Institution Geography Status

| Institution | Geography exported | Notes |
|-------------|-------------------|-------|
| Eastwick College | ✅ | CleryAOI (polygon), Clery_Crimes, geocoded points |
| FDU Clery Act | ✅ | FDU_Property, Surronding_Area [sic], +6 |
| Parisian (Parisian Beauty Academy) | ✅ | Parisian_Beauty (polygon) |
| Rutgers | ✅ | RUTGERS_CLERY_RMS_Geocoded (points) |
| Bergen Community College | ⚠️ | GDB has no top-level feature classes; may use feature datasets or hosted services |
| Bergen Community College Clery Act | — | APRX references FDU geodatabase |
| Bergen Academies | — | No GDB or APRX found |

---

## DO / DON'T

**DO:**
- Use `nibrs_to_clery_map.json` for crime classification
- Use exported GeoJSON for geography filtering when available
- Filter RMS data by date range (3 most recent calendar years)
- Flag VAWA crimes from narrative when relationship context present
- Report zero counts explicitly for all Clery categories (institutions must report zeros)
- Reference `REQUEST_CHECKLIST.md` for request requirements

**DON'T:**
- Run extraction script with system Python (use ArcGIS Pro Python)
- Assume all institutions have exported geography (Bergen CC structure differs)
- Report hate-crime-only categories (Simple Assault, Larceny, etc.) without bias motivation
- Modify `clery_crime_definitions.json` without DOE/FBI reference
- Include PII (names, DOB, SSN) in Clery exports — institutions receive aggregate counts only unless specifically requested with authorization

---

## Related Standards

- **NIBRS** — `Standards/NIBRS` — offense definitions, RMS to NIBRS mapping
- **RMS** — `Standards/RMS` — RMS field definitions
- **CAD_RMS** — `Standards/CAD_RMS` — cross-system mappings

---

## See Also

- [README.md](README.md) — Overview and quick start
- [SUMMARY.md](SUMMARY.md) — Executive summary
- [CHANGELOG.md](CHANGELOG.md) — Version history

---

## Path Resolution

OneDrive root resolves via two junctions (created 2026-03-22):
1. Profile junction:
     C:\Users\carucci_r  →  C:\Users\RobertCarucci
2. OneDrive junction (laptop only — must be replicated on desktop):
     C:\Users\RobertCarucci\OneDrive
     →  C:\Users\RobertCarucci\OneDrive - City of Hackensack

Active root returned by path_config.get_onedrive_root():
  C:\Users\carucci_r\OneDrive - City of Hackensack

### Rules for AI agents
- DO NOT change carucci_r to RobertCarucci in scripts or configs
- DO NOT change PowerBI_Data to PowerBI_Date (PowerBI_Date was the typo)
- scripts.json uses carucci_r paths — this is correct and intentional
- path_config.py resolves the correct root at runtime via get_onedrive_root()
- If a path appears broken, check junction status before editing any file

---

**Maintained by:** R. A. Carucci
