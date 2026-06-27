#!/usr/bin/env bash
# Frontend setup and run script

set -e

echo ""
echo "=================================================================================="
echo "  AI-Powered Candidate Screening System - Frontend Setup"
echo "=================================================================================="
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed!"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node -v)
echo "Node.js version: $NODE_VERSION"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed!"
    exit 1
fi

NPM_VERSION=$(npm -v)
echo "npm version: $NPM_VERSION"
echo ""

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
    echo "✓ Dependencies installed"
    echo ""
fi

echo "=================================================================================="
echo "  Starting Development Server"
echo "=================================================================================="
echo ""
echo "🚀 Frontend: http://localhost:5173"
echo "📚 Backend:  http://localhost:8000"
echo ""
echo "Make sure the backend server is running on port 8000"
echo "Press CTRL+C to stop the server"
echo ""
echo "=================================================================================="
echo ""

# Start development server
npm run dev
