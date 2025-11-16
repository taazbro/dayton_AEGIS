#!/usr/bin/env python3
"""
Test Supabase Integration
Verifies that AEGIS can log incidents to Supabase real-time database
"""

import os
from dotenv import load_dotenv
load_dotenv()

# First install the package
import subprocess
import sys

print("📦 Installing supabase package...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "supabase==2.12.0"])

from src.integrations.supabase_integration import SupabaseLogger

def test_supabase_connection():
    """Test basic connection to Supabase"""
    print("\n🔍 Testing Supabase Connection...")
    print("="*60)

    try:
        logger = SupabaseLogger()
        print("✅ Successfully connected to Supabase!")
        print(f"   URL: {os.getenv('SUPABASE_URL')}")
        return logger
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        return None

def test_log_incident(logger):
    """Test logging a sample incident"""
    print("\n📝 Testing Incident Logging...")
    print("="*60)

    try:
        result = logger.log_incident(
            attack_type="SQL Injection (Test)",
            severity="HIGH",
            source_ip="192.168.1.100",
            confidence=95.5,
            response_time=4.2,
            actions_taken=[
                "Session terminated",
                "IP blocked",
                "Database connection killed",
                "WAF rules updated",
                "Credentials rotated"
            ],
            data_loss=False,
            threat_score=8.7,
            kill_chain_stage="Exploitation",
            details={
                "test": True,
                "payload": "admin' OR '1'='1",
                "endpoint": "/api/users/login"
            }
        )

        if result:
            print("✅ Incident logged successfully!")
            print(f"   Incident ID: {result.get('id')}")
            print(f"   Timestamp: {result.get('timestamp')}")
            print(f"   Attack Type: {result.get('attack_type')}")
            return True
        else:
            print("❌ Failed to log incident (no result returned)")
            return False

    except Exception as e:
        print(f"❌ Error logging incident: {e}")
        return False

def test_get_incidents(logger):
    """Test retrieving recent incidents"""
    print("\n📊 Testing Incident Retrieval...")
    print("="*60)

    try:
        incidents = logger.get_recent_incidents(limit=5)
        print(f"✅ Retrieved {len(incidents)} recent incidents")

        if incidents:
            print("\nMost recent incident:")
            latest = incidents[0]
            print(f"   Type: {latest.get('attack_type')}")
            print(f"   Severity: {latest.get('severity')}")
            print(f"   Response Time: {latest.get('response_time')}s")
            print(f"   Source: {latest.get('source_ip')}")

        return True

    except Exception as e:
        print(f"❌ Error retrieving incidents: {e}")
        return False

def test_get_stats(logger):
    """Test getting statistics"""
    print("\n📈 Testing Statistics...")
    print("="*60)

    try:
        stats = logger.get_stats()
        print("✅ Statistics retrieved successfully!")
        print(f"   Total Incidents: {stats.get('total_incidents')}")
        print(f"   Avg Response Time: {stats.get('avg_response_time')}s")
        print(f"   Critical Incidents: {stats.get('critical_incidents')}")
        print(f"   Data Loss Incidents: {stats.get('data_loss_incidents')} (should be 0!)")
        return True

    except Exception as e:
        print(f"❌ Error getting stats: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🛡️  AEGIS SUPABASE INTEGRATION TEST")
    print("="*60)

    # Test connection
    logger = test_supabase_connection()
    if not logger:
        print("\n❌ Cannot proceed without Supabase connection")
        return

    # Test logging
    log_success = test_log_incident(logger)

    # Test retrieval
    get_success = test_get_incidents(logger)

    # Test stats
    stats_success = test_get_stats(logger)

    # Summary
    print("\n" + "="*60)
    print("📋 TEST SUMMARY")
    print("="*60)
    print(f"   Connection: {'✅ PASS' if logger else '❌ FAIL'}")
    print(f"   Logging: {'✅ PASS' if log_success else '❌ FAIL'}")
    print(f"   Retrieval: {'✅ PASS' if get_success else '❌ FAIL'}")
    print(f"   Statistics: {'✅ PASS' if stats_success else '❌ FAIL'}")

    if all([logger, log_success, get_success, stats_success]):
        print("\n🎉 All tests passed! Supabase integration is working!")
        print("\n📊 Open the live dashboard:")
        print("   file:///Users/tanjim/Downloads/Hackathon/aegis-web/dashboard.html")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")

    print("="*60)

if __name__ == "__main__":
    main()
