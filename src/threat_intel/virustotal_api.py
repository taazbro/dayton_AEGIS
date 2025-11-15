"""
VirusTotal API Integration — Threat intelligence and IOC enrichment
"""

import os
import requests
from typing import Dict, Any, List
import json
import hashlib


class VirusTotalAPI:
    """Interface with VirusTotal for threat intelligence"""

    def __init__(self):
        self.api_key = os.getenv("VIRUSTOTAL_API_KEY")
        self.base_url = "https://www.virustotal.com/api/v3"

    def check_ip_reputation(self, ip_address: str) -> Dict[str, Any]:
        """
        Check IP address reputation.

        Args:
            ip_address: IP address to check

        Returns:
            Reputation data dictionary
        """
        if not self.api_key:
            return {"error": "API key not configured"}

        try:
            headers = {
                "x-apikey": self.api_key
            }

            response = requests.get(
                f"{self.base_url}/ip_addresses/{ip_address}",
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                attributes = data.get("data", {}).get("attributes", {})

                last_analysis = attributes.get("last_analysis_stats", {})

                return {
                    "ip": ip_address,
                    "malicious": last_analysis.get("malicious", 0),
                    "suspicious": last_analysis.get("suspicious", 0),
                    "harmless": last_analysis.get("harmless", 0),
                    "undetected": last_analysis.get("undetected", 0),
                    "reputation": attributes.get("reputation", 0),
                    "country": attributes.get("country", "Unknown"),
                    "as_owner": attributes.get("as_owner", "Unknown"),
                    "is_malicious": last_analysis.get("malicious", 0) > 0
                }
            else:
                return {"error": f"API error: {response.status_code}"}

        except Exception as e:
            return {"error": str(e)}

    def check_url_reputation(self, url: str) -> Dict[str, Any]:
        """
        Check URL reputation.

        Args:
            url: URL to check

        Returns:
            Reputation data dictionary
        """
        if not self.api_key:
            return {"error": "API key not configured"}

        try:
            # VirusTotal requires URL to be base64 encoded (without padding)
            url_id = self._url_to_id(url)

            headers = {
                "x-apikey": self.api_key
            }

            response = requests.get(
                f"{self.base_url}/urls/{url_id}",
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                attributes = data.get("data", {}).get("attributes", {})

                last_analysis = attributes.get("last_analysis_stats", {})

                return {
                    "url": url,
                    "malicious": last_analysis.get("malicious", 0),
                    "suspicious": last_analysis.get("suspicious", 0),
                    "harmless": last_analysis.get("harmless", 0),
                    "undetected": last_analysis.get("undetected", 0),
                    "categories": attributes.get("categories", {}),
                    "is_malicious": last_analysis.get("malicious", 0) > 0
                }
            elif response.status_code == 404:
                # URL not in database, submit for scanning
                return self._submit_url_for_scan(url)
            else:
                return {"error": f"API error: {response.status_code}"}

        except Exception as e:
            return {"error": str(e)}

    def check_file_hash(self, file_hash: str) -> Dict[str, Any]:
        """
        Check file hash reputation.

        Args:
            file_hash: MD5, SHA1, or SHA256 hash

        Returns:
            Reputation data dictionary
        """
        if not self.api_key:
            return {"error": "API key not configured"}

        try:
            headers = {
                "x-apikey": self.api_key
            }

            response = requests.get(
                f"{self.base_url}/files/{file_hash}",
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                attributes = data.get("data", {}).get("attributes", {})

                last_analysis = attributes.get("last_analysis_stats", {})

                return {
                    "hash": file_hash,
                    "malicious": last_analysis.get("malicious", 0),
                    "suspicious": last_analysis.get("suspicious", 0),
                    "harmless": last_analysis.get("harmless", 0),
                    "undetected": last_analysis.get("undetected", 0),
                    "file_type": attributes.get("type_description", "Unknown"),
                    "file_names": attributes.get("names", []),
                    "is_malicious": last_analysis.get("malicious", 0) > 0
                }
            else:
                return {"error": f"API error: {response.status_code}"}

        except Exception as e:
            return {"error": str(e)}

    def enrich_threat_report(self, threat_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich threat report with VirusTotal intelligence.

        Args:
            threat_report: Threat report dictionary

        Returns:
            Enriched threat report
        """
        incident = threat_report.get("incident_summary", {})

        # Extract IPs from affected entities
        affected_entities = incident.get("affected_entities", [])
        enriched_entities = []

        for entity in affected_entities[:5]:  # Limit to 5 to avoid rate limits
            # Check if entity looks like an IP
            if self._is_ip_address(entity):
                reputation = self.check_ip_reputation(entity)
                enriched_entities.append({
                    "entity": entity,
                    "type": "ip",
                    "reputation": reputation
                })
            else:
                enriched_entities.append({
                    "entity": entity,
                    "type": "unknown"
                })

        threat_report["enriched_entities"] = enriched_entities
        return threat_report

    def _url_to_id(self, url: str) -> str:
        """Convert URL to VirusTotal ID"""
        import base64
        url_bytes = url.encode('utf-8')
        url_base64 = base64.urlsafe_b64encode(url_bytes).decode('utf-8').rstrip('=')
        return url_base64

    def _submit_url_for_scan(self, url: str) -> Dict[str, Any]:
        """Submit URL for scanning"""
        try:
            headers = {
                "x-apikey": self.api_key
            }

            data = {
                "url": url
            }

            response = requests.post(
                f"{self.base_url}/urls",
                headers=headers,
                data=data,
                timeout=10
            )

            if response.status_code == 200:
                return {
                    "url": url,
                    "status": "submitted_for_scan",
                    "message": "URL submitted to VirusTotal for analysis"
                }
            else:
                return {"error": f"Scan submission failed: {response.status_code}"}

        except Exception as e:
            return {"error": str(e)}

    def _is_ip_address(self, entity: str) -> bool:
        """Check if string is an IP address"""
        parts = entity.split('.')
        if len(parts) != 4:
            return False
        try:
            return all(0 <= int(part) <= 255 for part in parts)
        except ValueError:
            return False


# Global instance
_virustotal_api = None


def get_virustotal_api() -> VirusTotalAPI:
    """Get singleton VirusTotal API instance"""
    global _virustotal_api
    if _virustotal_api is None:
        _virustotal_api = VirusTotalAPI()
    return _virustotal_api
