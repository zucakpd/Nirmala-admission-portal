#!/bin/bash

# Nirmala Admission Portal - Quick Start Script

echo "========================================"
echo "  NIRMALA ADMISSION PORTAL"
echo "  Quick Start Script"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt --break-system-packages

# Run the application
echo ""
echo "========================================"
echo "  Starting the server..."
echo "========================================"
echo ""
echo "The portal will be available at:"
echo "  http://localhost:5000"
echo ""
echo "Default Login Credentials:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
