# How to Deploy Your Skateskins Tool to the Web

## The Simplest Way (5 Minutes)

### Step 1: Make Sure Your Code is on GitHub

Your code is already pushed to GitHub at:
```
https://github.com/jredhalt/claude
```
Branch: `claude/video-compilation-tool-nihbl`

✅ This is done!

---

### Step 2: Go to Railway

1. Open your web browser
2. Go to: **https://railway.app**
3. Click **"Login"** in the top right
4. Click **"Login with GitHub"**
5. Authorize Railway to access your GitHub

---

### Step 3: Create New Project

1. Click **"New Project"** button
2. Select **"Deploy from GitHub repo"**
3. Find and click on **"jredhalt/claude"** repository
4. Select the branch: **"claude/video-compilation-tool-nihbl"**

---

### Step 4: Wait for Deploy (3-5 minutes)

Railway will automatically:
- ✅ Detect the Dockerfile
- ✅ Install Python
- ✅ Install FFmpeg
- ✅ Build your app
- ✅ Deploy it online

You'll see a progress bar. Just wait!

---

### Step 5: Get Your URL

1. Once deployed, click on your project
2. Click the **"Settings"** tab
3. Scroll to **"Domains"**
4. Click **"Generate Domain"**
5. You'll get a URL like: `https://your-app.up.railway.app`

---

### Step 6: Visit Your Tool!

1. Click on your Railway URL
2. You'll see your Skateskins Ad Generator!
3. Upload videos and photos
4. Generate unlimited ads
5. Access it from anywhere!

---

## That's It! 🎉

You now have a web-based ad generator!

### What You Can Do:
- ✅ Access from any computer
- ✅ Access from your phone
- ✅ Share with your team
- ✅ No installation needed
- ✅ Upload and generate ads anywhere

### Free Tier Limits:
- 500 hours per month (plenty for testing!)
- After that, it's $5/month for unlimited use

---

## Troubleshooting

### Can't see the website?
- Wait 5 minutes for deployment to finish
- Click the "View Logs" button to see progress
- Try refreshing the page

### Getting an error?
- Check the logs in Railway dashboard
- Make sure the deployment finished
- Try redeploying (click "Deploy" again)

### Need more help?
- Railway Docs: https://docs.railway.app
- Or see [DEPLOYMENT.md](DEPLOYMENT.md) for detailed info

---

## Other Options

Don't want to use Railway? You can also deploy to:

### Render (Also Easy):
1. Go to https://render.com
2. Connect GitHub
3. Deploy your repo
4. Done!

### Heroku:
1. Install Heroku CLI
2. Run: `heroku create`
3. Run: `git push heroku main`
4. Done!

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

---

## Using Your Web Tool

Once deployed, using it is the same as before:

1. **Upload Videos**: Click "Video Generator" → Upload your clips
2. **Upload Photos**: Click "Static Ads" → Upload product photos
3. **Generate Videos**: Choose quantity → Click "Generate Videos"
4. **Generate Ads**: Choose quantity → Click "Generate Static Ads"
5. **Download**: Go to "Gallery" → Download your creations

The only difference: It's now online and accessible from anywhere!

---

**Questions?** Check the [QUICKSTART_WEB.md](QUICKSTART_WEB.md) guide!
