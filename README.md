# Telegram to Alexa Bridge

This application bridges Telegram messages to Alexa devices, allowing you to send messages from Telegram that your Alexa devices will speak.

## Prerequisites

1. Amazon Developer Account
2. Telegram Bot Token
3. Domain name pointing to your server's IP address

## Setup Instructions

### 1. Create Alexa Skill

1. Go to [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask)
2. Create new skill:
   - Skill name: Telegram Bridge
   - Choose "Custom" model
   - Choose "Provision your own" backend
3. In the Interaction Model:
   - Add new intent "MessageIntent" with sample utterance "read my messages"
4. In the Endpoint:
   - Set Service Endpoint Type to HTTPS
   - Enter your domain URL (e.g., https://yourdomain.com/alexa)

### 2. Configure Telegram Bot

1. Create new bot using [BotFather](https://core.telegram.org/bots#botfather)
2. Set webhook:
   ```bash
   curl -F "url=https://yourdomain.com/telegram" \
   https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook
   ```

### 3. Environment Variables

Create `.env` file with following variables:

```bash
TELEGRAM_TOKEN=your_telegram_bot_token
ALEXA_APP_ID=your_alexa_app_id
DOMAIN_NAME=your.domain.com
LETSENCRYPT_EMAIL=your@email.com
```

### 4. Deployment

1. Build and push Docker image:
   ```bash
   docker build -t your-image-name .
   docker push your-image-name
   ```

2. Deploy to your server using Podman:
   ```bash
   podman run -d \
     --name telegram-alexa-bridge \
     --env-file .env \
     -p 80:80 -p 443:443 \
     your-image-name
   ```

## Activating the Skill

1. Open Alexa app on your phone
2. Go to Skills & Games
3. Search for "Telegram Bridge"
4. Enable the skill and link your account
5. Say "Alexa, open Telegram Bridge" to start using it

## HTTPS Setup

Caddy will automatically:
- Obtain Let's Encrypt certificates using HTTP-01 challenge
- Handle certificate renewals
- Redirect HTTP to HTTPS
- Serve your application over HTTPS