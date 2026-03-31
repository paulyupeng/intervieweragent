#!/bin/bash
# GitHub Setup Script for Linux/Mac

echo "========================================="
echo " GitHub Setup for Interviewer Agent"
echo "========================================="
echo ""

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "GitHub CLI (gh) is not installed."
    echo ""
    echo "Install GitHub CLI:"
    echo "  Mac:   brew install gh"
    echo "  Linux: https://github.com/cli/cli/blob/trunk/docs/install_linux.md"
    echo ""
    exit 1
fi

echo "Checking GitHub authentication..."
if ! gh auth status &> /dev/null; then
    echo ""
    echo "Not authenticated with GitHub."
    echo "Starting authentication process..."
    echo ""
    gh auth login --hostname github.com
fi

echo ""
echo "========================================="
echo " Creating GitHub Repository"
echo "========================================="
echo ""

# Ask for repository name
read -p "Enter repository name (default: intervieweragent): " REPO_NAME
REPO_NAME=${REPO_NAME:-intervieweragent}

# Ask for repository visibility
echo ""
echo "Repository visibility:"
echo "1. public  (anyone can view, recommended for open source)"
echo "2. private (only you can view)"
echo ""
read -p "Choose (1=public, 2=private) [default: public]: " VISIBILITY
if [ "$VISIBILITY" = "2" ]; then
    VIS_ARG="--private"
else
    VIS_ARG="--public"
fi

echo ""
echo "Creating repository: $REPO_NAME ..."
gh repo create "$REPO_NAME" $VIS_ARG --source=. --remote=origin --push

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================="
    echo " Setup Complete!"
    echo "========================================="
    echo ""
    echo "Your repository is now live at:"
    echo "https://github.com/$(gh api user | jq -r '.login')/$REPO_NAME"
    echo ""
    echo "Next steps:"
    echo "1. Visit the repository URL above"
    echo "2. Add repository description and topics"
    echo "3. Consider adding a LICENSE file"
    echo ""
else
    echo ""
    echo "Repository creation failed."
    echo "It may already exist. Try connecting existing repo:"
    echo ""
    echo "   git remote add origin https://github.com/\$(gh api user | jq -r '.login')/$REPO_NAME.git"
    echo "   git push -u origin main"
    echo ""
fi
