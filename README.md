# Claude Code Config

Ma configuration personnalisée Claude Code, versionnée et portable.

## Installation

```bash
git clone <repo> ~/code/claude-config
cd ~/code/claude-config
./scripts/symlink.sh
```

Le script :
1. Backup les fichiers existants dans `~/.claude.backup.<timestamp>/`
2. Crée les symlinks vers `~/.claude/`
3. Installe les dépendances npm pour les hooks TypeScript

## Contenu

### Agents

| Nom | Description | Model |
|-----|-------------|-------|
| `backend-architect` | Architecture backend, API design, microservices | sonnet |
| `code-reviewer` | Review code : qualité, sécurité, maintenabilité | sonnet |
| `doc-writer` | Rédacteur documentation technique optimisée LLM | sonnet |
| `frontend-developer` | Développement React, responsive design, a11y | sonnet |

### Skills

| Nom | Description | Déclencheur |
|-----|-------------|-------------|
| `error-memory` | Documente les erreurs pour éviter de les répéter | Erreur, correction user, mauvaise approche |
| `llm-doc-writer` | Écriture documentation token-efficient | Création CLAUDE.md, README, docs techniques |

### Hooks

| Hook | Event | Description |
|------|-------|-------------|
| `skill-activation-prompt` | UserPromptSubmit | Suggère les skills pertinents à chaque prompt |
| `usage-tracker` | PreToolUse (Skill\|Task) | Track l'utilisation des skills et agents |

### Commands

| Commande | Description |
|----------|-------------|
| `/usage-stats` | Affiche les statistiques d'utilisation des outils |

### Plugins (externes)

Installés via marketplace, référencés dans `settings.json` :

| Plugin | Source | Description |
|--------|--------|-------------|
| `typescript-lsp` | claude-plugins-official | LSP TypeScript pour navigation code |
| `ralph-wiggum` | claude-plugins-official | Technique de réflexion itérative |
| `frontend-design` | claude-plugins-official | Design frontend production-grade |
| `superpowers` | superpowers-marketplace | Skills workflow (TDD, debugging, planning, etc.) |

Installation : `claude mcp add <plugin>` ou via UI Claude Code.

## Configuration

| Fichier | Contenu |
|---------|---------|
| `src/CLAUDE.md` | Instructions globales (langue, style) |
| `src/settings.json` | Permissions, hooks config, plugins activés |

## Structure

```
.
├── .claude/           # Config locale de ce projet
├── scripts/
│   └── symlink.sh     # Script d'installation
├── src/               # Fichiers linkés vers ~/.claude/
│   ├── CLAUDE.md
│   ├── settings.json
│   ├── agents/
│   ├── commands/
│   ├── hooks/
│   └── skills/
└── README.md
```

## Ajouter un outil

1. Créer le fichier dans `src/<type>/`
2. Si nouveau chemin, ajouter dans `scripts/symlink.sh` (array `ITEMS`)
3. Mettre à jour ce README
4. `./scripts/symlink.sh`
5. Commit

## Fichiers exclus (jamais commités)

| Fichier | Raison |
|---------|--------|
| `.credentials.json` | Tokens OAuth |
| `settings.local.json` | Permissions locales |
| `history.jsonl` | Historique personnel |
| `plugins/` | Installés via marketplace |
| `node_modules/` | Dépendances |
