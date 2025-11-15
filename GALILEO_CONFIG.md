# 🔭 Galileo AI Observability - Configuration Guide

## Official Documentation
- **SDK Docs**: https://docs.rungalileo.io/galileo/llm-studio/python-sdk
- **Dashboard**: https://app.galileo.ai/

## Installation

```bash
pip install galileo python-dotenv
```

## Environment Variables

```bash
# Required
export GALILEO_API_KEY="XGbRylWbkLquGu0p4rkmBKLswzeuRM8nRaUzKMyYG_E"

# Optional (auto-created if not specified)
export GALILEO_PROJECT="aegis"
export GALILEO_LOG_STREAM="default"
```

## SDK Initialization (Official Method)

### Basic Usage

```python
from galileo import galileo_context
from galileo.config import GalileoPythonConfig

# Initialize Galileo context
galileo_context.init(project="aegis", log_stream="default")

# Get logger instance
logger = galileo_context.get_logger_instance()

# Start a session (required before logging)
logger.start_session()
```

### Logging AI Interactions

```python
from datetime import datetime

# Start a trace (conversation step)
logger.start_trace(name="Attack Detection", input="DDoS attack from 203.45.67.89")

# Prepare messages format
messages = [
    {"role": "system", "content": "You are a cyber defense AI"},
    {"role": "user", "content": "Analyze this DDoS attack"}
]

# Get response from Claude (example)
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Analyze this DDoS attack"}]
)

# Calculate duration
start_time_ns = datetime.now().timestamp() * 1_000_000_000

# Add LLM span with full token metrics
logger.add_llm_span(
    input=messages,
    output=response.content[0].text,
    model="claude-sonnet-4-5-20250929",
    num_input_tokens=response.usage.input_tokens,
    num_output_tokens=response.usage.output_tokens,
    total_tokens=response.usage.input_tokens + response.usage.output_tokens,
    duration_ns=(datetime.now().timestamp() * 1_000_000_000) - start_time_ns,
)

# Conclude and flush
logger.conclude(output=response.content[0].text)
logger.flush()
```

## Active Projects in AEGIS

| Project Name | Purpose |
|-------------|---------|
| `AEGIS` | Base project |
| `AEGIS_ATTACK_SIM` | Attack simulations |
| `AEGIS_ATTACK_DEMO` | Defense demonstrations |
| `AEGIS_3v3_WARFARE` | 6-model AI warfare |
| `AEGIS_DUAL_CLAUDE` | Dual-AI operations |
| `AEGIS_PARALLEL_TEST` | Parallel sponsor tests |

## Generated Node IDs (Sample)

Recent nodes logged to Galileo platform:

```
98a856cb-feaf-4aab-bf6b-b8be2d121ebf (DDOS attack)
ed993978-c572-40d7-8591-09a66b6da72c (Ransomware)
b6cfec26-a609-490f-8fe0-e8e4c5234574 (Zero-Day)
71719a75-48b4-40f2-845f-87ee99221815 (Data Exfiltration)
037f77b2-be76-4f3d-910f-2f23d707cdf9 (Privilege Escalation)
... and 40+ more
```

## Verification

### View Your Data

1. Go to https://app.galileo.ai/
2. Login with your account
3. Select any AEGIS project from the dropdown
4. Filter by tags:
   - `attack-defense`
   - `red-team`
   - `blue-team`
   - `threat-level-10`

### Search by Node ID

Use the search feature to find specific interactions by their node IDs listed above.

## Integration in AEGIS

All AEGIS attack/defense operations automatically log to Galileo:

- ✅ Attack simulations
- ✅ Defense responses
- ✅ AI model interactions
- ✅ Threat analysis
- ✅ 3v3 AI warfare events
- ✅ Multi-model operations

## Troubleshooting

### SDK Not Finding API Key

```bash
# Verify environment variable is set
echo $GALILEO_API_KEY

# If not set, export it
export GALILEO_API_KEY="XGbRylWbkLquGu0p4rkmBKLswzeuRM8nRaUzKMyYG_E"
```

### Project Not Showing

Projects are auto-created when first used. Wait a few moments and refresh the Galileo dashboard.

---

**All AEGIS operations are now being tracked in Galileo AI Observability! 🎯**
