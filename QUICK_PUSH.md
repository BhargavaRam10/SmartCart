# 🚀 Quick Push Guide - Option A (HTTPS)

## Step 1: Get Your Personal Access Token

1. Go to: **https://github.com/settings/tokens**
2. Click **"Generate new token (classic)"**
3. Fill in:
   - **Note**: `Smartcart Project`
   - **Expiration**: Choose 90 days (or your preference)
   - **Select scopes**: ✅ Check `repo` (Full control of private repositories)
4. Click **"Generate token"**
5. **IMPORTANT**: Copy the token immediately (you won't see it again!)
   - It looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

## Step 2: Push Your Code

Open Terminal and run:

```bash
cd /Users/bhargav/Desktop/SmartCart
git push -u origin main
```

When prompted:
- **Username**: `BhargavaRam10`
- **Password**: Paste your Personal Access Token (NOT your GitHub password)

## Alternative: Use the Helper Script

```bash
cd /Users/bhargav/Desktop/SmartCart
./push_to_github.sh
```

## After Successful Push

Your code will be available at:
**https://github.com/BhargavaRam10/Smartcart**

## Troubleshooting

### "Authentication failed"
- Make sure you're using the Personal Access Token, not your GitHub password
- Check that the token has `repo` scope enabled
- Verify the token hasn't expired

### "Repository not found"
- Make sure the repository `Smartcart` exists on GitHub
- Check the repository name matches exactly (case-sensitive)

### "Permission denied"
- Verify you have write access to the repository
- Check that your GitHub username is correct

## Store Credentials (Optional)

To avoid entering credentials every time:

```bash
git config --global credential.helper osxkeychain
```

Then push once, and macOS Keychain will remember your token.

---

**Need help?** Check `GITHUB_AUTH_GUIDE.md` for more details.

