#!/bin/bash

# This script helps set up your Heroku app after connecting it to GitHub
# Usage: bash heroku-setup.sh your-app-name

if [ -z "$1" ]; then
  echo "Please provide your Heroku app name"
  echo "Usage: bash heroku-setup.sh your-app-name"
  exit 1
fi

APP_NAME=$1

echo "Setting up $APP_NAME on Heroku..."

# Ensure Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
  echo "Heroku CLI is not installed. Please install it first."
  exit 1
fi

# Check if logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
  echo "Please log in to Heroku first using 'heroku login'"
  exit 1
fi

# Enable auto migrations via release phase
echo "Ensuring release phase is configured..."
heroku buildpacks:clear -a $APP_NAME
heroku buildpacks:set heroku/python -a $APP_NAME

# Add PostgreSQL add-on
echo "Adding PostgreSQL add-on..."
heroku addons:create heroku-postgresql:hobby-dev -a $APP_NAME

# Add Redis add-on
echo "Adding Redis add-on..."
heroku addons:create heroku-redis:hobby-dev -a $APP_NAME

# Ensure environment variables are set
echo "Setting up environment variables..."
heroku config:set DEBUG=False -a $APP_NAME
heroku config:set DISABLE_COLLECTSTATIC=0 -a $APP_NAME

echo ""
echo "IMPORTANT: You still need to set these environment variables manually:"
echo "1. heroku config:set SECRET_KEY=your-secret-key -a $APP_NAME"
echo "2. heroku config:set OPENAI_API_KEY=your-openai-api-key -a $APP_NAME"

echo ""
echo "After deployment, you'll need to create a superuser:"
echo "heroku run python manage.py createsuperuser -a $APP_NAME"

echo ""
echo "Setup complete! You can now connect your GitHub repository to this Heroku app."
echo "After deployment, check if your workers are running:"
echo "heroku ps:scale worker=1 -a $APP_NAME" 