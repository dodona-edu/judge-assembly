#!/usr/bin/env bash
# Runs devel/run-tests.sh as root inside the judge image. Arguments are passed
# on, e.g. `-v -k narayana`.
#
#   IMAGE=...           judge image (default ghcr.io/dodona-edu/dodona-assembly:latest)
#   UPDATE_EXPECTED=1   rewrite the expected output

set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"

docker run --rm --platform linux/amd64 --user root \
  ${UPDATE_EXPECTED:+--env UPDATE_EXPECTED} \
  --volume "$repo:/judge-assembly" \
  --workdir /judge-assembly \
  "${IMAGE:-ghcr.io/dodona-edu/dodona-assembly:latest}" \
  devel/run-tests.sh "$@"
