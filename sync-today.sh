#!/bin/bash
# Hoy.md Generator — produce lista de tareas del día actual
# Escanea todas las notas del vault en busca de tareas con 📅 YYYY-MM-DD = hoy
# Separa pendientes [ ] de completadas [x]
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

# ── Gather all markdown files ──
mapfile -t MD_FILES < <(find . -name "*.md" \
  -not -name "_VAULT-INDEX.md" \
  -not -name "_VAULT-SNAPSHOT.md" \
  -not -name "Hoy.md" \
  -not -path "./.git/*" \
  | sort)

# ── Scan: separate pending vs completed ──
PENDING_ENTRIES=()
COMPLETED_ENTRIES=()
PENDING=0
COMPLETED=0

for f in "${MD_FILES[@]}"; do
    relpath=$(echo "$f" | sed 's/^\.\///')
    
    while IFS= read -r line; do
        if echo "$line" | grep -qE "📅[[:space:]]*$TODAY"; then
            if echo "$line" | grep -qE '^- \[ \]'; then
                PENDING_ENTRIES+=("$relpath|$(echo "$line" | sed 's/^- //')")
                PENDING=$((PENDING + 1))
            elif echo "$line" | grep -qE '^- \[x\]'; then
                COMPLETED_ENTRIES+=("$relpath|$(echo "$line" | sed 's/^- //')")
                COMPLETED=$((COMPLETED + 1))
            fi
        fi
    done < "$f"
done

# ── Build Hoy.md ──
{
    echo "# 📋 Hoy — $TODAY_SHORT"
    echo ""
    
    if [ "$PENDING" -eq 0 ] && [ "$COMPLETED" -eq 0 ]; then
        echo "*Sin tareas programadas para hoy.* 🎯"
    else
        # ── Summary ──
        echo "**⏳ $PENDING pendientes | ✅ $COMPLETED completadas**"
        echo ""
        
        # ── Pending section ──
        if [ "$PENDING" -gt 0 ]; then
            echo "## ⏳ Pendientes"
            echo ""
            last_src=""
            for entry in "${PENDING_ENTRIES[@]}"; do
                src="${entry%%|*}"
                task="${entry#*|}"
                [ "$src" != "$last_src" ] && echo "### 📁 $src" && last_src="$src"
                echo "- $task"
            done
            echo ""
        fi
        
        # ── Completed section ──
        if [ "$COMPLETED" -gt 0 ]; then
            echo "## ✅ Completadas"
            echo ""
            last_src=""
            for entry in "${COMPLETED_ENTRIES[@]}"; do
                src="${entry%%|*}"
                task="${entry#*|}"
                [ "$src" != "$last_src" ] && echo "### 📁 $src" && last_src="$src"
                echo "- $task"
            done
            echo ""
        fi
    fi
    
    echo "---"
    echo "*Auto-generado: $(date '+%Y-%m-%d %H:%M') UTC-5*"
} > "$TODAY_FILE"

log "HOY: $PENDING pendientes, $COMPLETED completadas para $TODAY"
echo "[OK] Hoy.md generado — $PENDING pendientes, $COMPLETED completadas"
