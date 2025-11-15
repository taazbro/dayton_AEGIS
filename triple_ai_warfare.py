"""
AEGIS Triple-AI Warfare System (3v3)
RED TEAM: Opus 4.1 + Sonnet 4.5 + Haiku 4.5 (Attackers)
BLUE TEAM: Opus 4.1 + Sonnet 4.5 + Haiku 4.5 (Defenders)
Using 100% realistic real-world attack scenarios
"""

import os
import sys
import time
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import anthropic
    CLAUDE_AVAILABLE = True
except:
    print("❌ Anthropic SDK not available")
    sys.exit(1)

try:
    import sentry_sdk
    from sentry_sdk import capture_message
except:
    pass

try:
    from galileo_observe import GalileoObserve
    from galileo_core.schemas.shared.workflows.node_type import NodeType
except:
    pass


# Real-world attack scenarios (100% realistic)
REAL_WORLD_ATTACKS = [
    {
        "name": "SolarWinds-style Supply Chain Attack",
        "description": "Compromise software update mechanism to inject malicious code into trusted applications",
        "real_example": "SolarWinds Orion attack (2020)",
        "severity": "CRITICAL"
    },
    {
        "name": "Log4Shell Remote Code Execution",
        "description": "Exploit Log4j vulnerability (CVE-2021-44228) for remote code execution",
        "real_example": "Log4Shell global exploit (2021)",
        "severity": "CRITICAL"
    },
    {
        "name": "Ransomware Double Extortion",
        "description": "Encrypt files + exfiltrate data, threaten to leak if ransom not paid",
        "real_example": "Colonial Pipeline attack (2021)",
        "severity": "CRITICAL"
    },
    {
        "name": "Business Email Compromise (BEC)",
        "description": "Spear phishing targeting executives to authorize fraudulent wire transfers",
        "real_example": "Toyota Boshoku Corporation $37M loss (2019)",
        "severity": "HIGH"
    },
    {
        "name": "Kerberoasting Active Directory Attack",
        "description": "Extract service account credentials from Active Directory for privilege escalation",
        "real_example": "Common enterprise network attack",
        "severity": "HIGH"
    },
    {
        "name": "DNS Tunneling Data Exfiltration",
        "description": "Use DNS queries to bypass firewall and exfiltrate sensitive data",
        "real_example": "APT groups common technique",
        "severity": "MEDIUM"
    },
    {
        "name": "Living off the Land (LOLBins)",
        "description": "Use legitimate system tools (PowerShell, WMI) to evade detection",
        "real_example": "Widespread APT technique",
        "severity": "HIGH"
    },
    {
        "name": "Golden Ticket Attack",
        "description": "Forge Kerberos TGT tickets for unlimited domain access",
        "real_example": "Advanced persistent threat technique",
        "severity": "CRITICAL"
    },
]


