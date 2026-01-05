# Deploy to Web in 5 Minutes ⚡

The fastest way to get your Skateskins Ad Generator online!

---

## Method 1: Deploy to Railway (1-Click!)

**This is the EASIEST option.**

### Step 1: Push to GitHub
```bash
# If not already pushed
git push origin claude/video-compilation-tool-nihbl
```

### Step 2: Deploy to Railway

1. Go to **https://railway.app**
2. Click **"Start a New Project"**
3. Click **"Deploy from GitHub repo"**
4. Select **your repository**
5. Railway auto-detects everything and deploys!

### Step 3: Get Your URL

Railway gives you a URL like:
```
https://skateskins-generator-production.up.railway.app
```

**Done!** Visit the URL and start generating ads!

---

## Method 2: One-Click Deploy Buttons

### Deploy to Railway
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

### Deploy to Render
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

Just click the button and follow the prompts!

---

## What Happens After Deployment?

1. **Build Process** (3-5 minutes)
   - Installs Python
   - Installs FFmpeg
   - Sets up the app
   - Starts the server

2. **You Get a URL**
   - Access from anywhere
   - Share with your team
   - Use on mobile or desktop

3. **Start Using It**
   - Upload videos and photos
   - Generate unlimited variations
   - Download and use in ads

---

## Using Your Web Tool

### Upload Content:
1. Go to your Railway URL
2. Click "Video Generator" tab
3. Upload your b-roll clips
4. Click "Static Ads" tab
5. Upload product photos

### Generate Ads:
1. Choose how many videos (start with 5)
2. Click "Generate Videos"
3. Wait 2-3 minutes
4. Download from Gallery tab

### Generate Image Ads:
1. Choose how many ads (start with 10)
2. Select platform (Instagram, TikTok, etc.)
3. Click "Generate Static Ads"
4. Download from Gallery tab

---

## Important Notes

### Free Tier Limits:
- ✅ Good for testing and light use
- ✅ 500 hours/month on Railway
- ⚠️ May sleep after inactivity (wake on visit)
- ⚠️ Limited storage (download files regularly)

### When to Upgrade:
- Generating 50+ videos per week
- Need faster processing
- Need more storage
- Want 24/7 availability

**Upgrade cost:** $7-20/month

---

## Troubleshooting

### "Application Error"
- Wait 5 minutes for deployment to complete
- Check Railway logs for errors
- Redeploy if needed

### Slow Generation
- Normal on free tier
- Video processing takes time
- Upgrade for faster speeds

### Files Disappearing
- Free tiers may restart and clear files
- Download generated content regularly
- Upgrade for persistent storage

---

## Alternative: Use Docker

If you want to deploy anywhere:

```bash
# Build
docker build -t skateskins .

# Run
docker run -p 8000:8000 skateskins

# Access at http://localhost:8000
```

Deploy this Docker container to:
- Google Cloud Run
- AWS ECS
- DigitalOcean
- Azure
- Your own server

---

## Cost Breakdown

### FREE (Good for starting):
- Railway: 500 hours/month
- Render: Limited hours, sleeps after 15 min
- Heroku: Limited hours per month

### PAID (For production):
- Railway Pro: $20/month (recommended)
- Render Standard: $7/month
- Heroku Hobby: $7/month

---

## Recommended: Start Free, Upgrade Later

1. **Week 1:** Deploy to Railway free tier
2. **Test:** Generate 10-20 videos
3. **Evaluate:** See if it meets your needs
4. **Upgrade:** If generating lots of content

---

## Need Help?

Check the full deployment guide: [DEPLOYMENT.md](DEPLOYMENT.md)

Or visit your platform's documentation:
- Railway: https://docs.railway.app
- Render: https://render.com/docs
- Heroku: https://devcenter.heroku.com

---

**Ready? Go deploy!** 🚀
