# 🚀 AEGIS Daytona Setup Guide (A → Z)

## ✅ Complete Step-by-Step Instructions for Running AEGIS in Daytona

---

## 📋 Prerequisites

Before you begin, make sure you have:

1. ✅ **Daytona workspace created** for your project
   - Workspace name: `zyberpol-aegis` (or your choice)
   - Connected to your GitHub repository

2. ✅ **GitHub repository** with AEGIS code
   - Repository: https://github.com/taazbro/dayton_AEGIS

3. ✅ **API Keys** ready (see below for where to get them)

4. ✅ **Terminal access** to your Daytona workspace

---

## 🔑 Required API Keys

### Essential (For Core Demo)

| Service | Get Key From | Required? | Used For |
|---------|-------------|-----------|----------|
| **Sentry** | https://sentry.io/ | ✅ YES | Error tracking, event monitoring |
| **Claude** | https://console.anthropic.com/ | ✅ YES | AI threat analysis |
| **Galileo** | https://app.galileo.ai/ | ✅ YES | AI observability |

### Optional (Enhanced Features)

| Service | Get Key From | Required? | Used For |
|---------|-------------|-----------|----------|
| **Slack** | https://api.slack.com/messaging/webhooks | ⚠️ Optional | SOC notifications |
| **BrowserUse** | https://browseruse.com/ | ⚠️ Optional | Forensic automation |
| **Daytona** | Your Daytona dashboard | ⚠️ Optional | IDE sync |

---

## 🏗️ Step-by-Step Setup

### Step A — Open Your Daytona Workspace

1. **Log into Daytona** (web UI or CLI):
   ```bash
   daytona login
   ```

2. **Open your workspace**:
   ```bash
   daytona open zyberpol-aegis
   ```
   Or use the web UI: https://app.daytona.io

3. **Verify you're in the project root**:
   ```bash
   pwd
   ls
   ```

   You should see:
   ```
   main.py
   src/
   config/
   requirements.txt
   run_all.sh
   ...
   ```

---

### Step B — Create .env File

1. **Create the .env file** in your project root:
   ```bash
   nano .env
   ```

2. **Add your API keys** (copy-paste this template):

   ```bash
   # ========================================
   # AEGIS ENVIRONMENT CONFIGURATION
   # ========================================

   # SPONSOR 1: Sentry (Error Tracking)
   SENTRY_DSN=https://YOUR_SENTRY_DSN@sentry.io/YOUR_PROJECT
   SENTRY_ENVIRONMENT=daytona-aegis

   # SPONSOR 2: Claude AI (Anthropic)
   ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE
   # Alternative:
   # CLAUDE_API_KEY=sk-ant-api03-YOUR_KEY_HERE

   # SPONSOR 3: Galileo (AI Observability)
   GALILEO_API_KEY=YOUR_GALILEO_KEY_HERE
   GALILEO_PROJECT=aegis
   GALILEO_LOG_STREAM=daytona-demo

   # SPONSOR 4: BrowserUse (Optional)
   BROWSERUSE_API_KEY=YOUR_BROWSERUSE_KEY_HERE

   # SPONSOR 5: Daytona (Optional)
   DAYTONA_API_KEY=YOUR_DAYTONA_KEY_HERE

   # SPONSOR 6: Slack Notifications (Optional)
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

   # Additional Integrations (Optional)
   # VIRUSTOTAL_API_KEY=your_vt_key_here
   # DATADOG_API_KEY=your_dd_key_here
   # PAGERDUTY_API_KEY=your_pd_key_here
   ```

3. **Save the file**:
   - Press `Ctrl+O` (write out)
   - Press `Enter` (confirm)
   - Press `Ctrl+X` (exit)

4. **Verify it was created**:
   ```bash
   cat .env | grep -v "^#" | grep "="
   ```

---

### Step C — Run the Automated Setup Script

This single command does EVERYTHING:

```bash
./run_all.sh
```

