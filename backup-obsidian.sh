#!/bin/bash

# Backup Script for Obsidian Vault
# Simple, reliable, and production-ready

set -o errexit  # Exit on error
set -o pipefail # Fail on pipeline errors

# Configuration
WORKSPACE="/root/.openclaw/workspace/obsidian-vault"
BACKUP_LOG="/var/log/obsidian-backup.log"
SSH_KEY="/root/.ssh/id_ed25519_obsidian2"

# Logging with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$BACKUP_LOG"
}

# Main execution
main() {
    log "Starting backup process..."
    
    # Navigate to workspace
    cd "$WORKSPACE" || { log "ERROR: Cannot access workspace"; return 1; }
    
    # Load SSH key if available
    if [[ -f "$SSH_KEY" ]]; then
        ssh-add "$SSH_KEY" 2>/dev/null || true
        log "SSH key loaded"
    else
        log "No SSH key found, continuing without"
    fi
    
    # Add files from known patterns (ignore errors if no files match)
    add_files "*.md"
    add_files "*.json"
    add_files "*.yaml"
    add_files "*.txt"
    add_files "*.csv"
    
    # Check if there are changes to commit
    if git diff --cached --quiet; then
        log "No changes detected - backup skipped"
        return 0
    fi
    
    # Commit changes
    local commit_msg="SYNC: $(date +'%Y-%m-%d %H:%M')"
    git commit -m "$commit_msg" || { log "ERROR: Git commit failed"; return 1; }
    log "Committed: $commit_msg"
    
    # Push to GitHub
    git fetch origin || { log "ERROR: Git fetch failed"; return 1; }
    git push --force-with-lease origin HEAD:main || { log "ERROR: Git push failed"; return 1; }
    
    log "Backup completed successfully"
    return 0
}

# Helper function to add files safely
add_files() {
    local pattern="$1"
    git add $pattern 2>/dev/null || true
    # Log if files were added
    local count=$(git status --porcelain $pattern 2>/dev/null | wc -l)
    if [[ $count -gt 0 ]]; then
        log "Added $count file(s) from pattern: $pattern"
    fi
}

# Run main function
main "$@"
