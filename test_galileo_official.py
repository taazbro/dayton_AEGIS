"""
Test Official Galileo SDK Integration with AEGIS
Using the official galileo package with trace/span logging
"""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set environment variables
os.environ['GALILEO_API_KEY'] = "XGbRylWbkLquGu0p4rkmBKLswzeuRM8nRaUzKMyYG_E"
os.environ['GALILEO_PROJECT'] = "aegis"
os.environ['GALILEO_LOG_STREAM'] = "official-sdk-test"

print("\n" + "="*70)
print("🔭 TESTING OFFICIAL GALILEO SDK INTEGRATION")
print("="*70)

try:
    from galileo import galileo_context
    from galileo.config import GalileoPythonConfig
    from anthropic import Anthropic

    print("\n✅ Galileo SDK imported successfully (Official Package)")

    # Initialize Galileo context
    print("\n📡 Initializing Galileo context...")
    galileo_context.init(
        project="aegis",
        log_stream="official-sdk-test"
    )
    print("   ✅ Context initialized")

    # Get logger instance
    print("\n🔧 Getting logger instance...")
    logger = galileo_context.get_logger_instance()
    print(f"   ✅ Logger obtained")
    print(f"   Project ID: {logger.project_id if hasattr(logger, 'project_id') else 'unknown'}")

    # Start session
    print("\n🚀 Starting Galileo session...")
    logger.start_session()
    print("   ✅ Session started")

    # Initialize Anthropic client
    print("\n🤖 Initializing Claude...")
    claude_api_key = os.getenv("CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    if not claude_api_key:
        raise ValueError("CLAUDE_API_KEY or ANTHROPIC_API_KEY must be set")
    client = Anthropic(api_key=claude_api_key)

    # Test prompt
    user_prompt = "Describe a DDoS attack and how to defend against it in 2 sentences."

    print(f"\n📝 Test Prompt: {user_prompt}")

    # Start trace
    print("\n🎯 Starting trace...")
    logger.start_trace(name="AEGIS Cyber Defense Test", input=user_prompt)
    print("   ✅ Trace started")

    # Prepare messages
    messages = [
        {"role": "user", "content": user_prompt}
    ]

    # Capture start time
    start_time_ns = datetime.now().timestamp() * 1_000_000_000

    # Call Claude
    print("\n⚡ Calling Claude API...")
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=200,
        messages=[{"role": "user", "content": user_prompt}]
    )
    print("   ✅ Claude responded")

    # Calculate duration
    end_time_ns = datetime.now().timestamp() * 1_000_000_000
    duration_ns = int(end_time_ns - start_time_ns)

    # Extract response
    response_text = response.content[0].text

    print(f"\n💬 Claude Response: {response_text}")

    # Add LLM span
    print("\n📊 Adding LLM span to Galileo...")
    logger.add_llm_span(
        input=messages,
        output=response_text,
        model="claude-sonnet-4-5-20250929",
        num_input_tokens=response.usage.input_tokens,
        num_output_tokens=response.usage.output_tokens,
        total_tokens=response.usage.input_tokens + response.usage.output_tokens,
        duration_ns=duration_ns,
    )
    print(f"   ✅ Span added")
    print(f"   Tokens: {response.usage.input_tokens} in + {response.usage.output_tokens} out = {response.usage.input_tokens + response.usage.output_tokens} total")

    # Conclude trace
    print("\n🏁 Concluding trace...")
    logger.conclude(output=response_text)
    print("   ✅ Trace concluded")

    # Flush to Galileo
    print("\n🔄 Flushing to Galileo platform...")
    logger.flush()
    print("   ✅ Data flushed to Galileo")

    # Show Galileo URLs
    config = GalileoPythonConfig.get()
    project_url = f"{config.console_url}/project/{logger.project_id}"
    log_stream_url = f"{project_url}/log-streams/{logger.log_stream_id}"

    print("\n" + "="*70)
    print("✅ OFFICIAL GALILEO SDK TEST: SUCCESS")
    print("="*70)
    print(f"\n🔗 View your data:")
    print(f"   Project   : {project_url}")
    print(f"   Log Stream: {log_stream_url}")
    print(f"\n📊 Summary:")
    print(f"   • Project: aegis")
    print(f"   • Log Stream: official-sdk-test")
    print(f"   • Model: claude-sonnet-4-5-20250929")
    print(f"   • Tokens: {response.usage.input_tokens + response.usage.output_tokens}")
    print(f"   • Duration: {duration_ns / 1_000_000:.0f}ms")
    print(f"\n🎯 AEGIS is now using the OFFICIAL Galileo SDK!\n")

except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("\nInstall the official Galileo SDK:")
    print("   pip install galileo python-dotenv")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
