#!/bin/bash

# MJnCompany_2-0 Installer for Claude Code
# Automatically installs to ~/.claude/plugins/marketplaces/

set -e

PLUGIN_NAME="MJnCompany_2-0"
REPO_URL="https://github.com/nh-investment-squad1/MJnCompany_2-0"
INSTALL_DIR="$HOME/.claude/plugins/marketplaces/$PLUGIN_NAME"

echo "Installing MJnCompany_2-0 for Claude Code..."

# Create marketplaces directory if it doesn't exist
mkdir -p "$HOME/.claude/plugins/marketplaces"

# Check if already installed
if [ -d "$INSTALL_DIR" ]; then
    echo "MJnCompany_2-0 already installed. Updating..."
    cd "$INSTALL_DIR"
    git pull origin main
    echo "Updated successfully!"
else
    echo "Cloning repository..."
    git clone "$REPO_URL" "$INSTALL_DIR"
    echo "Installed successfully!"
fi

echo ""
echo "Installation complete!"
echo "Location: $INSTALL_DIR"
echo ""
echo "Please restart Claude Code to load the new plugins."
echo ""
echo "Available team members:"
echo "  - cs-ceo              : CEO / orchestrator"
echo "  - cs-clarify          : PM / requirements elicitation"
echo "  - CS-plan             : Architect (TDD + Clean Architecture)"
echo "  - cs-design           : Designer (5-agent design review)"
echo "  - cs-design-sample1   : Design system reference"
echo "  - CS-test             : QA engineer (14-agent web testing)"
echo "  - CS-codebase-review  : Code reviewer (5-agent parallel review)"
echo "  - cs-ship             : DevOps (pre-PR validation gate)"
echo "  - cs-smart-run        : Team lead (Opus plan + Sonnet parallel execution)"
echo "  - cs-experiencing     : Knowledge keeper"
echo "  - convo-maker         : Language coach"
