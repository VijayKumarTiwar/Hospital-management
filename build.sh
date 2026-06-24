#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations
cd backend
python manage.py migrate

# Populate database with dummy data
python populate.py
