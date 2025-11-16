# Deploy AEGIS to Vercel

## ⚡ Quick Deploy (Recommended - 2 minutes)

### Option 1: GitHub Integration (Easiest)

1. **Push to GitHub:**
   ```bash
   cd /Users/tanjim/Downloads/Hackathon
   git add aegis-web/
   git commit -m "Add AEGIS web showcase"
   git push origin main
   ```

2. **Deploy on Vercel:**
   - Go to https://vercel.com/new
   - Sign in with GitHub
   - Click "Import Project"
   - Select your `dayton_AEGIS` repository
   - Set Root Directory: `aegis-web`
   - Click "Deploy"
   - Done! Your site will be live at: `https://aegis-[random].vercel.app`

### Option 2: Vercel CLI

1. **Login:**
   ```bash
   npx vercel login
   ```

2. **Deploy:**
   ```bash
   cd aegis-web
   npx vercel --prod
   ```

### Option 3: Drag & Drop

1. Go to https://vercel.com/new
2. Drag the `aegis-web` folder onto the page
3. Click "Deploy"

## 🎯 After Deployment

Your AEGIS showcase will be live at:
- **Production URL:** `https://aegis-[your-project].vercel.app`
- **Custom Domain:** Can be added in Vercel dashboard

## 📊 What's Included

- ✅ Responsive landing page
- ✅ Live metrics display
- ✅ Sponsor showcase
- ✅ GitHub integration
- ✅ Modern glassmorphism UI

## 🔗 Links to Update

After deployment, update these links in `index.html`:
- GitHub repository link
- Demo video link (once uploaded)
- Documentation links

## 🚀 Quick Start

**Recommended:** Use Option 1 (GitHub Integration) - it's the easiest and automatically redeploys on git push!
