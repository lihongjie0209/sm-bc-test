#!/bin/bash
# Setup script for sm-bc-test project
# Installs dependencies for all language wrappers

set -e

echo "=== SM Cross-Language Test Setup ==="
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 not found. Please install Python 3.7 or later."
    exit 1
fi
echo "✓ Python 3 found: $(python3 --version)"

if ! command_exists node; then
    echo "⚠️  Node.js not found. JavaScript wrapper will not be available."
else
    echo "✓ Node.js found: $(node --version)"
fi

if ! command_exists php; then
    echo "⚠️  PHP not found. PHP wrapper will not be available."
else
    echo "✓ PHP found: $(php --version | head -n1)"
fi

if ! command_exists go; then
    echo "⚠️  Go not found. Go wrapper will not be available."
else
    echo "✓ Go found: $(go version)"
fi

echo ""
echo "=== Installing Dependencies ==="
echo ""

# Python wrapper
echo "Installing Python dependencies..."
cd wrappers/py
if pip3 install -r requirements.txt; then
    echo "✓ Python dependencies installed"
else
    echo "⚠️  Failed to install Python dependencies"
fi
cd ../..

# JavaScript wrapper
if command_exists node; then
    echo "Installing JavaScript dependencies..."
    cd wrappers/js
    if npm install; then
        echo "✓ JavaScript dependencies installed"
    else
        echo "⚠️  Failed to install JavaScript dependencies"
    fi
    cd ../..
fi

# PHP wrapper
if command_exists php && command_exists composer; then
    echo "Installing PHP dependencies..."
    cd wrappers/php
    if composer install; then
        echo "✓ PHP dependencies installed"
    else
        echo "⚠️  Failed to install PHP dependencies"
    fi
    cd ../..
elif command_exists php; then
    echo "⚠️  Composer not found. Skipping PHP dependency installation."
fi

# Go wrapper
if command_exists go; then
    echo "Building Go wrapper..."
    cd wrappers/go
    if go mod tidy && go build -o wrapper wrapper.go; then
        echo "✓ Go wrapper built successfully"
    else
        echo "⚠️  Failed to build Go wrapper"
    fi
    cd ../..
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "To run tests:"
echo "  cd runner"
echo "  python3 runner.py"
echo ""
