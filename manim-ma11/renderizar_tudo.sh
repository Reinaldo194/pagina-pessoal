#!/usr/bin/env bash
# Renderiza todas as cenas. Uso: bash renderizar_tudo.sh [-ql|-qm|-qh|-qk]
set -e
Q="${1:--ql}"
cd "$(dirname "$0")"
for f in 0*.py funcoes/*.py; do
  manim "$Q" -a "$f"
done
