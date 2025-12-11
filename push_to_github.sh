#!/bin/bash

echo "🚀 Pushing SmartCart to GitHub..."
echo ""
echo "You'll be prompted for credentials:"
echo "  Username: BhargavaRam10"
echo "  Password: [Paste your Personal Access Token]"
echo ""
echo "If you don't have a token yet:"
echo "  1. Go to: https://github.com/settings/tokens"
echo "  2. Click 'Generate new token (classic)'"
echo "  3. Name: Smartcart"
echo "  4. Select scope: repo"
echo "  5. Generate and copy the token"
echo ""
read -p "Press Enter to continue with push..."
echo ""

cd /Users/bhargav/Desktop/SmartCart
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Success! Your code has been pushed to GitHub!"
    echo "🌐 View your repository at: https://github.com/BhargavaRam10/Smartcart"
else
    echo ""
    echo "❌ Push failed. Please check:"
    echo "   1. Your Personal Access Token is correct"
    echo "   2. The repository exists on GitHub"
    echo "   3. You have write access to the repository"
fi

