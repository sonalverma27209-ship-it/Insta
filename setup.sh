#!/bin/bash

echo "Setting up SHIVANSHI Instagram OSINT Tool"

pkg install python -y 2>/dev/null || sudo apt install python3 -y
pip install --upgrade pip
pip install instaloader colorama

chmod +x run.sh

echo "Setup completed"
echo "Run this command run.sh"
