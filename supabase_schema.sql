-- AEGIS Security Incidents Table
-- Run this in your Supabase SQL Editor to create the incidents table

CREATE TABLE IF NOT EXISTS security_incidents (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    attack_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    source_ip VARCHAR(100) NOT NULL,
    confidence DECIMAL(5,2) NOT NULL,
    response_time DECIMAL(6,2) NOT NULL,
    actions_taken TEXT[] NOT NULL,
    data_loss BOOLEAN NOT NULL DEFAULT FALSE,
    threat_score DECIMAL(4,2),
    kill_chain_stage VARCHAR(50),
    details JSONB,
    status VARCHAR(20) DEFAULT 'neutralized',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_security_incidents_timestamp ON security_incidents(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_security_incidents_severity ON security_incidents(severity);
CREATE INDEX IF NOT EXISTS idx_security_incidents_attack_type ON security_incidents(attack_type);

-- Enable Row Level Security
ALTER TABLE security_incidents ENABLE ROW LEVEL SECURITY;

-- Create policy to allow anonymous inserts (for demo purposes)
-- In production, you'd want stricter policies!
CREATE POLICY "Enable insert for anon" ON security_incidents
    FOR INSERT TO anon WITH CHECK (true);

-- Create policy to allow anonymous reads (for live dashboard)
CREATE POLICY "Enable read for anon" ON security_incidents
    FOR SELECT TO anon USING (true);

-- Enable real-time
ALTER PUBLICATION supabase_realtime ADD TABLE security_incidents;

-- Create a view for dashboard stats
CREATE OR REPLACE VIEW incident_stats AS
SELECT
    COUNT(*) as total_incidents,
    ROUND(AVG(response_time)::numeric, 2) as avg_response_time,
    COUNT(*) FILTER (WHERE severity = 'CRITICAL') as critical_count,
    COUNT(*) FILTER (WHERE severity = 'HIGH') as high_count,
    COUNT(*) FILTER (WHERE severity = 'MEDIUM') as medium_count,
    COUNT(*) FILTER (WHERE severity = 'LOW') as low_count,
    COUNT(*) FILTER (WHERE data_loss = true) as data_loss_count,
    MAX(timestamp) as last_incident
FROM security_incidents;

-- Grant access to anon role
GRANT SELECT ON incident_stats TO anon;

COMMENT ON TABLE security_incidents IS 'AEGIS autonomous defense system - security incident log';
COMMENT ON COLUMN security_incidents.timestamp IS 'When the incident was detected';
COMMENT ON COLUMN security_incidents.attack_type IS 'Type of attack (e.g., SQL Injection, Ransomware)';
COMMENT ON COLUMN security_incidents.severity IS 'Severity: CRITICAL, HIGH, MEDIUM, LOW';
COMMENT ON COLUMN security_incidents.source_ip IS 'Source IP address or hostname of attacker';
COMMENT ON COLUMN security_incidents.confidence IS 'Detection confidence percentage (0-100)';
COMMENT ON COLUMN security_incidents.response_time IS 'Time to neutralize threat in seconds';
COMMENT ON COLUMN security_incidents.actions_taken IS 'Array of automated defensive actions';
COMMENT ON COLUMN security_incidents.data_loss IS 'Whether any data was lost (should always be FALSE for AEGIS!)';
COMMENT ON COLUMN security_incidents.threat_score IS 'Behavioral threat score (0-10)';
COMMENT ON COLUMN security_incidents.kill_chain_stage IS 'Stage in cyber kill chain';
COMMENT ON COLUMN security_incidents.details IS 'Additional incident details as JSON';
