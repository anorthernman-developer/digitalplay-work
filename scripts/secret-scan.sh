#!/usr/bin/env bash
# Fails (exit 1) if anything that looks like a key or token is found. Run before every commit and deploy.
set -u
dir="${1:-.}"
pat='AIza[0-9A-Za-z_-]{20,}|ghp_[0-9A-Za-z]{20,}|github_pat_[0-9A-Za-z_]{20,}|gho_[0-9A-Za-z]{20,}|sk-[A-Za-z0-9_-]{20,}|sk_live_[0-9A-Za-z]{10,}|xox[abprs]-[0-9A-Za-z-]{10,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|nfp_[0-9A-Za-z]{20,}|"?(api[_-]?key|secret|token|password)"?\s*[:=]\s*"[^"$ ]{12,}"'
if grep -rInE "$pat" "$dir" --exclude-dir=.git --exclude-dir=node_modules --exclude=secret_scan.sh; then echo "SECRET SCAN: possible secret found in $dir" >&2; exit 1; fi
if find "$dir" -path "$dir/.git" -prune -o \( -name ".env" -o -name ".env.*" -o -name "*.pem" -o -name "*.key" \) -print | grep -q .; then echo "SECRET SCAN: key-like file present in $dir" >&2; exit 1; fi
echo "secret scan clean: $dir"
