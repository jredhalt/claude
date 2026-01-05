# Deploy Skateskins Ad Generator to the Web

This guide shows you how to deploy your tool online so you can access it from anywhere!

---

## Option 1: Railway (Recommended - Easiest!)

Railway is the easiest option with a generous free tier.

### Steps:

1. **Create a Railway account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Deploy from GitHub**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect the Dockerfile and deploy!

3. **Wait for deployment** (3-5 minutes)
   - Railway will build and deploy automatically
   - You'll get a URL like: `your-app.railway.app`

4. **Access your tool**
   - Click the URL Railway gives you
   - Start using your tool online!

**Cost:** Free tier includes 500 hours/month (enough for testing)

---

## Option 2: Render

Render is another great free option.

### Steps:

1. **Create a Render account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create a new Web Service**
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository

3. **Configure the service**
   - Name: `skateskins-ad-generator`
   - Environment: `Docker`
   - Plan: `Free`
   - Click "Create Web Service"

4. **Wait for deployment** (5-10 minutes)
   - Render will build and deploy
   - You'll get a URL like: `your-app.onrender.com`

5. **Access your tool**
   - Visit the URL
   - Start generating ads!

**Cost:** Free tier available (sleeps after 15 mins of inactivity)

---

## Option 3: Heroku

Classic platform with free tier.

### Steps:

1. **Install Heroku CLI**
   ```bash
   # Mac
   brew install heroku/brew/heroku

   # Windows
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create a new app**
   ```bash
   heroku create skateskins-ad-generator
   ```

4. **Add buildpacks** (for FFmpeg support)
   ```bash
   heroku buildpacks:add --index 1 https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
   heroku buildpacks:add --index 2 heroku/python
   ```

5. **Deploy**
   ```bash
   git push heroku claude/video-compilation-tool-nihbl:main
   ```

6. **Open your app**
   ```bash
   heroku open
   ```

**Cost:** Free tier available (limited hours per month)

---

## Option 4: Docker Anywhere

You can deploy the Docker container to any cloud provider.

### Build and run locally:

```bash
# Build the image
docker build -t skateskins-generator .

# Run the container
docker run -p 8000:8000 skateskins-generator
```

### Deploy to:
- **Google Cloud Run**: `gcloud run deploy`
- **AWS ECS**: Upload container to ECR and deploy
- **DigitalOcean App Platform**: Connect GitHub repo
- **Azure Container Apps**: Deploy from container registry

---

## After Deployment

### Using Your Web Tool:

1. **Visit your URL**
   - Railway: `https://your-app.railway.app`
   - Render: `https://your-app.onrender.com`
   - Heroku: `https://your-app.herokuapp.com`

2. **Upload content**
   - Upload your video clips
   - Upload your product photos

3. **Generate ads**
   - Create unlimited variations
   - Download and use in your campaigns

### Important Notes:

⚠️ **Storage Limits:**
- Free tiers have limited storage
- Generated files are temporary (may be deleted on restart)
- Download your generated content regularly

⚠️ **Processing Limits:**
- Video generation is CPU-intensive
- May be slow on free tiers
- Consider upgrading for heavy use

⚠️ **File Upload Limits:**
- Most platforms limit request size to 100MB
- Upload files in batches if needed

---

## Upgrading to Paid Plans

For serious use, consider upgrading:

### Railway Pro ($20/month):
- More CPU and memory
- No sleep time
- Better for video processing

### Render Standard ($7/month):
- Always-on instance
- Better performance
- No cold starts

### Heroku Hobby ($7/month):
- Always-on dyno
- Better for production

---

## Using Docker Compose (Local Development)

For local testing before deployment:

```bash
# Start the app
docker-compose up

# Access at http://localhost:8000

# Stop the app
docker-compose down
```

---

## Troubleshooting

### "Application Error" or 503
- Check deployment logs in your platform dashboard
- Ensure FFmpeg is installed (should be automatic)
- Verify PORT environment variable is set

### "Out of Memory"
- Video processing needs RAM
- Upgrade to a paid plan
- Generate fewer videos at once

### Uploads failing
- Check file size limits
- Ensure uploads directory has write permissions
- Check platform storage limits

### Videos not generating
- Verify FFmpeg is installed in logs
- Check for build errors
- Ensure enough CPU/memory allocated

---

## Security Notes

This tool is meant for personal/business use. For production:

1. **Add authentication** - Protect your tool with login
2. **Rate limiting** - Prevent abuse
3. **Storage cleanup** - Auto-delete old files
4. **API keys** - Protect API endpoints

---

## Cost Estimates

### Free Tier Usage:
- **Light use** (10-20 videos/week): FREE on all platforms
- **Medium use** (50+ videos/week): May exceed free limits

### Paid Plans:
- **Railway Pro** ($20/mo): Unlimited use
- **Render Standard** ($7/mo): Good for most use cases
- **Heroku Hobby** ($7/mo): Basic production use

---

## Recommended Path

**For beginners:**
1. Start with Railway (easiest setup)
2. Test the free tier
3. Upgrade if you need more

**For developers:**
1. Use Docker Compose for local testing
2. Deploy to Render for production
3. Consider Railway for simplicity

**For heavy use:**
1. Deploy to Railway Pro or dedicated server
2. Add cloud storage (S3) for files
3. Set up automated cleanup

---

## Next Steps

After deploying:

1. **Share the URL** with your team
2. **Upload your Skateskins content**
3. **Generate test ads**
4. **Run A/B tests** with the variations
5. **Scale what works**

Need help? Check the logs in your deployment platform's dashboard!
