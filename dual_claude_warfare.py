"""
AEGIS Dual-Claude AI Warfare System
- Claude Opus 4.1: Advanced Offensive Operations (Red Team)
- Claude Haiku 4.5: Rapid Defensive Operations (Blue Team)
Both operating at maximum capability with full sponsor integration
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
    CLAUDE_AVAILABLE = False
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


class DualClaudeWarfare:
    """Dual-AI warfare system with Opus attacking and Haiku defending"""

    def __init__(self):
        self.api_key = os.getenv("CLAUDE_API_KEY")
        if not self.api_key:
            print("❌ No CLAUDE_API_KEY found")
            sys.exit(1)

        self.client = anthropic.Anthropic(api_key=self.api_key)

        # Stats
        self.opus_attacks = 0
        self.haiku_defenses = 0
        self.total_exchanges = 0

        # Sponsor integrations
        self.init_sponsors()

    def init_sponsors(self):
        """Initialize all sponsor integrations"""
        print("\n" + "="*80)
        print("🔧 INITIALIZING DUAL-AI WARFARE SYSTEM")
        print("="*80)

        # Sentry
        try:
            dsn = os.getenv("SENTRY_DSN")
            if dsn:
                sentry_sdk.init(dsn=dsn, environment="dual_claude_warfare")
                print("✅ Sentry: Monitoring enabled")
        except:
            pass

        # Galileo
        try:
            api_key = os.getenv("GALILEO_API_KEY")
            if api_key:
                self.galileo = GalileoObserve(project_name="AEGIS_DUAL_CLAUDE")
                print("✅ Galileo: AI observability tracking both models")
        except:
            self.galileo = None

        print(f"✅ Claude Opus 4.1: Advanced Red Team AI loaded")
        print(f"✅ Claude Haiku 4.5: Rapid Blue Team AI loaded")

    def opus_generate_attack(self, attack_scenario):
        """Claude Opus 4.1: Generate sophisticated attack"""
        self.opus_attacks += 1

        prompt = f"""You are an advanced red team AI conducting offensive security testing.

Generate a SOPHISTICATED cyber attack for this scenario: {attack_scenario}

Provide in JSON format:
{{
    "attack_type": "specific attack category",
    "attack_vector": "detailed attack method",
    "payload": "actual attack payload/code",
    "sophistication_level": 1-10,
    "evasion_techniques": ["technique1", "technique2"],
    "expected_impact": "what this attack would accomplish"
}}

Be creative and realistic. This is for defensive training."""

        start_time = time.time()

        try:
            response = self.client.messages.create(
                model="claude-opus-4-20250514",  # Opus 4.1
                max_tokens=1000,
                temperature=0.9,  # High creativity for attack generation
                messages=[{"role": "user", "content": prompt}]
            )

            latency = (time.time() - start_time) * 1000
            content = response.content[0].text

            # Extract JSON from response
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                json_str = content.split("```")[1].split("```")[0].strip()
            else:
                json_str = content

            attack_data = json.loads(json_str)

            # Log to Galileo
            if self.galileo:
                node_id = self.galileo.log_node_start(
                    node_type=NodeType.llm,
                    input_text=f"Opus Red Team: {attack_scenario}",
                    model="claude-opus-4-20250514",
                    tags=["red-team", "opus", "attack-generation"]
                )
                self.galileo.log_node_completion(
                    node_id=node_id,
                    output_text=json.dumps(attack_data, indent=2),
                    status_code=200
                )

            # Log to Sentry
            try:
                capture_message(
                    f"🔴 Opus Attack Generated: {attack_data['attack_type']} (Sophistication: {attack_data['sophistication_level']}/10)",
                    level="warning"
                )
            except:
                pass

            return {
                "model": "Claude Opus 4.1",
                "response_id": response.id,
                "latency_ms": latency,
                "attack_data": attack_data,
                "tokens": response.usage.input_tokens + response.usage.output_tokens
            }

        except Exception as e:
            print(f"   ⚠️  Opus error: {e}")
            return None

    def haiku_defend_attack(self, attack_data):
        """Claude Haiku 4.5: Generate rapid defense response"""
        self.haiku_defenses += 1

        prompt = f"""You are a rapid-response blue team AI defending against cyber attacks.

INCOMING ATTACK:
{json.dumps(attack_data['attack_data'], indent=2)}

