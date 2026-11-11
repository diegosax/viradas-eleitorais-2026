#!/bin/sh
set -eu
test -s public/data/results.json
printf 'Official TSE results ready.\n'
