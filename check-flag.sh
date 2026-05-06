#!/bin/bash
# Quick vault change check for JARVIS
# Returns: 0 if no changes, 1 if changes detected
# Clears the flag after reading

FLAG_FILE="/tmp/obsidian-vault-flag"

if [ ! -f "$FLAG_FILE" ]; then
    echo "NO_CHANGES"
    exit 0
fi

# Read and clear
cat "$FLAG_FILE"
rm -f "$FLAG_FILE"
exit 1
