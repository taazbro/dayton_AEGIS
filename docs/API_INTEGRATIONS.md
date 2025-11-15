# AEGIS API Integrations Guide

## Overview

AEGIS maximizes API usage across 12+ external services while minimizing Claude API calls by 90% through intelligent caching, rate limiting, and severity gating.

---

## 🎯 API Usage Strategy

### Claude API Optimization (90% Reduction)

**Location:** `src/forensics/claude_interface.py`

**Optimizations Applied:**
1. **Severity Gating** - Only calls Claude for HIGH/CRITICAL threats
2. **5-Minute Response Cache** - Identical threats reuse cached analysis
3. **Rate Limiting** - Max 10 API calls per minute
4. **Graceful Degradation** - Falls back to offline analysis

**Before:** Called on every incident
**After:** Only called on ~10% of incidents (HIGH/CRITICAL only)

```python
# Example usage
from src.forensics.claude_interface import get_claude_summary

# Automatically cached, rate-limited, and severity-gated
analysis = get_claude_summary(threat_report)
```

---

## 📡 Active API Integrations (11 New Services)

### 1. PagerDuty (Incident Escalation)

**Purpose:** Escalate critical incidents to on-call responders
**Location:** `src/alerts/pagerduty_notifier.py`
**Trigger:** HIGH/CRITICAL severity incidents only

**Configuration:**
```bash
PAGERDUTY_INTEGRATION_KEY=your-integration-key-here
```

**Features:**
- Automatic severity mapping (CRITICAL → critical, HIGH → error)
- Deduplication (groups similar incidents within 1 hour)
- MITRE ATT&CK technique tags
- Custom event details

**API Endpoint:** `https://events.pagerduty.com/v2/enqueue`

---

### 2. Microsoft Teams (Notifications)

**Purpose:** Send rich alerts to Teams channels
**Location:** `src/alerts/teams_notifier.py`
**Trigger:** All severity levels

**Configuration:**
```bash
TEAMS_WEBHOOK_URL=https://your-org.webhook.office.com/webhookb2/YOUR-URL
```

**Features:**
- Adaptive Card formatting
- Color-coded by severity
- MITRE ATT&CK tags
- Detection engine attribution
- Action buttons (View Dashboard)

**API Type:** Incoming Webhook

---

### 3. Discord (Notifications)

**Purpose:** Send embeds to Discord security channels
**Location:** `src/alerts/discord_notifier.py`
**Trigger:** All severity levels

**Configuration:**
```bash
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR-WEBHOOK-URL
```

**Features:**
- Rich embeds with color coding
- Emoji-enhanced fields
- MITRE technique formatting
- Custom bot avatar
- Timestamp tracking

**API Type:** Discord Webhook

---

### 4. Datadog (APM & Metrics)

**Purpose:** Application performance monitoring and metrics
**Location:** `src/monitoring/datadog_integration.py`
**Trigger:** Every incident

**Configuration:**
```bash
DATADOG_API_KEY=your-datadog-api-key
DATADOG_APP_KEY=your-datadog-app-key
DATADOG_SITE=datadoghq.com
```

**Metrics Sent:**
- `aegis.threats.detected` (counter)
- `aegis.threats.severity` (gauge)
- `aegis.events.count` (gauge)
- `aegis.detection.engine` (counter per engine)

**Events Sent:**
- Incident alerts with full context
- Automatic alert_type mapping (critical/error/warning/info)

**API Endpoints:**
- Metrics: `https://api.datadoghq.com/api/v2/series`
- Events: `https://api.datadoghq.com/api/v1/events`

---

### 5. Splunk HEC (SIEM Forwarding)

**Purpose:** Forward all security events to Splunk
**Location:** `src/monitoring/splunk_hec.py`
**Trigger:** Every incident

**Configuration:**
```bash
SPLUNK_HEC_TOKEN=your-hec-token
SPLUNK_HEC_URL=https://your-splunk:8088/services/collector/event
SPLUNK_INDEX=aegis_security
```

**Features:**
- HTTP Event Collector (HEC) protocol
- Structured JSON events
- Custom source/sourcetype
- Field extraction ready
- Metric support

**API Endpoint:** Splunk HEC `/services/collector/event`

---

### 6. MITRE ATT&CK API (Threat Intel)

**Purpose:** Enrich incidents with MITRE technique details
**Location:** `src/threat_intel/mitre_attack_api.py`
**Trigger:** Every incident
**API Key:** NOT REQUIRED (uses public STIX data)

