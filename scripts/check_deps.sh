#!/bin/bash
set -e
missing=()
for bin in nmap nikto gobuster whatweb; do
    if ! command -v $bin >/dev/null 2>&1; then
        echo "[WARN] $bin not found"
        missing+=("$bin")
    else
        echo "[OK] $bin available"
    fi
done
if [ ${#missing[@]} -eq 0 ]; then
    echo "All binaries found."
else
    echo "Missing: ${missing[@]}"
    exit 1
fi
