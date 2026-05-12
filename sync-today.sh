#!/bin/bash
# Hoy.md Generator — produce lista de tareas del día actual
# Escanea todas las notas del vault en busca de tareas con 📅 YYYY-MM-DD = hoy
# Output: /root/.openclaw/workspace/obsidian-vault/Hoy.md

VAULT_DIR="/root/.openclaw/workspace/obsidian-vault"
TODAY_FILE="$VAULT_DIR/Hoy.md"
LOG_FILE="/var/log/obsidian-sync.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
}

cd "$VAULT_DIR" || { log "TODAY ERROR: cannot cd to vault"; exit 1; }

TODAY=$(date '+%Y-%m-%d')
TODAY_SHORT=$(date '+%d/%m/%Y')

# ── Gather all markdown files (exclude system files and git) ──
mapfile -t MD_FILES < <(find . -name "*.md" \
  -not -name "_VAULT-INDEX.md" \
  -not -name "_VAULT-SNAPSHOT.md" \
  -not -name "Hoy.md" \
  -not -path "./.git/*" \
  | sort)

TODAY_TASKS=()
PENDING=0
COMPLETED=0

for f in "${MD_FILES[@]}"; do
    relpath=$(echo "$f" | sed 's/^\.\///')
    content=$(cat "$f")
    file_tasks=()
    
    while IFS= read -r line; do
        # Match task lines with today's date: - [ ] ... 📅 2026-05-11 ...
        if echo "$line" | grep -qE "📅[[:space:]]*$TODAY"; then
            # Clean the task text
            task=$(echo "$line")
            file_tasks+=("$task")
        fi
    done <<< "$content"
    
    if [ ${#file_tasks[@]} -gt 0 ]; then
        TODAY_TASKS+=("$(printf '%s\n' "${file_tasks[@]}")")
        TOTAL_FOUND=$((TOTAL_FOUND + ${#file_tasks[@]}))
    fi
done

# ── Build Hoy.md ──
{
    echo "# 📋 Hoy — $TODAY_SHORT"
    echo ""
    
    if [ "$TOTAL_FOUND" -eq 0 ]; then
        echo "*Sin tareas programadas para hoy.* 🎯"
    else
        echo "**$TOTAL_FOUND tarea(s) pendiente(s)**"
        echo ""
        echo "## ✅ Por hacer"
        echo ""
        for f in "${MD_FILES[@]}"; do
            relpath=$(echo "$f" | sed 's/^\.\///')
            content=$(cat "$f")
            source_printed=false
            
            while IFS= read -r line; do
                if echo "$line" | grep -qE "📅[[:space:]]*$TODAY"; then
                    if [ "$source_printed" = false ]; then
                        echo "### 📁 $relpath"
                        source_printed=true
                    fi
                    # Remove leading - if present to avoid double dash
                    clean_line=$(echo "$line" | sed 's/^- //')
                    echo "- $clean_line"
                fi
            done <<< "$content"
            
            if [ "$source_printed" = true ]; then
                echo ""
            fi
        done
    fi
    
    echo "---"
    echo "*Auto-generado: $(date '+%Y-%m-%d %H:%M') UTC-5*"
} > "$TODAY_FILE"

log "HOY: $TOTAL_FOUND tareas para $TODAY"
echo "[OK] Hoy.md generado — $TOTAL_FOUND tareas para $TODAY"
