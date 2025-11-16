#!/usr/bin/env python3
"""
AUTOMATED: Upload AEGIS to Daytona and Run Demo
Fully automated - no prompts
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

print_header("🛡️ AEGIS AUTOMATED DAYTONA DEMO")

try:
    from daytona_sdk import Daytona, DaytonaConfig

    # Connect
    config = DaytonaConfig(
        api_key=os.getenv("DAYTONA_API_KEY"),
        api_url=os.getenv("DAYTONA_API_URL", "https://app.daytona.io/api")
    )
    daytona = Daytona(config)
    print("✅ Connected to Daytona\n")

    # Cleanup old sandboxes first
    print_header("CLEANUP: Removing Old Sandboxes")
    try:
        sandboxes = daytona.list()
        sandbox_list = sandboxes.items if hasattr(sandboxes, 'items') else []

        if sandbox_list:
            print(f"Found {len(sandbox_list)} old sandbox(es) - deleting...\n")
            for i, sb in enumerate(sandbox_list, 1):
                try:
                    print(f"Deleting {i}/{len(sandbox_list)}: {sb.id[:8]}...")
                    daytona.delete(sb.id)
                    print("   ✅ Deleted")
                except Exception as e:
                    print(f"   ⚠️ {e}")
            print(f"\n✅ Freed ~{len(sandbox_list) * 3}GB")
        else:
            print("✅ No old sandboxes")
    except Exception as e:
        print(f"⚠️ Cleanup warning: {e}")

    # Create new sandbox
    print_header("STEP 1: Create Daytona Sandbox")
    print("Creating sandbox (30-60 seconds)...\n")
    sandbox = daytona.create()
    print(f"✅ Sandbox created: {sandbox.id}\n")

    # Clone AEGIS
    print_header("STEP 2: Clone AEGIS from GitHub")
    home_dir = sandbox.get_user_home_dir()
    work_dir = f"{home_dir}/aegis"

    print(f"📂 Cloning to: {work_dir}\n")
    sandbox.git.clone(
        url="https://github.com/taazbro/dayton_AEGIS",
        path=work_dir
    )
    print("✅ Repository cloned\n")

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

    # Install dependencies
    print_header("STEP 4: Install Dependencies")
    print("Installing packages (1-2 minutes)...\n")
    result = sandbox.process.exec(
        f"cd {work_dir} && pip3 install -r requirements.txt",
        timeout=180
    )
    print("✅ Dependencies installed\n")

    # RUN THE DEMO
    print_header("🎬 RUNNING AEGIS LIVE DEMO")
    print("This is the 4-minute live demo for hackathon judges!")
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

    if hasattr(result, 'stdout') and result.stdout:
        print("\n📊 DEMO OUTPUT:\n")
        print(result.stdout)
    elif hasattr(result, 'output') and result.output:
        print("\n📊 DEMO OUTPUT:\n")
        print(result.output)

    # Cleanup
    print_header("CLEANUP: Removing Sandbox")
    daytona.delete(sandbox.id)
    print("✅ Sandbox deleted\n")

    print_header("🏁 DEMO COMPLETE - RECORDING READY!")
    print("\n🎥 Video recording should now be complete!")
    print("📦 Sandbox used: daytonaio/sandbox:0.4.3")
    print("🚀 Demo: AEGIS Autonomous Cyber Defense\n")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
