# 🔐 GitHub Authentication Setup Guide

This guide will help you set up authentication for GitHub so you can push your code without entering credentials every time.

## Option 1: SSH Keys (Recommended - Most Secure) ⭐

SSH keys provide the most secure and convenient way to authenticate with GitHub.

### Step 1: Check if you already have SSH keys

```bash
ls -la ~/.ssh
```

If you see `id_ed25519` or `id_rsa`, you already have keys!

### Step 2: Generate a new SSH key (if needed)

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

- Press Enter to accept default file location
- Optionally set a passphrase (recommended for security)
- Or press Enter twice for no passphrase

### Step 3: Add SSH key to ssh-agent

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### Step 4: Copy your public key

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the entire output (starts with `ssh-ed25519`)

### Step 5: Add key to GitHub

1. Go to: https://github.com/settings/keys
2. Click **"New SSH key"**
3. Title: `MacBook Air` (or any name)
4. Key: Paste your public key
5. Click **"Add SSH key"**

### Step 6: Update remote URL to use SSH

```bash
cd /Users/bhargav/Desktop/SmartCart
git remote set-url origin git@github.com:BhargavaRam10/Smartcart.git
```

### Step 7: Test connection

```bash
ssh -T git@github.com
```

You should see: `Hi BhargavaRam10! You've successfully authenticated...`

### Step 8: Push your code

```bash
git push -u origin main
```

---

## Option 2: Personal Access Token (PAT)

If you prefer using HTTPS instead of SSH:

### Step 1: Generate a Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Name: `Smartcart Project`
4. Expiration: Choose your preference (90 days recommended)
5. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (if you plan to use GitHub Actions)
6. Click **"Generate token"**
7. **IMPORTANT**: Copy the token immediately (you won't see it again!)

### Step 2: Use token as password

When you push, use:
- **Username**: `BhargavaRam10`
- **Password**: Your Personal Access Token (not your GitHub password)

### Step 3: Store credentials (macOS Keychain)

```bash
git config --global credential.helper osxkeychain
```

Now Git will store your credentials securely in macOS Keychain.

### Step 4: Push your code

```bash
git push -u origin main
```

Enter your token when prompted (it will be saved in Keychain).

---

## Option 3: GitHub CLI (Easiest)

### Step 1: Install GitHub CLI

```bash
brew install gh
```

### Step 2: Authenticate

```bash
gh auth login
```

Follow the prompts:
- Choose GitHub.com
- Choose HTTPS or SSH
- Authenticate via browser or token
- Choose your preferred protocol

### Step 3: Push your code

```bash
git push -u origin main
```

---

## Quick Setup Script

I've created a setup script for you. Run:

```bash
cd /Users/bhargav/Desktop/SmartCart
./setup_github_auth.sh
```

This will:
- Check for existing SSH keys
- Generate new keys if needed
- Show you your public key to add to GitHub
- Update your remote URL to use SSH

---

## Troubleshooting

### "Permission denied (publickey)" error

1. Make sure your SSH key is added to GitHub
2. Test connection: `ssh -T git@github.com`
3. Check SSH agent: `ssh-add -l`

### "Host key verification failed"

```bash
ssh-keyscan github.com >> ~/.ssh/known_hosts
```

### Reset remote URL

```bash
git remote set-url origin https://github.com/BhargavaRam10/Smartcart.git
# or
git remote set-url origin git@github.com:BhargavaRam10/Smartcart.git
```

---

## Recommended: SSH Keys

SSH keys are the most secure and convenient option. Once set up, you won't need to enter credentials again!

Need help? Check GitHub's official guide: https://docs.github.com/en/authentication

