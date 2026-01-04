#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
SRC_DIR="$REPO_DIR/src"
CLAUDE_DIR="$HOME/.claude"
BACKUP_DIR="$HOME/.claude.backup.$(date +%Y%m%d_%H%M%S)"

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== Claude Config Installer ===${NC}"
echo "Source: $SRC_DIR"
echo "Target: $CLAUDE_DIR"
echo ""

# Liste des éléments à linker
ITEMS=(
    "CLAUDE.md"
    "settings.json"
    "agents"
    "commands"
    "skills"
    "hooks/skill-activation-prompt"
    "hooks/usage-tracker"
)

# Vérifier les fichiers existants (non-symlinks)
EXISTING=()
for item in "${ITEMS[@]}"; do
    target="$CLAUDE_DIR/$item"
    if [[ -e "$target" && ! -L "$target" ]]; then
        EXISTING+=("$item")
    fi
done

# Backup si nécessaire
if [[ ${#EXISTING[@]} -gt 0 ]]; then
    echo -e "${YELLOW}Fichiers existants à sauvegarder:${NC}"
    for item in "${EXISTING[@]}"; do
        echo "  - $item"
    done
    echo ""
    echo -e "Backup vers: ${YELLOW}$BACKUP_DIR${NC}"

    mkdir -p "$BACKUP_DIR"
    for item in "${EXISTING[@]}"; do
        src="$CLAUDE_DIR/$item"
        dst="$BACKUP_DIR/$item"
        mkdir -p "$(dirname "$dst")"
        mv "$src" "$dst"
        echo -e "  ${GREEN}✓${NC} $item"
    done
    echo ""
fi

# Créer les dossiers parents si nécessaire
mkdir -p "$CLAUDE_DIR/hooks"

# Créer les symlinks
echo -e "${GREEN}Création des symlinks:${NC}"
for item in "${ITEMS[@]}"; do
    src="$SRC_DIR/$item"
    target="$CLAUDE_DIR/$item"

    # Supprimer symlink existant
    if [[ -L "$target" ]]; then
        rm "$target"
    fi

    ln -s "$src" "$target"
    echo -e "  ${GREEN}✓${NC} $item -> $src"
done
echo ""

# Installer les dépendances npm pour les hooks TypeScript
if [[ -f "$CLAUDE_DIR/hooks/skill-activation-prompt/package.json" ]]; then
    echo -e "${GREEN}Installation des dépendances npm...${NC}"
    (cd "$CLAUDE_DIR/hooks/skill-activation-prompt" && npm install --silent 2>/dev/null) || true
    echo -e "  ${GREEN}✓${NC} node_modules installé"
    echo ""
fi

echo -e "${GREEN}=== Installation terminée ===${NC}"
if [[ -d "$BACKUP_DIR" ]]; then
    echo -e "Backup disponible: ${YELLOW}$BACKUP_DIR${NC}"
fi
