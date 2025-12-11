# 🔑 Add SSH Key to GitHub - Quick Guide

## Your SSH Public Key

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAID4FhnWcMMzegtlvGOe3WzzwIAnS8cgEqX36Et6EDsE1 BhargavaRam10@github
```

## Steps to Add SSH Key

1. **Copy the key above** (the entire line starting with `ssh-ed25519`)

2. **Go to GitHub SSH Settings**:
   - Open: https://github.com/settings/keys
   - Or: GitHub → Settings → SSH and GPG keys

3. **Add New SSH Key**:
   - Click **"New SSH key"** button
   - **Title**: `MacBook Air` (or any name you prefer)
   - **Key type**: `Authentication Key`
   - **Key**: Paste the entire key from above
   - Click **"Add SSH key"**

4. **Verify** (optional):
   ```bash
   ssh -T git@github.com
   ```
   You should see: `Hi BhargavaRam10! You've successfully authenticated...`

5. **Push your code**:
   ```bash
   cd /Users/bhargav/Desktop/SmartCart
   git push -u origin main
   ```

## Quick Copy Command

Run this to copy your key to clipboard:
```bash
cat ~/.ssh/id_ed25519.pub | pbcopy
```

Then paste it into GitHub!

