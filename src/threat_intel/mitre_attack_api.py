"""
MITRE ATT&CK API Integration — Real-time technique lookups and enrichment
"""

import os
import requests
from typing import Dict, Any, List
import json


class MITREAttackAPI:
    """Interface with MITRE ATT&CK framework for technique enrichment"""

    def __init__(self):
        # MITRE ATT&CK TAXII server
        self.api_root = "https://cti-taxii.mitre.org/taxii/"
        self.collection_id = "95ecc380-afe9-11e4-9b6c-751b66dd541e"  # Enterprise ATT&CK
        self.stix_url = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

        # Cache for technique data
        self._technique_cache = {}
        self._cache_loaded = False

    def enrich_technique(self, technique_id: str) -> Dict[str, Any]:
        """
        Enrich a MITRE ATT&CK technique with full details.

        Args:
            technique_id: Technique ID (e.g., "T1190", "T1566.001")

        Returns:
            Dictionary with technique details
        """
        if not self._cache_loaded:
            self._load_techniques()

        technique_id = technique_id.upper()

        if technique_id in self._technique_cache:
            return self._technique_cache[technique_id]

        # If not in cache, try to fetch from API
        try:
            return self._fetch_technique_from_api(technique_id)
        except Exception as e:
            print(f"⚠️  MITRE ATT&CK API error: {e}")
            return self._get_fallback_technique(technique_id)

    def _load_techniques(self):
        """Load MITRE ATT&CK techniques from STIX data"""
        try:
            response = requests.get(self.stix_url, timeout=10)
            if response.status_code == 200:
                stix_data = response.json()

                # Parse techniques from STIX bundle
                for obj in stix_data.get("objects", []):
                    if obj.get("type") == "attack-pattern":
                        external_refs = obj.get("external_references", [])
                        for ref in external_refs:
                            if ref.get("source_name") == "mitre-attack":
                                technique_id = ref.get("external_id")
                                if technique_id:
                                    self._technique_cache[technique_id] = {
                                        "id": technique_id,
                                        "name": obj.get("name"),
                                        "description": obj.get("description", ""),
                                        "tactics": [phase.get("phase_name") for phase in obj.get("kill_chain_phases", [])],
                                        "url": ref.get("url", ""),
                                        "platforms": obj.get("x_mitre_platforms", []),
                                        "data_sources": obj.get("x_mitre_data_sources", []),
                                        "detection": obj.get("x_mitre_detection", ""),
                                    }

                self._cache_loaded = True
                print(f"✅ Loaded {len(self._technique_cache)} MITRE ATT&CK techniques")
        except Exception as e:
            print(f"⚠️  Failed to load MITRE techniques: {e}")
            self._cache_loaded = False

    def _fetch_technique_from_api(self, technique_id: str) -> Dict[str, Any]:
        """Fetch technique details from MITRE API"""
        # Fallback to static data if API unavailable
        return self._get_fallback_technique(technique_id)

    def _get_fallback_technique(self, technique_id: str) -> Dict[str, Any]:
        """Return basic technique info when API unavailable"""
        # Static mapping of common techniques
        fallback_techniques = {
            "T1190": {
                "id": "T1190",
                "name": "Exploit Public-Facing Application",
                "description": "Adversaries may attempt to exploit a weakness in an Internet-facing host.",
                "tactics": ["initial-access"],
                "url": "https://attack.mitre.org/techniques/T1190/",
                "platforms": ["Linux", "Windows", "macOS"],
                "data_sources": ["Application Log", "Web Application Firewall Logs"],
                "detection": "Monitor application logs for suspicious activity."
            },
            "T1566": {
                "id": "T1566",
                "name": "Phishing",
                "description": "Adversaries may send phishing messages to gain access.",
                "tactics": ["initial-access"],
                "url": "https://attack.mitre.org/techniques/T1566/",
                "platforms": ["Linux", "Windows", "macOS"],
                "data_sources": ["Email Gateway", "Email Server"],
                "detection": "Monitor for suspicious email patterns."
            },
            "T1078": {
                "id": "T1078",
                "name": "Valid Accounts",
                "description": "Adversaries may obtain and use valid accounts.",
                "tactics": ["defense-evasion", "persistence", "privilege-escalation", "initial-access"],
                "url": "https://attack.mitre.org/techniques/T1078/",
                "platforms": ["Linux", "Windows", "macOS", "Azure AD"],
                "data_sources": ["Authentication logs"],
                "detection": "Monitor authentication logs for unusual patterns."
            },
            "T1098": {
                "id": "T1098",
                "name": "Account Manipulation",
                "description": "Adversaries may manipulate accounts to maintain access.",
                "tactics": ["persistence"],
                "url": "https://attack.mitre.org/techniques/T1098/",
                "platforms": ["Windows", "Azure AD", "Office 365"],
                "data_sources": ["Authentication logs"],
                "detection": "Monitor for unexpected account modifications."
            },
            "T1046": {
                "id": "T1046",
                "name": "Network Service Discovery",
                "description": "Adversaries may attempt to discover services.",
                "tactics": ["discovery"],
                "url": "https://attack.mitre.org/techniques/T1046/",
                "platforms": ["Linux", "Windows", "macOS"],
                "data_sources": ["Network Traffic", "Packet Capture"],
                "detection": "Monitor for port scanning activity."
            }
        }

        return fallback_techniques.get(technique_id, {
            "id": technique_id,
            "name": "Unknown Technique",
            "description": f"Technique {technique_id} not in local cache.",
            "tactics": ["unknown"],
            "url": f"https://attack.mitre.org/techniques/{technique_id}/",
            "platforms": [],
            "data_sources": [],
            "detection": ""
        })

    def enrich_threat_report(self, threat_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich threat report with detailed MITRE ATT&CK data.

        Args:
            threat_report: Threat report dictionary

        Returns:
            Enriched threat report
        """
        mitre_tags = threat_report.get("mitre_tags", [])

        enriched_tags = []
        for tag in mitre_tags:
            technique_id = tag.get("technique", "")
            if technique_id:
                enriched_data = self.enrich_technique(technique_id)
                enriched_tag = {
                    **tag,
                    "technique_name": enriched_data.get("name"),
                    "description": enriched_data.get("description"),
                    "url": enriched_data.get("url"),
                    "platforms": enriched_data.get("platforms", []),
                    "detection": enriched_data.get("detection", "")
                }
                enriched_tags.append(enriched_tag)

        threat_report["mitre_tags"] = enriched_tags
        return threat_report


# Global instance
_mitre_api = None


def get_mitre_api() -> MITREAttackAPI:
    """Get singleton MITRE ATT&CK API instance"""
    global _mitre_api
    if _mitre_api is None:
        _mitre_api = MITREAttackAPI()
    return _mitre_api