**What it does automatically:**
- ✅ Creates Python virtual environment
- ✅ Activates the venv
- ✅ Installs all dependencies from `requirements.txt`
- ✅ Loads environment variables from `.env`
- ✅ Verifies all API keys are set
- ✅ Tests Sentry connection
- ✅ Launches AEGIS main orchestrator

**Expected output:**
```
════════════════════════════════════════════════════════════════════════════
🛡️  AEGIS AUTONOMOUS CYBER DEFENSE - DAYTONA AUTO-SETUP
════════════════════════════════════════════════════════════════════════════

[1/8] Verifying project structure...
✓ Project structure verified

[2/8] Setting up Python virtual environment...
✓ Virtual environment active

[3/8] Installing Python dependencies...
✓ Dependencies installed

[4/8] Loading environment variables...
✓ Environment variables loaded

[5/8] Verifying sponsor API keys...
✓ All critical API keys present

[6/8] Testing Sentry connection...
✓ Sentry initialized

[7/8] Pre-flight check...
✓ All critical Python packages installed

════════════════════════════════════════════════════════════════════════════
✅ SETUP COMPLETE - LAUNCHING AEGIS
════════════════════════════════════════════════════════════════════════════

🎯 Starting main orchestrator...
   Press Ctrl+C to stop

────────────────────────────────────────────────────────────────────────────

🔥 AEGIS — Autonomous Cyber Defense Agent
   Daytona HackSprint 2025
...
```

---

### Step D — Verify Components Are Running

Once AEGIS launches, you should see:

1. **Sentry Initialization:**
   ```
   [SENTRY] Initialized for environment: daytona-aegis
   ```

2. **Event Processor Started:**
   ```
   ✓ Event processor started
   ```

3. **Dashboard Started:**
   ```
   ✓ Dashboard started
   ```

4. **Attack Simulator Started:**
   ```
   ✓ Attack simulator started
   ```

5. **Incident Detection:**
   ```
   🚨 INCIDENT DETECTED: sql_injection_attempt
      Recommended Action: quarantine
   ```

---

### Step E — Validate Sponsor Integrations

While AEGIS is running, verify each sponsor tool:

#### 1. **Sentry** (Error Tracking)
- Open: https://sentry.io
- Go to your project
- Check "Issues" tab
- You should see AEGIS events appearing

#### 2. **Claude** (AI Analysis)
- Watch the terminal output
- Look for:
  ```
  📊 CLAUDE BASIC ANALYSIS:
  ...
  🤖 CLAUDE AGENT SDK - AUTONOMOUS ANALYSIS:
  ...
  ```

#### 3. **Galileo** (AI Observability)
- Open: https://app.galileo.ai
- Select project: `aegis`
- Check log stream: `daytona-demo`
- You should see traces/spans appearing

#### 4. **BrowserUse** (Optional)
- Open BrowserUse dashboard
- Check for new session executions
- Verify replay artifacts

#### 5. **Daytona** (Optional)
- Already running in Daytona!
- Check project sync in your workspace

#### 6. **Slack** (Optional - if configured)
- Open your Slack workspace
- Check the configured channel
- You should see security alerts

---

## 🛠️ Manual Setup (Alternative Method)

If you prefer to run commands manually instead of using `run_all.sh`:

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# 5. Verify Sentry
python3 -c "from src.sentry_init import init_sentry; init_sentry()"

