"""
Signature Detector — Pattern matching against known attack signatures
"""

from typing import Dict, List, Any, Optional
import re
import json


class AttackSignature:
    """Represents a known attack signature."""

    def __init__(
        self,
        signature_id: str,
        name: str,
        patterns: List[str],
        severity: str,
        mitre_attack: str = None,
    ):
        """
        Initialize attack signature.

        Args:
            signature_id: Unique signature identifier
            name: Human-readable name
            patterns: List of regex patterns to match
            severity: Severity level (low, medium, high, critical)
            mitre_attack: MITRE ATT&CK technique ID
        """
        self.signature_id = signature_id
        self.name = name
        self.patterns = [re.compile(p, re.IGNORECASE) for p in patterns]
        self.severity = severity
        self.mitre_attack = mitre_attack


class SignatureDetector:
    """Detects attacks using signature-based pattern matching."""

    def __init__(self):
        """Initialize signature detector with attack signature database."""
        self.signatures: List[AttackSignature] = []
        self._load_default_signatures()

    def _load_default_signatures(self) -> None:
        """Load default attack signatures."""
        default_signatures = [
            AttackSignature(
                signature_id="SIG-001",
                name="SQL Injection",
                patterns=[
                    r"(\bunion\b.*\bselect\b)",
                    r"(\bdrop\b.*\btable\b)",
                    r"(1=1|1' OR '1'='1)",
                    r"(\bor\b.*=.*\bor\b)",
                ],
                severity="high",
                mitre_attack="T1190",
            ),
            AttackSignature(
                signature_id="SIG-002",
                name="XSS Attack",
                patterns=[
                    r"(<script[^>]*>.*?</script>)",
                    r"(javascript:)",
                    r"(onerror\s*=)",
                    r"(onload\s*=)",
                ],
                severity="high",
                mitre_attack="T1059",
            ),
            AttackSignature(
                signature_id="SIG-003",
                name="Command Injection",
                patterns=[
                    r"(;\s*(cat|ls|pwd|whoami|id)\b)",
                    r"(\|\s*(cat|ls|pwd|whoami|id)\b)",
                    r"(`.*`)",
                    r"(\$\(.*\))",
                ],
                severity="critical",
                mitre_attack="T1059.004",
            ),
            AttackSignature(
                signature_id="SIG-004",
                name="Path Traversal",
                patterns=[
                    r"(\.\./\.\./)",
                    r"(\.\.\\\.\.\\)",
                    r"(/etc/passwd)",
                    r"(c:\\windows\\)",
                ],
                severity="high",
                mitre_attack="T1083",
            ),
            AttackSignature(
                signature_id="SIG-005",
                name="Credential Stuffing",
                patterns=[
                    r"(admin:admin)",
                    r"(root:root)",
                    r"(test:test)",
                    r"(password123)",
                ],
                severity="high",
                mitre_attack="T1110.004",
            ),
            AttackSignature(
                signature_id="SIG-006",
                name="Remote Code Execution",
                patterns=[
                    r"(eval\s*\()",
                    r"(exec\s*\()",
                    r"(system\s*\()",
                    r"(shell_exec\s*\()",
                ],
                severity="critical",
                mitre_attack="T1203",
            ),
            AttackSignature(
                signature_id="SIG-007",
                name="LDAP Injection",
                patterns=[
                    r"(\*\)\(.*=)",
                    r"(admin\)\(|)",
                    r"(\)\(&)",
                ],
                severity="high",
                mitre_attack="T1078",
            ),
            AttackSignature(
                signature_id="SIG-008",
                name="XML External Entity (XXE)",
                patterns=[
                    r"(<!ENTITY.*SYSTEM)",
                    r"(<!DOCTYPE.*\[)",
                    r"(SYSTEM\s+[\"']file://)",
                ],
                severity="high",
                mitre_attack="T1203",
            ),
        ]

        self.signatures.extend(default_signatures)

    def add_signature(self, signature: AttackSignature) -> None:
        """
        Add a new attack signature.

        Args:
            signature: Attack signature to add
        """
        self.signatures.append(signature)

    def match_signatures(self, event: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Match event against all signatures.

        Args:
            event: Event to check

        Returns:
            List of matched signatures with details
        """
        matches = []

        # Extract searchable content from event
        content = self._extract_content(event)

        for signature in self.signatures:
            for pattern in signature.patterns:
                if pattern.search(content):
                    matches.append({
                        "signature_id": signature.signature_id,
                        "name": signature.name,
                        "severity": signature.severity,
                        "mitre_attack": signature.mitre_attack,
                        "matched_pattern": pattern.pattern,
                    })
                    break  # One match per signature is enough

        return matches

    def _extract_content(self, event: Dict[str, Any]) -> str:
        """
        Extract searchable content from event.

        Args:
            event: Event to extract from

        Returns:
            Combined string content
        """
        content_parts = []

        # Extract common fields
        for field in ["payload", "data", "request", "query", "path", "headers"]:
            if field in event:
                value = event[field]
                if isinstance(value, str):
                    content_parts.append(value)
                elif isinstance(value, dict):
                    content_parts.append(json.dumps(value))

        return " ".join(content_parts)

    def detect_signature_based_attack(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Detect signature-based attack in event.

        Args:
            event: Event to analyze

        Returns:
            Incident if signature matched, None otherwise
        """
        matches = self.match_signatures(event)

        if not matches:
            return None

        # Get highest severity match
        severity_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        highest_match = max(matches, key=lambda m: severity_order.get(m["severity"], 0))

        action = "kill" if highest_match["severity"] == "critical" else "quarantine"

        return {
            "threat_type": "signature_match",
            "action": action,
            "severity": highest_match["severity"],
            "reason": f"Attack signature matched: {highest_match['name']}",
            "signature_id": highest_match["signature_id"],
            "mitre_attack": highest_match["mitre_attack"],
            "all_matches": [m["name"] for m in matches],
        }

    def export_signatures(self, filepath: str) -> None:
        """
        Export signatures to JSON file.

        Args:
            filepath: Output file path
        """
        export_data = []
        for sig in self.signatures:
            export_data.append({
                "signature_id": sig.signature_id,
                "name": sig.name,
                "patterns": [p.pattern for p in sig.patterns],
                "severity": sig.severity,
                "mitre_attack": sig.mitre_attack,
            })

        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)

        print(f"✓ Exported {len(export_data)} signatures to {filepath}")
