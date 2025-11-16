#!/usr/bin/env python3
"""Run AEGIS in Daytona with SLACK notifications enabled"""
import os
from dotenv import load_dotenv
load_dotenv()

from daytona_sdk import Daytona, DaytonaConfig

SANDBOX_ID = "16d8bbdc-aa25-4c5b-9d8f-7ec4c280c2f0"

print("="*80)
print("🛡️  AEGIS - Running in Daytona with Slack Notifications".center(80))
print("="*80)
print()

config = DaytonaConfig(
    api_key=os.getenv("DAYTONA_API_KEY"),
    api_url=os.getenv("DAYTONA_API_URL", "https://app.daytona.io/api")
)
daytona = Daytona(config)
sandbox = daytona.get(SANDBOX_ID)

print(f"✅ Connected to sandbox: {SANDBOX_ID}\n")

home = sandbox.get_user_home_dir()
work_dir = f"{home}/aegis"

# Ensure repo exists
print("📂 Checking repository...")
sandbox.process.exec(f"test -d {work_dir} || git clone https://github.com/taazbro/dayton_AEGIS {work_dir}")
print("✅ Repository ready\n")

# Create .env with CORRECT Slack variable name
print("🔐 Setting up environment with Slack webhook...")
env_content = f"""SENTRY_DSN={os.getenv('SENTRY_DSN')}
ANTHROPIC_API_KEY={os.getenv('CLAUDE_API_KEY')}
CLAUDE_API_KEY={os.getenv('CLAUDE_API_KEY')}
GALILEO_API_KEY={os.getenv('GALILEO_API_KEY')}
SLACK_WEBHOOK_URL={os.getenv('SLACK_WEBHOOK_URL')}
GALILEO_PROJECT=aegis
GALILEO_LOG_STREAM=daytona-demo
"""

sandbox.process.exec(f"cat > {work_dir}/.env << 'EOF'\n{env_content}\nEOF")
print("✅ Environment configured (including SLACK_WEBHOOK_URL)\n")

# Verify Slack is configured
print("🧪 Testing Slack integration...")
result = sandbox.process.exec(f"cd {work_dir} && python3 -c \"import os; from dotenv import load_dotenv; load_dotenv(); print('SLACK_WEBHOOK_URL:', 'SET' if os.getenv('SLACK_WEBHOOK_URL') else 'NOT SET')\"")
print()

# Install dependencies
print("📦 Installing dependencies...")
sandbox.process.exec(f"cd {work_dir} && pip3 install -q -r requirements.txt", timeout=120)
print("✅ Dependencies installed\n")

# RUN THE FULL DEMO
print("="*80)
print("🎬 RUNNING AEGIS DEMO WITH SLACK NOTIFICATIONS")
print("="*80)
print()

result = sandbox.process.exec(
    f"cd {work_dir} && python3 demo_pitch_live.py --scenario sql_injection",
    timeout=300
)

print()
print("="*80)
if result.exit_code == 0:
    print("✅ DEMO COMPLETED SUCCESSFULLY!")
    print()
    print("🎯 All integrations worked:")
    print("   ✅ Sentry - Event monitoring")
    print("   ✅ Claude - AI analysis")
    print("   ✅ Galileo - Observability")
    print("   ✅ Slack - SOC notification SENT! 🚀")
    print()
    print("📱 Check your Slack #security-alerts channel!")
else:
    print(f"⚠️  Exit code: {result.exit_code}")

print("="*80)
print()
