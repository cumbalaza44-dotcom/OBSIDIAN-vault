#!/bin/bash
# Vault File Watcher — reactive push on file changes
# Uses inotify to detect writes and triggers sync-push.sh with debounce.
# Runs as a systemd service. Zero token cost.

VAULT_DIR="/root/.openclaw/workspace/obsidian-vault"
LOG_FILE="/var/log/obsidian-sync.log"
PID_FILE="/tmp/obsidian-watcher.pid"

echo $$ > "$PID_FILE"

# Debounce: wait for N seconds of silence before pushing
# Reads lines from inotifywait, tracks last event time
debounce() {
    local debounce_sec=3
    local last_event=0

    while IFS= read -r line; do
        # Only trigger on .md files
        case "$line" in
            *.md)
                last_event=$(date +%s)
                ;;
            *) continue ;;
        esac

        # Wait for debounce window (no new .md events)
        while true; do
            current=$(date +%s)
            if [ $((current - last_event)) -ge "$debounce_sec" ]; then
                break
            fi
            sleep 0.5
        done

        # Debounce expired — push
        bash "$VAULT_DIR/sync-push.sh" <&- &
    done
}

cd "$VAULT_DIR" || exit 1

# Monitor for close_write events, exclude .git
inotifywait -m -r -e close_write \
    --exclude '\.git/' \
    --format '%w%f' \
    "$VAULT_DIR" 2>/dev/null | debounce

# inotifywait died — restart
exec bash "$0"
