#!/bin/bash
# Quick vault change check for JARVIS
# Also checks if watcher is alive and if push is needed.
# Run at session startup and heartbeat.

FLAG_FILE="/tmp/obsidian-vault-flag"
WATCHER_SERVICE="obsidian-watcher.service"

# Check flag first (remote changes from Mr. Jair)
if [ -f "$FLAG_FILE" ]; then
    echo "=== VAULT FLAG DETECTED ==="
    cat "$FLAG_FILE"
    rm -f "$FLAG_FILE"
    
    # Read snapshot - it's already regenerated
    SNAPSHOT="/root/.openclaw/workspace/obsidian-vault/_VAULT-SNAPSHOT.md"
    if [ -f "$SNAPSHOT" ]; then
        echo "--- Snapshot ---"
        head -30 "$SNAPSHOT"
    fi
    exit 1
fi

# Check watcher health
WATCHER_OK=$(systemctl is-active "$WATCHER_SERVICE" 2>/dev/null)
if [ "$WATCHER_OK" != "active" ]; then
    echo "WARN: watcher not running, attempting restart"
    systemctl restart "$WATCHER_SERVICE" 2>/dev/null
fi

echo "NO_CHANGES"
exit 0
