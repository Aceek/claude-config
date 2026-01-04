#!/bin/bash
set -e

cd "$HOME/.claude/hooks/skill-activation-prompt"
cat | npx tsx index.ts
