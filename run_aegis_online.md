# Run AEGIS Demo Online

## 🎯 Current Setup

**Static Website (Vercel):**
- Landing page: ✅ Works perfectly
- URL: https://aegis.vercel.app
- Shows features, metrics, sponsors

**Python Demo (Needs Backend):**
- Demo scripts: ❌ Can't run on Vercel (static-only)
- Need: Python runtime environment

---

## ✅ **Solution 1: Daytona Sandbox (Recommended)**

**Already configured and ready!**

```bash
# Run demo in Daytona sandbox
python3 run_demo_existing_sandbox.py
```

**Share the demo:**
- Run demo in Daytona
- Record the output
- Upload video to YouTube/Loom
- Embed in website or share link

---

## ✅ **Solution 2: Deploy to Render/Railway (Free)**

### Deploy to Render:

1. **Create `render.yaml`:**

```yaml
services:
  - type: web
    name: aegis-demo
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "python demo_pitch_live.py --scenario sql_injection"
```

2. **Deploy:**
   - Go to https://render.com
   - Connect GitHub repo
   - Deploy `dayton_AEGIS`
   - Will run the demo 24/7

### Deploy to Railway:

1. **Go to:** https://railway.app
2. **New Project** → **Deploy from GitHub**
3. **Select:** `taazbro/dayton_AEGIS`
4. **Environment:** Python
5. **Start Command:** `python demo_pitch_live.py`

---

## ✅ **Solution 3: Embed Video Demo**

**Best for hackathon judges:**

1. **Record demo locally:**
   ```bash
   python3 demo_pitch_live.py --scenario sql_injection | tee demo_output.txt
   ```

2. **Upload to:**
   - YouTube (unlisted)
   - Loom
   - Vimeo

3. **Update website:**
   Add video embed to `aegis-web/index.html`

---

## ✅ **Solution 4: Create Web API (Advanced)**

Convert demo to a web service:

```python
# api/demo.py
from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run-demo')
def run_demo():
    result = subprocess.run(
        ['python3', 'demo_pitch_live.py', '--scenario', 'sql_injection'],
        capture_output=True,
        text=True
    )
    return jsonify({
        'output': result.stdout,
        'status': 'success'
    })

if __name__ == '__main__':
    app.run()
```

Deploy to:
- Render
- Railway
- Heroku
- Google Cloud Run

---

## 🎯 **Recommended Approach for Hackathon:**

**Two-Tier Setup:**

1. **Frontend (Vercel):**
   - Professional landing page ✅
   - Showcase features and metrics
   - Link to video demo

2. **Demo (Video):**
   - Record AEGIS demo locally (looks amazing!)
   - Upload to YouTube/Loom
   - Embed in website or share link

**Why this works:**
- Judges see beautiful landing page
- Video shows actual working demo
- No infrastructure complexity
- Works 100% reliably

---

## 🚀 **Quick Action:**

**Want me to create a Flask API or help with video recording?**

Choose:
1. Create Flask web API for demo
2. Set up Railway/Render deployment
3. Keep it simple with video embed
4. Use Daytona for live demo
