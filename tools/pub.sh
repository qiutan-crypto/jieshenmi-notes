#!/bin/sh
# Usage: tools/pub.sh "commit message"   (run from anywhere; repo root = parent of this script)
cd "$(dirname "$0")/.." && python3 tools/build.py && (cd tools && python3 build_reports.py) && git add -A && git commit -q -m "$1" && git -c push.negotiate=true push origin main 2>&1 | tail -1
