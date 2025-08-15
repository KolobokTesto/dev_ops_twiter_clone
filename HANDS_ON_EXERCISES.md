# Twitter Clone - Hands-On Learning Exercises

## 🎯 Overview

This guide provides structured, hands-on exercises to deepen your understanding of DevOps concepts using the Twitter clone project. Each exercise builds upon previous knowledge and introduces new concepts progressively.

---

## 📈 Learning Progression

### Phase 1: Foundation (Beginner)
- Django application basics
- Local development workflow
- Basic Docker concepts
- Environment management

### Phase 2: Containerization (Intermediate)
- Multi-container applications
- Volume and network management
- Production containerization
- Health checks and monitoring

### Phase 3: Infrastructure as Code (Advanced)
- Terraform fundamentals
- State management
- Resource dependencies
- Infrastructure scaling

### Phase 4: Production Readiness (Expert)
- Security hardening
- Monitoring and logging
- CI/CD implementation
- Performance optimization

---

## 🔬 Phase 1: Foundation Exercises

### Exercise 1.1: Django Application Exploration

**Objective**: Understand the Django application structure and data flow.

**Tasks**:
1. Set up local development environment
2. Analyze the Tweet model and its relationships
3. Trace a request from URL to database and back

**Instructions**:
```bash
# Step 1: Set up local environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Step 2: Examine the database
python manage.py migrate
python manage.py shell
```

**Django Shell Exploration**:
```python
# In Django shell (python manage.py shell)
from tweets.models import Tweet
from django.contrib.auth.models import User

# Create a user
user = User.objects.create_user('student', password='learning123')

# Create a tweet
tweet = Tweet.objects.create(text="My first tweet!", author=user)

# Examine the relationship
print(f"Tweet: {tweet}")
print(f"Author: {tweet.author}")
print(f"Created: {tweet.created_at}")

# Query tweets
tweets = Tweet.objects.all()
print(f"Total tweets: {tweets.count()}")

# Explore model methods
print(f"String representation: {str(tweet)}")
```

**Learning Goals**:
- Understand Django ORM relationships
- Practice model creation and querying
- Explore Django's built-in features

**Verification**:
- [ ] Successfully created user and tweet
- [ ] Understood the ForeignKey relationship
- [ ] Explored model methods and properties

### Exercise 1.2: Environment Configuration Deep Dive

**Objective**: Master environment-based configuration management.

**Tasks**:
1. Modify environment variables
2. Test configuration changes
3. Understand security implications

**Instructions**:
```bash
# Step 1: Copy and modify environment file
cp .env.example .env

# Step 2: Change database settings
# Edit .env file with different values
POSTGRES_DB=tweets_dev
POSTGRES_USER=dev_user
POSTGRES_PASSWORD=secure_password_123

# Step 3: Test configuration loading
python manage.py shell
```

**Configuration Testing**:
```python
# In Django shell
from django.conf import settings
import os

# Check loaded settings
print("Database config:")
print(f"DB Name: {settings.DATABASES['default']['NAME']}")
print(f"DB User: {settings.DATABASES['default']['USER']}")
print(f"DB Host: {settings.DATABASES['default']['HOST']}")

# Check environment variables
print("\nEnvironment variables:")
print(f"DEBUG: {os.getenv('DJANGO_DEBUG')}")
print(f"SECRET_KEY: {os.getenv('DJANGO_SECRET_KEY')[:10]}...")
```

**Security Exercise**:
```bash
# Generate a secure secret key
python -c "
import secrets
import string
alphabet = string.ascii_letters + string.digits
key = ''.join(secrets.choice(alphabet) for i in range(50))
print(f'DJANGO_SECRET_KEY={key}')
"
```

**Learning Goals**:
- Understand 12-Factor App configuration principles
- Practice secure configuration management
- Learn environment variable precedence

**Verification**:
- [ ] Successfully modified environment settings
- [ ] Generated secure secret key
- [ ] Understood configuration loading process

### Exercise 1.3: Request/Response Flow Analysis

**Objective**: Trace and understand the complete Django request flow.

