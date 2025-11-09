# FanAssist Deployment Guide

## Architecture
- **Frontend**: Vercel (React + Vite)
- **Backend**: Render (FastAPI + Python)

## Prerequisites
1. GitHub account with this repo pushed
2. Vercel account (free): https://vercel.com
3. Render account (free): https://render.com

---

## Part 1: Deploy Backend to Render

### Step 1: Push to GitHub
```bash
git push origin demo
```

### Step 2: Create Render Service
1. Go to https://render.com and sign in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select the `FanAssist` repository
5. Select the `demo` branch

### Step 3: Configure Render Service
- **Name**: `fanassist-backend`
- **Region**: Choose closest to you
- **Branch**: `demo`
- **Root Directory**: `backend`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Plan**: `Free`

### Step 4: Add Environment Variables (if needed)
- Click **"Environment"** tab
- Add any API keys or secrets your backend needs

### Step 5: Deploy
- Click **"Create Web Service"**
- Wait 5-10 minutes for deployment
- Copy your backend URL (will be like: `https://fanassist-backend.onrender.com`)

### Step 6: Test Backend
Visit: `https://your-backend-url.onrender.com/docs`
You should see the FastAPI Swagger documentation.

---

## Part 2: Deploy Frontend to Vercel

### Step 1: Update API URL in Frontend
Before deploying, update the API base URL:

1. Open `frontend/src/services/api.ts`
2. Find the `API_BASE_URL` constant
3. Update it to your Render backend URL:
```typescript
const API_BASE_URL = 'https://fanassist-backend.onrender.com';
```

4. Commit the change:
```bash
git add frontend/src/services/api.ts
git commit -m "Update API URL for production"
git push origin demo
```

### Step 2: Update vercel.json
1. Open `frontend/vercel.json`
2. Replace `your-backend-url.onrender.com` with your actual Render URL
3. Commit:
```bash
git add frontend/vercel.json
git commit -m "Update Vercel config with Render URL"
git push origin demo
```

### Step 3: Deploy to Vercel
1. Go to https://vercel.com and sign in
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository
4. Select the `FanAssist` repository

### Step 4: Configure Vercel Project
- **Framework Preset**: Vite
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

### Step 5: Add Environment Variables (Optional)
Click **"Environment Variables"** and add:
- `VITE_API_URL`: Your Render backend URL

### Step 6: Deploy
- Click **"Deploy"**
- Wait 2-3 minutes
- Your site will be live at: `https://your-project.vercel.app`

---

## Part 3: Configure CORS on Backend

Your backend needs to allow requests from your Vercel frontend.

1. Open `backend/app/main.py`
2. Update the CORS origins to include your Vercel URL:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000", 
        "https://your-project.vercel.app",  # Add your Vercel URL
        "https://*.vercel.app",  # Allow all Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

3. Commit and push:
```bash
git add backend/app/main.py
git commit -m "Add Vercel URL to CORS origins"
git push origin demo
```

4. Render will auto-deploy the backend changes

---

## Part 4: Test Your Deployed App

1. Visit your Vercel URL: `https://your-project.vercel.app`
2. Open browser DevTools → Network tab
3. Click to load players
4. Check that API calls are going to your Render backend
5. Test placing a bet to ensure full functionality

---

## Important Notes

### Free Tier Limitations

**Render (Backend):**
- ✅ 750 free hours/month
- ⚠️ Spins down after 15 minutes of inactivity
- ⚠️ Cold start takes ~30 seconds
- ✅ Auto-deploys on git push

**Vercel (Frontend):**
- ✅ Unlimited bandwidth
- ✅ 100 GB/month
- ✅ Auto-deploys on git push
- ✅ No cold starts

### Cold Start Solution
Add a "wake up" function that pings your backend every 14 minutes to keep it alive:
- Use a service like UptimeRobot (free)
- Set it to ping: `https://your-backend-url.onrender.com/`
- Interval: Every 14 minutes

---

## Updating Your Deployment

### To update frontend:
```bash
git add .
git commit -m "Your changes"
git push origin demo
```
Vercel auto-deploys in ~2 minutes.

### To update backend:
```bash
git add .
git commit -m "Your changes"
git push origin demo
```
Render auto-deploys in ~5 minutes.

---

## Custom Domain (Optional)

### Vercel:
1. Go to Project Settings → Domains
2. Add your domain
3. Update DNS records as instructed

### Render:
1. Upgrade to paid plan ($7/month)
2. Go to Settings → Custom Domain
3. Add your backend domain

---

## Troubleshooting

### Frontend can't reach backend
- Check CORS settings in `backend/app/main.py`
- Verify Render URL is correct in `frontend/src/services/api.ts`
- Check Render logs: Dashboard → Logs

### Backend cold starts
- Normal on free tier
- Consider upgrading Render or using UptimeRobot

### Build failures
- Check build logs in Vercel/Render dashboard
- Verify all dependencies are in `requirements.txt` and `package.json`

---

## Cost Summary
- **Render Free Tier**: $0/month (with cold starts)
- **Vercel Free Tier**: $0/month (no cold starts)
- **Total**: $0/month ✅

To eliminate cold starts, upgrade Render to $7/month.

---

## Support
- Vercel Docs: https://vercel.com/docs
- Render Docs: https://render.com/docs
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/
