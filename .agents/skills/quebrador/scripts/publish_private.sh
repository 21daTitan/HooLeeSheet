#!/usr/bin/env bash
# Publicação segura com comando único; requer login interativo prévio no GitHub CLI.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
REPO='21daTitan/foco-no-progresso'
for bin in git gh python3; do command -v "$bin" >/dev/null || { echo "Faltando $bin; ver docs/PUBLISH.md"; exit 2; }; done
gh auth status -h github.com >/dev/null || { echo 'Execute gh auth login interativamente primeiro.'; exit 2; }
if gh repo view "$REPO" >/dev/null 2>&1; then
  echo "Repositório $REPO já existe. Parando para não sobrescrever."; exit 3
fi
if [ ! -r /dev/tty ]; then
  echo 'Bloqueado: autorização interativa de dSanT é obrigatória.'; exit 4
fi
printf 'Para publicar PRIVADO em %s, digite: PUBLICAR %s\n> ' "$REPO" "$REPO" > /dev/tty
IFS= read -r CONFIRM </dev/tty || { echo 'Sem autorização. Abortado.'; exit 4; }
if [ "$CONFIRM" != "PUBLICAR $REPO" ]; then
  echo 'Sem permissão explícita. Abortado.'; exit 4
fi
python3 -m pytest tests/ -v 2>/dev/null || python3 -m unittest discover -s tests -v
for file in .env .env.local secrets.json credentials.json; do
  if [ -e "$file" ]; then echo "Arquivo de credencial detectado: $file. Revise antes de publicar."; exit 3; fi
done
if [ ! -d .git ]; then git init -b main; fi
if git remote get-url origin >/dev/null 2>&1; then
  echo 'Remote origin já existe. Revise antes de substituir.'; exit 3
fi
git add .
git diff --cached --quiet && { echo 'Nada novo para publicar'; exit 3; }
git commit -m 'feat: skill Quebrador — Foco No Progresso v1.1.0'
gh repo create "$REPO" --private --source=. --remote=origin --push
echo "Publicado privadamente: https://github.com/$REPO"
