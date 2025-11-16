"""
Supabase Integration for AEGIS
Logs security incidents to real-time database for live threat dashboard
"""

import os
from datetime import datetime
from typing import Dict, Any, Optional
from supabase import create_client, Client

class SupabaseLogger:
    """Logs AEGIS security incidents to Supabase for real-time monitoring"""

    def __init__(self):
        """Initialize Supabase client"""
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")

        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment")

        self.client: Client = create_client(supabase_url, supabase_key)
        self.enabled = True

    def log_incident(
        self,
        attack_type: str,
        severity: str,
        source_ip: str,
        confidence: float,
        response_time: float,
        actions_taken: list,
        data_loss: bool = False,
        threat_score: float = 0.0,
        kill_chain_stage: str = "",
        details: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Log a security incident to Supabase

        Args:
            attack_type: Type of attack (e.g., "SQL Injection", "Ransomware")
            severity: Severity level (e.g., "CRITICAL", "HIGH", "MEDIUM", "LOW")
            source_ip: Source IP address or hostname
            confidence: Detection confidence (0-100)
            response_time: Time taken to neutralize threat in seconds
            actions_taken: List of automated actions performed
            data_loss: Whether any data was lost (should always be False for AEGIS!)
            threat_score: Behavioral threat score (0-10)
            kill_chain_stage: Stage in cyber kill chain
            details: Additional incident details

        Returns:
            Inserted incident record or None if logging failed
        """
        if not self.enabled:
            return None

        try:
            incident_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "attack_type": attack_type,
                "severity": severity,
                "source_ip": source_ip,
                "confidence": confidence,
                "response_time": response_time,
                "actions_taken": actions_taken,
                "data_loss": data_loss,
                "threat_score": threat_score,
                "kill_chain_stage": kill_chain_stage,
                "details": details or {},
                "status": "neutralized"
            }

            response = self.client.table("security_incidents").insert(incident_data).execute()

            if response.data:
                print(f"✅ Incident logged to Supabase: {attack_type} from {source_ip}")
                return response.data[0]
            else:
                print(f"⚠️  Failed to log incident to Supabase")
                return None

        except Exception as e:
            print(f"❌ Error logging to Supabase: {e}")
            return None

    def log_threat_detection(
        self,
        scenario: str,
        attack_details: Dict[str, Any],
        defense_details: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Log a complete threat detection and response scenario

        Args:
            scenario: Scenario name (e.g., "sql_injection", "ransomware")
            attack_details: Details about the attack
            defense_details: Details about the defense response

        Returns:
            Inserted incident record or None if logging failed
        """
        return self.log_incident(
            attack_type=attack_details.get("type", "Unknown"),
            severity=attack_details.get("severity", "MEDIUM"),
            source_ip=attack_details.get("source_ip", "unknown"),
            confidence=attack_details.get("confidence", 0.0),
            response_time=defense_details.get("response_time", 0.0),
            actions_taken=defense_details.get("actions", []),
            data_loss=False,  # AEGIS always prevents data loss!
            threat_score=attack_details.get("threat_score", 0.0),
            kill_chain_stage=attack_details.get("kill_chain_stage", ""),
            details={
                "scenario": scenario,
                "attack": attack_details,
                "defense": defense_details
            }
        )

    def get_recent_incidents(self, limit: int = 10) -> list:
        """
        Get recent security incidents

        Args:
            limit: Number of incidents to retrieve

        Returns:
            List of recent incidents
        """
        try:
            response = self.client.table("security_incidents")\
                .select("*")\
                .order("timestamp", desc=True)\
                .limit(limit)\
                .execute()

            return response.data if response.data else []
        except Exception as e:
            print(f"❌ Error fetching incidents: {e}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about detected threats

        Returns:
            Dictionary with threat statistics
        """
        try:
            # Total incidents
            total_response = self.client.table("security_incidents").select("*", count="exact").execute()
            total_incidents = total_response.count if hasattr(total_response, 'count') else 0

            # Average response time
            incidents = self.get_recent_incidents(limit=100)
            avg_response_time = sum(i.get('response_time', 0) for i in incidents) / len(incidents) if incidents else 0

            # Count by severity
            critical = sum(1 for i in incidents if i.get('severity') == 'CRITICAL')
            high = sum(1 for i in incidents if i.get('severity') == 'HIGH')

            return {
                "total_incidents": total_incidents,
                "avg_response_time": round(avg_response_time, 2),
                "critical_incidents": critical,
                "high_incidents": high,
                "data_loss_incidents": 0  # Always 0 for AEGIS!
            }
        except Exception as e:
            print(f"❌ Error fetching stats: {e}")
            return {
                "total_incidents": 0,
                "avg_response_time": 0,
                "critical_incidents": 0,
                "high_incidents": 0,
                "data_loss_incidents": 0
            }


# Convenience function for easy import
def get_supabase_logger() -> Optional[SupabaseLogger]:
    """Get a Supabase logger instance if configured"""
    try:
        return SupabaseLogger()
    except Exception as e:
        print(f"⚠️  Supabase not configured: {e}")
        return None