class TripleAIWarfare:
    """3v3 AI warfare: 3 Claudes attacking vs 3 Claudes defending"""

    def __init__(self):
        self.api_key = os.getenv("CLAUDE_API_KEY")
        if not self.api_key:
            print("❌ No CLAUDE_API_KEY found")
            sys.exit(1)

        self.client = anthropic.Anthropic(api_key=self.api_key)

        # Model configurations
        self.models = {
            "opus": "claude-opus-4-20250514",
            "sonnet": "claude-sonnet-4-5-20250929",
            "haiku": "claude-haiku-4-5-20250529"
        }

        # Stats
        self.red_team_attacks = {"opus": 0, "sonnet": 0, "haiku": 0}
        self.blue_team_defenses = {"opus": 0, "sonnet": 0, "haiku": 0}
        self.total_engagements = 0

        self.init_sponsors()

    def init_sponsors(self):
        """Initialize all sponsor integrations"""
        print("\n" + "="*80)
        print("🔧 INITIALIZING 3v3 AI WARFARE SYSTEM")
        print("="*80)

        # Sentry
        try:
            dsn = os.getenv("SENTRY_DSN")
            if dsn:
                sentry_sdk.init(dsn=dsn, environment="triple_ai_warfare")
                print("✅ Sentry: Combat monitoring enabled")
        except:
            pass

        # Galileo
        try:
            api_key = os.getenv("GALILEO_API_KEY")
            if api_key:
                self.galileo = GalileoObserve(project_name="AEGIS_3v3_WARFARE")
                print("✅ Galileo: Tracking all 6 AI combatants")
        except:
            self.galileo = None

        print(f"\n🔴 RED TEAM (Offensive):")
        print(f"   • Opus 4.1 - Strategic Attack Planning")
        print(f"   • Sonnet 4.5 - Tactical Attack Execution")
        print(f"   • Haiku 4.5 - Rapid Attack Variations")

        print(f"\n🔵 BLUE TEAM (Defensive):")
        print(f"   • Opus 4.1 - Strategic Defense Coordination")
        print(f"   • Sonnet 4.5 - Tactical Defense Response")
        print(f"   • Haiku 4.5 - Rapid Threat Mitigation")

    def red_team_attack(self, model_name, attack_scenario, role):
        """Red Team: Generate attack using specified model"""
        self.red_team_attacks[model_name] += 1

        prompt = f"""You are a RED TEAM offensive security AI ({role}).

MISSION: Generate a realistic attack based on this real-world scenario:
{json.dumps(attack_scenario, indent=2)}

Provide detailed attack plan in JSON:
{{
    "attack_vector": "specific attack method",
    "execution_steps": ["step1", "step2", "step3"],
    "payload_example": "realistic payload/exploit code",
    "evasion_tactics": ["tactic1", "tactic2"],
    "target_systems": ["system1", "system2"],
    "expected_impact": "detailed impact description",
    "difficulty": 1-10,
    "detection_likelihood": 1-10
}}

Make it 100% realistic based on actual APT tactics."""

        start_time = time.time()

        try:
            response = self.client.messages.create(
                model=self.models[model_name],
                max_tokens=1200,
                temperature=0.8,
                messages=[{"role": "user", "content": prompt}]
            )

            latency = (time.time() - start_time) * 1000
            content = response.content[0].text

            # Extract JSON
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                json_str = content.split("```")[1].split("```")[0].strip()
            else:
                json_str = content

            try:
                attack_data = json.loads(json_str)
            except:
                attack_data = {"error": "Failed to parse", "raw": content[:200]}

            # Log to Galileo
            if self.galileo:
                node_id = self.galileo.log_node_start(
                    node_type=NodeType.llm,
                    input_text=f"RED {model_name.upper()}: {attack_scenario['name']}",
                    model=self.models[model_name],
                    tags=["red-team", model_name, "attack"]
                )
                self.galileo.log_node_completion(
                    node_id=node_id,
                    output_text=json.dumps(attack_data, indent=2)[:500],
                    status_code=200
                )

            return {
                "model": model_name,
                "role": role,
                "response_id": response.id,
                "latency_ms": latency,
                "attack_data": attack_data,
                "tokens": response.usage.input_tokens + response.usage.output_tokens
            }

        except Exception as e:
            return {"model": model_name, "error": str(e)}

    def blue_team_defend(self, model_name, attack_data, role):
        """Blue Team: Generate defense using specified model"""
        self.blue_team_defenses[model_name] += 1

        prompt = f"""You are a BLUE TEAM defensive security AI ({role}).

THREAT DETECTED:
Scenario: {attack_data['scenario']['name']}
Attack Details: {json.dumps(attack_data.get('attack_data', {}), indent=2)[:500]}

Provide comprehensive defense strategy in JSON:
{{
    "threat_assessment": "critical analysis of the threat",
    "immediate_actions": ["action1", "action2", "action3"],
    "detection_methods": ["method1", "method2"],
    "mitigation_steps": ["step1", "step2", "step3"],
    "long_term_hardening": ["measure1", "measure2"],
    "effectiveness_rating": 1-10,
    "response_priority": "HIGH/MEDIUM/LOW",
    "threat_neutralized": true/false
}}

Use industry best practices and real defensive techniques."""

        start_time = time.time()

        try:
            response = self.client.messages.create(
                model=self.models[model_name],
                max_tokens=1200,
                temperature=0.4,
                messages=[{"role": "user", "content": prompt}]
            )

            latency = (time.time() - start_time) * 1000
            content = response.content[0].text

            # Extract JSON
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                json_str = content.split("```")[1].split("```")[0].strip()
            else:
                json_str = content

            try:
                defense_data = json.loads(json_str)
            except:
                defense_data = {"error": "Failed to parse", "raw": content[:200]}

            # Log to Galileo
            if self.galileo:
                node_id = self.galileo.log_node_start(
                    node_type=NodeType.llm,
                    input_text=f"BLUE {model_name.upper()}: Defending {attack_data['scenario']['name']}",
                    model=self.models[model_name],
                    tags=["blue-team", model_name, "defense"]
                )
                self.galileo.log_node_completion(
                    node_id=node_id,
                    output_text=json.dumps(defense_data, indent=2)[:500],
                    status_code=200
                )

            # Log to Sentry
            try:
                neutralized = defense_data.get('threat_neutralized', False)
                capture_message(
                    f"🛡️ BLUE {model_name.upper()}: {attack_data['scenario']['name']} - {'NEUTRALIZED' if neutralized else 'MITIGATING'}",
                    level="info"
                )
            except:
                pass

            return {
                "model": model_name,
                "role": role,
                "response_id": response.id,
                "latency_ms": latency,
                "defense_data": defense_data,
                "tokens": response.usage.input_tokens + response.usage.output_tokens
            }

        except Exception as e:
            return {"model": model_name, "error": str(e)}

    def run_3v3_engagement(self, engagement_num, attack_scenario):
        """Run full 3v3 engagement"""
        self.total_engagements += 1

        timestamp = datetime.now().strftime("%H:%M:%S")

        print(f"\n{'='*80}")
        print(f"⚔️  ENGAGEMENT #{engagement_num} @ {timestamp}")
        print(f"{'='*80}")
        print(f"🎯 SCENARIO: {attack_scenario['name']}")
        print(f"📋 Based on: {attack_scenario['real_example']}")
        print(f"⚠️  Severity: {attack_scenario['severity']}")

        # PHASE 1: RED TEAM ATTACKS (All 3 models in parallel)
        print(f"\n{'─'*80}")
        print(f"🔴 PHASE 1: RED TEAM OFFENSIVE (3 AI attackers)")
        print(f"{'─'*80}")

        red_team_roles = {
            "opus": "Strategic Attack Planner",
            "sonnet": "Tactical Attack Executor",
            "haiku": "Rapid Attack Generator"
        }

        red_results = {}
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(self.red_team_attack, model, attack_scenario, role): model
                for model, role in red_team_roles.items()
            }

            for future in as_completed(futures):
                model = futures[future]
                result = future.result()
                red_results[model] = result
                if "error" not in result:
                    print(f"   🔴 {model.upper():7} ({result['role']})")
                    print(f"      ⏱️  {result['latency_ms']:.0f}ms | 🎯 ID: {result['response_id'][:20]}...")

        time.sleep(0.5)

        # PHASE 2: BLUE TEAM DEFENSES (All 3 models in parallel)
        print(f"\n{'─'*80}")
        print(f"🔵 PHASE 2: BLUE TEAM DEFENSIVE (3 AI defenders)")
        print(f"{'─'*80}")

        blue_team_roles = {
            "opus": "Strategic Defense Coordinator",
            "sonnet": "Tactical Defense Responder",
            "haiku": "Rapid Threat Mitigator"
        }

        # Prepare attack data for defenders
        attack_data = {
            "scenario": attack_scenario,
            "red_team_attacks": red_results
        }

        blue_results = {}
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(self.blue_team_defend, model, attack_data, role): model
                for model, role in blue_team_roles.items()
            }

            for future in as_completed(futures):
                model = futures[future]
                result = future.result()
                blue_results[model] = result
                if "error" not in result:
                    neutralized = result['defense_data'].get('threat_neutralized', False)
                    status = "✅ NEUTRALIZED" if neutralized else "⚠️ MITIGATING"
                    print(f"   🔵 {model.upper():7} ({result['role']})")
                    print(f"      ⏱️  {result['latency_ms']:.0f}ms | {status}")

        # Calculate outcome
        neutralized_count = sum(
            1 for r in blue_results.values()
            if r.get('defense_data', {}).get('threat_neutralized', False)
        )

        print(f"\n{'─'*80}")
        print(f"📊 ENGAGEMENT OUTCOME")
        print(f"{'─'*80}")
        print(f"   Defense Success: {neutralized_count}/3 AI defenders neutralized threat")

        if neutralized_count >= 2:
            print(f"   🛡️  RESULT: BLUE TEAM VICTORY - Threat contained")
            outcome = "BLUE_WIN"
        elif neutralized_count == 1:
            print(f"   ⚔️  RESULT: CONTESTED - Partial defense")
            outcome = "CONTESTED"
        else:
            print(f"   🔴 RESULT: RED TEAM BREAKTHROUGH - Defense penetrated")
            outcome = "RED_WIN"

        # Log to Sentry
        try:
            capture_message(
                f"⚔️ 3v3 Engagement: {attack_scenario['name']} - {outcome}",
                level="warning" if outcome == "RED_WIN" else "info"
            )
        except:
            pass

        return {
            "engagement_num": engagement_num,
            "scenario": attack_scenario,
            "red_results": red_results,
            "blue_results": blue_results,
            "outcome": outcome,
            "neutralized_count": neutralized_count
        }