**Tasks**:
1. Add logging to trace requests
2. Create a custom view
3. Analyze the complete data flow

**Instructions**:
```bash
# Step 1: Add logging configuration
# Add to config/settings.py
```

**Enhanced Logging Configuration**:
```python
# Add to config/settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'tweets': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

**Custom View with Logging**:
```python
# Add to tweets/views.py
import logging

logger = logging.getLogger('tweets')

def debug_tweet_create(request):
    """Debug version of tweet creation with detailed logging."""
    logger.info(f"Request method: {request.method}")
    logger.info(f"Request path: {request.path}")
    logger.info(f"Request user: {request.user}")
    
    if request.method == 'POST':
        logger.info(f"POST data: {request.POST}")
        logger.info(f"Files: {request.FILES}")
        
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            logger.info("Form is valid")
            tweet = form.save(commit=False)
            
            # Demo user creation with logging
            demo_user, created = User.objects.get_or_create(
                username='demo',
                defaults={'password': 'demo12345', 'is_active': True}
            )
            logger.info(f"Demo user {'created' if created else 'retrieved'}: {demo_user}")
            
            tweet.author = demo_user
            tweet.save()
            logger.info(f"Tweet saved: {tweet}")
            
            messages.success(request, 'Tweet posted successfully!')
            return redirect('tweet_list')
        else:
            logger.warning(f"Form validation failed: {form.errors}")
    else:
        logger.info("GET request - rendering empty form")
        form = TweetForm()
    
    logger.info("Rendering tweet form template")
    return render(request, 'tweets/tweet_form.html', {'form': form})
```

**URL Configuration**:
```python
# Add to tweets/urls.py
urlpatterns = [
    path('', views.tweet_list, name='tweet_list'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('debug-create/', views.debug_tweet_create, name='debug_tweet_create'),
]
```

**Learning Goals**:
- Understand Django request/response cycle
- Practice logging for debugging
- Analyze form processing workflow

**Verification**:
- [ ] Successfully added logging
- [ ] Created custom debug view
- [ ] Traced complete request flow

---

## 🐳 Phase 2: Containerization Exercises

### Exercise 2.1: Docker Image Optimization

**Objective**: Learn Docker best practices through hands-on optimization.

**Tasks**:
1. Analyze current Dockerfile
2. Optimize for size and security
3. Implement multi-stage builds

**Current Image Analysis**:
```bash
# Build and analyze current image
docker build -t tweets-web:current .
docker images tweets-web:current
docker history tweets-web:current

# Analyze image layers
docker run --rm tweets-web:current ls -la /app
```

**Optimized Dockerfile**:
```dockerfile
# Create: Dockerfile.optimized
# Multi-stage build for optimization
FROM python:3.12-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.12-slim

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libjpeg62-turbo \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Set up application
WORKDIR /app
COPY . .
RUN chown -R appuser:appuser /app

# Create media directory
RUN mkdir -p /app/media && chown appuser:appuser /app/media

# Switch to non-root user
USER appuser

# Update PATH
ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8000

COPY docker/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
```

**Size Comparison**:
```bash
# Build optimized version
docker build -f Dockerfile.optimized -t tweets-web:optimized .

# Compare sizes
docker images | grep tweets-web

# Analyze security improvements
docker run --rm tweets-web:optimized whoami
docker run --rm tweets-web:optimized id
```

**Learning Goals**:
- Understand Docker layer caching
- Practice multi-stage builds
- Implement security best practices

**Verification**:
- [ ] Reduced image size by at least 20%
- [ ] Implemented non-root user
- [ ] Maintained full functionality

### Exercise 2.2: Advanced Docker Compose Configuration

**Objective**: Master Docker Compose advanced features and production patterns.

**Tasks**:
1. Add development vs production configurations
2. Implement health checks
3. Add monitoring containers

**Development Override**:
```yaml
# Create: docker-compose.override.yml (automatically loaded)
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - .:/app  # Hot reload for development
    environment:
      - DJANGO_DEBUG=1
    command: python manage.py runserver 0.0.0.0:8000

  db:
    ports:
      - "5432:5432"  # Expose DB port for debugging
```

**Production Configuration**:
```yaml
# Create: docker-compose.prod.yml
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile.optimized
    restart: unless-stopped
    environment:
      - DJANGO_DEBUG=0
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  db:
    restart: unless-stopped
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $POSTGRES_USER -d $POSTGRES_DB"]
      interval: 10s
      timeout: 5s
      retries: 5

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - media:/var/www/media
    depends_on:
      - web
    restart: unless-stopped

volumes:
  pgdata:
  media:
```

**Nginx Configuration**:
```nginx
# Create: nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream web {
        server web:8000;
    }

    server {
        listen 80;
        
        location / {
            proxy_pass http://web;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        
        location /media/ {
            alias /var/www/media/;
        }
    }
}
```

**Health Check Testing**:
```bash
# Start production stack
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Monitor health status
watch docker-compose ps

