# AEGIS Supabase Integration Setup

Real-time threat dashboard powered by Supabase! 🚀

## Step 1: Create Database Schema

1. Go to your Supabase Dashboard: https://supabase.com/dashboard
2. Select your project: `rqxodksektmbzmjmebft`
3. Click **SQL Editor** in the left sidebar
4. Click **New Query**
5. Copy and paste the entire contents of `supabase_schema.sql`
6. Click **Run** (or press Cmd/Ctrl + Enter)

You should see: **Success. No rows returned**

This creates:
- ✅ `security_incidents` table
- ✅ Indexes for fast queries
- ✅ Row Level Security policies
- ✅ Real-time subscriptions enabled
- ✅ `incident_stats` view for dashboard

## Step 2: Verify Environment Variables

Check your `.env` file has:
```bash
SUPABASE_URL=https://rqxodksektmbzmjmebft.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Step 3: Test the Integration

Run the test script:
```bash
python3 test_supabase.py
```

You should see:
```
🛡️  AEGIS SUPABASE INTEGRATION TEST
============================================================
🔍 Testing Supabase Connection...
✅ Successfully connected to Supabase!

📝 Testing Incident Logging...
✅ Incident logged successfully!

📊 Testing Incident Retrieval...
✅ Retrieved 1 recent incidents

📈 Testing Statistics...
✅ Statistics retrieved successfully!

🎉 All tests passed! Supabase integration is working!
```

## Step 4: View the Live Dashboard

Open the dashboard in your browser:
```bash
open aegis-web/dashboard.html
```

Or visit: `file:///Users/tanjim/Downloads/Hackathon/aegis-web/dashboard.html`

The dashboard shows:
- 📊 **Real-time statistics** - Total threats, avg response time, critical count
- 📡 **Live incident feed** - Auto-updates when new threats detected
- 🎯 **Incident details** - Attack type, severity, confidence, response time
- ⚡ **Automated actions** - All defensive actions taken

## Step 5: Run AEGIS Demo with Supabase Logging

The demo will automatically log to Supabase if credentials are configured:

```bash
python3 demo_pitch_live.py --scenario sql_injection
```

Watch the live dashboard update in real-time! 🔥

## What's Happening Under the Hood

1. **AEGIS detects threat** → Behavioral analysis runs
2. **Autonomous response** → Killswitch activates, neutralizes threat
3. **Log to Supabase** → Incident saved to real-time database
4. **Dashboard updates** → WebSocket subscription pushes new data
5. **SOC notified** → Slack alert sent

## Database Schema

```sql
security_incidents (
    id                BIGSERIAL PRIMARY KEY,
    timestamp         TIMESTAMPTZ,
    attack_type       VARCHAR(100),
    severity          VARCHAR(20),      -- CRITICAL, HIGH, MEDIUM, LOW
    source_ip         VARCHAR(100),
    confidence        DECIMAL(5,2),     -- 0-100%
    response_time     DECIMAL(6,2),     -- seconds
    actions_taken     TEXT[],           -- Array of actions
    data_loss         BOOLEAN,          -- Always FALSE for AEGIS!
    threat_score      DECIMAL(4,2),     -- 0-10
    kill_chain_stage  VARCHAR(50),
    details           JSONB,
    status            VARCHAR(20)
)
```

## Real-Time Features

The dashboard uses Supabase real-time subscriptions:
- **Instant updates** when new threats detected
- **No polling** - true WebSocket push notifications
- **Automatic reconnection** if connection drops
- **10-second fallback** polling for reliability

## Production Deployment

For production use:

1. **Update RLS policies** in Supabase to restrict access
2. **Use service role key** for server-side logging
3. **Add authentication** to dashboard
4. **Enable database backups** in Supabase settings
5. **Set up monitoring** with Supabase alerts

## Troubleshooting

**Connection Error:**
- Check `.env` has correct SUPABASE_URL and SUPABASE_ANON_KEY
- Verify schema was created (check Supabase Table Editor)

**No Real-Time Updates:**
- Ensure real-time is enabled: `ALTER PUBLICATION supabase_realtime ADD TABLE security_incidents;`
- Check browser console for WebSocket errors

**Permission Denied:**
- Verify RLS policies are set correctly
- Check anon key has INSERT and SELECT permissions

## Next Steps

- Deploy dashboard to Vercel
- Add authentication for SOC team access
- Create analytics views for threat trends
- Set up Supabase Edge Functions for automated responses

---

**Ready for Demo Day!** 🎯

Your AEGIS system now has:
1. ✅ Real-time threat detection
2. ✅ Autonomous response (<5s)
3. ✅ Live dashboard with Supabase
4. ✅ Slack notifications
5. ✅ All 6+ sponsor integrations working

The live dashboard proves AEGIS is production-ready with real-time monitoring!
