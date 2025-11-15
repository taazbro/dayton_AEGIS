#!/bin/bash

# Install Anthropic Claude SDK for AI analysis

echo ""
echo "🤖 Installing Claude SDK..."

pip install anthropic --quiet

if [ $? -eq 0 ]; then
    echo "✓ Claude SDK installed successfully"
else
    echo "❌ Claude SDK installation failed"
    exit 1
fi
