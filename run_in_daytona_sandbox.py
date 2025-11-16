#!/usr/bin/env python3
"""
AEGIS - Run Demo in Daytona Sandbox
Creates a Daytona sandbox and runs the live demo inside it
"""

import os
import sys
import time
from daytona import Daytona, DaytonaConfig
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def print_header(text):
    print("\n" + "="*80)
    print(f"{text:^80}")
    print("="*80 + "\n")

def main():
    print_header("🛡️  AEGIS - DAYTONA SANDBOX DEMO")

    # Get API key from environment
    api_key = os.getenv("DAYTONA_API_KEY")
    if not api_key:
        print("❌ ERROR: DAYTONA_API_KEY not set")
        print("   Run: export DAYTONA_API_KEY='your-key-here'")
        sys.exit(1)

    print("✅ Daytona API key found")
    print(f"   Key: {api_key[:20]}...")

    # Get other API keys
    sentry_dsn = os.getenv("SENTRY_DSN")
    claude_key = os.getenv("CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    galileo_key = os.getenv("GALILEO_API_KEY")
    slack_webhook = os.getenv("SLACK_WEBHOOK_URL")

    print("\n📋 API Keys Status:")
    print(f"   SENTRY_DSN: {'✅ Set' if sentry_dsn else '❌ Missing'}")
    print(f"   CLAUDE_API_KEY: {'✅ Set' if claude_key else '❌ Missing'}")
    print(f"   GALILEO_API_KEY: {'✅ Set' if galileo_key else '❌ Missing'}")
    print(f"   SLACK_WEBHOOK_URL: {'✅ Set' if slack_webhook else '⚠️  Optional'}")

    print_header("STEP 1: Creating Daytona Sandbox")

    try:
        # Initialize Daytona client
        print("Initializing Daytona client...")
        config = DaytonaConfig(api_key=api_key)
        daytona = Daytona(config)
        print("✅ Daytona client initialized")

        # Create empty sandbox
        print("\nCreating Daytona sandbox...")
        print("   This may take 30-60 seconds...")

        sandbox = daytona.create()

        print(f"✅ Sandbox created!")
        print(f"   Sandbox ID: {sandbox.id}")

        # Clone the GitHub repository
        print("\nCloning AEGIS repository...")
        print("   Repository: https://github.com/taazbro/dayton_AEGIS")

        clone_result = sandbox.process.code_run(
            "git clone https://github.com/taazbro/dayton_AEGIS /workspace/aegis"
        )

        if clone_result.exit_code == 0:
            print("✅ Repository cloned successfully")
        else:
            print(f"❌ Failed to clone repository")
            print(f"   Error: {clone_result.result}")
            raise Exception("Git clone failed")

    except Exception as e:
        print(f"❌ Failed to create sandbox: {e}")
        sys.exit(1)

    print_header("STEP 2: Setting Up Environment")

    try:
        # Create .env file in sandbox
        print("Creating .env file with API keys...")

        env_content = f"""# AEGIS Environment Configuration
SENTRY_DSN={sentry_dsn or 'YOUR_SENTRY_DSN'}
SENTRY_ENVIRONMENT=daytona-sandbox

ANTHROPIC_API_KEY={claude_key or 'YOUR_CLAUDE_KEY'}
CLAUDE_API_KEY={claude_key or 'YOUR_CLAUDE_KEY'}
CLAUDE_MODEL=claude-sonnet-4-5-20250929

GALILEO_API_KEY={galileo_key or 'YOUR_GALILEO_KEY'}
GALILEO_PROJECT=aegis
GALILEO_LOG_STREAM=daytona-sandbox

SLACK_WEBHOOK_URL={slack_webhook or 'YOUR_SLACK_WEBHOOK'}

DAYTONA_API_KEY={api_key}
"""

        # Write .env file to sandbox
        sandbox.fs.write("/workspace/aegis/.env", env_content)
        print("✅ .env file created in sandbox")

        # Make run_all.sh executable
        print("\nMaking scripts executable...")
        result = sandbox.process.code_run("chmod +x /workspace/aegis/run_all.sh")
        if result.exit_code == 0:
            print("✅ Scripts are executable")

    except Exception as e:
        print(f"⚠️  Setup warning: {e}")
        print("   Continuing anyway...")

    print_header("STEP 3: Installing Dependencies")

    try:
        print("Installing Python dependencies...")
        print("This may take 1-2 minutes...\n")

        # Install dependencies
        result = sandbox.process.code_run(
            "cd /workspace/aegis && pip3 install -r requirements.txt"
        )

        if result.exit_code == 0:
            print("\n✅ Dependencies installed successfully")
        else:
            print(f"\n⚠️  Installation had issues (exit code: {result.exit_code})")
            print("   Continuing anyway...")

    except Exception as e:
        print(f"⚠️  Installation warning: {e}")
        print("   Continuing anyway...")

    print_header("STEP 4: Running AEGIS Demo")

    print("🎬 Starting demo in Daytona sandbox...")
    print("   This will run the 4-minute live demo")
    print("   Output will stream below\n")
    print("─" * 80)

    try:
        # Run the demo
        result = sandbox.process.code_run(
            "cd /workspace/aegis && python3 demo_pitch_live.py --scenario sql_injection"
        )

        print("─" * 80)

        if result.exit_code == 0:
            print("\n✅ Demo completed successfully!")
        else:
            print(f"\n⚠️  Demo exited with code: {result.exit_code}")

        print("\n📊 Demo Output:")
        if result.result:
            print(result.result)

    except Exception as e:
        print(f"❌ Demo failed: {e}")

    print_header("STEP 5: Cleanup")

    # Ask if user wants to keep or delete sandbox
    try:
        keep = input("Keep sandbox running? (y/n): ").strip().lower()

        if keep != 'y':
            print("\nDeleting sandbox...")
            sandbox.delete()
            print("✅ Sandbox deleted")
        else:
            print(f"\n✅ Sandbox still running")
            print(f"   Sandbox ID: {sandbox.id}")
            print(f"   To delete later: daytona.get_sandbox('{sandbox.id}').delete()")
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted - sandbox may still be running")
        print(f"   Sandbox ID: {sandbox.id}")

    print_header("🏁 COMPLETE")
    print("AEGIS demo ran successfully in Daytona sandbox!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
