#!/usr/bin/env python3
"""
Upload AEGIS to Daytona Sandbox - Simple Git Clone Approach
Uses daytonaio/sandbox:0.4.3 and clones from GitHub
"""

import os
import sys
from dotenv import load_dotenv

# Load environment
load_dotenv()

def print_header(text):
    print("\n" + "="*80)
    print(f"{text:^80}")
    print("="*80 + "\n")

def main():
    print_header("🛡️  AEGIS → DAYTONA SANDBOX")

    # Configuration
    DAYTONA_API_KEY = os.getenv("DAYTONA_API_KEY")
    DAYTONA_API_URL = os.getenv("DAYTONA_API_URL", "https://app.daytona.io/api")
    GITHUB_REPO = "https://github.com/taazbro/dayton_AEGIS"

    print(f"🔑 API Key: {DAYTONA_API_KEY[:20]}...")
    print(f"🌐 API URL: {DAYTONA_API_URL}")
    print(f"📦 GitHub Repo: {GITHUB_REPO}")

    print_header("STEP 1: Connect to Daytona")

    try:
        from daytona_sdk import Daytona, DaytonaConfig

        config = DaytonaConfig(
            api_key=DAYTONA_API_KEY,
            api_url=DAYTONA_API_URL
        )

        daytona = Daytona(config)
        print("✅ Connected to Daytona")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        sys.exit(1)

    print_header("STEP 2: Create Sandbox")

    try:
        print("Creating sandbox (30-60 seconds)...")
        sandbox = daytona.create()
        print(f"✅ Sandbox created!")
        print(f"   ID: {sandbox.id}")
    except Exception as e:
        print(f"❌ Failed: {e}")
        sys.exit(1)

    print_header("STEP 3: Clone AEGIS from GitHub")

    try:
        # Get home directory
        home_dir = sandbox.get_user_home_dir()
        work_dir = f"{home_dir}/aegis"

        print(f"📂 Home: {home_dir}")
        print(f"📂 Work dir: {work_dir}")

        # Clone repository
        print(f"\nCloning {GITHUB_REPO}...")
        sandbox.git.clone(
            url=GITHUB_REPO,
            path=work_dir
        )
        print("✅ Repository cloned")
    except Exception as e:
        print(f"❌ Clone failed: {e}")
        print("\nTrying alternative method...")
        try:
            result = sandbox.process.exec(
                f"git clone {GITHUB_REPO} {work_dir}"
            )
            if result.exit_code == 0:
                print("✅ Clone successful (alternative method)")
            else:
                print(f"❌ Failed: {result}")
                sys.exit(1)
        except Exception as e2:
            print(f"❌ All methods failed: {e2}")
            sys.exit(1)

    print_header("STEP 4: Setup Environment")

    try:
        # Read local API keys
        sentry_dsn = os.getenv("SENTRY_DSN")
        claude_key = os.getenv("CLAUDE_API_KEY")
        galileo_key = os.getenv("GALILEO_API_KEY")
        slack_webhook = os.getenv("SLACK_WEBHOOK_URL")

        print("Creating .env file in sandbox...")

        env_content = f"""SENTRY_DSN={sentry_dsn}
ANTHROPIC_API_KEY={claude_key}
CLAUDE_API_KEY={claude_key}
GALILEO_API_KEY={galileo_key}
SLACK_WEBHOOK_URL={slack_webhook}
GALILEO_PROJECT=aegis
GALILEO_LOG_STREAM=daytona-demo
"""

        # Write .env file
        result = sandbox.process.exec(
            f"cat > {work_dir}/.env << 'ENVEOF'\n{env_content}\nENVEOF"
        )

        if result.exit_code == 0:
            print("✅ Environment configured")
        else:
            print(f"⚠️  Environment setup issue")

    except Exception as e:
        print(f"⚠️  Warning: {e}")

    print_header("STEP 5: Install Dependencies")

    try:
        print("Installing Python packages (1-2 minutes)...\n")

        result = sandbox.process.exec(
            f"cd {work_dir} && pip3 install -r requirements.txt",
            timeout=180
        )

        if result.exit_code == 0:
            print("\n✅ Dependencies installed")
        else:
            print(f"\n⚠️  Installation issues (continuing anyway)")

    except Exception as e:
        print(f"⚠️  Warning: {e}")

    print_header("STEP 6: Verify Setup")

    try:
        result = sandbox.process.exec(f"ls -la {work_dir}")
        if result.exit_code == 0:
            print("✅ Files verified")
            print("\n📋 Contents:")
            if hasattr(result, 'stdout'):
                print(result.stdout)
            elif hasattr(result, 'output'):
                print(result.output)

    except Exception as e:
        print(f"⚠️  Verification warning: {e}")

    print_header("STEP 7: Run Demo")

    choice = input("\nRun AEGIS demo now? (y/n): ").strip().lower()

    if choice == 'y':
        print("\n🎬 Running demo...")
        print("─" * 80)

        try:
            result = sandbox.process.exec(
                f"cd {work_dir} && python3 demo_pitch_live.py --scenario sql_injection",
                timeout=300
            )

            print("─" * 80)

            if result.exit_code == 0:
                print("\n✅ Demo completed!")
            else:
                print(f"\n⚠️  Exit code: {result.exit_code}")

            if hasattr(result, 'stdout') and result.stdout:
                print("\n📊 Output:")
                print(result.stdout)
            elif hasattr(result, 'output') and result.output:
                print("\n📊 Output:")
                print(result.output)

        except Exception as e:
            print(f"❌ Demo failed: {e}")
    else:
        print(f"\n✅ Skipped demo")
        print(f"\nTo run manually:")
        print(f"   cd {work_dir}")
        print(f"   python3 demo_pitch_live.py")

    print_header("STEP 8: Sandbox Info")

    print(f"📦 Sandbox ID: {sandbox.id}")
    print(f"📂 Workspace: {work_dir}")

    keep = input("\nKeep sandbox running? (y/n): ").strip().lower()

    if keep != 'y':
        print("\nDeleting sandbox...")
        try:
            if hasattr(sandbox, 'remove'):
                sandbox.remove()
            else:
                daytona.delete(sandbox.id)
            print("✅ Deleted")
        except Exception as e:
            print(f"⚠️  Delete warning: {e}")
    else:
        print(f"\n✅ Sandbox still running: {sandbox.id}")

    print_header("🏁 COMPLETE")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
