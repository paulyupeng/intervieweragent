#!/bin/bash
# Export project to a tarball (Linux/Mac)

echo 📦 Packing Interviewer Agent for export...

# Create exports directory
mkdir -p exports

# Create tarball
tar -czvf exports/interviewer-agent-export.tar.gz \
    --exclude='.claude' \
    --exclude='exports' \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    --exclude='node_modules' \
    --exclude='.next' \
    --exclude='recordings' \
    backend/ \
    frontend/ \
    question_banks/ \
    database/ \
    .env.example \
    docker-compose.yml \
    README.md \
    QUICKSTART.md \
    .gitignore \
    package.json \
    start.sh \
    start.bat \
    export.bat \
    export.sh

echo.
echo ✅ Export complete!
echo 📁 File location: exports/interviewer-agent-export.tar.gz
echo.
echo To import on another computer:
echo 1. Copy the archive to the target computer
echo 2. Extract: tar -xzf interviewer-agent-export.tar.gz
echo 3. Copy your .env file (with API keys) to the extracted folder
echo 4. Run docker-compose up -d
