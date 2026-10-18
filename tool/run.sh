#!/usr/bin/env bash
# Static compatibility check of the oxlorg.opnsense collection against OPNsense releases.
#
#   run.sh <collection-checkout> <target-tag> [baseline-tag]
#
# e.g. run.sh ~/collection_opnsense 26.7.7 26.1.11
# Clones opnsense/core and opnsense/plugins at the given tags (shallow, cached in $WORK),
# builds an API snapshot per tag and writes report-<target>.md/.json to $OUT.
# Exit code 1 when errors were found (use FAIL_ON=never to disable).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
COLL="$1"; TARGET="$2"; BASE="${3:-}"
WORK="${WORK:-$HOME/.cache/opn-api-check}"; OUT="${OUT:-.}"; FAIL_ON="${FAIL_ON:-ERROR}"
mkdir -p "$WORK" "$OUT"

snapshot() {
  local tag="$1"
  for repo in core plugins; do
    [ -d "$WORK/$repo-$tag" ] || git clone -q --depth 1 -b "$tag" "https://github.com/opnsense/$repo" "$WORK/$repo-$tag"
  done
  python3 -I "$HERE/opn_snapshot.py" --core "$WORK/core-$tag" --plugins "$WORK/plugins-$tag" \
    --label "$tag" --out "$WORK/snap-$tag.json"
}

snapshot "$TARGET"
[ -n "$BASE" ] && snapshot "$BASE"
python3 "$HERE/oxl_extract.py" --collection "$COLL" --out "$WORK/collection.json"
python3 -I "$HERE/oxl_check.py" --collection "$WORK/collection.json" --snapshot "$WORK/snap-$TARGET.json" \
  ${BASE:+--baseline "$WORK/snap-$BASE.json"} --md "$OUT/report-$TARGET.md" --json "$OUT/report-$TARGET.json" \
  --fail-on "$FAIL_ON"
