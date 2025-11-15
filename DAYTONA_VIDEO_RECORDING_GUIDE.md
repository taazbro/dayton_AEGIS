# 🎥 AEGIS Daytona Video Recording Guide

Complete step-by-step guide for running AEGIS in Daytona and recording a professional demo video.

---

## 📋 Overview

**Goal:** Record a 4-minute demo video showing AEGIS running in Daytona
**Tools Needed:** Daytona workspace, screen recorder, API keys
**Expected Output:** Professional demo video for hackathon submission

---

## 🚀 Part 1: Daytona Workspace Setup (5 minutes)

### Step 1: Create Daytona Workspace

1. **Go to Daytona Dashboard:**
   - Visit: https://app.daytona.io
   - Log in with your account

2. **Create New Workspace:**
   ```
   Click: "New Workspace" or "Create Workspace"

   Repository: https://github.com/taazbro/dayton_AEGIS
   Branch: main
   Workspace Name: aegis-demo (or your choice)
   ```

3. **Wait for Workspace to Initialize:**
   - Daytona will clone the repository
   - Wait for "Ready" status (usually 30-60 seconds)

4. **Open Workspace:**
   - Click "Open" or "Open in Browser"
   - You'll see VS Code in browser OR connect via desktop

### Step 2: Open Terminal in Daytona

