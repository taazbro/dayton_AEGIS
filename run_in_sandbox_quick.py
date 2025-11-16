#!/usr/bin/env python3
"""Quick run AEGIS in existing sandbox"""
import os
from dotenv import load_dotenv
load_dotenv()

from daytona_sdk import Daytona, DaytonaConfig

SANDBOX_ID = "16d8bbdc-aa25-4c5b-9d8f-7ec4c280c2f0"

print("🛡️ Running AEGIS in Daytona Sandbox...\n")

config = DaytonaConfig(
    api_key=os.getenv("DAYTONA_API_KEY"),
    api_url=os.getenv("DAYTONA_API_URL", "https://app.daytona.io/api")
)
daytona = Daytona(config)
sandbox = daytona.get(SANDBOX_ID)

home = sandbox.get_user_home_dir()
work_dir = f"{home}/aegis"

# Make sure repo exists
print("📂 Checking AEGIS repository...")
result = sandbox.process.exec(f"test -d {work_dir} && echo 'EXISTS' || git clone https://github.com/taazbro/dayton_AEGIS {work_dir}")
print("✅ Repository ready\n")

# Set environment
print("🔐 Setting environment variables...")
env_content = f"""SENTRY_DSN={os.getenv('SENTRY_DSN')}
ANTHROPIC_API_KEY={os.getenv('CLAUDE_API_KEY')}
CLAUDE_API_KEY={os.getenv('CLAUDE_API_KEY')}
GALILEO_API_KEY={os.getenv('GALILEO_API_KEY')}
SLACK_WEBHOOK_URL={os.getenv('SLACK_WEBHOOK_URL')}
GALILEO_PROJECT=aegis
GALILEO_LOG_STREAM=daytona-demo
"""
sandbox.process.exec(f"cat > {work_dir}/.env << 'EOF'\n{env_content}\nEOF")
print("✅ Environment set\n")

# Install deps (quick check)
print("📦 Installing dependencies...")
sandbox.process.exec(f"cd {work_dir} && pip3 install -q -r requirements.txt", timeout=120)
print("✅ Dependencies ready\n")

# RUN THE DEMO
print("="*80)
print("🎬 RUNNING AEGIS AUTONOMOUS DEFENSE DEMO")
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
else:
    print(f"⚠️ Exit code: {result.exit_code}")

print()
print("🎯 Demo ran in Daytona sandbox online!")
print(f"📦 Sandbox ID: {SANDBOX_ID}")
print()
