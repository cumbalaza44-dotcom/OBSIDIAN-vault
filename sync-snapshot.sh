#!/bin/bash
# Vault Snapshot Generator — produce resumen LLM-legible del vault
# Llamado por sync-pull.sh cuando detecta cambios.
# Output: ~20 líneas de markdown puro. Sin Dataview. Sin queries.

VAULT_DIR="/root/.openclaw/workspace/obsidian-vault"
SNAPSHOT_FILE="/root/.openclaw/workspace/obsidian-vault/_VAULT-SNAPSHOT.md"
LOG_FILE="/var/log/obsidian-sync.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
}

cd "$VAULT_DIR" || { log "ERROR: cannot cd to vault"; exit 1; }

# ── Gather all markdown files (exclude index/snapshot/git) ──
mapfile -t MD_FILES < <(find . -name "*.md" \
  -not -name "_VAULT-INDEX.md" \
  -not -name "_VAULT-SNAPSHOT.md" \
  -not -path "./.git/*" \
  | sort)

TOTAL=${#MD_FILES[@]}

# ── Extract folders ──
declare -A FOLDERS
for f in "${MD_FILES[@]}"; do
    dir=$(dirname "$f" | sed 's/^\.\///')
    [ -z "$dir" ] && dir="(root)"
    FOLDERS["$dir"]=$((FOLDERS["$dir"] + 1))
done
FOLDER_COUNT=${#FOLDERS[@]}

# ── Extract incomplete tasks ──
TASKS=()
EMPTY_FILES=()
for f in "${MD_FILES[@]}"; do
    content=$(cat "$f")
    lines=$(echo "$content" | wc -l)
    
    # Empty detection
    trimmed=$(echo "$content" | tr -d '[:space:]')
    if [ -z "$trimmed" ] || [ "$lines" -le 1 ]; then
        EMPTY_FILES+=("$(echo "$f" | sed 's/^\.\///')")
    fi
    
    # Task extraction
    while IFS= read -r line; do
        if echo "$line" | grep -qE '^\s*-\s*\[ \]'; then
            # Clean up: remove leading - [ ] and trim
            task=$(echo "$line" | sed 's/^\s*-\s*\[ \]\s*//')
            filepath=$(echo "$f" | sed 's/^\.\///')
            TASKS+=("- [ ] $task  — *$filepath*")
        fi
    done <<< "$content"
done

# ── Get last 3 created notes ──
RECENT=()
while IFS= read -r f; do
    RECENT+=("$(echo "$f" | sed 's/^\.\///')")
done < <(for f in "${MD_FILES[@]}"; do
    echo "$(stat -c '%Y' "$f" 2>/dev/null || echo 0)|$f"
done | sort -t'|' -k1 -rn | head -3 | cut -d'|' -f2)

# ── Build snapshot ──
{
    echo "# VAULT SNAPSHOT"
    echo "> Generado: $(date '+%Y-%m-%d %H:%M') UTC-5"
    echo ""
    echo "## 📊 Stats"
    echo "- Notas: **$TOTAL** | Carpetas: **$FOLDER_COUNT** | Vacías: **${#EMPTY_FILES[@]}** | Tareas pendientes: **${#TASKS[@]}**"
    echo ""

    if [ ${#TASKS[@]} -gt 0 ]; then
        echo "## 📝 Tareas pendientes"
        for t in "${TASKS[@]}"; do
            echo "$t"
        done
        echo ""
    fi

    if [ ${#RECENT[@]} -gt 0 ]; then
        echo "## 🆕 Cambios recientes"
        for r in "${RECENT[@]}"; do
            echo "- $r"
        done
        echo ""
    fi

    if [ ${#EMPTY_FILES[@]} -gt 0 ]; then
        echo "## 📄 Notas vacías"
        for e in "${EMPTY_FILES[@]}"; do
            echo "- $e"
        done
        echo ""
    fi

    echo "---"
    echo "*Snapshot auto-generado por sync-pull.sh — 0 tokens de LLM*"
} > "$SNAPSHOT_FILE"

log "SNAPSHOT: $TOTAL notas, ${#TASKS[@]} tasks, ${#EMPTY_FILES[@]} vacías"