# 6. Run AEGIS
python3 main.py
```

---

## 🎬 For Demo Day

### Before the Demo

1. **Start AEGIS early:**
   ```bash
   ./run_all.sh
   ```

2. **Open monitoring dashboards:**
   - Sentry: https://sentry.io
   - Galileo: https://app.galileo.ai
   - Slack: Your workspace

3. **Prepare terminal:**
   - Increase font size (for visibility)
   - Dark theme recommended
   - Split screen with dashboards

### During the Demo

1. **Show terminal output:**
   - Point to incident detections
   - Show automated responses
   - Highlight API integrations

2. **Switch to sponsor dashboards:**
   - Show real-time Sentry events
   - Show Galileo AI traces
   - Show Slack notifications (if configured)

3. **Explain the workflow:**
   > "Here you can see AEGIS detecting a SQL injection attack in real-time.
   > Sentry captured the event, our behavioral analyzer identified the pattern,
   > and Claude generated a forensic report—all happening autonomously in seconds."

### After the Demo

1. **Stop gracefully:**
   - Press `Ctrl+C` in terminal
   - Wait for shutdown message

2. **Show sponsor verification:**
   ```bash
   python3 verify_pitch_requirements.py
   ```

---

## 🧪 Testing Individual Components

### Test Sentry Connection
```bash
python3 -c "from src.sentry_init import init_sentry; init_sentry(); print(1/0)"
```

### Test Claude API
```bash
python3 -c "from anthropic import Anthropic; client = Anthropic(); print(client.messages.create(model='claude-sonnet-4-5-20250929', max_tokens=50, messages=[{'role': 'user', 'content': 'Say: AEGIS working'}]).content[0].text)"
```

### Test Galileo SDK
```bash
python3 test_galileo_simple.py
```

### Test All Sponsors
```bash
python3 test_sponsor_responses.py
```

### Test Slack Integration
```bash
python3 src/integrations/slack_integration.py
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"

**Solution:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "SENTRY_DSN not set"

**Solution:**
1. Check `.env` file exists
2. Verify SENTRY_DSN is set correctly
3. Reload environment:
   ```bash
   export $(cat .env | xargs)
   ```

### Issue: "Claude API error"

**Solution:**
1. Verify API key is correct
2. Check you have credits: https://console.anthropic.com/
3. Test with simple call:
   ```bash
   python3 -c "from anthropic import Anthropic; print(Anthropic().messages.create(model='claude-sonnet-4-5-20250929', max_tokens=10, messages=[{'role': 'user', 'content': 'hi'}]))"
   ```

### Issue: "Permission denied: ./run_all.sh"

**Solution:**
```bash
chmod +x run_all.sh
./run_all.sh
```

### Issue: "No incidents detected"

**Explanation:** This is normal! The attack simulator runs periodically.
- Wait 10-30 seconds
- Incidents will start appearing
- Check `src/attack_simulator/simulate_attack.py` for timing

---

## 📊 Performance Metrics

When running in Daytona, expect:

| Metric | Value |
|--------|-------|
| **Startup Time** | ~5-10 seconds |
| **Memory Usage** | ~200-300 MB |
| **CPU Usage** | ~5-10% (idle) |
| **Response Time** | <5 seconds |
| **Events/Minute** | ~10-20 (simulated) |

---

## 🔗 Quick Reference

**Important Files:**
- `main.py` - Main orchestrator
- `run_all.sh` - Automated setup script
- `.env` - Environment variables
- `requirements.txt` - Python dependencies

**Important Commands:**
```bash
# Run everything
./run_all.sh

# Activate venv manually
source venv/bin/activate

# Test sponsors
python3 test_sponsor_responses.py

# Verify pitch claims
python3 verify_pitch_requirements.py

# Run live demo
python3 demo_pitch_live.py --scenario sql_injection
```

**Sponsor Dashboards:**
- Sentry: https://sentry.io
- Claude: https://console.anthropic.com
- Galileo: https://app.galileo.ai
- BrowserUse: https://browseruse.com
- Daytona: https://app.daytona.io

---

## 🎯 Success Checklist

Before demo day, verify:

- [ ] Daytona workspace created and accessible
- [ ] GitHub repo cloned in workspace
- [ ] `.env` file created with all API keys
- [ ] `./run_all.sh` runs without errors
- [ ] Sentry showing events
- [ ] Claude generating reports
- [ ] Galileo logging traces
- [ ] Terminal output clear and readable
- [ ] Sponsor dashboards accessible
- [ ] Backup plan ready (screenshots/video)

---

## 🚀 You're Ready!

Once `./run_all.sh` completes successfully, AEGIS is running in Daytona!

**For questions or issues:**
- Check this guide first
- Review `DEMO_GUIDE.md` for presentation tips
- Test with `verify_pitch_requirements.py`

**Good luck with your demo!** 🛡️
