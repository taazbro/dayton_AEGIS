# 🔥 Zyberpol AEGIS

**Autonomous Cyber Defense Agent for Daytona HackSprint**

AEGIS (Autonomous Engine for Global Intrusion Security) is a real-time cyber defense system that detects, analyzes, and responds to security threats autonomously.

## 🎯 Features

- **Real-time Attack Detection**: Pattern-based and rate-based anomaly detection
- **Autonomous Response**: Automated kill-switch, quarantine, and credential rotation
- **BrowserUse Replay**: Attack sequence replay for forensic analysis
- **AI-Powered Forensics**: Claude-based threat analysis and recommendations
- **Live Dashboard**: Real-time TUI monitoring interface
- **Sentry Integration**: Error tracking and performance monitoring

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    ZYBERPOL AEGIS                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐      ┌──────────────┐              │
│  │   Attack     │─────>│    Event     │              │
│  │  Simulator   │      │  Processor   │              │
│  └──────────────┘      └──────┬───────┘              │
│                               │                        │
│                        ┌──────▼───────┐               │
│                        │   Pattern    │               │
│                        │   Detector   │               │
│                        └──────┬───────┘               │
│                               │                        │
│                        ┌──────▼───────┐               │
│                        │  Responders  │               │
│                        │ • Kill Switch│               │
│                        │ • Quarantine │               │
│                        │ • Rotation   │               │
│                        └──────┬───────┘               │
│                               │                        │
│                    ┌──────────▼──────────┐            │
│                    │   Forensics Engine  │            │
│                    │  • Threat Report    │            │
│                    │  • Claude Analysis  │            │
│                    └─────────────────────┘            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Virtual environment (recommended)
- API keys for:
  - Sentry (monitoring)
  - Claude (AI analysis)
  - Daytona (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/taazbro/dayton_AEGIS.git
   cd dayton_AEGIS
   ```

2. **Run bootstrap setup**
   ```bash
   bash setup/bootstrap.sh
   ```

3. **Configure environment variables**
   ```bash
   cp setup/env_template.env .env
   # Edit .env with your API keys
   ```

4. **Activate virtual environment**
   ```bash
   source venv/bin/activate
   ```

5. **Run AEGIS**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
zyberpol-aegis/
├── main.py                      # Main orchestrator
├── src/
│   ├── attack_simulator/        # Attack event generator
│   ├── detector/                # Detection engines
│   │   ├── event_processor.py
│   │   ├── pattern_detector.py
│   │   └── rate_analyzer.py
│   ├── responder/              # Response actions
│   │   ├── kill_switch.py
│   │   ├── rotate_credentials.py
│   │   └── quarantine.py
│   ├── browseruse_agent/       # Attack replay
│   ├── forensics/              # Threat analysis
│   │   ├── threat_report.py
│   │   └── claude_interface.py
│   ├── dashboard/              # TUI dashboard
│   └── sentry_init.py          # Monitoring setup
├── config/                     # Configuration files
├── setup/                      # Setup scripts
├── requirements.txt
└── README.md
```

## 🔒 Safety Features

AEGIS is designed for **hackathon demonstration** and includes important safety measures:

- **Mocked Responses**: All destructive actions are simulated, not executed
- **No Privileged Commands**: No actual system-level changes
- **Sandboxed Operation**: Safe for demo environments
- **BrowserUse Mock Mode**: Optional real browser automation

## 🎮 Usage

### Running the System

```bash
# Start AEGIS
python main.py
```

The system will:
1. Initialize Sentry monitoring
2. Start event processor
3. Launch TUI dashboard
4. Begin attack simulation
5. Detect and respond to threats
6. Generate forensic reports

### Monitoring Dashboard

The dashboard displays:
- Real-time incident detection
- Threat severity levels
- Response actions taken
- Event counts and sequences

### Configuration

Edit `config/agent_config.yaml` to customize:
- Detection thresholds
- Response delays
- Simulator settings
- BrowserUse options
- Dashboard preferences

## 🔍 Detection Capabilities

### Pattern-Based Detection
- **Data Exfiltration**: Immediate kill-switch
- **Active Exploitation**: Quarantine + credential rotation
- **Credential Attacks**: Rate limiting + monitoring
- **Port Scanning**: Enhanced monitoring

### Sequence-Based Detection
- **Kill-Chain Detection**: Recon → Scan → Exploit
- **Post-Exploit Exfil**: Exploitation followed by data theft

### Rate-Based Detection
- Sliding window analysis (60 seconds default)
- Per-event-type rate limiting
- Burst detection

## 🤖 Claude AI Integration

AEGIS uses Claude for forensic analysis:
- Threat severity assessment
- MITRE ATT&CK technique identification
- Actionable recommendations
- Long-term security improvements

Fallback: If Claude API is unavailable, uses offline analysis.

## 📊 Sentry Monitoring

Real-time monitoring includes:
- Error tracking
- Performance metrics
- Distributed tracing
- Custom event logging

## 🛠️ Development

### Adding New Detectors

1. Create detector in `src/detector/`
2. Implement detection logic
3. Register in `PatternDetector` or `EventProcessor`
4. Update configuration in `config/agent_config.yaml`

### Adding Response Actions

1. Create responder in `src/responder/`
2. Implement response logic (keep it mocked!)
3. Call from `main.py` incident handler
4. Document in configuration

### Extending BrowserUse

1. Edit `src/browseruse_agent/replay_attack.py`
2. Add real Playwright automation (optional)
3. Update artifact collection
4. Enhance insights generation

## 🧪 Testing

```bash
# Run AEGIS with default settings
python main.py

# Monitor dashboard output
# Watch for incident detection
# Review Claude analysis
```

## 📝 Environment Variables

Required:
- `SENTRY_DSN`: Sentry error tracking DSN
- `CLAUDE_API_KEY`: Claude API key for analysis

Optional:
- `SENTRY_ENVIRONMENT`: Environment name (default: daytona-aegis)
- `CLAUDE_MODEL`: Claude model to use
- `DAYTONA_API_KEY`: Daytona integration
- `BROWSERUSE_KEY`: BrowserUse API key
- `SLACK_WEBHOOK`: Slack notifications

## 🏆 Hackathon Highlights

- **Pure Python**: No frameworks, clean architecture
- **Modular Design**: Easy to extend and modify
- **Safe Demo**: All actions mocked for safety
- **AI-Powered**: Claude forensic analysis
- **Real-time**: Live monitoring and response
- **Production-Ready Patterns**: Scalable architecture

## 🤝 Contributing

This is a hackathon project built for Daytona HackSprint. Contributions welcome!

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Built for Daytona HackSprint
- Powered by Claude AI
- Monitored by Sentry

## 📞 Support

For issues or questions:
- GitHub Issues: https://github.com/taazbro/dayton_AEGIS/issues
- Documentation: See CLAUDE_CODE_CONTEXT.md

---

**Built with ❤️ for autonomous cyber defense**