**Features:**
- Loads 1000+ techniques from MITRE CTI repo
- Local cache for instant lookups
- Technique name, description, tactics
- Platform and data source mapping
- Detection guidance

**Data Source:**
```
https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json
```

**Example Enrichment:**
```python
from src.threat_intel.mitre_attack_api import get_mitre_api

mitre = get_mitre_api()
enriched_report = mitre.enrich_threat_report(threat_report)
# Adds: technique_name, description, url, platforms, detection
```

---

### 7. Jira (Ticket Creation)

**Purpose:** Auto-create tickets for MEDIUM+ severity incidents
**Location:** `src/integrations/jira_integration.py`
**Trigger:** MEDIUM, HIGH, CRITICAL severity only

**Configuration:**
```bash
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@company.com
JIRA_API_TOKEN=your-jira-api-token
JIRA_PROJECT=SEC
JIRA_DEFAULT_ASSIGNEE=security-team@company.com
```

**Features:**
- Jira Cloud API v3
- Basic authentication
- Rich ticket descriptions (Jira markup)
- MITRE technique links
- Auto-priority mapping
- Security labels

**API Endpoint:** `https://your-domain.atlassian.net/rest/api/3/issue`

**Priority Mapping:**
- CRITICAL → Highest
- HIGH → High
- MEDIUM → Medium
- LOW → Low

---

### 8. VirusTotal (Threat Intelligence)

**Purpose:** IP/URL/file hash reputation lookups
**Location:** `src/threat_intel/virustotal_api.py`
**Trigger:** Incidents with IP addresses in affected_entities

**Configuration:**
```bash
VIRUSTOTAL_API_KEY=your-virustotal-api-key
```

**Features:**
- IP reputation checks
- URL reputation checks
- File hash lookups (MD5/SHA1/SHA256)
- Automatic URL submission for scanning
- Country/ASN enrichment
- Malicious/suspicious/harmless counts

**API Endpoints:**
- IP: `https://www.virustotal.com/api/v3/ip_addresses/{ip}`
- URL: `https://www.virustotal.com/api/v3/urls/{url_id}`
- File: `https://www.virustotal.com/api/v3/files/{hash}`

**Rate Limits:** Free tier = 4 requests/minute

---

### 9. Prometheus (Metrics Export)

**Purpose:** Export metrics for Prometheus scraping
**Location:** `src/monitoring/prometheus_exporter.py`
**Trigger:** Built-in HTTP server on startup
**API Key:** NOT REQUIRED

**Configuration:**
```bash
PROMETHEUS_EXPORTER_PORT=9090
```

**Metrics Exported:**
- `aegis_threats_total` (counter)
- `aegis_critical_threats_total` (counter)
- `aegis_high_threats_total` (counter)
- `aegis_medium_threats_total` (counter)
- `aegis_low_threats_total` (counter)
- `aegis_threat_type_*_total` (counter per type)
- `aegis_detection_engine_*_total` (counter per engine)
- `aegis_response_action_*_total` (counter per action)
- `aegis_current_threat_level` (gauge)
- `aegis_detection_latency_ms` (histogram)

**Endpoints:**
- Metrics: `http://localhost:9090/metrics`
- Health: `http://localhost:9090/health`

**Prometheus Scrape Config:**
```yaml
scrape_configs:
  - job_name: 'aegis'
    static_configs:
      - targets: ['localhost:9090']
```

---

## 🔄 Integration Flow

For each detected incident, AEGIS calls APIs in this order:

```
1. Incident Detected
   ↓
2. MITRE ATT&CK Enrichment (no key required)
   ↓
3. VirusTotal Intelligence (if IPs present)
   ↓
4. Claude AI Analysis (cached, rate-limited, HIGH/CRITICAL only)
   ↓
5. Datadog Metrics + Events
   ↓
6. Splunk HEC Event Forwarding
   ↓
7. Prometheus Metrics Recording
   ↓
8. PagerDuty Escalation (HIGH/CRITICAL only)
   ↓
9. Microsoft Teams Alert
   ↓
10. Discord Alert
    ↓
11. Slack Alert (existing)
    ↓
12. Jira Ticket Creation (MEDIUM+)
```

**Total API Calls Per Incident:**
- LOW severity: ~7 API calls (no Claude, PagerDuty, or Jira)
- MEDIUM severity: ~9 API calls (no Claude or PagerDuty)
- HIGH severity: ~11 API calls (includes Claude, limited by cache)
- CRITICAL severity: ~11 API calls (includes Claude, limited by cache)

---

## 📊 API Usage Statistics

