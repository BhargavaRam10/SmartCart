#!/bin/bash

echo "🔐 GitHub Authentication Setup Guide"
echo "===================================="
echo ""

# Check if SSH key exists
if [ -f ~/.ssh/id_ed25519 ] || [ -f ~/.ssh/id_rsa ]; then
    echo "✅ SSH key found!"
    if [ -f ~/.ssh/id_ed25519.pub ]; then
        echo "📋 Your public SSH key (id_ed25519.pub):"
        cat ~/.ssh/id_ed25519.pub
    elif [ -f ~/.ssh/id_rsa.pub ]; then
        echo "📋 Your public SSH key (id_rsa.pub):"
        cat ~/.ssh/id_rsa.pub
    fi
    echo ""
    echo "👉 Copy the key above and add it to GitHub:"
    echo "   https://github.com/settings/keys"
else
    echo "📝 Generating new SSH key..."
    echo ""
    read -p "Enter your GitHub email: " email
    ssh-keygen -t ed25519 -C "$email" -f ~/.ssh/id_ed25519 -N ""
    
    echo ""
    echo "✅ SSH key generated!"
    echo "📋 Your public SSH key:"
    cat ~/.ssh/id_ed25519.pub
    echo ""
    echo "👉 Copy the key above and add it to GitHub:"
    echo "   https://github.com/settings/keys"
    echo ""
    echo "Then run: ssh-add ~/.ssh/id_ed25519"
fi

echo ""
echo "🔄 Updating remote URL to use SSH..."
cd /Users/bhargav/Desktop/SmartCart
git remote set-url origin git@github.com:BhargavaRam10/Smartcart.git

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Add your SSH key to GitHub (if you haven't already)"
echo "2. Test connection: ssh -T git@github.com"
echo "3. Push your code: git push -u origin main"

