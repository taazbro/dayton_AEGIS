"""
Simple Test of Official Galileo SDK Integration
Tests the SDK without requiring Claude API calls
"""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set environment variables
os.environ['GALILEO_API_KEY'] = "XGbRylWbkLquGu0p4rkmBKLswzeuRM8nRaUzKMyYG_E"
os.environ['GALILEO_PROJECT'] = "aegis"
os.environ['GALILEO_LOG_STREAM'] = "sdk-verification"

print("\n" + "="*70)
print("🔭 GALILEO OFFICIAL SDK - SIMPLE TEST")
print("="*70)

try:
    from galileo import galileo_context
    from galileo.config import GalileoPythonConfig

    print("\n✅ Official Galileo SDK imported successfully")
    print(f"   Package: galileo")

    # Initialize Galileo context
    print("\n📡 Initializing Galileo...")
    galileo_context.init(
        project="aegis",
        log_stream="sdk-verification"
    )
    print("   ✅ Context initialized")

    # Get logger instance
    print("\n🔧 Getting logger...")
    logger = galileo_context.get_logger_instance()
    print(f"   ✅ Logger obtained")
    print(f"   Project ID: {logger.project_id}")
    print(f"   Log Stream ID: {logger.log_stream_id}")

    # Start session
    print("\n🚀 Starting session...")
    logger.start_session()
    print("   ✅ Session started")

    # Test data
    user_prompt = "AEGIS detected a DDoS attack from 203.45.67.89"
    ai_response = "DDoS attack neutralized. Rate limiting applied. IP blocked for 24 hours."

    # Start trace
    print(f"\n🎯 Starting trace...")
    logger.start_trace(name="DDoS Defense Test", input=user_prompt)
    print("   ✅ Trace started")

    # Prepare messages
    messages = [
        {"role": "system", "content": "You are AEGIS cyber defense AI"},
        {"role": "user", "content": user_prompt}
    ]

    # Simulate timing
    start_time_ns = datetime.now().timestamp() * 1_000_000_000
    # Simulate processing delay
    import time
    time.sleep(0.1)
    end_time_ns = datetime.now().timestamp() * 1_000_000_000
    duration_ns = int(end_time_ns - start_time_ns)

    # Add LLM span
    print("\n📊 Adding LLM span...")
    logger.add_llm_span(
        input=messages,
        output=ai_response,
        model="aegis-defense-v1",
        num_input_tokens=15,
        num_output_tokens=18,
        total_tokens=33,
        duration_ns=duration_ns,
    )
    print("   ✅ Span added successfully")
    print(f"   Model: aegis-defense-v1")
    print(f"   Tokens: 15 in + 18 out = 33 total")
    print(f"   Duration: {duration_ns / 1_000_000:.0f}ms")

    # Conclude
    print("\n🏁 Concluding trace...")
    logger.conclude(output=ai_response)
    print("   ✅ Trace concluded")

    # Flush
    print("\n🔄 Flushing to Galileo...")
    logger.flush()
    print("   ✅ Data sent to Galileo platform")

    # Get URLs
    config = GalileoPythonConfig.get()
    project_url = f"{config.console_url}/project/{logger.project_id}"
    log_stream_url = f"{project_url}/log-streams/{logger.log_stream_id}"

    print("\n" + "="*70)
    print("✅ OFFICIAL GALILEO SDK: FULLY WORKING")
    print("="*70)
    print(f"\n🔗 View your data:")
    print(f"   Dashboard: https://app.galileo.ai/")
    print(f"   Project: {project_url}")
    print(f"   Log Stream: {log_stream_url}")
    print(f"\n📊 Data logged:")
    print(f"   ✓ Trace: DDoS Defense Test")
    print(f"   ✓ Input: {user_prompt}")
    print(f"   ✓ Output: {ai_response}")
    print(f"   ✓ Tokens: 33 total")
    print(f"   ✓ Model: aegis-defense-v1")
    print(f"\n🎯 AEGIS now using Official Galileo SDK!\n")

except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("\nInstall the official Galileo SDK:")
    print("   pip install galileo python-dotenv")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
