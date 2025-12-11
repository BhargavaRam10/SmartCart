# 🚀 Deploy SmartCart to Streamlit Cloud

## Prerequisites ✅

- ✅ Code pushed to GitHub: https://github.com/BhargavaRam10/SmartCart
- ✅ `requirements.txt` file exists
- ✅ `app.py` is the main file
- ✅ All dependencies are listed

## Step-by-Step Deployment

### Step 1: Go to Streamlit Cloud

1. Open: **https://share.streamlit.io**
2. Click **"Sign in"** (top right)
3. Sign in with your **GitHub account** (BhargavaRam10)

### Step 2: Create New App

1. Click **"New app"** button
2. Fill in the form:

   **Repository**: `BhargavaRam10/SmartCart`
   
   **Branch**: `main`
   
   **Main file path**: `app.py`
   
   **App URL** (optional): `smartcart` (will create: `smartcart.streamlit.app`)

3. Click **"Deploy"**

### Step 3: Wait for Deployment

- Streamlit Cloud will:
  - Install dependencies from `requirements.txt`
  - Run your app
  - Show build logs
  - Deploy your app

### Step 4: Access Your Live App

Once deployed, your app will be available at:
**https://smartcart.streamlit.app**

Or a custom URL like:
**https://share.streamlit.io/BhargavaRam10/SmartCart/main**

## Configuration Options

### Custom Domain (Optional)

1. Go to app settings
2. Click "Custom domain"
3. Add your domain

### Environment Variables (If Needed)

If you need to add secrets or environment variables:

1. Go to app settings
2. Click "Secrets"
3. Add key-value pairs

### Resource Limits

Free tier includes:
- 1 GB RAM
- 1 CPU
- Unlimited apps
- Public apps only

## Troubleshooting

### Build Fails

- Check `requirements.txt` has all dependencies
- Verify Python version compatibility
- Check build logs for errors

### App Crashes

- Check Streamlit Cloud logs
- Verify data files are in the repository
- Ensure file paths are correct

### Import Errors

- Make sure all imports are in `requirements.txt`
- Check that `src/` directory is included in repo
- Verify Python path is correct

## Update Your App

Every time you push to GitHub, Streamlit Cloud will automatically redeploy!

```bash
git add .
git commit -m "Update app"
git push
```

## View Your Deployed Apps

Go to: **https://share.streamlit.io** to see all your deployed apps.

---

**Ready to deploy?** Go to: https://share.streamlit.io

