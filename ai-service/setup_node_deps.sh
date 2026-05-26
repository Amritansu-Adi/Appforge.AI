#!/usr/bin/env bash
# setup_node_deps.sh
# Installs Node.js packages required by Python MCP validation tools.
# Run once after cloning, or add to your Dockerfile RUN step.
# These are called via subprocess from validate_js.py, validate_jsx.py, validate_mermaid.py

set -e

echo "Installing Node.js dependencies for Python MCP validation tools..."

npm install -g acorn @babel/parser

echo "✅ Node.js MCP dependencies installed."
echo "   acorn     — JS syntax validation"
echo "   @babel/parser — JSX syntax validation"
echo ""
echo "Note: Mermaid validation uses a lightweight built-in check."
echo "      For full Mermaid parsing, install: npm install -g @mermaid-js/mermaid-cli"
