# Deployment Guide

This guide provides step-by-step instructions for deploying the Construction Management Server to production environments.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Production Setup](#production-setup)
- [Database Configuration](#database-configuration)
- [Web Server Setup](#web-server-setup)
- [Process Management](#process-management)
- [Monitoring and Logging](#monitoring-and-logging)
- [Security Hardening](#security-hardening)
- [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

- **Server**: Ubuntu 20.04+ or equivalent Linux distribution
- **Python**: 3.12+
- **Database**: PostgreSQL 12+
- **Cache**: Redis 6+
- **Web Server**: Nginx or Apache
- **Process Manager**: Supervisor or systemd
- **SSL Certificate**: Let's Encrypt or commercial certificate

## 🚀 Production Setup

### 1. Server Preparation

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y python3.12 python3.12-venv python3-pip
sudo apt install -y postgresql postgresql-contrib nginx redis-server
sudo apt install -y build-essential libpq-dev
```

### 2. Application Setup

```bash
# Create application user
sudo useradd -m -s /bin/bash construction
sudo su - construction

# Clone repository
git clone https://github.com/your-org/construction-management-server.git
cd construction-management-server

# Create virtual environment
python3.12 -m venv env
source env/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

### 3. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

**Production `.env` Configuration:**

```env
environment=production
DEBUG=False
SECRET_KEY='generate-strong-secret-key-here'
ALLOWED_HOSTS='yourdomain.com,www.yourdomain.com'

# Database
DATABASE_URL=postgresql://construction:strong_password@localhost:5432/construction_db

# Redis
REDIS_URL=redis://localhost:6379/0

# CORS
FRONTEND_URL="https://yourdomain.com"
CORS_ALLOWED_ORIGINS="https://yourdomain.com,https://www.yourdomain.com"

# Email (optional but recommended)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
```

### 4. Generate Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 💾 Database Configuration

### PostgreSQL Setup

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE construction_db;
CREATE USER construction WITH PASSWORD 'strong_password';
GRANT ALL PRIVILEGES ON DATABASE construction_db TO construction;
\q
```

### Run Migrations

```bash
cd /home/construction/construction-management-server
source env/bin/activate
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## 🌐 Web Server Setup

### Nginx Configuration

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/construction-management
```

**Nginx Configuration:**

```nginx
upstream construction_backend {
    server unix:/home/construction/construction-management-server/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Media and Static Files
    location /media/ {
        alias /home/construction/construction-management-server/media/;
        expires 30d;
    }

    location /static/ {
        alias /home/construction/construction-management-server/staticfiles/;
        expires 30d;
    }

    # Proxy to Gunicorn
    location / {
        proxy_pass http://construction_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

### Enable Nginx Configuration

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/construction-management /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

## 🔄 Process Management

### Gunicorn Configuration

Create Gunicorn systemd service:

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

**Gunicorn Service Configuration:**

```ini
[Unit]
Description=Gunicorn daemon for Construction Management
After=network.target

[Service]
User=construction
Group=construction
WorkingDirectory=/home/construction/construction-management-server
ExecStart=/home/construction/construction-management-server/env/bin/gunicorn \
          --workers 3 \
          --bind unix:/home/construction/construction-management-server/gunicorn.sock \
          construction_server.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Start and Enable Services

```bash
# Reload systemd
sudo systemctl daemon-reload

# Start Gunicorn
sudo systemctl start gunicorn

# Enable Gunicorn to start on boot
sudo systemctl enable gunicorn

# Check status
sudo systemctl status gunicorn
```

## 🔒 Security Hardening

### SSL Certificate Setup

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal setup (already configured by certbot)
sudo certbot renew --dry-run
```

### Firewall Configuration

```bash
# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

### Database Security

```bash
# Edit PostgreSQL configuration
sudo nano /etc/postgresql/12/main/postgresql.conf

# Listen only on localhost
listen_addresses = 'localhost'

# Require MD5 encryption
password_encryption = md5

# Restart PostgreSQL
sudo systemctl restart postgresql
```

### Application Security

```bash
# Set proper file permissions
sudo chown -R construction:construction /home/construction/construction-management-server
sudo chmod -R 750 /home/construction/construction-management-server
sudo chmod 600 /home/construction/construction-management-server/.env
```

## 📊 Monitoring and Logging

### Application Logging

Configure logging in Django settings:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/home/construction/construction-management-server/logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Log Rotation

```bash
# Create logrotate configuration
sudo nano /etc/logrotate.d/construction-management
```

**Logrotate Configuration:**

```
/home/construction/construction-management-server/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 construction construction
}
```

### Monitoring Tools

```bash
# Install monitoring tools
sudo apt install -y htop iotop

# Monitor system resources
htop

# Monitor disk I/O
sudo iotop
```

## 🚨 Troubleshooting

### Application Not Starting

```bash
# Check Gunicorn status
sudo systemctl status gunicorn

# Check Gunicorn logs
sudo journalctl -u gunicorn -f

# Check application logs
tail -f /home/construction/construction-management-server/logs/django.log
```

### Database Connection Issues

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-12-main.log

# Test database connection
psql -U construction -d construction_db
```

### Nginx Configuration Issues

```bash
# Test Nginx configuration
sudo nginx -t

# Check Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Check Nginx access logs
sudo tail -f /var/log/nginx/access.log
```

### Redis Connection Issues

```bash
# Check Redis status
sudo systemctl status redis-server

# Test Redis connection
redis-cli ping

# Check Redis logs
sudo tail -f /var/log/redis/redis-server.log
```

## 🔄 Updates and Maintenance

### Application Updates

```bash
# Switch to application user
sudo su - construction

# Navigate to project directory
cd construction-management-server

# Activate virtual environment
source env/bin/activate

# Pull latest changes
git pull origin main

# Install new dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart Gunicorn
sudo systemctl restart gunicorn
```

### Database Backup

```bash
# Create backup script
nano backup-db.sh
```

**Backup Script:**

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/construction/backups"
BACKUP_FILE="$BACKUP_DIR/construction_db_$DATE.dump"

mkdir -p $BACKUP_DIR
pg_dump -U construction construction_db > $BACKUP_FILE

# Keep only last 7 days of backups
find $BACKUP_DIR -name "construction_db_*.dump" -mtime +7 -delete

echo "Backup completed: $BACKUP_FILE"
```

```bash
# Make script executable
chmod +x backup-db.sh

# Add to crontab for daily backups
crontab -e

# Add line for daily backup at 2 AM
0 2 * * * /home/construction/construction-management-server/backup-db.sh
```

## 📞 Support

For deployment issues or questions:

- **Email**: support@construction-management.com
- **Documentation**: Check README.md and API documentation
- **Issues**: Create GitHub issue with detailed information

## 📝 Additional Resources

- [Django Production Deployment Guide](https://docs.djangoproject.com/en/5.2/howto/deployment/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)

---

**Last Updated**: 2026-04-17
**Version**: 1.0.0
