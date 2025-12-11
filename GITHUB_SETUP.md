# GitHub Setup Instructions

## Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `Smartcart`
3. Description: "E-Commerce Recommendation Engine with Market Basket Analysis and Collaborative Filtering"
4. Choose **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **"Create repository"**

## Step 2: Push Your Code

After creating the repository, run these commands:

```bash
cd /Users/bhargav/Desktop/SmartCart
git push -u origin main
```

If you're prompted for credentials:
- **Username**: BhargavaRam10
- **Password**: Use a Personal Access Token (not your GitHub password)

### Creating a Personal Access Token (if needed):

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name (e.g., "Smartcart Push")
4. Select scopes: `repo` (full control of private repositories)
5. Click "Generate token"
6. Copy the token and use it as your password when pushing

## Step 3: Verify

After pushing, visit:
https://github.com/BhargavaRam10/Smartcart

Your code should be visible!

## Optional: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select repository: `BhargavaRam10/Smartcart`
5. Main file path: `app.py`
6. Click "Deploy"

Your app will be live at: `https://smartcart.streamlit.app`

