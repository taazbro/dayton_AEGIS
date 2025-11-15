# 🎥 AEGIS Video Recording - Quick Start

**Ultimate speed run guide - 10 minutes total**

---

## ⚡ 3 Steps to Record Your Demo

### Step 1: Setup Daytona (5 minutes)

```bash
# 1. Create Daytona workspace from GitHub
#    Repository: https://github.com/taazbro/dayton_AEGIS

# 2. Open terminal in Daytona

# 3. Create .env file
nano .env

# Paste this (with YOUR actual keys):
SENTRY_DSN=https://YOUR_SENTRY_DSN@sentry.io/PROJECT
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE
GALILEO_API_KEY=YOUR_GALILEO_KEY_HERE
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Save: Ctrl+O, Enter, Ctrl+X

# 4. Run setup
./run_all.sh

# Wait for "✅ SETUP COMPLETE"
# Press Ctrl+C to stop (we'll restart for recording)
```

### Step 2: Prepare Recording (2 minutes)

```bash
# 1. Increase terminal font
Settings → Terminal → Font Size → 18

# 2. Clear terminal
clear

# 3. Open screen recorder
# - Mac: QuickTime → File → New Screen Recording
# - Windows: Win+G (Game Bar)
# - Any: Download Loom (loom.com) - easiest!

# 4. Position terminal window in center
```

### Step 3: Record (4 minutes)

```bash
# 1. Start your screen recorder

# 2. In terminal, run:
python3 demo_pitch_live.py --scenario sql_injection

# 3. Don't touch anything - let it run
#    The demo is fully automated

# 4. After ~4 minutes, it completes

# 5. Stop screen recorder

# DONE! ✅
```

---

## 🎬 What Gets Recorded

Your video will show:

**Phase 1 (30s):** Autonomous attack simulation
- Port scanning → SQL injection → Data exfiltration

**Phase 2 (30s):** Sentry telemetry
- Real-time event logging
- Severity levels, network connections

**Phase 3 (1m):** AEGIS detection & response
- 95.7% confidence detection
- 4.7 second response time
- 5 automated actions

**Phase 4 (1m):** Claude AI report
- Forensic analysis
- Timeline reconstruction
- Actionable recommendations

**Phase 5 (30s):** Slack notification
- SOC team alert
- Incident summary

---

## 🎤 Optional: Add Narration

### While Recording (Live):

"Hi, I'm [name]. This is AEGIS running live in Daytona - watch it detect and
neutralize a SQL injection attack in under 5 seconds."

[Let demo run]

"Response time: 4.7 seconds. Zero data loss. That's AEGIS."

### After Recording (Voiceover):

Record silently, add voice later using:
- iMovie (Mac)
- DaVinci Resolve (Free, all platforms)
- Kapwing (Online, super easy)

---

## 📤 Upload & Share

1. **Export as MP4** (1920x1080 if possible)

2. **Upload to:**
   - YouTube (unlisted) ← Best for hackathons
   - Vimeo
   - Loom (easiest)

3. **Get shareable link**

4. **Add to hackathon submission**

---

## 🚨 If Something Goes Wrong

### Demo doesn't start:
```bash
source venv/bin/activate
pip install -r requirements.txt
python3 demo_pitch_live.py --scenario sql_injection
```

### "ModuleNotFoundError":
```bash
./run_all.sh
```

### Want to re-record:
```bash
clear
python3 demo_pitch_live.py --scenario sql_injection
```

No problem! Just re-run the command.

---

## 💡 Pro Tips

1. **Practice once** before final recording
2. **Increase font size** - viewers need to read terminal
3. **Use dark theme** - better for video
4. **Record full screen** or just terminal window
5. **Keep it simple** - the demo speaks for itself

---

## ⏱️ Timeline

- **0:00-0:15** - Your intro (optional)
- **0:15-3:45** - Demo runs (automated)
- **3:45-4:00** - Your outro (optional)

**Total: 4 minutes** ✅

---

## 🎯 Absolute Minimum (If Rushed)

```bash
# 1. In Daytona terminal
nano .env          # Add API keys

# 2. Run this
./run_all.sh

# 3. Press Ctrl+C when you see "✅ SETUP COMPLETE"

# 4. Start screen recorder

# 5. Run this
clear
python3 demo_pitch_live.py --scenario sql_injection

# 6. Wait 4 minutes

# 7. Stop recorder

# DONE!
```

---

## 📞 Need More Details?

See: **DAYTONA_VIDEO_RECORDING_GUIDE.md**

Covers:
- Advanced recording techniques
- Multi-dashboard switching
- Editing tips
- Platform-specific instructions
- Troubleshooting

---

**Ready? Let's record! 🎬**
