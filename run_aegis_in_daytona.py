#!/usr/bin/env python3
"""
AEGIS - Run in Daytona Sandbox (SDK-based)
Uses official Daytona SDK to run AEGIS demo
"""

import os
from daytona import Daytona, DaytonaConfig
from dotenv import load_dotenv

# Load environment
load_dotenv()

print("="*80)
print("🛡️  AEGIS - DAYTONA SANDBOX DEMO".center(80))
print("="*80)
print()

# Get API keys
daytona_key = os.getenv("DAYTONA_API_KEY")
sentry_dsn = os.getenv("SENTRY_DSN")
claude_key = os.getenv("CLAUDE_API_KEY")
galileo_key = os.getenv("GALILEO_API_KEY")
slack_webhook = os.getenv("SLACK_WEBHOOK_URL")

print("📋 API Keys Status:")
print(f"   DAYTONA: {'✅' if daytona_key else '❌'}")
print(f"   SENTRY: {'✅' if sentry_dsn else '❌'}")
print(f"   CLAUDE: {'✅' if claude_key else '❌'}")
print(f"   GALILEO: {'✅' if galileo_key else '❌'}")
print(f"   SLACK: {'✅' if slack_webhook else '⚠️'}")
print()

# Initialize Daytona
print("Initializing Daytona...")
config = DaytonaConfig(api_key=daytona_key)
daytona = Daytona(config)
print("✅ Daytona initialized")
print()

# Create sandbox
print("Creating sandbox (this may take 30-60 seconds)...")
sandbox = daytona.create()
print(f"✅ Sandbox created: {sandbox.id}")

# Get sandbox home directory
home_dir = sandbox.get_user_home_dir()
work_dir = f"{home_dir}/aegis"
print(f"   Home: {home_dir}")
print(f"   Work dir: {work_dir}")
print()

# Clone repository
print("Cloning AEGIS repository...")
sandbox.git.clone(
    url="https://github.com/taazbro/dayton_AEGIS",
    path=work_dir
)
print("✅ Repository cloned")
print()

# Create .env file
print("Setting up environment...")
env_commands = f"""cat > {work_dir}/.env << 'EOF'
SENTRY_DSN={sentry_dsn}
ANTHROPIC_API_KEY={claude_key}
CLAUDE_API_KEY={claude_key}
GALILEO_API_KEY={galileo_key}
SLACK_WEBHOOK_URL={slack_webhook}
GALILEO_PROJECT=aegis
GALILEO_LOG_STREAM=daytona-demo
EOF
"""
result = sandbox.process.exec(env_commands, cwd=work_dir)
if result.exit_code == 0:
    print("✅ Environment configured")
else:
    print(f"⚠️  Environment setup issue (exit code: {result.exit_code})")
print()

# Install dependencies
print("Installing dependencies (1-2 minutes)...")
result = sandbox.process.exec(
    "pip3 install -r requirements.txt",
    cwd=work_dir,
    timeout=180
)
if result.exit_code == 0:
    print("✅ Dependencies installed")
else:
    print(f"⚠️  Installation issues (exit code: {result.exit_code})")
print()

# Run the demo
print("="*80)
print("🎬 RUNNING AEGIS DEMO".center(80))
print("="*80)
print()

result = sandbox.process.exec(
    "python3 demo_pitch_live.py --scenario sql_injection",
    cwd=work_dir,
    timeout=300
)

print()
print("="*80)

if result.exit_code == 0:
    print("✅ Demo completed successfully!")
else:
    print(f"⚠️  Demo exited with code: {result.exit_code}")

print()
print("📊 Output:")
print("-"*80)
if hasattr(result, 'stdout') and result.stdout:
    print(result.stdout)
elif hasattr(result, 'output') and result.output:
    print(result.output)
else:
    print(result)
print("-"*80)

# Cleanup
print()
keep = input("Keep sandbox running? (y/n): ").strip().lower()
if keep != 'y':
    print("Deleting sandbox...")
    sandbox.delete()
    print("✅ Sandbox deleted")
else:
    print(f"✅ Sandbox still running: {sandbox.id}")

print()
print("="*80)
print("🏁 COMPLETE".center(80))
print("="*80)
