# Claude Config - Project Instructions

Projet de gestion de ma configuration Claude Code personnelle.

## Objectif

Maintenir et versionner la configuration ~/.claude/ de manière sécurisée.

## Structure

```
.
├── .claude/           # Config locale de ce projet (méta)
├── scripts/
│   └── symlink.sh     # Installation des symlinks
├── src/               # Fichiers linkés vers ~/.claude/
│   ├── CLAUDE.md      # Instructions globales
│   ├── settings.json  # Permissions, hooks, plugins
│   ├── agents/        # Agents custom
│   ├── commands/      # Commandes custom
│   ├── hooks/         # Hooks custom
│   └── skills/        # Skills custom
└── README.md          # Documentation
```

## Workflows

### Ajouter un nouvel outil

1. Créer le fichier dans `src/<type>/`
2. Si nouveau chemin, ajouter l'entrée dans `scripts/symlink.sh` (array ITEMS)
3. Mettre à jour README.md
4. Relancer `./scripts/symlink.sh`
5. Commit

### Modifier un outil existant

1. Éditer directement dans `src/` (le symlink reflète les changements)
2. Tester avec Claude Code
3. Commit

### Installation sur nouvelle machine

```bash
git clone <repo> ~/code/claude-config
cd ~/code/claude-config
./scripts/symlink.sh
```

## Standards

- Documentation en français
- Code/commits en anglais
- Pas de secrets dans le repo (voir .gitignore)
