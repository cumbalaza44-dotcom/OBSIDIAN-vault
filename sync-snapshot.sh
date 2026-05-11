#!/bin/bash
# Vault Snapshot Generator — produce resumen LLM-legible del vault
# Llamado por sync-pull.sh cuando detecta cambios.
# Output: ~40 líneas de markdown. Sin Dataview. Sin queries.

VAULT_DIR="/root/.openclaw/workspace/obsidian-vault"
SNAPSHOT_FILE="/root/.openclaw/workspace/obsidian-vault/_VAULT-SNAPSHOT.md"
LOG_FILE="/var/log/obsidian-sync.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
}

cd "$VAULT_DIR" || { log "ERROR: cannot cd to vault"; exit 1; }

# ── Gather all markdown files (exclude system files and git) ──
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
            task=$(echo "$line" | sed 's/^\s*-\s*\[ \]\s*//')
            filepath=$(echo "$f" | sed 's/^\.\///')
            TASKS+=("- [ ] $task  — *$filepath*")
        fi
    done <<< "$content"
done

# ── Get recently modified notes (top 5 by mtime) ──
RECENT_FILES=()
while IFS= read -r line; do
    RECENT_FILES+=("$line")
done < <(for f in "${MD_FILES[@]}"; do
    mtime=$(stat -c '%Y' "$f" 2>/dev/null || echo 0)
    echo "$mtime|$(echo "$f" | sed 's/^\.\///')"
done | sort -t'|' -k1 -rn | head -5)

# ── Generate directory tree ──
generate_tree() {
    # Build a flat list of entries (dir|file) sorted
    local tmp_entries=$(mktemp)
    local tmp_dirs=$(mktemp)
    
    for f in "${MD_FILES[@]}"; do
        relpath=$(echo "$f" | sed 's/^\.\///')
        dir=$(dirname "$relpath")
        base=$(basename "$relpath")
        
        if [ "$dir" = "." ]; then
            echo "ROOT|$base" >> "$tmp_entries"
        else
            echo "$dir|$base" >> "$tmp_entries"
            # Register directory and all parents
            local pd="$dir"
            while [ -n "$pd" ] && [ "$pd" != "." ]; do
                echo "$pd" >> "$tmp_dirs"
                pd=$(dirname "$pd")
            done
        fi
    done
    
    # Print root files
    while IFS='|' read -r _ base; do
        echo "📄 $base"
    done < <(grep "^ROOT|" "$tmp_entries" | sort)
    
    # Get sorted unique directories (by path)
    local sorted_dirs=$(sort -u "$tmp_dirs" | sort -t'/' -k1,10)
    local printed=""
    
    while IFS= read -r d; do
        [ -z "$d" ] && continue
        # Check if already printed (parent would have printed it)
        case " $printed " in
            *" $d "*) continue ;;
        esac
        
        local depth=$(echo "$d" | tr -cd '/' | wc -c)
        local dname=$(basename "$d")
        local indent=""
        local i=0
        while [ "$i" -lt "$depth" ]; do
            indent="${indent}  "
            i=$((i+1))
        done
        
        echo "${indent}📁 $dname/"
        printed="$printed $d "
        
        # Gather files in this directory
        local dir_escaped=$(echo "$d" | sed 's|/|\\/|g')
        local file_entries=$(grep "^$d_escaped|" "$tmp_entries" | sort)
        local total=$(echo "$file_entries" | grep -c .)
        [ "$total" -eq 0 ] && continue
        
        local idx=0
        while IFS='|' read -r _ base; do
            [ -z "$base" ] && continue
            idx=$((idx+1))
            if [ "$idx" -eq "$total" ]; then
                echo "${indent}  └── $base"
            else
                echo "${indent}  ├── $base"
            fi
        done <<< "$file_entries"
    done <<< "$sorted_dirs"
    
    rm -f "$tmp_entries" "$tmp_dirs"
}

# ── Build snapshot ──
{
    echo "# VAULT SNAPSHOT"
    echo "> Generado: $(date '+%Y-%m-%d %H:%M') UTC-5"
    echo ""
    echo "## 📊 Stats"
    echo "- Notas: **$TOTAL** | Carpetas: **$FOLDER_COUNT** | Vacías: **${#EMPTY_FILES[@]}** | Tareas pendientes: **${#TASKS[@]}**"
    echo ""
    
    # ── Directory tree ──
    echo "## 📁 Estructura del vault ($TOTAL archivos)"
    generate_tree
    echo ""

    # ── Recently modified ──
    if [ ${#RECENT_FILES[@]} -gt 0 ]; then
        echo "## 🆕 Modificados recientemente"
        for entry in "${RECENT_FILES[@]}"; do
            mtime_epoch=$(echo "$entry" | cut -d'|' -f1)
            filepath=$(echo "$entry" | cut -d'|' -f2-)
            readable=$(date -d "@$mtime_epoch" '+%Y-%m-%d %H:%M' 2>/dev/null)
            echo "- $filepath — *$readable*"
        done
        echo ""
    fi

    # ── Pending tasks ──
    if [ ${#TASKS[@]} -gt 0 ]; then
        echo "## 📝 Tareas pendientes"
        for t in "${TASKS[@]}"; do
            echo "$t"
        done
        echo ""
    fi

    # ── Empty notes ──
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