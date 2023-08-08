#!/bin/sh
DIR="$(dirname $0)"
cat "$DIR/sample-exercise/config.json" | "$DIR/run"
