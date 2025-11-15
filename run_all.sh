#!/bin/bash

##############################################################################
# AEGIS DAYTONA AUTO-RUN SCRIPT
# Automatically sets up and runs AEGIS in a Daytona workspace
##############################################################################

set -e  # Exit on error

echo "════════════════════════════════════════════════════════════════════════════"
echo "🛡️  AEGIS AUTONOMOUS CYBER DEFENSE - DAYTONA AUTO-SETUP"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

##############################################################################
# STEP 1: Verify we're in the project root
##############################################################################

echo -e "${YELLOW}[1/8] Verifying project structure...${NC}"

if [ ! -f "main.py" ]; then
    echo -e "${RED}❌ ERROR: main.py not found. Are you in the project root?${NC}"
    exit 1
fi

if [ ! -d "src" ]; then
    echo -e "${RED}❌ ERROR: src/ directory not found. Are you in the project root?${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Project structure verified${NC}"
echo ""

##############################################################################
# STEP 2: Create/Activate Virtual Environment
##############################################################################

echo -e "${YELLOW}[2/8] Setting up Python virtual environment...${NC}"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo -e "${GREEN}✓ Virtual environment active${NC}"
echo ""

##############################################################################
# STEP 3: Install Dependencies
##############################################################################

echo -e "${YELLOW}[3/8] Installing Python dependencies...${NC}"

if [ -f "requirements.txt" ]; then
    pip install --quiet --upgrade pip
    pip install --quiet -r requirements.txt
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠️  requirements.txt not found, skipping...${NC}"
fi

echo ""

##############################################################################
# STEP 4: Load Environment Variables
##############################################################################

echo -e "${YELLOW}[4/8] Loading environment variables...${NC}"

if [ -f ".env" ]; then
    echo "Loading from .env file..."
    export $(cat .env | grep -v '^#' | xargs)
    echo -e "${GREEN}✓ Environment variables loaded${NC}"
else
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    echo "   Using existing environment variables..."
fi

echo ""

##############################################################################
# STEP 5: Verify Critical Environment Variables
##############################################################################

echo -e "${YELLOW}[5/8] Verifying sponsor API keys...${NC}"

# Check critical env vars
MISSING_VARS=()

[ -z "$SENTRY_DSN" ] && MISSING_VARS+=("SENTRY_DSN")
[ -z "$ANTHROPIC_API_KEY" ] && [ -z "$CLAUDE_API_KEY" ] && MISSING_VARS+=("ANTHROPIC_API_KEY or CLAUDE_API_KEY")
[ -z "$GALILEO_API_KEY" ] && MISSING_VARS+=("GALILEO_API_KEY")

if [ ${#MISSING_VARS[@]} -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Missing environment variables:${NC}"
    for var in "${MISSING_VARS[@]}"; do
        echo "   - $var"
    done
    echo ""
    echo "   The demo will run but some features may not work."
    echo "   Set these in your .env file for full functionality."
    echo ""
else
    echo -e "${GREEN}✓ All critical API keys present${NC}"
fi

# Show what we have
echo ""
echo "📋 Configuration Status:"
echo "   SENTRY_DSN: ${SENTRY_DSN:+SET}"
echo "   CLAUDE_API_KEY: ${ANTHROPIC_API_KEY:-${CLAUDE_API_KEY:+SET}}"
echo "   GALILEO_API_KEY: ${GALILEO_API_KEY:+SET}"
echo "   SLACK_WEBHOOK_URL: ${SLACK_WEBHOOK_URL:+SET}"
echo "   BROWSERUSE_API_KEY: ${BROWSERUSE_API_KEY:+SET}"
echo "   DAYTONA_API_KEY: ${DAYTONA_API_KEY:+SET}"
echo ""

##############################################################################
# STEP 6: Quick Sentry Test
##############################################################################

echo -e "${YELLOW}[6/8] Testing Sentry connection...${NC}"

if [ -n "$SENTRY_DSN" ]; then
    python3 -c "
from src.sentry_init import init_sentry
try:
    init_sentry()
    print('${GREEN}✓ Sentry initialized${NC}')
except Exception as e:
    print('${YELLOW}⚠️  Sentry init failed:', str(e), '${NC}')
" || echo -e "${YELLOW}⚠️  Sentry test failed (continuing anyway)${NC}"
else
    echo -e "${YELLOW}⚠️  Sentry DSN not set, skipping test${NC}"
fi

echo ""

##############################################################################
# STEP 7: Pre-flight Check
##############################################################################

echo -e "${YELLOW}[7/8] Pre-flight check...${NC}"

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "   Python version: $PYTHON_VERSION"

# Check if we can import key modules
python3 -c "
import sys
import os

modules_to_check = [
    'sentry_sdk',
    'anthropic',
]

missing = []
for module in modules_to_check:
    try:
        __import__(module)
    except ImportError:
        missing.append(module)

if missing:
    print('${YELLOW}⚠️  Missing Python packages:', ', '.join(missing), '${NC}')
    print('   Run: pip install', ' '.join(missing))
else:
    print('${GREEN}✓ All critical Python packages installed${NC}')
"

echo ""

##############################################################################
# STEP 8: Launch AEGIS
##############################################################################

echo "════════════════════════════════════════════════════════════════════════════"
echo -e "${GREEN}✅ SETUP COMPLETE - LAUNCHING AEGIS${NC}"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""
echo "🎯 Starting main orchestrator..."
echo "   Press Ctrl+C to stop"
echo ""
echo "────────────────────────────────────────────────────────────────────────────"
echo ""

# Launch main.py
python3 main.py

##############################################################################
# Cleanup on exit
##############################################################################

echo ""
echo "════════════════════════════════════════════════════════════════════════════"
echo "🛑 AEGIS SHUTDOWN COMPLETE"
echo "════════════════════════════════════════════════════════════════════════════"
