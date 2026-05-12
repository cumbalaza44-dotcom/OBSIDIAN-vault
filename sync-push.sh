#!/bin/bash
# Vault Push — add, commit, push for local JARVIS edits
# Called by watcher.sh or manually. Zero token cost.

VAULT_DIR="/root/.openclaw/workspace/obsidian-vault"
LOG_FILE="/var/log/obsidian-sync.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
}

cd "$VAULT_DIR" || { log "PUSH ERROR: cannot cd to vault"; exit 1; }

# Check if there are local changes
if git diff --quiet && git diff --cached --quiet; then
    # No changes - nothing to push
    exit 0
fi

# Count changed files
CHANGED=$(git status --porcelain | wc -l)

# Add all, commit, push
git add -A 2>/dev/null
git commit -m "JARVIS sync: $(date '+%Y-%m-%d %H:%M')" 2>/dev/null

if git push --force-with-lease origin HEAD:main 2>/dev/null; then
    log "PUSH OK: $CHANGED file(s) pushed"
    exit 0
else
    log "PUSH ERROR: push failed for $CHANGED file(s)"
    exit 1
fi