### Before Optimization
- **Claude API:** 100% of incidents (100+ calls/hour)
- **Other APIs:** 2 (Sentry, Slack)
- **Total APIs:** 3

### After Optimization
- **Claude API:** ~10% of incidents (10-15 calls/hour) - **90% reduction**
- **Other APIs:** 11 (PagerDuty, Teams, Discord, Datadog, Splunk, MITRE, Jira, VirusTotal, Prometheus, Sentry, Slack)
- **Total APIs:** 12
- **API Calls Per Incident:** 7-11 depending on severity
- **Total API Calls/Hour:** ~500-800 (vs. previous ~100)

**Net Result:** 5-8x increase in API usage while reducing Claude by 90%

---

## 🔐 Security Best Practices

1. **API Keys:** Never commit API keys to git
2. **Encryption:** Use `tools/secrets_manager.py` to encrypt `.env`
3. **Rate Limits:** All integrations have retry logic
4. **Graceful Degradation:** System works offline if APIs unavailable
5. **HTTPS Only:** All API calls use TLS 1.2+
6. **Timeouts:** 5-10 second timeouts on all external calls
7. **Validation:** Input sanitization before API calls

---

## 🚀 Quick Start

### 1. Configure API Keys

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API keys
nano .env
```

### 2. Enable Specific Integrations

Each integration checks for its API key on startup. If not configured, it gracefully skips.

**Minimum Required:**
- None (system works offline)

**Recommended for Production:**
- SENTRY_DSN (error tracking)
- SLACK_WEBHOOK (basic alerts)
- PROMETHEUS_EXPORTER_PORT (metrics)

**Optional (maximize API usage):**
- PAGERDUTY_INTEGRATION_KEY
- TEAMS_WEBHOOK_URL
- DISCORD_WEBHOOK_URL
- DATADOG_API_KEY
- SPLUNK_HEC_TOKEN
- JIRA_API_TOKEN
- VIRUSTOTAL_API_KEY
- CLAUDE_API_KEY (for HIGH/CRITICAL only)

### 3. Run AEGIS

```bash
python main.py
```

---

## 📈 Monitoring API Usage

### Prometheus Metrics Dashboard

Access metrics at `http://localhost:9090/metrics`

### Datadog Dashboard

View real-time metrics in Datadog:
- Threat detection rate
- Severity distribution
- Detection engine performance
- API latency

### Splunk Dashboards

Query events in Splunk:
```spl
index=aegis_security sourcetype=_json
| stats count by threat_type severity
```

---

## 🐛 Troubleshooting

### API Call Failures

All integrations have graceful error handling:
```
⚠️  PagerDuty integration key not configured
❌ Teams API error: 400 - Invalid webhook URL
```

### Claude Rate Limiting

If you see:
```
[RATE LIMITED] OFFLINE ANALYSIS...
```

This is expected! Rate limiting is working to reduce Claude usage.

### Cached Responses

If you see:
```
[CACHED] Threat assessment: CRITICAL...
```

This is expected! Caching is working to reduce duplicate API calls.

---

## 🔮 Future Integrations

Potential additions:
- AWS Security Hub
- CrowdStrike Falcon API
- Microsoft Defender API
- Okta API
- Cloudflare API
- ServiceNow ITSM
- Elasticsearch
- Grafana

---

## 📚 API Documentation Links

- [PagerDuty Events API](https://developer.pagerduty.com/docs/ZG9jOjExMDI5NTgw-events-api-v2-overview)
- [Microsoft Teams Webhooks](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)
- [Discord Webhooks](https://discord.com/developers/docs/resources/webhook)
- [Datadog API](https://docs.datadoghq.com/api/latest/)
- [Splunk HEC](https://docs.splunk.com/Documentation/Splunk/latest/Data/UsetheHTTPEventCollector)
- [MITRE ATT&CK STIX](https://github.com/mitre/cti)
- [Jira Cloud API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- [VirusTotal API](https://docs.virustotal.com/reference/overview)
- [Prometheus Exporters](https://prometheus.io/docs/instrumenting/writing_exporters/)
- [Anthropic Claude API](https://docs.anthropic.com/en/api/getting-started)

---

## 📞 Support

For integration issues:
1. Check `.env` configuration
2. Verify API key validity
3. Review logs for error messages
4. Test individual integrations in isolation
5. Check rate limits on external services

---

**Last Updated:** 2025-11-15
**AEGIS Version:** 1.0.0
**Total API Integrations:** 12
**Claude API Reduction:** 90%
