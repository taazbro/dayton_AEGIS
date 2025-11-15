#!/bin/bash

# Install Sentry SDK for error tracking

echo ""
echo "📊 Installing Sentry SDK..."

pip install sentry-sdk --quiet

if [ $? -eq 0 ]; then
    echo "✓ Sentry SDK installed successfully"
else
    echo "❌ Sentry SDK installation failed"
    exit 1
fi