# Test health endpoints
curl -f http://localhost/
docker-compose exec web python manage.py check --deploy
```

**Learning Goals**:
- Understand Compose configuration inheritance
- Implement proper health checks
- Practice reverse proxy configuration

**Verification**:
- [ ] Development hot reload works
- [ ] Production health checks pass
- [ ] Nginx reverse proxy functions correctly

### Exercise 2.3: Container Debugging and Troubleshooting

**Objective**: Develop skills for debugging containerized applications.

**Tasks**:
1. Simulate common container problems
2. Practice debugging techniques
3. Implement monitoring solutions

**Debugging Scenarios**:

**Scenario 1: Database Connection Issues**
```bash
# Simulate: Start web without database
docker run --name test-web -p 8000:8000 tweets-web:dev

# Debug: Check logs
docker logs test-web

# Debug: Interactive container exploration
docker run -it --entrypoint /bin/bash tweets-web:dev
# Inside container:
env | grep POSTGRES
ping db  # Will fail - no network
```

**Scenario 2: Permission Issues**
```bash
# Simulate: Wrong volume permissions
docker volume create test-media
docker run -v test-media:/app/media tweets-web:dev

# Debug: Check permissions
docker run -v test-media:/app/media --entrypoint /bin/bash -it tweets-web:dev
ls -la /app/media
```

**Debugging Tools Container**:
```yaml
# Add to docker-compose.debug.yml
version: '3.8'

services:
  debug:
    image: nicolaka/netshoot
    command: sleep infinity
    networks:
      - tweets_net
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock

networks:
  tweets_net:
    external: true
```

**Debugging Commands**:
```bash
# Network debugging
docker-compose -f docker-compose.debug.yml run debug nslookup db
docker-compose -f docker-compose.debug.yml run debug curl web:8000

# Container inspection
docker inspect tweets_web | jq '.[0].NetworkSettings.Networks'
docker exec tweets_web netstat -tulpn

# Performance monitoring
docker stats
docker exec tweets_web top
docker exec tweets_db pg_stat_activity
```

**Learning Goals**:
- Master container debugging techniques
- Understand networking and volumes
- Practice systematic troubleshooting

**Verification**:
- [ ] Successfully debugged connection issues
- [ ] Resolved permission problems
- [ ] Used debugging tools effectively

---

## 🏗️ Phase 3: Infrastructure as Code Exercises

### Exercise 3.1: Terraform State Management

**Objective**: Understand Terraform state and lifecycle management.

**Tasks**:
1. Explore Terraform state
2. Practice state manipulation
3. Implement remote state storage

**State Exploration**:
```bash
# Initial deployment
cd terraform
terraform init
terraform plan
terraform apply

# Examine state
terraform state list
terraform state show docker_container.web
terraform show
```

**State Manipulation**:
```bash
# Import existing resources
docker run -d --name manual-container nginx
terraform import docker_container.manual manual-container

# Move resources
terraform state mv docker_container.web docker_container.web_renamed

# Remove from state (without destroying)
terraform state rm docker_container.manual
```

**Remote State Configuration**:
```hcl
# Add to terraform/backend.tf
terraform {
  backend "local" {
    path = "terraform.tfstate.backup"
  }
  # For teams, use remote backend:
  # backend "s3" {
  #   bucket = "my-terraform-state"
  #   key    = "tweets/terraform.tfstate"
  #   region = "us-west-2"
  # }
}
```

**State Backup and Recovery**:
```bash
# Backup current state
cp terraform.tfstate terraform.tfstate.backup

