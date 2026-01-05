#!/bin/bash

echo "================================================"
echo "  Skateskins - Quick Railway Deploy"
echo "================================================"
echo ""
echo "This script will deploy your app using Railway CLI"
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli

    if [ $? -ne 0 ]; then
        echo "❌ Installation failed. Try manual install:"
        echo "   curl -fsSL https://railway.app/install.sh | sh"
        exit 1
    fi
fi

echo "✅ Railway CLI installed"
echo ""

# Login
echo "🔐 Opening browser for login..."
railway login

if [ $? -ne 0 ]; then
    echo "❌ Login failed. Please try again."
    exit 1
fi

echo "✅ Logged in"
echo ""

# Initialize project
echo "🚀 Initializing Railway project..."
railway init

# Deploy
echo "📤 Deploying your app..."
railway up

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================"
    echo "✅ Deployment successful!"
    echo "================================================"
    echo ""
    echo "Getting your URL..."
    railway domain
    echo ""
    echo "Your app is now live! 🎉"
else
    echo "❌ Deployment failed. Check the error above."
fi
