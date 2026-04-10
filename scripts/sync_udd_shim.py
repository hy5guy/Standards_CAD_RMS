"""
sync_udd_shim.py — Keep unified_data_dictionary shim files in sync with CAD_RMS canonical copies.

Usage:
    python sync_udd_shim.py                  # from Standards root
    python sync_udd_shim.py --standards-root "C:\\path\\to\\Standards"
    python sync_udd_shim.py --dry-run        # report only, no copies
"""

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description="Sync UDD shim files from canonical sources")
    parser.add_argument("--standards-root", type=Path, default=None,
                        help="Path to 09_Reference/Standards (default: script parent's parent)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Report mismatches without copying")
    args = parser.parse_args()

    if args.standards_root:
        root = args.standards_root.resolve()
    else:
        root = Path(__file__).resolve().parent.parent

    manifest_path = root / "scripts" / "shim_sync_manifest.json"
    if not manifest_path.exists():
        print(f"ERROR: Manifest not found: {manifest_path}")
        sys.exit(1)

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    pairs = manifest["pairs"]
    synced = 0
    skipped = 0
    errors = 0

    for pair in pairs:
        canonical = root / pair["canonical"]
        shim = root / pair["shim"]

        if not canonical.exists():
            print(f"  ERROR  {pair['canonical']} — canonical file missing")
            errors += 1
            continue

        if not shim.exists():
            print(f"  ERROR  {pair['shim']} — shim file missing")
            errors += 1
            continue

        hash_c = sha256(canonical)
        hash_s = sha256(shim)

        if hash_c == hash_s:
            print(f"  OK     {pair['shim']}")
            skipped += 1
        else:
            if args.dry_run:
                print(f"  DRIFT  {pair['shim']} — would copy from canonical")
                synced += 1
            else:
                shutil.copy2(canonical, shim)
                print(f"  SYNCED {pair['shim']} <- {pair['canonical']}")
                synced += 1

    print()
    print(f"Results: {skipped} in sync, {synced} {'would sync' if args.dry_run else 'synced'}, {errors} errors")

    if errors > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