# Simulate state corruption
echo "invalid json" > terraform.tfstate

# Restore from backup
cp terraform.tfstate.backup terraform.tfstate

# Verify recovery
terraform plan
```

**Learning Goals**:
- Understand Terraform state concepts
- Practice state manipulation commands
- Learn backup and recovery procedures

**Verification**:
- [ ] Successfully explored state structure
- [ ] Practiced state manipulation safely
- [ ] Implemented backup procedures

### Exercise 3.2: Resource Dependencies and Provisioners

**Objective**: Master Terraform resource relationships and advanced features.

**Tasks**:
1. Create complex resource dependencies
2. Use provisioners for configuration
3. Implement data sources

**Enhanced Infrastructure**:
```hcl
# Add to terraform/monitoring.tf
# Data source for existing network
data "docker_network" "tweets_net" {
  name = docker_network.tweets_net.name
}

# Redis cache container
resource "docker_image" "redis" {
  name = "redis:7-alpine"
}

resource "docker_container" "redis" {
  image = docker_image.redis.image_id
  name  = "${var.project_name}_redis"

  ports {
    internal = 6379
    external = 6379
  }

  networks_advanced {
    name = docker_network.tweets_net.name
  }

  restart = "unless-stopped"
}

# Update web container to depend on Redis
resource "docker_container" "web" {
  # ... existing configuration
  
  env = [
    "DJANGO_SECRET_KEY=${var.django_secret_key}",
    "REDIS_URL=redis://${docker_container.redis.name}:6379/0",
    # ... other env vars
  ]

  depends_on = [
    docker_container.db,
    docker_container.redis
  ]

  # Provisioner to wait for services
  provisioner "local-exec" {
    command = "sleep 30 && curl -f http://localhost:${var.web_port}/ || exit 1"
  }

  # Provisioner to run health check
  provisioner "local-exec" {
    when    = create
    command = "docker exec ${self.name} python manage.py check --deploy"
  }
}
```

**Monitoring Stack**:
```hcl
# Add to terraform/monitoring.tf
resource "docker_image" "grafana" {
  name = "grafana/grafana:latest"
}

resource "docker_container" "grafana" {
  image = docker_image.grafana.image_id
  name  = "${var.project_name}_grafana"

  ports {
    internal = 3000
    external = 3000
  }

  env = [
    "GF_SECURITY_ADMIN_PASSWORD=admin"
  ]

  volumes {
    volume_name    = docker_volume.grafana_data.name
    container_path = "/var/lib/grafana"
  }

  networks_advanced {
    name = docker_network.tweets_net.name
  }
}

resource "docker_volume" "grafana_data" {
  name = "${var.project_name}_grafana_data"
}
```

**Dependency Visualization**:
```bash
# Generate dependency graph
terraform graph | dot -Tpng > terraform-graph.png

# Apply with parallelism control
terraform apply -parallelism=2

# Force replacement of specific resource
terraform apply -replace=docker_container.web
```

**Learning Goals**:
- Understand implicit vs explicit dependencies
- Practice using provisioners effectively
- Learn data source usage patterns

**Verification**:
- [ ] Created complex resource dependencies
- [ ] Used provisioners for validation
- [ ] Generated dependency visualizations

### Exercise 3.3: Terraform Modules and Scaling

**Objective**: Create reusable Terraform modules and scaling patterns.

**Tasks**:
1. Extract functionality into modules
2. Create scaling configurations
3. Implement variable validation

**Module Structure**:
```
terraform/
├── modules/
│   ├── web-app/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── database/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
└── environments/
    ├── dev/
    └── prod/
```

**Web App Module**:
```hcl
# modules/web-app/main.tf
variable "project_name" {
  type = string
}

variable "image_tag" {
  type = string
}

variable "replicas" {
  type    = number
  default = 1
  
  validation {
    condition     = var.replicas >= 1 && var.replicas <= 10
    error_message = "Replicas must be between 1 and 10."
  }
}