**In Daytona VS Code:**
1. Click **Terminal** → **New Terminal** (or press `` Ctrl+` ``)
2. You should see a bash prompt
3. Verify you're in the project root:
   ```bash
   pwd
   ls -la
   ```

   You should see:
   ```
   main.py
   src/
   requirements.txt
   run_all.sh
   DAYTONA_SETUP.md
   ...
   ```

### Step 3: Create .env File with API Keys

1. **Create the .env file:**
   ```bash
   nano .env
   ```

2. **Copy and paste your API keys:**
   ```bash
   # ========================================
   # AEGIS ENVIRONMENT CONFIGURATION
   # ========================================

   # SPONSOR 1: Sentry (Error Tracking)
   SENTRY_DSN=https://YOUR_SENTRY_DSN@sentry.io/YOUR_PROJECT

   # SPONSOR 2: Claude AI (Anthropic)
   ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE

   # SPONSOR 3: Galileo (AI Observability)
   GALILEO_API_KEY=YOUR_GALILEO_KEY_HERE
   GALILEO_PROJECT=aegis
   GALILEO_LOG_STREAM=daytona-demo

   # SPONSOR 4: Slack Notifications
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

   # SPONSOR 5: BrowserUse (Optional)
   BROWSERUSE_API_KEY=YOUR_BROWSERUSE_KEY_HERE

   # SPONSOR 6: Daytona (Optional)
   DAYTONA_API_KEY=YOUR_DAYTONA_KEY_HERE
   ```

3. **Save the file:**
   - Press `Ctrl+O` (write out)
   - Press `Enter` (confirm)
   - Press `Ctrl+X` (exit)

4. **Verify it was created:**
   ```bash
   cat .env | grep -v "^#" | grep "="
   ```

### Step 4: Run Automated Setup

**Execute the setup script:**
```bash
chmod +x run_all.sh
./run_all.sh
```

**What happens:**
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
```

**If successful, you'll see AEGIS running!**

To **stop** AEGIS (for now): Press `Ctrl+C`

---

## 🎬 Part 2: Preparing for Video Recording (10 minutes)

### Step 1: Choose Your Recording Tool

**Option A: OBS Studio (Recommended - Free)**
- Download: https://obsproject.com/
- Pros: Professional quality, free, cross-platform
- Best for: Longer demos, multiple scenes

**Option B: Loom (Easiest - Free Tier)**
- Website: https://www.loom.com/
- Pros: Super easy, instant sharing
- Best for: Quick demos, immediate upload

**Option C: macOS QuickTime (Mac Only)**
- Built-in on Mac
- Pros: Simple, no install needed
- File → New Screen Recording

**Option D: Windows Game Bar (Windows Only)**
- Built-in on Windows 10/11
- Press `Win+G` to open
- Pros: Simple, no install needed

### Step 2: Optimize Terminal for Recording

**Before recording, make your terminal look professional:**

1. **Increase Font Size:**
   - In Daytona VS Code terminal
   - Settings → Terminal → Font Size → 16-18px
   - Make it readable in video

2. **Use Dark Theme:**
   - Settings → Color Theme → Dark+ (default dark)
   - Better contrast for recording

3. **Clear Terminal:**
   ```bash
   clear
   ```

4. **Set Terminal Size:**
   - Make terminal window large
   - Viewers should easily see text

### Step 3: Prepare Additional Windows

**Open these in separate browser tabs (for switching during demo):**

1. **Sentry Dashboard:**
   - https://sentry.io
   - Navigate to your AEGIS project
   - Keep "Issues" tab open

2. **Galileo Dashboard:**
   - https://app.galileo.ai
   - Navigate to "aegis" project
   - Keep traces view open

3. **Slack Workspace:**
   - Your Slack workspace
   - Keep the channel with webhook open

4. **GitHub Repository:**
   - https://github.com/taazbro/dayton_AEGIS
   - Show the code if needed

### Step 4: Create a Script/Outline

**What you'll say during each phase:**

```
INTRO (15 seconds):
"Hello, I'm [name] and this is AEGIS - an autonomous AI-powered cyber defense
system running live in Daytona. Watch as it detects and neutralizes a
SQL injection attack in under 5 seconds."

PHASE 1 - Attack (30s):
"Starting the autonomous attack simulation..."

PHASE 2 - Sentry (30s):
"Sentry is capturing every event in real-time..."

PHASE 3 - Detection (1m):
"AEGIS detected the attack with 95.7% confidence. Response time: 4.7 seconds.
Watch the 5 automated actions..."

PHASE 4 - Claude (1m):
"Claude AI is generating the forensic report..."

PHASE 5 - Slack (30s):
"SOC team receives immediate notification..."

CLOSING (15s):
"That's AEGIS: autonomous detection, instant response, zero data loss."
```

---

## 🎥 Part 3: Recording the Demo (4 minutes)

### Recording Checklist

**Before you hit record:**
- [ ] Terminal font size increased (16-18px)
- [ ] Terminal window is large and centered
- [ ] All API keys are set (verified with `./run_all.sh`)
- [ ] Sentry, Galileo, Slack dashboards open in tabs
- [ ] Script/outline ready
- [ ] Close distracting apps/notifications
- [ ] Check audio (if recording voice)
- [ ] Test screen recorder works

### Recording Method 1: Terminal Only (Simplest)

**Best for:** Focused technical demo

1. **Start Screen Recording**
   - Record only the terminal window
   - Or full screen with terminal maximized

2. **Run the Main Demo:**
   ```bash
   clear
   python3 demo_pitch_live.py --scenario sql_injection
   ```

3. **Let it run for 4 minutes**
   - The script is self-paced
   - Each phase auto-advances
   - Shows all 5 phases

4. **Stop Recording**
   - Wait for demo to complete
   - Press `Ctrl+C` if needed
   - Stop screen recorder

**Output:** Clean 4-minute terminal demo video

### Recording Method 2: Terminal + Dashboards (Professional)

**Best for:** Showing sponsor integrations

1. **Start with Terminal View**
   ```bash
   clear
   python3 demo_pitch_live.py --scenario sql_injection
   ```

2. **During Phase 2 (Sentry Telemetry):**
   - Switch to Sentry dashboard tab
   - Show events appearing in real-time
   - Switch back to terminal

3. **During Phase 4 (Claude Report):**
   - Show the terminal output
   - Optionally switch to Claude console

4. **During Phase 5 (Slack):**
   - Switch to Slack workspace
   - Show the alert message
   - Switch back to terminal

**Output:** Professional multi-view demo

### Recording Method 3: Picture-in-Picture (Advanced)

**Best for:** Maximum professional look

1. **Setup:**
   - Use OBS Studio
   - Scene 1: Terminal (main)
   - Scene 2: Sentry dashboard
   - Scene 3: Slack workspace

2. **During Recording:**
   - Switch scenes at appropriate times
   - Use transitions (fade, slide)

3. **Add Overlays (Optional):**
   - Your name/project name
   - Phase labels ("Phase 3: Detection")
   - Timer showing <5s response

---

## 🎤 Part 4: Audio & Narration (Optional)

### Option A: Record Voice Live

**During screen recording:**
- Explain what's happening
- Follow your script
- Keep it conversational

**Tips:**
- Use a decent microphone (not laptop mic)
- Speak clearly and not too fast
- Practice once before final recording

### Option B: Add Voiceover After

**After screen recording:**
1. Record screen silently
2. Use tool to add audio later:
   - iMovie (Mac)
   - DaVinci Resolve (Free, all platforms)
   - Camtasia (Paid)

### Option C: Add Captions Only

**No voice, just text:**
- Record screen silently
- Add text overlays explaining each phase
- Add background music (optional)

**Free tools:**
- Kapwing (online)
- OpenShot (desktop)

---

## 📝 Part 5: Post-Recording Editing (10-15 minutes)

### Basic Edits You Might Want:

1. **Trim Start/End:**
   - Remove setup time before demo starts
   - Cut after demo completes

2. **Add Title Screen (5 seconds):**
   ```
   AEGIS
   Autonomous Cyber Defense
   Running in Daytona
   ```

3. **Add Phase Labels (Optional):**
   - "Phase 1: Autonomous Attack"
   - "Phase 2: Sentry Telemetry"
   - "Phase 3: AEGIS Detection"
   - "Phase 4: Claude AI Report"
   - "Phase 5: Slack Notification"

4. **Add Closing Screen (5 seconds):**
   ```
   AEGIS - Autonomous Defense

   GitHub: github.com/taazbro/dayton_AEGIS
   Built with: Sentry | Claude | Galileo
              Slack | BrowserUse | Daytona
   ```

### Free Editing Tools:

- **iMovie** (Mac) - Simple, built-in
- **DaVinci Resolve** (All platforms) - Professional, free
- **OpenShot** (All platforms) - Open source
- **Kapwing** (Online) - Browser-based, very easy

---

## 🎯 Part 6: Demo Recording Scripts

### Script 1: Quick 4-Minute Demo (Just Terminal)

```bash
# 1. Clear and prepare
clear

# 2. Start recording

# 3. Run main demo
python3 demo_pitch_live.py --scenario sql_injection

# 4. Wait for completion (~4 minutes)

# 5. Stop recording
```

**Narration points:**
- Intro: "Watch AEGIS detect and respond to a SQL injection attack"
- During: Let the terminal output speak for itself
- End: "Response time: 4.7 seconds. Zero data loss."

### Script 2: Demo with Dashboard Switching (5 minutes)

```bash
# Terminal window
python3 demo_pitch_live.py --scenario sql_injection

# While running:
# - Phase 1: Show terminal (attack simulation)
# - Phase 2: Switch to Sentry dashboard
# - Phase 3: Back to terminal (show 5 actions)
# - Phase 4: Terminal (Claude report)
# - Phase 5: Switch to Slack workspace
```

### Script 3: Fast Demo (30 seconds)

```bash
# For quick video
python3 fast_attack_demo.py
```

**Best for:** Social media, Twitter, LinkedIn

---

## 🎬 Part 7: Specific Recording Instructions by Platform

### Recording in Daytona Web IDE:

1. **Full Browser Window:**
   - Record entire browser window
   - Shows Daytona branding (good for sponsor)
   - Terminal is visible

2. **Just Terminal Pane:**
   - Focus recording on terminal only
   - Crop browser chrome
   - Cleaner look

### Recording in Daytona Desktop:

1. **If using VS Code Desktop:**
   - Connect Daytona via SSH
   - Record VS Code window
   - More responsive than browser

### Best Settings:

- **Resolution:** 1920x1080 (Full HD)
- **Frame Rate:** 30 FPS minimum
- **Audio:** 44.1kHz if recording voice
- **Format:** MP4 (most compatible)

---

## ✅ Pre-Recording Checklist

**30 Minutes Before Recording:**

- [ ] Daytona workspace is running
- [ ] `.env` file created with all API keys
- [ ] Ran `./run_all.sh` successfully once (to verify setup)
- [ ] Terminal font size increased (16-18px)
- [ ] Terminal theme is dark
- [ ] Sentry dashboard open in tab
- [ ] Galileo dashboard open in tab
- [ ] Slack workspace open in tab
- [ ] Screen recorder tested and working
- [ ] Notifications disabled (Do Not Disturb)
- [ ] Close unnecessary apps
- [ ] Clear browser tabs except needed ones
- [ ] Script/outline ready
- [ ] Practice run completed (optional but recommended)

**Right Before Recording:**

- [ ] Run `clear` in terminal
- [ ] Position terminal window center screen
- [ ] Check recording area is correct
- [ ] Take a deep breath
- [ ] Start recording
- [ ] Count "3, 2, 1" silently
- [ ] Begin!

---

## 🎥 Recommended Video Structure

### 4-Minute Video Outline:

**0:00-0:15 (15s) - Title Screen**
- AEGIS logo/title
- "Autonomous Cyber Defense in Daytona"

**0:15-0:30 (15s) - Intro**
- Quick explanation of what AEGIS does
- "Watch live demo in Daytona"

**0:30-3:30 (3m) - Live Demo**
- Run `demo_pitch_live.py`
- Show all 5 phases
- Switch to dashboards as needed

**3:30-3:45 (15s) - Results**
- Highlight: "4.7 seconds response time"
- "95.7% confidence detection"
- "Zero data loss"

**3:45-4:00 (15s) - Closing**
- Show sponsor logos
- GitHub link
- Call to action

---

## 🚨 Troubleshooting During Recording

### If Demo Fails:

**Option 1: Pause and Restart**
- Stop screen recording
- Fix the issue
- Start fresh recording

**Option 2: Keep Going**
- If minor issue, keep recording
- Can edit out issues later
- Shows real-world resilience

### Common Issues:

**"ModuleNotFoundError"**
```bash
# Solution:
source venv/bin/activate
pip install -r requirements.txt
```

**"SENTRY_DSN not set"**
```bash
# Solution:
export $(cat .env | grep -v '^#' | xargs)
```

**Terminal output too fast**
```bash
# Add delays to demo script (edit demo_pitch_live.py)
# Or use slower_output mode if available
```

---

## 📤 Part 8: After Recording - Export & Share

### Export Settings:

**For YouTube/Vimeo:**
- Format: MP4
- Codec: H.264
- Resolution: 1920x1080
- Bitrate: 5-10 Mbps
- Audio: AAC, 128-192 kbps

**For Social Media:**
- Twitter: Max 2:20, MP4
- LinkedIn: Max 10 min, MP4
- Instagram: Max 1 min (Stories), MP4

### Upload Locations:

1. **YouTube** (Recommended)
   - Unlisted or Public
   - Good for hackathon judges
   - Shareable link

2. **Vimeo**
   - Professional look
   - Good privacy controls

3. **Google Drive**
   - Easy sharing
   - Download link for judges

4. **Loom**
   - Instant upload
   - Auto-transcription
   - Easy sharing

---

## 🎯 Quick Start - TL;DR

**For the impatient - do this:**

1. **Setup Daytona (5 min):**
   ```bash
   # In Daytona workspace terminal:
   nano .env          # Add your API keys
   ./run_all.sh       # Verify everything works
   ```

2. **Prepare Recording (2 min):**
   - Increase terminal font size
   - Open screen recorder (Loom/OBS/QuickTime)
   - Position terminal window

3. **Record (4 min):**
   ```bash
   clear
   python3 demo_pitch_live.py --scenario sql_injection
   ```

4. **Done!**
   - Edit if needed (trim start/end)
   - Export as MP4
   - Upload to YouTube/Vimeo
   - Share link

---

## 📞 Need Help?

**Common Questions:**

Q: "Can I record in Daytona browser or need desktop?"
A: Either works! Browser is easier, desktop is more responsive.

Q: "What if my demo fails during recording?"
A: Pause, fix, re-record. Or keep going and edit later.

Q: "How long should my video be?"
A: 3-5 minutes is perfect. 4 minutes is ideal.

Q: "Should I add music?"
A: Optional. Keep it subtle, don't overpower narration.

Q: "What resolution should I record?"
A: 1920x1080 (1080p) is best. 1280x720 (720p) is acceptable.

---

## 🏆 Pro Tips

1. **Practice First:**
   - Do 2-3 practice runs
   - Get comfortable with timing
   - Know when to speak

2. **Keep It Simple:**
   - Don't over-edit
   - Let the demo speak
   - Clear > Fancy

3. **Show Real Results:**
   - Real Sentry events
   - Real Claude responses
   - Real Slack messages
   - Proves it's not mocked

4. **Use Zoom-In (Optional):**
   - Zoom terminal to highlight key moments
   - "See the 4.7s response time?"
   - Can do in post-production

5. **Add Subtitles:**
   - YouTube auto-captions work well
   - Or add manually
   - Accessibility + clarity

---

## ✅ Final Checklist

**Before Submitting Video:**

- [ ] Video is 3-5 minutes long
- [ ] Audio is clear (if included)
- [ ] Terminal text is readable
- [ ] Shows AEGIS running in Daytona
- [ ] Demonstrates all 5 phases
- [ ] Shows sponsor integrations
- [ ] Includes intro/outro
- [ ] Exported as MP4
- [ ] Tested playback
- [ ] Uploaded to platform
- [ ] Share link works
- [ ] Added to hackathon submission

---

**You're ready to record! 🎬**

Run through the demo once, hit record, and show the world what AEGIS can do!

Good luck! 🛡️
