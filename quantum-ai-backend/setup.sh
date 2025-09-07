#!/bin/bash
echo "Setting up Quantum AI Backend..."
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt
echo "Creating virtual environment..."
python -m venv venv
echo "Activating virtual environment..."
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
echo "Setup complete! Don't forget to:"
echo "1. Update the .env file with your API keys"
echo "2. Run 'python main.py' to start the server"
