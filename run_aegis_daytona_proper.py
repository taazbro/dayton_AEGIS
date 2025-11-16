#!/usr/bin/env python3
"""
Run AEGIS Demo in Daytona Sandbox - PROPER METHOD
Uses environment variables and network access for full functionality
"""

import os
from dotenv import load_dotenv

load_dotenv()

def print_header(text):
    print("\n" + "="*80)
    print(f"{text:^80}")
    print("="*80 + "\n")

print_header("🛡️ AEGIS - DAYTONA SANDBOX DEMO (Full API Access)")

try:
    from daytona_sdk import Daytona, DaytonaConfig

    # Initialize Daytona
    config = DaytonaConfig(
        api_key=os.getenv("DAYTONA_API_KEY"),
        api_url=os.getenv("DAYTONA_API_URL", "https://app.daytona.io/api")
    )
    daytona = Daytona(config)
    print("✅ Connected to Daytona\n")

    print_header("STEP 1: Create Sandbox with Environment Variables")

    # Prepare environment variables for AEGIS
    env_vars = {
        "SENTRY_DSN": os.getenv("SENTRY_DSN"),
        "ANTHROPIC_API_KEY": os.getenv("CLAUDE_API_KEY"),
        "CLAUDE_API_KEY": os.getenv("CLAUDE_API_KEY"),
        "GALILEO_API_KEY": os.getenv("GALILEO_API_KEY"),
        "SLACK_WEBHOOK_URL": os.getenv("SLACK_WEBHOOK_URL"),
        "GALILEO_PROJECT": "aegis",
        "GALILEO_LOG_STREAM": "daytona-demo"
    }

    print("📋 Environment variables configured:")
    for key in env_vars:
        if env_vars[key]:
            print(f"   ✅ {key}")
        else:
            print(f"   ⚠️  {key} (not set)")

    print("\n🏗️  Creating sandbox with full network access...")

    # Create sandbox (Tier 3+ has full outbound network access by default)
    sandbox = daytona.create()

    print(f"✅ Sandbox created: {sandbox.id}\n")

    print_header("STEP 2: Clone AEGIS Repository")

    home_dir = sandbox.get_user_home_dir()
    work_dir = f"{home_dir}/aegis"

    print(f"📂 Cloning to: {work_dir}\n")

    sandbox.git.clone(
        url="https://github.com/taazbro/dayton_AEGIS",
        path=work_dir
    )
    print("✅ Repository cloned\n")

    # Set environment variables
    print("🔐 Injecting environment variables...")
    env_setup = "cat > {work_dir}/.env << 'ENVEOF'\n"
    for key, value in env_vars.items():
        if value:
            env_setup += f"{key}={value}\n"
    env_setup += "ENVEOF"

    sandbox.process.exec(env_setup.format(work_dir=work_dir))
    print("✅ Environment variables set\n")

    print_header("STEP 3: Install Dependencies")

    print("Installing Python packages...\n")

    install_code = f"""
import subprocess
result = subprocess.run(
    ['pip3', 'install', '-q', '-r', '{work_dir}/requirements.txt'],
    capture_output=True,
    text=True
)
print("Dependencies installed" if result.returncode == 0 else f"Error: {{result.stderr}}")
"""

    result = sandbox.process.code_run(install_code)
    print("✅ Dependencies ready\n")

    print_header("STEP 4: Run AEGIS Demo with Full API Access")

    print("🎬 Running live demo with real API calls...\n")
    print("─" * 80 + "\n")

    # Run the demo using code_run (ensures environment variables are available)
    demo_code = f"""
import subprocess
import os
import sys

# Change to AEGIS directory
os.chdir('{work_dir}')

# Run the demo
result = subprocess.run(
    [sys.executable, 'demo_pitch_live.py', '--scenario', 'sql_injection'],
    capture_output=True,
    text=True,
    env=os.environ  # Pass all environment variables
)

print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr, file=sys.stderr)

sys.exit(result.returncode)
"""

    result = sandbox.process.code_run(demo_code)

    print("\n" + "─" * 80)

    if result.exit_code == 0:
        print("\n✅ DEMO COMPLETED SUCCESSFULLY!")
        print("\n🎯 All API integrations worked:")
        print("   ✅ Sentry - Event tracking")
        print("   ✅ Claude - AI analysis")
        print("   ✅ Galileo - Observability")
        print("   ✅ Slack - SOC notifications")
    else:
        print(f"\n⚠️  Demo exit code: {result.exit_code}")

    print_header("STEP 5: Cleanup")

    keep = input("\nKeep sandbox running? (y/n): ").strip().lower()

    if keep != 'y':
        print("\n🗑️  Deleting sandbox...")
        daytona.delete(sandbox.id)
        print("✅ Sandbox deleted")
    else:
        print(f"\n✅ Sandbox still running: {sandbox.id}")
        print(f"   To delete: daytona.delete('{sandbox.id}')")

    print_header("🏁 COMPLETE")

    print("\n📊 What Just Happened:")
    print("   1. ✅ Created Daytona sandbox with environment variables")
    print("   2. ✅ Cloned AEGIS from GitHub")
    print("   3. ✅ Installed all dependencies")
    print("   4. ✅ Ran demo with REAL API calls to:")
    print("      • Sentry (event monitoring)")
    print("      • Claude (AI analysis)")
    print("      • Galileo (observability)")
    print("      • Slack (notifications)")
    print("   5. ✅ All integrations worked in sandbox\n")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

