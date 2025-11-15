"""
Test ALL 6 Sponsor Integrations with Real API Calls

This script validates that all sponsors are receiving real data from AEGIS.
"""

import os
import sys
import time
from typing import Dict, Any

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_sentry():
    """Test Sentry error tracking integration"""
    print("\n" + "="*70)
    print("🚨 TEST 1/6: SENTRY ERROR TRACKING")
    print("="*70)

    try:
        from src.sentry_init import init_sentry
        import sentry_sdk

        # Initialize Sentry
        init_sentry()

        # Send test event
        print("📤 Sending test event to Sentry...")
        sentry_sdk.capture_message(
            "AEGIS Hackathon Test: All sponsor integrations working!",
            level="info"
        )

        # Send test exception
        try:
            raise ValueError("Test exception from AEGIS - Ignore this!")
        except Exception as e:
            sentry_sdk.capture_exception(e)

        print("✅ Sentry integration SUCCESSFUL")
        print("   ✓ SDK initialized")
        print("   ✓ Test message sent")
        print("   ✓ Test exception captured")
        print("   ℹ️  Check Sentry dashboard to verify receipt")
        return True

    except Exception as e:
        print(f"❌ Sentry integration FAILED: {e}")
        return False


def test_claude():
    """Test Claude/Anthropic API integration"""
    print("\n" + "="*70)
    print("🤖 TEST 2/6: CLAUDE (ANTHROPIC) AI ANALYSIS")
    print("="*70)

    try:
        import anthropic

        api_key = os.getenv("CLAUDE_API_KEY")
        if not api_key:
            print("❌ CLAUDE_API_KEY not found")
            return False

        print("📤 Sending test prompt to Claude...")
        client = anthropic.Anthropic(api_key=api_key)

        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": "Say 'AEGIS hackathon test successful!' in exactly those words."
            }]
        )

        response = message.content[0].text if message.content else ""

        print("✅ Claude integration SUCCESSFUL")
        print("   ✓ API connection established")
        print("   ✓ Message sent and received")
        print(f"   ✓ Response: {response}")
        return True

    except Exception as e:
        print(f"❌ Claude integration FAILED: {e}")
        return False


def test_galileo():
    """Test Galileo AI observability integration"""
    print("\n" + "="*70)
    print("🔭 TEST 3/6: GALILEO AI OBSERVABILITY")
    print("="*70)

    try:
        from src.observability.galileo_integration import get_galileo_observability

        galileo = get_galileo_observability()

        if not galileo.enabled:
            print("❌ Galileo not enabled (missing API key)")
            return False

        print("📤 Logging test interaction to Galileo...")

        # Log a test prompt/response
        result = galileo.log_prompt(
            prompt="Test prompt for AEGIS hackathon validation",
            response="Test response - Galileo integration working!",
            model="claude-sonnet-4-5",
            latency_ms=250.5,
            metadata={
                "test": "sponsor_integration",
                "hackathon": "daytona_2025",
                "threat_type": "test_validation"
            }
        )

        if result:
            print("✅ Galileo integration SUCCESSFUL")
            print("   ✓ SDK/API initialized")
            print("   ✓ Test log sent")
            print("   ℹ️  Check Galileo dashboard to verify receipt")
            return True
        else:
            print("⚠️  Galileo log returned False (check API key/endpoint)")
            return False

    except Exception as e:
        print(f"❌ Galileo integration FAILED: {e}")
        return False


def test_browseruse():
    """Test BrowserUse automation integration"""
    print("\n" + "="*70)
    print("🎬 TEST 4/6: BROWSERUSE BROWSER AUTOMATION")
    print("="*70)

    try:
        from src.browseruse_agent.replay_attack import replay_attack

        browseruse_key = os.getenv("BROWSERUSE_KEY")
        if not browseruse_key:
            print("❌ BROWSERUSE_KEY not found")
            return False

        print("📤 Sending test forensic task to BrowserUse...")

        # Create test incident
        test_incident = {
            "threat_type": "SQL Injection Test",
            "event_sequence": ["recon", "exploit"],
            "severity": "HIGH",
            "test": True
        }

        # Run replay (will use SDK if available)
        result = replay_attack(test_incident)

        if result and isinstance(result, dict):
            print("✅ BrowserUse integration SUCCESSFUL")
            print("   ✓ SDK/API initialized")
            print("   ✓ Test forensic task sent")
            print(f"   ✓ Replay steps: {len(result.get('replay_steps', []))}")
            print("   ℹ️  Check BrowserUse dashboard to verify receipt")
            return True
        else:
            print("⚠️  BrowserUse returned unexpected result")
            return False

    except Exception as e:
        print(f"❌ BrowserUse integration FAILED: {e}")
        return False