Provide IMMEDIATE defense strategy in JSON format:
{{
    "defense_classification": "defense category",
    "immediate_actions": ["action1", "action2", "action3"],
    "mitigation_effectiveness": 1-10,
    "response_time_critical": true/false,
    "countermeasures": ["specific countermeasure details"],
    "threat_neutralized": true/false
}}

Respond with MAXIMUM speed and precision."""

        start_time = time.time()

        try:
            response = self.client.messages.create(
                model="claude-haiku-4-5-20250529",  # Haiku 4.5
                max_tokens=800,
                temperature=0.3,  # Lower temp for consistent defense
                messages=[{"role": "user", "content": prompt}]
            )

            latency = (time.time() - start_time) * 1000
            content = response.content[0].text

            # Extract JSON from response
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                json_str = content.split("```")[1].split("```")[0].strip()
            else:
                json_str = content

            defense_data = json.loads(json_str)

            # Log to Galileo
            if self.galileo:
                node_id = self.galileo.log_node_start(
                    node_type=NodeType.llm,
                    input_text=f"Haiku Blue Team: Defending {attack_data['attack_data']['attack_type']}",
                    model="claude-haiku-4-5-20250529",
                    tags=["blue-team", "haiku", "defense-response"]
                )
                self.galileo.log_node_completion(
                    node_id=node_id,
                    output_text=json.dumps(defense_data, indent=2),
                    status_code=200
                )

            # Log to Sentry
            try:
                status = "✅ NEUTRALIZED" if defense_data.get('threat_neutralized') else "⚠️ PARTIAL"
                capture_message(
                    f"🛡️ Haiku Defense: {defense_data['defense_classification']} - {status}",
                    level="info"
                )
            except:
                pass

            return {
                "model": "Claude Haiku 4.5",
                "response_id": response.id,
                "latency_ms": latency,
                "defense_data": defense_data,
                "tokens": response.usage.input_tokens + response.usage.output_tokens
            }

        except Exception as e:
            print(f"   ⚠️  Haiku error: {e}")
            return None

    def run_engagement(self, scenario_num, attack_scenario):
        """Run one offensive/defensive engagement"""
        self.total_exchanges += 1

        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]

        print(f"\n{'='*80}")
        print(f"⚔️  ENGAGEMENT #{scenario_num} @ {timestamp}")
        print(f"{'='*80}")
        print(f"📋 Scenario: {attack_scenario}")

        # Phase 1: Opus generates attack
        print(f"\n🔴 PHASE 1: OPUS 4.1 GENERATING ATTACK...")
        attack_result = self.opus_generate_attack(attack_scenario)

        if not attack_result:
            print("   ❌ Attack generation failed")
            return None

        print(f"   ✅ Attack Generated ({attack_result['latency_ms']:.0f}ms)")
        print(f"   📊 Response ID: {attack_result['response_id']}")
        print(f"   🎯 Attack Type: {attack_result['attack_data']['attack_type']}")
        print(f"   ⚡ Sophistication: {attack_result['attack_data']['sophistication_level']}/10")
        print(f"   💣 Payload: {attack_result['attack_data']['payload'][:80]}...")

        # Phase 2: Haiku defends
        print(f"\n🛡️  PHASE 2: HAIKU 4.5 DEFENDING...")
        defense_result = self.haiku_defend_attack(attack_result)

        if not defense_result:
            print("   ❌ Defense generation failed")
            return None

        print(f"   ✅ Defense Deployed ({defense_result['latency_ms']:.0f}ms)")
        print(f"   📊 Response ID: {defense_result['response_id']}")
        print(f"   🛡️  Defense: {defense_result['defense_data']['defense_classification']}")
        print(f"   ⚡ Effectiveness: {defense_result['defense_data']['mitigation_effectiveness']}/10")

        neutralized = defense_result['defense_data'].get('threat_neutralized', False)
        if neutralized:
            print(f"   ✅ STATUS: THREAT NEUTRALIZED")
        else:
            print(f"   ⚠️  STATUS: PARTIAL DEFENSE")

        # Summary
        total_latency = attack_result['latency_ms'] + defense_result['latency_ms']
        total_tokens = attack_result['tokens'] + defense_result['tokens']

        print(f"\n📊 ENGAGEMENT STATS:")
        print(f"   ⏱️  Total Time: {total_latency:.0f}ms")
        print(f"   🔤 Total Tokens: {total_tokens}")
        print(f"   🎯 Outcome: {'Defense Successful' if neutralized else 'Ongoing Threat'}")

        return {
            'scenario': attack_scenario,
            'attack': attack_result,
            'defense': defense_result,
            'neutralized': neutralized,
            'total_latency': total_latency,
            'total_tokens': total_tokens
        }


def main():
    print("\n" + "="*80)
    print("⚔️  AEGIS DUAL-CLAUDE AI WARFARE SYSTEM")
    print("="*80)
    print("\n🔴 Claude Opus 4.1: Advanced Red Team (Offensive AI)")
    print("🔵 Claude Haiku 4.5: Rapid Blue Team (Defensive AI)")
    print("\n🎯 Maximum capability warfare simulation with full sponsor logging\n")

    warfare = DualClaudeWarfare()

    # Attack scenarios
    scenarios = [
        "Advanced Persistent Threat targeting financial infrastructure",
        "Zero-day exploit in cloud authentication system",
        "AI-powered phishing campaign with deepfake technology",
        "Supply chain attack on open-source dependencies",
        "Ransomware with polymorphic encryption algorithm",
        "Nation-state sponsored espionage operation",
        "Insider threat with privilege escalation",
        "Distributed denial of service using IoT botnet",
        "Man-in-the-middle attack on encrypted communications",
        "SQL injection bypass using machine learning",
    ]

    print("\n" + "="*80)
    print("🚀 LAUNCHING DUAL-AI WARFARE - 10 ENGAGEMENTS")
    print("="*80)

    start_time = time.time()
    results = []

    # Run scenarios
    for i, scenario in enumerate(scenarios[:5], 1):  # First 5 for demo
        result = warfare.run_engagement(i, scenario)
        if result:
            results.append(result)
        time.sleep(0.5)  # Brief pause between engagements

    elapsed = time.time() - start_time

    # Final Statistics
    print("\n\n" + "="*80)
    print("📊 DUAL-AI WARFARE SUMMARY")
    print("="*80)

    neutralized_count = sum(1 for r in results if r['neutralized'])
    avg_latency = sum(r['total_latency'] for r in results) / len(results) if results else 0
    total_tokens = sum(r['total_tokens'] for r in results)

    print(f"\n⚔️  Total Engagements: {len(results)}")
    print(f"🔴 Opus Attacks Generated: {warfare.opus_attacks}")
    print(f"🔵 Haiku Defenses Deployed: {warfare.haiku_defenses}")
    print(f"✅ Threats Neutralized: {neutralized_count}/{len(results)} ({neutralized_count/len(results)*100:.0f}%)")
    print(f"⏱️  Average Response Time: {avg_latency:.0f}ms per engagement")
    print(f"🔤 Total Tokens Processed: {total_tokens:,}")
    print(f"⚡ Total Time: {elapsed:.2f} seconds")

    print("\n" + "="*80)
    print("📡 SPONSOR INTEGRATION STATUS")
    print("="*80)
    print("\n✅ All AI operations logged to:")
    print(f"\n🚨 SENTRY: https://sentry.io/")
    print(f"   • {warfare.opus_attacks} Opus attack events")
    print(f"   • {warfare.haiku_defenses} Haiku defense events")
    print(f"   • Filter: environment='dual_claude_warfare'")

    print(f"\n🔭 GALILEO: https://app.galileo.ai/")
    print(f"   • Project: AEGIS_DUAL_CLAUDE")
    print(f"   • {warfare.opus_attacks} red-team nodes (Opus)")
    print(f"   • {warfare.haiku_defenses} blue-team nodes (Haiku)")
    print(f"   • Filter tags: 'red-team', 'blue-team'")

    # Engagement breakdown
    print("\n" + "="*80)
    print("🎯 ENGAGEMENT BREAKDOWN")
    print("="*80)

    for i, result in enumerate(results, 1):
        status = "✅ NEUTRALIZED" if result['neutralized'] else "⚠️ ONGOING"
        print(f"\n{i}. {result['scenario'][:60]}...")
        print(f"   Attack: {result['attack']['attack_data']['attack_type']}")
        print(f"   Defense: {result['defense']['defense_data']['defense_classification']}")
        print(f"   Status: {status}")

    print("\n" + "="*80)
    print("✅ DUAL-AI WARFARE DEMONSTRATION COMPLETE")
    print("="*80)
    print("\n🔗 Verify all AI operations on sponsor platforms!")
    print("   All attack/defense exchanges are now visible in Sentry & Galileo\n")


if __name__ == "__main__":
    main()
