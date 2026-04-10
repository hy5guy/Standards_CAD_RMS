#!/bin/bash
set -euo pipefail

# Only run in remote (Claude Code on the web) environments
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR"

# Install Python dependencies (idempotent, cached between sessions)
pip install -q -r requirements.txt 2>/dev/null || true

echo ""
echo "=== Standards Repository Session Start ==="
echo ""

# 1. Show Standards version
VERSION=$(cat VERSION 2>/dev/null || echo "UNKNOWN")
echo "Standards VERSION: $VERSION"
echo ""

# 2. Check shim sync status (drift detection)
echo "--- UDD Shim Sync Check ---"
if [ -f scripts/sync_udd_shim.py ]; then
  python scripts/sync_udd_shim.py --dry-run 2>&1 || echo "WARNING: Shim sync check failed"
else
  echo "WARNING: scripts/sync_udd_shim.py not found"
fi
echo ""

# 3. Report git status
echo "--- Git Status ---"
BRANCH=$(git branch --show-current 2>/dev/null || echo "detached")
echo "Branch: $BRANCH"

UNCOMMITTED=$(git status --porcelain 2>/dev/null | head -20)
if [ -z "$UNCOMMITTED" ]; then
  echo "Working tree: clean"
else
  COUNT=$(echo "$UNCOMMITTED" | wc -l)
  echo "Uncommitted changes: $COUNT file(s)"
  echo "$UNCOMMITTED"
fi
echo ""
echo "=== Session Start Complete ==="
