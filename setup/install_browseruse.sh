#!/bin/bash

# Install BrowserUse for attack replay (optional)

echo ""
echo "🌐 Installing BrowserUse dependencies..."

# BrowserUse is optional, so we don't fail if it's not available
pip install playwright --quiet 2>/dev/null || {
    echo "⚠️  Playwright installation skipped (optional)"
    echo "   BrowserUse will run in mock mode"
}

# Install Playwright browsers (if playwright was installed)
if command -v playwright &> /dev/null; then
    playwright install chromium --quiet 2>/dev/null || echo "⚠️  Browser installation skipped"
fi

echo "✓ BrowserUse setup complete (mock mode enabled)"
