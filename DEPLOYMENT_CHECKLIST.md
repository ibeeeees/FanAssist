# FanAssist Deployment Checklist

## ✅ Pre-Deployment Setup Complete
- [x] Created `demo` branch
- [x] Committed all UI improvements
- [x] Created deployment configuration files
- [x] Set up environment variables

## 📋 Deployment Steps

### Step 1: Push to GitHub
```bash
git push origin demo
```

### Step 2: Deploy Backend to Render (15 minutes)
1. Go to https://render.com
2. Sign in with GitHub
3. Click "New +" → "Web Service"
4. Select `FanAssist` repo, `demo` branch
5. Configure:
   - **Name**: `fanassist-backend`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free
6. Click "Create Web Service"
7. **SAVE YOUR BACKEND URL** (e.g., `https://fanassist-backend.onrender.com`)

### Step 3: Update Frontend Configuration (5 minutes)
1. Open `frontend/.env.production`
2. Replace the URL with your actual Render URL
3. Commit:
```bash
git add frontend/.env.production
git commit -m "Update production API URL"
git push origin demo
```

### Step 4: Update CORS in Backend (5 minutes)
1. Wait for Step 5 to get your Vercel URL first, then come back here
2. Open `backend/app/main.py`
3. Add your Vercel URL to CORS origins:
```python
allow_origins=[
    "http://localhost:5173",
    "https://your-actual-vercel-url.vercel.app",
    "https://*.vercel.app",
],
```
4. Commit and push:
```bash
git add backend/app/main.py
git commit -m "Add Vercel URL to CORS"
git push origin demo
```

### Step 5: Deploy Frontend to Vercel (5 minutes)
1. Go to https://vercel.com
2. Sign in with GitHub
3. Click "Add New..." → "Project"
4. Import `FanAssist` repo
5. Configure:
   - **Framework**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
6. Add Environment Variable:
   - **Key**: `VITE_API_URL`
   - **Value**: Your Render backend URL
7. Click "Deploy"
8. **SAVE YOUR VERCEL URL**

### Step 6: Complete CORS Setup
- Go back to Step 4 and add your Vercel URL to backend CORS

### Step 7: Test Your Live Site! 🎉
1. Visit your Vercel URL
2. Check that players load
3. Test selecting players
4. Test placing a bet
5. Check browser console for any errors

## ⚠️ Important Notes

### First Load Will Be Slow
- Render free tier spins down after 15 min
- First request takes ~30 seconds (cold start)
- Subsequent requests are fast

### Keep Backend Alive (Optional)
Use UptimeRobot (free) to ping your backend every 14 minutes:
1. Go to https://uptimerobot.com
2. Add monitor: `https://your-backend-url.onrender.com/`
3. Interval: 14 minutes

### Auto-Deployment
- Any push to `demo` branch auto-deploys to both services
- Vercel: ~2 minutes
- Render: ~5 minutes

## 🎯 URLs to Save
- **Backend**: `https://fanassist-backend.onrender.com`
- **Frontend**: `https://your-project.vercel.app`
- **Backend API Docs**: `https://fanassist-backend.onrender.com/docs`

## 📞 Need Help?
See detailed instructions in `DEPLOYMENT_GUIDE.md`

---

## Cost: $0/month ✅
Both services are completely free for your use case!
