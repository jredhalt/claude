# Start Using Your Tool Right Now (2 Minutes)

## Step 1: Install What You Need

### Install Python (if you don't have it)
- Go to https://python.org/downloads
- Download and install
- Check "Add to PATH" during installation

### Install FFmpeg

**Mac:**
```bash
brew install ffmpeg
```

**Windows:**
- Download from: https://www.gyan.dev/ffmpeg/builds/
- Get "ffmpeg-release-essentials.zip"
- Extract it
- Add to PATH (or just put ffmpeg.exe in the project folder)

**Linux:**
```bash
sudo apt-get install ffmpeg
```

---

## Step 2: Install Project Dependencies

```bash
cd /home/user/claude
pip install -r requirements.txt
```

---

## Step 3: Start the Server

**Mac/Linux:**
```bash
./start.sh
```

**Windows:**
```bash
start.bat
```

**Or manually:**
```bash
cd backend
python app.py
```

---

## Step 4: Open in Browser

Open your web browser and go to:
```
http://localhost:8000
```

**That's it!** You now have a fully functional web app running!

---

## Using the Tool

### Upload Content:
1. Click "Video Generator" tab
2. Upload your b-roll video clips (drag & drop works!)
3. Click "Static Ads" tab
4. Upload your product photos

### Generate Videos:
1. Choose quantity (start with 3-5)
2. Click "Generate Videos"
3. Wait a few minutes
4. Download from "Gallery" tab

### Generate Image Ads:
1. Choose quantity (start with 10)
2. Select platform size
3. Click "Generate Static Ads"
4. Download from "Gallery" tab

---

## Keep It Running

While the server is running:
- ✅ Access at http://localhost:8000 from any browser
- ✅ Leave the terminal window open
- ✅ Press Ctrl+C to stop when done

---

## Troubleshooting

### "Port already in use"
Someone else is using port 8000. Change the port:
```bash
PORT=8001 python backend/app.py
# Then visit http://localhost:8001
```

### "FFmpeg not found"
Make sure FFmpeg is installed and in your PATH

### "Module not found"
Run: `pip install -r requirements.txt`

---

## Want It Online Instead?

See [DEPLOYMENT.md](DEPLOYMENT.md) for free cloud options:
- Render (free tier)
- Fly.io (free tier)
- Replit (free)

But honestly, running locally is faster and better for video processing!