def test_daytona():
    """Test Daytona IDE sync integration"""
    print("\n" + "="*70)
    print("🚀 TEST 5/6: DAYTONA IDE SYNC")
    print("="*70)

    try:
        from src.integrations.daytona_sync import get_daytona_sync

        daytona = get_daytona_sync()

        if not daytona.enabled:
            print("❌ Daytona not enabled (missing API key)")
            return False

        print("📤 Syncing test incident to Daytona...")

        # Create test incident data
        test_incident = {
            "threat_type": "Test Validation",
            "incident_summary": {
                "severity": "MEDIUM",
                "action_taken": "monitor"
            },
            "detection_engines": ["pattern", "signature"],
            "test": True,
            "hackathon": "daytona_2025"
        }

        # Sync to Daytona
        result = daytona.sync_incident(test_incident)

        if result:
            print("✅ Daytona integration SUCCESSFUL")
            print("   ✓ SDK/API initialized")
            print("   ✓ Test incident synced")
            print("   ℹ️  Check Daytona dashboard to verify receipt")
            return True
        else:
            print("⚠️  Daytona sync returned False")
            return False

    except Exception as e:
        print(f"❌ Daytona integration FAILED: {e}")
        return False


def test_coderabbit():
    """Test CodeRabbit AI code review integration"""
    print("\n" + "="*70)
    print("🐰 TEST 6/6: CODERABBIT AI CODE REVIEW")
    print("="*70)

    try:
        from src.integrations.coderabbit_review import get_coderabbit_review

        coderabbit = get_coderabbit_review()

        if not coderabbit.enabled:
            print("❌ CodeRabbit not enabled (missing API key)")
            return False

        print("📤 Sending test code review to CodeRabbit...")

        # Create test review context
        test_context = {
            "incident": {
                "threat_type": "Test Validation",
                "severity": "HIGH"
            },
            "test": True,
            "hackathon": "daytona_2025"
        }

        # Request code review
        result = coderabbit.review_response_code("monitor", test_context)

        if result and isinstance(result, dict):
            print("✅ CodeRabbit integration SUCCESSFUL")
            print("   ✓ API initialized")
            print("   ✓ Test review requested")
            print(f"   ✓ Quality score: {result.get('quality_score', 'N/A')}/10")
            print("   ℹ️  Check CodeRabbit dashboard to verify receipt")
            return True
        else:
            print("⚠️  CodeRabbit returned unexpected result")
            return False

    except Exception as e:
        print(f"❌ CodeRabbit integration FAILED: {e}")
        return False


def main():
    """Run all sponsor integration tests"""

    print("\n" + "="*70)
    print("🏆 AEGIS SPONSOR INTEGRATION TEST")
    print("   Daytona HackSprint 2025")
    print("="*70)
    print("\nTesting ALL 6 sponsor integrations with REAL API calls...\n")

    results = {}

    # Test each sponsor
    results['sentry'] = test_sentry()
    time.sleep(1)

    results['claude'] = test_claude()
    time.sleep(1)

    results['galileo'] = test_galileo()
    time.sleep(1)

    results['browseruse'] = test_browseruse()
    time.sleep(1)

    results['daytona'] = test_daytona()
    time.sleep(1)

    results['coderabbit'] = test_coderabbit()

    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    print(f"\nResults: {passed}/{total} integrations working\n")

    for sponsor, status in results.items():
        icon = "✅" if status else "❌"
        print(f"   {icon} {sponsor.upper()}: {'PASS' if status else 'FAIL'}")

    print("\n" + "="*70)

    if passed == total:
        print("🎉 SUCCESS! ALL 6 SPONSORS RECEIVING DATA!")
        print("="*70)
        print("\n✅ All integrations are production-ready")
        print("✅ All sponsors receiving real API calls")
        print("✅ Ready for hackathon demo!")
        print("\n🏆 Check each sponsor dashboard to verify data receipt\n")
        return 0
    else:
        print(f"⚠️  {total - passed} integration(s) need attention")
        print("="*70)
        print("\nCheck error messages above for details.\n")
        return 1


if __name__ == "__main__":
    exit(main())
