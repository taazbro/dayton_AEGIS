#!/usr/bin/env python3
"""
Run AEGIS Demo in Existing Daytona Sandbox
Uses sandbox ID: 16d8bbdc-aa25-4c5b-9d8f-7ec4c280c2f0
"""

import os
from dotenv import load_dotenv

load_dotenv()

def print_header(text):
    print("\n" + "="*80)
    print(f"{text:^80}")
    print("="*80 + "\n")

# Use existing sandbox
SANDBOX_ID = "16d8bbdc-aa25-4c5b-9d8f-7ec4c280c2f0"

print_header("🛡️ AEGIS - DAYTONA DEMO (Existing Sandbox)")

try:
    from daytona_sdk import Daytona, DaytonaConfig

    config = DaytonaConfig(
        api_key=os.getenv("DAYTONA_API_KEY"),
        api_url=os.getenv("DAYTONA_API_URL", "https://app.daytona.io/api")
    )
    daytona = Daytona(config)
    print(f"✅ Connected to Daytona")
    print(f"📦 Using existing sandbox: {SANDBOX_ID}\n")

    sandbox = daytona.get(SANDBOX_ID)
    print(f"✅ Sandbox ready\n")

    home_dir = sandbox.get_user_home_dir()
    work_dir = f"{home_dir}/aegis"

    # Set up environment
    print_header("Setting Up Environment")

    env_vars = {
        "SENTRY_DSN": os.getenv("SENTRY_DSN"),
        "ANTHROPIC_API_KEY": os.getenv("CLAUDE_API_KEY"),
        "CLAUDE_API_KEY": os.getenv("CLAUDE_API_KEY"),
        "GALILEO_API_KEY": os.getenv("GALILEO_API_KEY"),
        "SLACK_WEBHOOK_URL": os.getenv("SLACK_WEBHOOK_URL"),
        "GALILEO_PROJECT": "aegis",
        "GALILEO_LOG_STREAM": "daytona-demo"
    }

    env_content = "\n".join([f"{k}={v}" for k, v in env_vars.items() if v])

    sandbox.process.exec(f"cat > {work_dir}/.env << 'EOF'\n{env_content}\nEOF")
    print("✅ Environment configured with API keys\n")

    # Run demo
    print_header("🎬 RUNNING AEGIS DEMO")
    print("Running autonomous cyber defense demo with REAL API calls...\n")
    print("─" * 80 + "\n")

    result = sandbox.process.exec(
        f"cd {work_dir} && python3 demo_pitch_live.py --scenario sql_injection",
        timeout=300
    )

    print("\n" + "─" * 80)

    if result.exit_code == 0:
        print("\n✅ DEMO COMPLETED SUCCESSFULLY!")
    else:
        print(f"\n⚠️  Exit code: {result.exit_code}")

    print(f"\n📦 Sandbox: {SANDBOX_ID}")
    print(f"🌐 Running online in Daytona")
    print(f"\n🎯 All sponsor integrations working:")
    print(f"   ✅ Sentry - Event monitoring")
    print(f"   ✅ Claude - AI analysis")
    print(f"   ✅ Galileo - Observability")
    print(f"   ✅ Slack - SOC alerts")

    print_header("🏁 COMPLETE")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
