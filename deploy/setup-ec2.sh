#!/bin/bash
# EC2 Setup Script — Run this on a fresh Ubuntu EC2 instance
# Usage: ssh into EC2 then: bash setup-ec2.sh

set -e

echo "=== Installing Docker ==="
sudo apt-get update -y
sudo apt-get install -y docker.io docker-compose-v2 awscli
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

echo "=== Logging into ECR ==="
AWS_REGION="ap-south-1"
AWS_ACCOUNT="713502469196"
ECR_URL="${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com"

aws ecr get-login-password --region $AWS_REGION | sudo docker login --username AWS --password-stdin $ECR_URL

echo "=== Pulling images ==="
sudo docker pull ${ECR_URL}/ai-persona-backend:latest
sudo docker pull ${ECR_URL}/ai-persona-frontend:latest

echo "=== Creating docker-compose.yml ==="
mkdir -p ~/ai-persona
cat > ~/ai-persona/docker-compose.yml << 'COMPOSE'
services:
  backend:
    image: 713502469196.dkr.ecr.ap-south-1.amazonaws.com/ai-persona-backend:latest
    container_name: ai-persona-backend
    env_file: ./.env
    ports:
      - "8001:8000"
    restart: unless-stopped

  frontend:
    image: 713502469196.dkr.ecr.ap-south-1.amazonaws.com/ai-persona-frontend:latest
    container_name: ai-persona-frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: ai-persona-nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - backend
      - frontend
    restart: unless-stopped
COMPOSE

echo "=== Creating nginx.conf ==="
cat > ~/ai-persona/nginx.conf << 'NGINX'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://frontend:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    location /api/ {
        proxy_pass http://backend:8000/api/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
    }

    location /health {
        proxy_pass http://backend:8000/health;
    }
}
NGINX

echo "=== Setup complete ==="
echo ""
echo "Next steps:"
echo "1. Create .env file:  nano ~/ai-persona/.env"
echo "2. Start services:    cd ~/ai-persona && sudo docker compose up -d"
echo "3. Check status:      sudo docker compose ps"
echo "4. View logs:         sudo docker compose logs -f"
echo ""
echo "Don't forget to update Vapi webhook URL to: http://<EC2-PUBLIC-IP>/api/vapi/webhook"
