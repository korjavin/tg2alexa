#!/bin/bash

# Variables
IMAGE_NAME="ghcr.io/your-username/your-repo:latest"
CONTAINER_NAME="telegram-alexa-bridge"

# Stop and remove existing container
podman stop $CONTAINER_NAME || true
podman rm $CONTAINER_NAME || true

# Pull latest image
podman pull $IMAGE_NAME

# Run new container
podman run -d \
  --name $CONTAINER_NAME \
  --env-file .env \
  -p 80:80 \
  -p 443:443 \
  --restart unless-stopped \
  $IMAGE_NAME

# Clean up unused images
podman image prune -f