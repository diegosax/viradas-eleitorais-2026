#!/bin/sh
set -eu
mkdir -p public/data
url=https://votosecreto.com/dados/arquivos/presidente_secao_2026.jsonl.gz
if curl -fL --max-time 120 "$url" -o /tmp/election-dataset.gz; then
  if echo '261f83fdc2a17ff4dcece9d2bcceced3a34dafb1a4507d3f283a89814463f1d2  /tmp/election-dataset.gz' | sha256sum -c -; then
    cp /tmp/election-dataset.gz public/data/presidente_secao_2026.jsonl.gz
  fi
fi
printf 'Static dashboard ready. Dataset may be loaded from source or local file.\n'
