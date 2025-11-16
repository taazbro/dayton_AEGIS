#!/usr/bin/env python3
"""
Cleanup old Daytona sandboxes to free up disk space
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("\n" + "="*80)
print("🧹 DAYTONA SANDBOX CLEANUP".center(80))
print("="*80 + "\n")

try:
    from daytona_sdk import Daytona, DaytonaConfig

    # Connect
    config = DaytonaConfig(
        api_key=os.getenv("DAYTONA_API_KEY"),
        api_url=os.getenv("DAYTONA_API_URL", "https://app.daytona.io/api")
    )

    daytona = Daytona(config)
    print("✅ Connected to Daytona\n")

    # List all sandboxes
    print("📋 Listing all sandboxes...")
    sandboxes_page = daytona.list()

    # Get the items from paginated response
    sandbox_list = sandboxes_page.items if hasattr(sandboxes_page, 'items') else []

    if not sandbox_list:
        print("✅ No sandboxes found - account is clean!")
    else:
        print(f"\nFound {len(sandbox_list)} sandbox(es):\n")

        for i, sb in enumerate(sandbox_list, 1):
            print(f"{i}. ID: {sb.id}")
            print(f"   State: {sb.state}")
            print(f"   Disk: {sb.disk}GB")
            print()

        print("─"*80)

        # Ask to delete all
        choice = input("\nDelete ALL sandboxes? (y/n): ").strip().lower()

        if choice == 'y':
            print("\n🗑️  Deleting sandboxes...\n")

            for i, sb in enumerate(sandbox_list, 1):
                try:
                    print(f"Deleting {i}/{len(sandbox_list)}: {sb.id}...")
                    daytona.delete(sb.id)
                    print(f"   ✅ Deleted")

                except Exception as e:
                    print(f"   ⚠️  Error: {e}")

            print("\n✅ Cleanup complete!")
            print(f"💾 Freed up: ~{len(sandbox_list) * 3}GB disk space")
        else:
            print("\n✅ Skipped deletion")

    print("\n" + "="*80)
    print("🏁 DONE".center(80))
    print("="*80 + "\n")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