variable "network_name" {
  type = string
}

resource "docker_container" "web" {
  count = var.replicas
  
  image = var.image_tag
  name  = "${var.project_name}_web_${count.index}"

  ports {
    internal = 8000
    external = 8000 + count.index
  }

  networks_advanced {
    name = var.network_name
  }
}

output "container_names" {
  value = docker_container.web[*].name
}

output "ports" {
  value = docker_container.web[*].ports
}
```

**Environment-Specific Configuration**:
```hcl
# environments/dev/main.tf
module "web_app" {
  source = "../../modules/web-app"
  
  project_name = "tweets-dev"
  image_tag    = "tweets-web:dev"
  replicas     = 1
  network_name = docker_network.dev_network.name
}

module "database" {
  source = "../../modules/database"
  
  project_name = "tweets-dev"
  db_password  = "dev_password"
  network_name = docker_network.dev_network.name
}

# environments/prod/main.tf
module "web_app" {
  source = "../../modules/web-app"
  
  project_name = "tweets-prod"
  image_tag    = "tweets-web:latest"
  replicas     = 3
  network_name = docker_network.prod_network.name
}
```

**Load Balancer Module**:
```hcl
# modules/load-balancer/main.tf
variable "upstream_containers" {
  type = list(object({
    name = string
    port = number
  }))
}

locals {
  nginx_config = templatefile("${path.module}/nginx.conf.tpl", {
    upstreams = var.upstream_containers
  })
}

resource "docker_container" "nginx" {
  image = "nginx:alpine"
  name  = "${var.project_name}_lb"

  ports {
    internal = 80
    external = 80
  }

  upload {
    content = local.nginx_config
    file    = "/etc/nginx/nginx.conf"
  }
}
```

**Scaling Commands**:
```bash
# Scale up web containers
terraform apply -var="web_replicas=3"

# Environment-specific deployment
cd environments/prod
terraform init
terraform apply

# Module testing
cd modules/web-app
terraform init
terraform apply -var="project_name=test" -var="image_tag=nginx" -var="network_name=bridge"
```

**Learning Goals**:
- Create reusable Terraform modules
- Implement scaling patterns
- Practice environment separation

**Verification**:
- [ ] Created functional modules
- [ ] Implemented scaling configurations
- [ ] Successfully deployed multiple environments

---

## 🚀 Phase 4: Production Readiness Exercises

### Exercise 4.1: Security Hardening

**Objective**: Implement comprehensive security measures.

**Tasks**:
1. Audit current security posture
2. Implement security hardening
3. Add security monitoring

**Security Audit**:
```bash
# Container security scanning
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image tweets-web:dev

# Django security check
docker-compose exec web python manage.py check --deploy

# Network security analysis
docker network ls
docker network inspect tweets_net
```

**Hardened Django Settings**:
```python
# Create: config/settings_production.py
from .settings import *

# Security Settings
DEBUG = False
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')

# HTTPS Security
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Content Security
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Session Security
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'

# CSRF Security
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'

# Database Connection Security
DATABASES['default']['OPTIONS'] = {
    'sslmode': 'require',
}

# Logging Security Events
LOGGING['loggers']['django.security'] = {
    'handlers': ['console'],
    'level': 'WARNING',
}
```

**Secrets Management**:
```bash
# Generate strong passwords
openssl rand -base64 32

# Docker secrets (Docker Swarm)
echo "strong_db_password" | docker secret create db_password -

