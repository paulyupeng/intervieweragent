#!/bin/bash
# Quick start script for Interviewer Agent

echo "🚀 Starting Interviewer Agent..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file. Please edit it with your API keys."
    echo ""
fi

# Start services
echo "📦 Starting Docker containers..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
echo "🔍 Checking service status..."
docker-compose ps

echo ""
echo "✅ Interviewer Agent is ready!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Next steps:"
echo "1. Edit .env with your API keys (Deepgram, ElevenLabs, Anthropic)"
echo "2. Restart the backend: docker-compose restart backend"
echo "3. Open http://localhost:3000 in your browser"