def main():
    print("\n" + "="*80)
    print("⚔️  AEGIS 3v3 AI WARFARE SYSTEM")
    print("="*80)
    print("\n🔴 RED TEAM: Opus 4.1 + Sonnet 4.5 + Haiku 4.5 (Attackers)")
    print("🔵 BLUE TEAM: Opus 4.1 + Sonnet 4.5 + Haiku 4.5 (Defenders)")
    print("\n🎯 Using 100% realistic real-world attack scenarios")
    print("📡 All operations logged to Sentry + Galileo\n")

    warfare = TripleAIWarfare()

    print("\n" + "="*80)
    print("🚀 LAUNCHING 3v3 WARFARE - 5 REAL-WORLD SCENARIOS")
    print("="*80)

    start_time = time.time()
    results = []

    # Run first 5 scenarios
    for i, scenario in enumerate(REAL_WORLD_ATTACKS[:5], 1):
        result = warfare.run_3v3_engagement(i, scenario)
        results.append(result)
        time.sleep(1)  # Brief pause between engagements

    elapsed = time.time() - start_time

    # FINAL SUMMARY
    print("\n\n" + "="*80)
    print("📊 3v3 WARFARE FINAL SUMMARY")
    print("="*80)

    blue_wins = sum(1 for r in results if r['outcome'] == 'BLUE_WIN')
    red_wins = sum(1 for r in results if r['outcome'] == 'RED_WIN')
    contested = sum(1 for r in results if r['outcome'] == 'CONTESTED')

    print(f"\n⚔️  Total Engagements: {len(results)}")
    print(f"🔴 Red Team Wins: {red_wins}")
    print(f"🔵 Blue Team Wins: {blue_wins}")
    print(f"⚖️  Contested: {contested}")
    print(f"\n🎯 Blue Team Defense Rate: {blue_wins/len(results)*100:.0f}%")

    total_red = sum(warfare.red_team_attacks.values())
    total_blue = sum(warfare.blue_team_defenses.values())

    print(f"\n📊 AI Operations:")
    print(f"   Red Team Attacks: {total_red} (Opus: {warfare.red_team_attacks['opus']}, Sonnet: {warfare.red_team_attacks['sonnet']}, Haiku: {warfare.red_team_attacks['haiku']})")
    print(f"   Blue Team Defenses: {total_blue} (Opus: {warfare.blue_team_defenses['opus']}, Sonnet: {warfare.blue_team_defenses['sonnet']}, Haiku: {warfare.blue_team_defenses['haiku']})")

    print(f"\n⏱️  Total Time: {elapsed:.2f} seconds")

    print("\n" + "="*80)
    print("📡 SPONSOR VERIFICATION")
    print("="*80)
    print(f"\n🚨 SENTRY: https://sentry.io/")
    print(f"   • Environment: 'triple_ai_warfare'")
    print(f"   • View all {len(results)} engagement outcomes")

    print(f"\n🔭 GALILEO: https://app.galileo.ai/")
    print(f"   • Project: 'AEGIS_3v3_WARFARE'")
    print(f"   • {total_red} red-team attack nodes")
    print(f"   • {total_blue} blue-team defense nodes")
    print(f"   • Filter by tags: 'red-team', 'blue-team'")

    print("\n" + "="*80)
    print("✅ 3v3 AI WARFARE COMPLETE - ALL DATA IN SPONSORS")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
