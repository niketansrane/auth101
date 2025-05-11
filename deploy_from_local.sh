
#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo ".env file not found. Please create one with the required variables."
  exit 1
fi

# Variables (loaded from .env)
# RESOURCE_GROUP, WEBAPP_NAME, ZIP_FILE, STARTUP_FILE, LOCATION are expected to be defined in .env

# Update requirements.txt in case you have downloaded new packages
echo "Generating requirements.txt..."
pip freeze > requirements.txt

# Create a zip file excluding unnecessary files
echo "Creating zip file..."
zip -r $ZIP_FILE . -x ".*" -x "*__pycache__*"
echo "Contents of the zip file:" && unzip -l $ZIP_FILE

# Set the startup file configuration
echo "Setting startup file configuration..."
az webapp config set --startup-file $STARTUP_FILE --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP

# Deploy the zip file to the web app
echo "Deploying zip file to Azure Web App..."
az webapp deploy --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP --src-path $ZIP_FILE

echo "Deployment completed successfully!"