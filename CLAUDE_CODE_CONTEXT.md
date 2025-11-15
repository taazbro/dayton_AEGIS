# 🔥 Zyberpol AEGIS — Claude Code System Document

(Paste this directly into Claude Code before writing any code)

---

## 📌 PROJECT OVERVIEW

Zyberpol AEGIS is an autonomous cyber-defense agent built for the Daytona HackSprint.
It performs:
- real-time attack pattern detection
- event stream processing
- burst/rate anomaly detection
- autonomous kill-switch activation
- mock credential rotation
- mock quarantine
- BrowserUse-based replay
- Claude-based forensics summary
- TUI-based monitoring dashboard

The system is written in pure Python (no framework).

Your role, Claude Code, is to:
1. Generate clean, correct Python code.
2. Maintain the exact folder/file structure.
3. Avoid introducing new dependencies unless explicitly allowed.
4. Keep logic modular, readable, and hackathon-friendly.
5. Never convert placeholder behavior into real privileged actions.
6. Always write code compatible with the existing architecture.

---

## 📁 PROJECT FILE STRUCTURE (MANDATORY)

Claude Code must always follow this exact structure:

```
zyberpol-aegis/
│
├── main.py
│
├── src/
│   ├── attack_simulator/
│   │       └── simulate_attack.py
│   ├── detector/
│   │       ├── event_processor.py
│   │       ├── pattern_detector.py
│   │       └── rate_analyzer.py
│   ├── responder/
│   │       ├── kill_switch.py
│   │       ├── rotate_credentials.py
│   │       └── quarantine.py
│   ├── browseruse_agent/
│   │       └── replay_attack.py
│   ├── forensics/
│   │       ├── threat_report.py
│   │       └── claude_interface.py
│   ├── dashboard/
│   │       └── tui.py
│   └── sentry_init.py
│
├── config/
│   ├── sentry.json
│   ├── daytona.json
│   └── agent_config.yaml
│
├── setup/
│   ├── bootstrap.sh
│   ├── install_sentry.sh
│   ├── install_browseruse.sh
│   ├── install_claude.sh
│   └── env_template.env
│
├── requirements.txt
└── README.md
```

Claude Code must never output files outside this structure unless asked.

---

## ⚙️ CORE MODULE BEHAVIOR REQUIREMENTS

Claude Code must ensure each module performs the following:

---

### 1. main.py
- orchestrates all components
- starts threads for processor + dashboard
- launches the attack simulator
- listens for incidents
- triggers responders
- generates forensics report
- forwards to Claude summary

---

### 2. Attack Simulator

**src/attack_simulator/simulate_attack.py**
- emits synthetic attack events
- supports sequences: recon → scan → exploit → cred-guess → exfil
- uses Queue to send events to processor
- should be simple, fast, and easy to modify

---

### 3. Event Processor

**src/detector/event_processor.py**
- consumes events
- updates rolling rate analyzer
- invokes pattern detector
- emits incidents

---

### 4. Pattern Detector

**src/detector/pattern_detector.py**
- performs rule-based detection
- simple heuristics only
- NO machine learning
- returns recommended action: monitor | quarantine | kill

---

### 5. Rate Analyzer

**src/detector/rate_analyzer.py**
- maintains sliding window of events
- returns count of event types
- supports pruning by timestamp

---

### 6. Responders

Located in **src/responder/**

**kill_switch.py**
- prints kill-switch activation
- no destructive system commands

**rotate_credentials.py**
- mock rotation only

**quarantine.py**
- mock quarantine only

Claude Code should NEVER introduce real destructive actions.

---

### 7. BrowserUse Replay

**src/browseruse_agent/replay_attack.py**
- prints steps
- returns replay artifacts
- BrowserUse integration is optional (mock is fine)

---

### 8. Forensics

Located in **src/forensics/**

**threat_report.py**
- assemble structured report for Claude

**claude_interface.py**
- if API key present: call Claude
- else: return offline summary

Claude Code must maintain this fallback behavior.

---

### 9. Dashboard

**src/dashboard/tui.py**
- Rich-powered TUI
- shows latest incidents
- autorefreshes

---

### 10. Sentry Initialization

**src/sentry_init.py**
- initialize Sentry with DSN
- environment name: "daytona-aegis"
- traces_sample_rate = 1.0
- safe initialization if key missing

---

## 🔒 SAFETY & HACKATHON RULES

Claude Code must:

✓ keep destructive behavior mocked
✓ avoid adding new dependencies without permission
✓ avoid any OS-level privileged commands
✓ keep BrowserUse usage safe and sandboxed
✓ avoid introducing long-running blocking loops
✓ not create deep nested abstractions
✓ write code fast, readable, hackathon-friendly

---

## 📦 CODING STYLE GUIDELINES

Claude Code must follow:
- Python 3.10+
- snake_case
- no unused imports
- type hints for function signatures
- use print() for logs, not logging module (simple for hackathon)
- maintain deterministic behavior for the demo
- avoid global state except for Queue and simple flags

---

## 🚨 CLAUDE CODE INSTRUCTIONS (VERY IMPORTANT)

Whenever Claude Code writes new code:
1. Always reference the project structure above.
2. Never overwrite files outside the asked scope.
3. Never introduce features that break hackathon compliance.
4. Default to stub/mocked behavior for anything not required.
5. **On multi-file outputs, produce sectioned responses:

```
# file: path/to/file.py
<code>
```

Only the code (no explanation).

---

## 📚 KNOWN ENVIRONMENT VARIABLES

Claude Code should rely on:

```
SENTRY_DSN
SENTRY_ENVIRONMENT
CLAUDE_API_KEY
CLAUDE_MODEL
BROWSERUSE_KEY
SLACK_WEBHOOK
```

All optional except DSN.

---

## 🎯 CLAUDE CODE'S ROLE DURING THE HACKATHON

Claude Code should help:
- write missing modules
- refactor logic
- fix runtime errors
- add extra detection heuristics
- generate test events
- add extra logs
- polish dashboard output
- assist in BrowserUse integration
- extend Claude prompts
- accelerate code writing
- generate fallback mocks
- help adapt to judges' feedback

Claude Code should ALWAYS output copy-ready code blocks.

---

## 🧠 EXTENDED CAPABILITIES CLAUDE CAN BE INSTRUCTED TO ADD

If asked:
- add new detectors
- add attack signatures
- add latency measurement
- add event tagging
- add alert webhooks
- simulate new threat types

But Claude should NOT add these unless explicitly requested.

---

## 🎉 DONE — This is the full Claude Code System Document.
