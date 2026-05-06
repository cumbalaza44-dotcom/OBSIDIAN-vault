#!/bin/bash
# Obsidian Vault sync pull - reactive flag on changes
# Runs from cron every 5 minutes. Zero token cost.

VAULT_DIR="/root/.openclaw/workspace/obsidian-vault"
FLAG_FILE="/tmp/obsidian-vault-flag"
LOG_FILE="/var/log/obsidian-sync.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
}

cd "$VAULT_DIR" || { log "ERROR: cannot cd to vault"; exit 1; }

# Get current HEAD before pull
BEFORE=$(git rev-parse HEAD)

# Pull quietly
git pull --ff-only -q 2>/dev/null
PULL_EXIT=$?

if [ $PULL_EXIT -ne 0 ]; then
    log "WARN: git pull failed (exit $PULL_EXIT)"
    exit 1
fi

# Get HEAD after pull
AFTER=$(git rev-parse HEAD)

# Compare - if changed, write flag
if [ "$BEFORE" != "$AFTER" ]; then
    # Count new commits
    NEW_COMMITS=$(git rev-list --count "$BEFORE..$AFTER" 2>/dev/null)
    # Get changed files summary
    CHANGED_FILES=$(git diff --name-only "$BEFORE" "$AFTER" 2>/dev/null | tr '\n' ',' | sed 's/,$//')
    
    # Write timestamp + summary to flag file
    echo "changed_at=$(date +%s)" > "$FLAG_FILE"
    echo "new_commits=$NEW_COMMITS" >> "$FLAG_FILE"
    echo "files_changed=$CHANGED_FILES" >> "$FLAG_FILE"
    
    log "CHANGE DETECTED: $NEW_COMMITS commit(s), files: $CHANGED_FILES"
fi
