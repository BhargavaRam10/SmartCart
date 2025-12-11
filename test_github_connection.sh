#!/bin/bash

echo "🧪 Testing GitHub Connection..."
echo ""

# Test SSH connection
echo "Testing SSH connection to GitHub..."
ssh -T git@github.com 2>&1

echo ""
echo "✅ If you see 'Hi BhargavaRam10! You've successfully authenticated...'"
echo "   then your SSH key is working correctly!"
echo ""
echo "📤 You can now push your code with:"
echo "   git push -u origin main"

