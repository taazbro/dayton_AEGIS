#!/usr/bin/env python3
"""
Upload AEGIS to Daytona Sandbox
Uses daytonaio/sandbox:0.4.3 image and uploads entire local project
"""

import os
import sys
from pathlib import Path

def print_header(text):
    print("\n" + "="*80)
    print(f"{text:^80}")
    print("="*80 + "\n")

def main():
    print_header("🛡️  AEGIS → DAYTONA SANDBOX UPLOAD")

    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    # Configuration
    DAYTONA_API_KEY = os.getenv("DAYTONA_API_KEY")
    DAYTONA_API_URL = os.getenv("DAYTONA_API_URL", "https://app.daytona.io/api")
    SANDBOX_CODE = os.getenv("DAYTONA_SANDBOX_CODE", "DAYTONA_HACK_1P9TLWZO")
    SANDBOX_IMAGE = "daytonaio/sandbox:0.4.3"

    print(f"📦 Sandbox Image: {SANDBOX_IMAGE}")
    print(f"🔑 API Key: {DAYTONA_API_KEY[:20] if DAYTONA_API_KEY else 'Not set'}...")
    print(f"🌐 API URL: {DAYTONA_API_URL}")

    # Get project root
    project_root = Path(__file__).parent.absolute()
    print(f"📂 Project Root: {project_root}")

    print_header("STEP 1: Initialize Daytona Client")

    try:
        print("Connecting to Daytona...")
        from daytona_sdk import Daytona, DaytonaConfig

        config = DaytonaConfig(
            api_key=DAYTONA_API_KEY,
            api_url=DAYTONA_API_URL
        )

        daytona = Daytona(config)
        print("✅ Connected to Daytona")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        sys.exit(1)

    print_header("STEP 2: Create Sandbox")

    try:
        print(f"Creating sandbox...")
        print("This may take 30-60 seconds...")

        sandbox = daytona.create()

        print(f"✅ Sandbox created!")
        print(f"   ID: {sandbox.id if hasattr(sandbox, 'id') else 'created'}")
    except Exception as e:
        print(f"❌ Failed to create sandbox: {e}")
        sys.exit(1)

    print_header("STEP 3: Upload AEGIS Project Files")

    # Files and directories to upload
    upload_items = [
        # Core source code
        "src/",

        # Configuration
        ".env",
        "requirements.txt",

        # Demo scripts
        "demo_pitch_live.py",
        "advanced_threat_defense.py",
        "triple_ai_warfare.py",

        # Test scripts
        "test_sponsor_integrations.py",
        "verify_pitch_requirements.py",

        # Documentation (optional but useful)
        "README.md",
        "PITCH.md",
        "DEMO_GUIDE.md",

        # Config files
        "config/",
    ]

    workspace_dir = "/workspace/aegis"

    try:
        # Create workspace directory
        print(f"Creating workspace directory: {workspace_dir}")
        result = sandbox.process.code_run(f"mkdir -p {workspace_dir}")
        print("✅ Workspace created")

        print("\nUploading files...")
        uploaded_count = 0

        for item in upload_items:
            local_path = project_root / item
            remote_path = f"{workspace_dir}/{item}"

            if not local_path.exists():
                print(f"⚠️  Skipping {item} (not found)")
                continue

            try:
                if local_path.is_dir():
                    print(f"📁 Uploading directory: {item}")
                    # Upload directory recursively using tar
                    import tarfile
                    import tempfile

                    with tempfile.NamedTemporaryFile(suffix='.tar.gz', delete=False) as tmp:
                        tar_path = tmp.name
                        with tarfile.open(tar_path, 'w:gz') as tar:
                            tar.add(str(local_path), arcname=item)

                        # Upload tar file
                        with open(tar_path, 'rb') as f:
                            content = f.read()
                            sandbox.fs.write(f"{workspace_dir}/temp.tar.gz", content)

                        # Extract in sandbox
                        sandbox.process.code_run(
                            f"cd {workspace_dir} && tar -xzf temp.tar.gz && rm temp.tar.gz"
                        )

                        os.unlink(tar_path)
                else:
                    print(f"📄 Uploading file: {item}")
                    with open(local_path, 'rb') as f:
                        content = f.read()
                        sandbox.fs.write(remote_path, content)

                uploaded_count += 1
                print(f"   ✅ {item}")

            except Exception as e:
                print(f"   ⚠️  Error uploading {item}: {e}")

        print(f"\n✅ Uploaded {uploaded_count} items")

    except Exception as e:
        print(f"❌ Upload failed: {e}")
        print("Cleaning up sandbox...")
        sandbox.delete()
        sys.exit(1)

    print_header("STEP 4: Setup Environment")

    try:
        # Read local .env for reference (we'll use actual keys)
        print("Reading API keys from local .env...")
        from dotenv import load_dotenv
        load_dotenv()

        sentry_dsn = os.getenv("SENTRY_DSN")
        claude_key = os.getenv("CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        galileo_key = os.getenv("GALILEO_API_KEY")
        slack_webhook = os.getenv("SLACK_WEBHOOK_URL")

        print(f"   SENTRY: {'✅' if sentry_dsn else '❌'}")
        print(f"   CLAUDE: {'✅' if claude_key else '❌'}")
        print(f"   GALILEO: {'✅' if galileo_key else '❌'}")
        print(f"   SLACK: {'✅' if slack_webhook else '⚠️'}")

        # The .env file is already uploaded, so we're good
        print("✅ Environment configured")

    except Exception as e:
        print(f"⚠️  Environment warning: {e}")
        print("   Continuing anyway...")

    print_header("STEP 5: Install Dependencies")

    try:
        print("Installing Python dependencies...")
        print("This may take 1-2 minutes...\n")

        result = sandbox.process.code_run(
            f"cd {workspace_dir} && pip3 install -r requirements.txt"
        )

        if result.exit_code == 0:
            print("\n✅ Dependencies installed")
        else:
            print(f"\n⚠️  Installation issues (exit code: {result.exit_code})")
            if hasattr(result, 'result') and result.result:
                print(f"   Output: {result.result[:500]}")

    except Exception as e:
        print(f"⚠️  Installation warning: {e}")
        print("   Continuing anyway...")

    print_header("STEP 6: Verify Upload")

    try:
        print("Checking uploaded files...")
        result = sandbox.process.code_run(f"ls -la {workspace_dir}")

        if result.exit_code == 0:
            print("✅ Files verified")
            print("\n📋 Contents:")
            if hasattr(result, 'result'):
                print(result.result)

    except Exception as e:
        print(f"⚠️  Verification warning: {e}")

    print_header("STEP 7: Run AEGIS Demo")

    choice = input("\nRun demo now? (y/n): ").strip().lower()

    if choice == 'y':
        print("\n🎬 Running AEGIS demo...")
        print("─" * 80)

        try:
            result = sandbox.process.code_run(
                f"cd {workspace_dir} && python3 demo_pitch_live.py --scenario sql_injection"
            )

            print("─" * 80)

            if result.exit_code == 0:
                print("\n✅ Demo completed successfully!")
            else:
                print(f"\n⚠️  Demo exited with code: {result.exit_code}")

            if hasattr(result, 'result') and result.result:
                print("\n📊 Output:")
                print(result.result)

        except Exception as e:
            print(f"❌ Demo failed: {e}")
    else:
        print("\n✅ Skipping demo execution")
        print(f"\nTo run manually:")
        print(f"   cd {workspace_dir}")
        print(f"   python3 demo_pitch_live.py --scenario sql_injection")

    print_header("STEP 8: Sandbox Management")

    print(f"📦 Sandbox Information:")
    print(f"   ID: {sandbox.id}")
    print(f"   Image: {SANDBOX_IMAGE}")
    print(f"   Workspace: {workspace_dir}")

    print("\n🔧 Available Commands:")
    print(f"   - SSH into sandbox: daytona ssh {sandbox.id}")
    print(f"   - View logs: daytona logs {sandbox.id}")
    print(f"   - Delete: daytona delete {sandbox.id}")

    keep = input("\nKeep sandbox running? (y/n): ").strip().lower()

    if keep != 'y':
        print("\nDeleting sandbox...")
        try:
            if hasattr(sandbox, 'remove'):
                sandbox.remove()
            else:
                sandbox.delete()
            print("✅ Sandbox deleted")
        except Exception as e:
            print(f"⚠️  Delete failed: {e}")
    else:
        print(f"\n✅ Sandbox still running")
        print(f"   Remember to delete when done: daytona delete {sandbox.id}")

    print_header("🏁 COMPLETE")
    print("AEGIS successfully uploaded to Daytona sandbox!")

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
