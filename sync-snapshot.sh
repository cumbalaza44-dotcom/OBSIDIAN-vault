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
    # Collect unique directory paths sorted
    declare -A DIR_FILES
    declare -A DIR_PARENT
    
    for f in "${MD_FILES[@]}"; do
        relpath=$(echo "$f" | sed 's/^\.\///')
        dir=$(dirname "$relpath")
        base=$(basename "$relpath")
        
        if [ "$dir" = "." ]; then
            dir=""
        fi
        DIR_FILES["$dir"]="${DIR_FILES["$dir"]}|$base"
    done
    
    # Collect all directories including nested ones
    declare -A ALL_DIRS
    for dir in "${!DIR_FILES[@]}"; do
        [ -z "$dir" ] && continue
        ALL_DIRS["$dir"]=1
        # Also register parent directories
        parent="$dir"
        while true; do
            parent=$(dirname "$parent")
            [ "$parent" = "." ] || [ -z "$parent" ] && break
            ALL_DIRS["$parent"]=1
        done
    done
    
    # Sort directories (root first, then by path)
    mapfile -t SORTED_DIRS < <(for d in "${!ALL_DIRS[@]}"; do echo "$d"; done | sort)
    
    # Helper: count indentation level
    level_of() {
        local d="$1"
        [ -z "$d" ] && echo "0" && return
        echo "$d" | tr -cd '/' | wc -c
        # plus 1 since empty root is level 0, top-level dirs are level 1
    }
    
    # Print files under root first (no directory prefix)
    root_files="${DIR_FILES[""]}"
    if [ -n "$root_files" ]; then
        IFS='|' read -ra files <<< "$root_files"
        # Remove empty first element from the split
        local first=true
        for rf in "${files[@]}"; do
            [ -z "$rf" ] && continue
            echo "📄 $rf"
        done
    fi
    
    # Print each directory and its files
    local prev_level=0
    for d in "${SORTED_DIRS[@]}"; do
        [ -z "$d" ] && continue
        
        level=$(level_of "$d")
        dirname=$(basename "$d")
        indent=""
        for ((i=0; i<level; i++)); do indent="${indent}  "; done
        
        echo "${indent}📁 $dirname/"
        
        # Print files in this directory
        files="${DIR_FILES["$d"]}"
        if [ -n "$files" ]; then
            IFS='|' read -ra file_list <<< "$files"
            local count=${#file_list[@]}
            local idx=0
            for rf in "${file_list[@]}"; do
                [ -z "$rf" ] && continue
                idx=$((idx+1))
                if [ $idx -eq $count ]; then
                    echo "${indent}  └── $rf"
                else
                    echo "${indent}  ├── $rf"
                fi
            done
        fi
    done
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