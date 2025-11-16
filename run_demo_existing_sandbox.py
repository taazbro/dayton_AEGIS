#!/usr/bin/env python3
"""
Run AEGIS Demo in EXISTING Daytona Sandbox
Uses already-created sandbox to avoid disk limit
"""

import os
import sys
import time
from dotenv import load_dotenv

load_dotenv()

def print_header(text):
    print("\n" + "="*80)
    print(f"{text:^80}")
    print("="*80 + "\n")

print_header("🛡️ AEGIS DAYTONA DEMO (Existing Sandbox)")

try:
    from daytona_sdk import Daytona, DaytonaConfig

    # Connect
    config = DaytonaConfig(
        api_key=os.getenv("DAYTONA_API_KEY"),
        api_url=os.getenv("DAYTONA_API_URL", "https://app.daytona.io/api")
    )
    daytona = Daytona(config)
    print("✅ Connected to Daytona\n")

    # Use existing sandbox
    SANDBOX_ID = "16d8bbdc-aa25-4c5b-9d8f-7ec4c280c2f0"

    print_header("STEP 1: Connect to Existing Sandbox")
    print(f"Using sandbox: {SANDBOX_ID}\n")
    sandbox = daytona.get(SANDBOX_ID)
    print(f"✅ Connected to sandbox\n")

    # Setup paths
    home_dir = sandbox.get_user_home_dir()
    work_dir = f"{home_dir}/aegis"

    # Clone AEGIS (skip if exists)
    print_header("STEP 2: Clone AEGIS Repository")
    print(f"📂 Cloning to: {work_dir}\n")
    try:
        sandbox.git.clone(
            url="https://github.com/taazbro/dayton_AEGIS",
            path=work_dir
        )
        print("✅ Repository cloned\n")
    except Exception as e:
        if "already exists" in str(e).lower() or "exists" in str(e).lower():
            print(f"✅ AEGIS already exists at {work_dir}\n")
        else:
            print(f"⚠️ Clone info: {e}\n")

    # Setup environment
    print_header("STEP 3: Configure Environment")
    env_content = f"""SENTRY_DSN={os.getenv('SENTRY_DSN')}
ANTHROPIC_API_KEY={os.getenv('CLAUDE_API_KEY')}
CLAUDE_API_KEY={os.getenv('CLAUDE_API_KEY')}
GALILEO_API_KEY={os.getenv('GALILEO_API_KEY')}
SLACK_WEBHOOK_URL={os.getenv('SLACK_WEBHOOK_URL')}
GALILEO_PROJECT=aegis
GALILEO_LOG_STREAM=daytona-demo
"""

    sandbox.process.exec(f"cat > {work_dir}/.env << 'EOF'\n{env_content}\nEOF")
    print("✅ Environment configured\n")

    # Install dependencies (if needed)
    print_header("STEP 4: Install Dependencies")
    print("Checking/installing packages...\n")
    result = sandbox.process.exec(
        f"cd {work_dir} && pip3 install -q -r requirements.txt",
        timeout=120
    )
    print("✅ Dependencies ready\n")

    # RUN THE DEMO
    print_header("🎬 RUNNING AEGIS LIVE DEMO")
    print("4-minute autonomous cyber defense demo!")
    print("─" * 80 + "\n")

    time.sleep(2)

    result = sandbox.process.exec(
        f"cd {work_dir} && python3 demo_pitch_live.py --scenario sql_injection",
        timeout=300
    )

    print("\n" + "─" * 80)

    if result.exit_code == 0:
        print("\n✅ DEMO COMPLETED SUCCESSFULLY!")
    else:
        print(f"\n⚠️ Demo exit code: {result.exit_code}")

    # Print output
    print("\n📊 DEMO OUTPUT:\n")
    print(result)

    print_header("🏁 DEMO COMPLETE!")
    print(f"\n✅ Sandbox still running: {SANDBOX_ID}")
    print("📦 Image: daytonaio/sandbox:0.4.3")
    print("🚀 Demo: AEGIS Autonomous Cyber Defense\n")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