# Environment secrets
export DJANGO_SECRET_KEY=$(python -c "
import secrets
import string
alphabet = string.ascii_letters + string.digits + '!@#$%^&*'
print(''.join(secrets.choice(alphabet) for i in range(50)))
")
```

**Security Headers with Nginx**:
```nginx
# Update: nginx.conf
server {
    listen 80;
    
    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=tweets:10m rate=10r/m;
    
    location / {
        limit_req zone=tweets burst=20 nodelay;
        proxy_pass http://web;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Learning Goals**:
- Identify security vulnerabilities
- Implement defense-in-depth strategy
- Practice secrets management

**Verification**:
- [ ] Passed security audit
- [ ] Implemented security headers
- [ ] Configured secure secrets management

### Exercise 4.2: Monitoring and Observability

**Objective**: Implement comprehensive monitoring stack.

**Tasks**:
1. Add application metrics
2. Implement log aggregation
3. Create alerting rules

**Application Metrics**:
```python
# Add to requirements.txt
django-prometheus==2.3.1

# Add to config/settings.py
INSTALLED_APPS = [
    # ... existing apps
    'django_prometheus',
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    # ... existing middleware
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

# Database metrics
DATABASES['default']['ENGINE'] = 'django_prometheus.db.backends.postgresql'
```

**Custom Metrics**:
```python
# Add to tweets/metrics.py
from prometheus_client import Counter, Histogram
import time

# Custom metrics
TWEET_CREATED_COUNTER = Counter('tweets_created_total', 'Total tweets created')
TWEET_REQUEST_DURATION = Histogram('tweet_request_duration_seconds', 'Tweet request duration')

def track_tweet_creation():
    """Decorator to track tweet creation metrics."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                TWEET_CREATED_COUNTER.inc()
                return result
            finally:
                TWEET_REQUEST_DURATION.observe(time.time() - start_time)
        return wrapper
    return decorator

# Update tweets/views.py
from .metrics import track_tweet_creation

@track_tweet_creation()
def tweet_create(request):
    # ... existing code
```

**Monitoring Stack**:
```yaml
# Add to docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
    networks:
      - tweets_net

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana-dashboards:/etc/grafana/provisioning/dashboards
    networks:
      - tweets_net

  alertmanager:
    image: prom/alertmanager:latest
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml
    networks:
      - tweets_net

volumes:
  prometheus_data:
  grafana_data:
```

**Prometheus Configuration**:
```yaml
# Create: prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'django'
    static_configs:
      - targets: ['web:8000']
    metrics_path: '/metrics'

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
```

**Alert Rules**:
```yaml
# Create: alert_rules.yml
groups:
  - name: tweets_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(django_http_responses_total{status=~"5.."}[5m]) > 0.1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: High error rate detected

      - alert: DatabaseDown
        expr: up{job="postgres"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: PostgreSQL database is down
```

**Log Aggregation**:
```yaml
# Add to docker-compose.logging.yml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.8.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data

  logstash:
    image: docker.elastic.co/logstash/logstash:8.8.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf

  kibana:
    image: docker.elastic.co/kibana/kibana:8.8.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
```

**Learning Goals**:
- Implement application monitoring
- Create custom metrics
- Set up alerting systems

**Verification**:
- [ ] Metrics visible in Prometheus
- [ ] Grafana dashboards functional
- [ ] Alerts triggering correctly

### Exercise 4.3: CI/CD Pipeline Implementation

**Objective**: Create automated deployment pipeline.

**Tasks**:
1. Set up automated testing
2. Implement build pipeline
3. Configure deployment automation

**GitHub Actions Workflow**:
```yaml
# Create: .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_tweets
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'

    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run linting
      run: |
        pip install flake8 black
        flake8 . --count --max-line-length=88 --extend-ignore=E203
        black --check .

    - name: Run tests
      run: python manage.py test
      env:
        POSTGRES_HOST: localhost
        POSTGRES_PORT: 5432
        POSTGRES_DB: test_tweets
        POSTGRES_USER: postgres
        POSTGRES_PASSWORD: postgres
        DJANGO_SECRET_KEY: test-secret-key

    - name: Run security checks
      run: |
        pip install safety bandit
        safety check
        bandit -r . -x tests/

  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=sha

    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        platforms: linux/amd64,linux/arm64
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    environment: staging
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Deploy to staging
      run: |
        # Update image tag in terraform variables
        sed -i 's/tweets-web:dev/tweets-web:${{ github.sha }}/g' terraform/terraform.tfvars
        
        # Deploy with Terraform
        cd terraform
        terraform init
        terraform plan
        terraform apply -auto-approve

  deploy-production:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Deploy to production
      run: |
        # Production deployment with approval
        echo "Deploying to production..."
        # Add production deployment logic here
```

**Pre-commit Hooks**:
```yaml
# Create: .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pycqa/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ["-x", "tests/"]
```

**Deployment Scripts**:
```bash
#!/bin/bash
# Create: scripts/deploy.sh

set -e

ENVIRONMENT=${1:-staging}
IMAGE_TAG=${2:-latest}

echo "Deploying to $ENVIRONMENT with image tag $IMAGE_TAG"

# Update configuration
envsubst < terraform/terraform.tfvars.template > terraform/terraform.tfvars

# Deploy infrastructure
cd terraform
terraform init
terraform plan -var="image_tag=$IMAGE_TAG"
terraform apply -auto-approve

# Verify deployment
echo "Verifying deployment..."
curl -f http://localhost:8000/ || exit 1

echo "Deployment successful!"
```

**Testing Environment**:
```yaml
# Create: docker-compose.test.yml
version: '3.8'

services:
  test-db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: test_tweets
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
    tmpfs:
      - /var/lib/postgresql/data

  test-web:
    build: .
    environment:
      POSTGRES_HOST: test-db
      POSTGRES_DB: test_tweets
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
      DJANGO_SECRET_KEY: test-secret
    depends_on:
      - test-db
    command: |
      bash -c "
        python manage.py migrate &&
        python manage.py test &&
        python manage.py check --deploy
      "
```

**Learning Goals**:
- Implement automated testing
- Create CI/CD pipelines
- Practice deployment automation

**Verification**:
- [ ] CI pipeline runs on commits
- [ ] Automated tests pass
- [ ] Deployment pipeline functional

---

## 🎯 Final Project: Production Deployment

### Objective
Deploy the Twitter clone to a production-like environment with full DevOps practices.

### Requirements
1. **Infrastructure**: Use Terraform to deploy to cloud provider (AWS/GCP/Azure)
2. **Security**: Implement all security best practices
3. **Monitoring**: Full observability stack deployed
4. **CI/CD**: Automated pipeline with staging and production environments
5. **Documentation**: Complete runbook and troubleshooting guide

### Deliverables
- [ ] Cloud infrastructure deployed via Terraform
- [ ] SSL certificates and domain configuration
- [ ] Monitoring dashboards and alerting
- [ ] CI/CD pipeline with multiple environments
- [ ] Load testing and performance optimization
- [ ] Disaster recovery procedures
- [ ] Complete documentation

### Evaluation Criteria
- Infrastructure reproducibility
- Security posture
- Monitoring coverage
- Automation completeness
- Documentation quality

---

## 📈 Learning Assessment

### Knowledge Check Questions

1. **Django Architecture**: Explain the request flow from URL to database response.
2. **Docker Optimization**: What are the benefits of multi-stage builds?
3. **Terraform State**: How does Terraform track infrastructure changes?
4. **Security**: List 5 security measures implemented in this project.
5. **Monitoring**: What metrics would you track for a production web application?

### Practical Challenges

1. **Debug Challenge**: Given a failing container, identify and fix the issue.
2. **Scaling Challenge**: Modify the infrastructure to handle 10x traffic.
3. **Security Challenge**: Implement authentication and authorization.
4. **Performance Challenge**: Optimize database queries and add caching.
5. **Disaster Recovery**: Implement backup and restore procedures.

---

## 🎓 Next Steps

### Advanced Topics to Explore
- Kubernetes orchestration
- Service mesh implementation
- Advanced monitoring with distributed tracing
- GitOps workflows
- Infrastructure testing

### Career Pathways
- **DevOps Engineer**: Focus on automation and infrastructure
- **Site Reliability Engineer**: Emphasize monitoring and reliability
- **Platform Engineer**: Build internal developer platforms
- **Cloud Architect**: Design cloud-native solutions
- **Security Engineer**: Specialize in DevSecOps practices

---

This hands-on guide provides structured learning experiences that build from basic concepts to production-ready deployments. Each exercise includes clear objectives, step-by-step instructions, and verification criteria to ensure solid understanding of DevOps principles and practices. 