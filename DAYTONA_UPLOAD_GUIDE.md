# Upload AEGIS to Daytona Sandbox

## Quick Start

Upload the entire AEGIS project to Daytona sandbox using `daytonaio/sandbox:0.4.3`:

```bash
# 1. Install Daytona SDK (if not already installed)
pip3 install daytona-sdk

# 2. Run the upload script
python3 upload_to_daytona_sandbox.py
```

## What This Does

The `upload_to_daytona_sandbox.py` script will:

1. ✅ Connect to Daytona with API key: `DAYTONA_HACK_1P9TLWZO`
2. ✅ Create sandbox using image: `daytonaio/sandbox:0.4.3`
3. ✅ Upload entire AEGIS project:
   - Source code (`src/`)
   - Demo scripts (`demo_pitch_live.py`, etc.)
   - Configuration (`.env`, `requirements.txt`)
   - Documentation
4. ✅ Install dependencies in sandbox
5. ✅ Verify upload
6. ✅ Optionally run demo
7. ✅ Manage sandbox lifecycle

## Files Uploaded

```
aegis/
├── src/                          # All source code
├── demo_pitch_live.py            # Main demo
├── advanced_threat_defense.py    # 10 threat scenarios
├── triple_ai_warfare.py          # AI vs AI warfare
├── requirements.txt              # Dependencies
├── .env                          # API keys
├── config/                       # Configuration
├── README.md                     # Documentation
└── PITCH.md                      # Pitch deck
```

## Configuration

### API Key (Already Set)
```
DAYTONA_API_KEY=DAYTONA_HACK_1P9TLWZO
```

### Sandbox Image (Already Set)
```
SANDBOX_IMAGE=daytonaio/sandbox:0.4.3
```

### Workspace Directory
All files uploaded to: `/workspace/aegis/`

## Manual Commands

If you prefer to use Daytona CLI directly:

```bash
# Create sandbox
daytona create --image daytonaio/sandbox:0.4.3 --name aegis-demo

# Upload files (requires sandbox ID from previous step)
daytona upload <sandbox-id> /Users/tanjim/Downloads/Hackathon /workspace/aegis

# SSH into sandbox
daytona ssh <sandbox-id>

# Inside sandbox, install and run
cd /workspace/aegis
pip3 install -r requirements.txt
python3 demo_pitch_live.py --scenario sql_injection
```

## Troubleshooting

### SDK Not Found
```bash
pip3 install daytona-sdk python-dotenv
```

### Connection Issues
- Check API key is correct: `DAYTONA_HACK_1P9TLWZO`
- Verify Daytona service is running
- Check network connectivity

### Upload Failures
- Ensure files exist locally
- Check disk space in sandbox
- Verify sandbox status: `daytona status <sandbox-id>`

### Demo Won't Run
```bash
# SSH into sandbox
daytona ssh <sandbox-id>

# Check environment
cd /workspace/aegis
cat .env
pip3 list | grep -E "sentry|anthropic|dotenv"

# Run manually
python3 demo_pitch_live.py --scenario sql_injection
```

## Sandbox Management

### View Running Sandboxes
```bash
daytona list
```

### Delete Sandbox
```bash
daytona delete <sandbox-id>
```

### View Logs
```bash
daytona logs <sandbox-id>
```

## What Happens After Upload

Once uploaded, the sandbox contains a **complete, runnable AEGIS system**:

1. **All source code** for detection, analysis, response
2. **All integrations** (Sentry, Claude, Galileo, Slack, etc.)
3. **All demos** (live pitch, threat defense, AI warfare)
4. **All tests** and verification scripts
5. **Environment configured** with your API keys

## Running Demos in Sandbox

### Option 1: From Upload Script
The script will ask: "Run demo now? (y/n)"
- Choose `y` to run immediately
- Choose `n` to run later

### Option 2: SSH and Run Manually
```bash
# SSH into sandbox
daytona ssh <sandbox-id>

# Run main demo
cd /workspace/aegis
python3 demo_pitch_live.py --scenario sql_injection

# Or run threat defense
python3 advanced_threat_defense.py

# Or run AI warfare
python3 triple_ai_warfare.py
```

### Option 3: Remote Execute
```python
# From your local machine
from daytona_sdk import Daytona

daytona = Daytona(api_key="DAYTONA_HACK_1P9TLWZO")
sandbox = daytona.get_sandbox("<sandbox-id>")

result = sandbox.exec(
    "cd /workspace/aegis && python3 demo_pitch_live.py --scenario sql_injection"
)
print(result.stdout)
```

## Expected Results

### Successful Upload
```
================================================================================
              🛡️  AEGIS → DAYTONA SANDBOX UPLOAD
================================================================================

📦 Sandbox Image: daytonaio/sandbox:0.4.3
🔑 API Key: DAYTONA_HACK_1P9...

================================================================================
                    STEP 1: Initialize Daytona Client
================================================================================

Connecting to Daytona...
✅ Connected to Daytona

================================================================================
                        STEP 2: Create Sandbox
================================================================================

Creating sandbox with image: daytonaio/sandbox:0.4.3
This may take 30-60 seconds...
✅ Sandbox created!
   ID: abc123xyz
   Status: running

================================================================================
                 STEP 3: Upload AEGIS Project Files
================================================================================

Creating workspace directory: /workspace/aegis
✅ Workspace created

Uploading files...
📁 Uploading directory: src/
   ✅ src/
📄 Uploading file: .env
   ✅ .env
📄 Uploading file: requirements.txt
   ✅ requirements.txt
...

✅ Uploaded 12 items
```

### Successful Demo Run
```
================================================================================
                      STEP 7: Run AEGIS Demo
================================================================================

🎬 Running AEGIS demo...
────────────────────────────────────────────────────────────────────────────────

🛡️  AEGIS LIVE DEMO - Autonomous Cyber Defense

PHASE 1: Autonomous Attack Simulation
   Simulating SQL injection attack...
   ✅ Attack simulation active

PHASE 2: Real-time Telemetry
   Sentry event logged: c8f9e12a-...
   ✅ Telemetry captured

PHASE 3: AEGIS Detection (<5s)
   Behavioral analysis: SQL injection detected (95% confidence)
   ✅ Threat detected in 4.7s

PHASE 4: AI-Powered Analysis
   Claude analyzing incident...
   ✅ Incident report generated

PHASE 5: Automated Response
   Actions taken: 5/5 completed
   ✅ Attack neutralized

✅ Demo completed successfully!
```

## Next Steps

1. ✅ Upload complete - AEGIS running in Daytona
2. 🎬 Run demo to verify
3. 📊 Show sponsors the integration
4. 🚀 Deploy for hackathon presentation

## Support

- Daytona Docs: https://www.daytona.io/docs
- AEGIS README: `/workspace/aegis/README.md`
- Demo Guide: `/workspace/aegis/DEMO_GUIDE.md`
