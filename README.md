# Twitter Clone - DevOps Practice Project

A minimal Twitter-like application built with Django and PostgreSQL, containerized with Docker and deployable via Docker Compose or Terraform.

## Features

- 📝 Post tweets (max 280 characters) with optional images
- 📱 Simple, responsive web interface
- 🗄️ PostgreSQL database with persistent storage
- 🐳 Containerized with Docker
- 🚀 Deployable with Docker Compose or Terraform
- 🧪 Automated tests included

## Prerequisites

- **Docker Desktop** (for containers)
- **Docker Compose** (included with Docker Desktop)
- **Terraform** >= 1.7 (for Infrastructure as Code)
- **Git** (for cloning)

### macOS/Linux Installation

```bash
# Install Docker Desktop from https://docker.com/products/docker-desktop

# Install Terraform (macOS with Homebrew)
brew install terraform

# Or download from https://terraform.io/downloads
```

## Quick Start Options

### Option 1: Docker Compose (Recommended for Development)

```bash
# Clone the repository
git clone <repository-url>
cd dev_ops_twiter_clone

# Start the application
make setup-compose

# Or manually:
cp .env.example .env
docker compose up --build -d

# Visit http://localhost:8000
```

### Option 2: Terraform (Infrastructure as Code)

```bash
# Clone the repository
git clone <repository-url>
cd dev_ops_twiter_clone

# Setup with Terraform
make setup-terraform

# Or manually:
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
make tf-init
make tf-apply

# Visit http://localhost:8000
```

## Development Setup

### Local Development (without Docker)

```bash
# Create virtual environment
make venv
source venv/bin/activate

# Copy environment file
cp .env.example .env

# Start PostgreSQL locally (adjust POSTGRES_HOST in .env to localhost)
# Run migrations and start server
make run
```

### Running Tests

```bash
# With Docker Compose
docker compose exec web python manage.py test

# Or locally (after venv setup)
make test
```

## Makefile Commands

```bash
make help          # Show available commands
make venv          # Create virtual environment
make run           # Run Django dev server locally
make test          # Run tests locally
make build         # Build Docker image
make up            # Start with Docker Compose
make down          # Stop Docker Compose services
make tf-init       # Initialize Terraform
make tf-apply      # Deploy with Terraform
make tf-destroy    # Destroy Terraform resources
make clean         # Clean up Docker resources
```

## Project Structure

```
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── manage.py                   # Django management script
├── Makefile                    # Development automation
├── Dockerfile                  # Web app container definition
├── docker-compose.yml          # Multi-container setup
├── .env.example               # Environment variables template
├── config/                    # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tweets/                    # Django app
│   ├── models.py              # Tweet model
│   ├── views.py               # Web views
│   ├── forms.py               # Django forms
│   ├── urls.py                # URL routing
│   ├── admin.py               # Admin interface
│   └── tests/                 # Test suite
├── templates/                 # HTML templates
│   └── tweets/
├── docker/                    # Docker helper scripts
│   └── entrypoint.sh
└── terraform/                 # Infrastructure as Code
    ├── main.tf                # Main Terraform config
    ├── variables.tf           # Input variables
    ├── outputs.tf             # Output values
    ├── web.tf                 # Web container config
    ├── db.tf                  # Database container config
    └── terraform.tfvars.example
```

## Environment Configuration

### Environment Variables

Copy `.env.example` to `.env` and adjust as needed:

```bash
DJANGO_SECRET_KEY=changeme           # Change in production!
DJANGO_DEBUG=1                       # Set to 0 in production
DJANGO_ALLOWED_HOSTS=*               # Restrict in production
POSTGRES_DB=tweets
POSTGRES_USER=tweets
POSTGRES_PASSWORD=tweets             # Change in production!
POSTGRES_HOST=db                     # Container name for Docker
POSTGRES_PORT=5432
MEDIA_ROOT=/app/media
```

### Terraform Variables

Copy `terraform/terraform.tfvars.example` to `terraform/terraform.tfvars` and adjust:

```hcl
project_name = "tweets"
web_port     = 8000
django_secret_key    = "changeme"
postgres_password    = "tweets"
# ... other variables
```

## Usage

### Creating Your First Tweet

1. Open http://localhost:8000
2. Click "Post a Tweet"
3. Enter text (max 280 characters)
4. Optionally upload an image
5. Click "Post Tweet"
6. View your tweet on the home page

### Admin Interface

Access Django admin at http://localhost:8000/admin

Default credentials: `demo` / `demo12345`

## Docker Compose vs Terraform

### Docker Compose
- **Pros**: Simple, fast development, built-in networking
- **Cons**: Less infrastructure control, not production-ready
- **Use when**: Local development, quick prototyping

### Terraform
- **Pros**: Infrastructure as Code, version control, reproducible
- **Cons**: More complex, requires Terraform knowledge
- **Use when**: Production deployments, team environments

## Troubleshooting

### Common Issues

#### "Database is unavailable"
```bash
# Check database container
docker ps
docker logs <db-container-name>

# Restart services
make down && make up
```

#### Permission Denied (Media Files)
```bash
# Fix media directory permissions
docker compose exec web chown -R app:app /app/media
```

#### "Port already in use"
```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process or change port in .env
```

#### Migration Issues
```bash
# Reset database (⚠️ destroys data)
make down
docker volume prune -f
make up
```

#### Terraform State Issues
```bash
# If state is corrupted
cd terraform
terraform state list
terraform import docker_image.web tweets-web:dev
```

### Health Checks

```bash
# Check container health
docker ps

# Check logs
docker compose logs web
docker compose logs db

# Database connectivity
docker compose exec web python manage.py dbshell
```

## Testing

### Run All Tests
```bash
# Docker Compose
docker compose exec web python manage.py test

# Local
python manage.py test
```

### Test Coverage
```bash
# Install coverage
pip install coverage

# Run with coverage
coverage run manage.py test
coverage report
```

## Production Considerations

⚠️ **This is a development setup. For production:**

1. **Security**:
   - Change `DJANGO_SECRET_KEY`
   - Set `DJANGO_DEBUG=0`
   - Restrict `DJANGO_ALLOWED_HOSTS`
   - Use strong database passwords
   - Enable HTTPS

2. **Database**:
   - Use managed PostgreSQL service
   - Regular backups
   - Connection pooling

3. **Media Files**:
   - Use cloud storage (S3, GCS)
   - CDN for static files

4. **Monitoring**:
   - Application logs
   - Health checks
   - Error tracking

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Run tests: `make test`
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

---

## Quick Reference

### Essential Commands
```bash
# Docker Compose workflow
make up                    # Start everything
# Visit http://localhost:8000
make down                  # Stop everything

# Terraform workflow  
make tf-init               # One-time setup
make tf-apply              # Deploy
# Visit http://localhost:8000
make tf-destroy            # Cleanup

# Development
make venv                  # Local setup
make test                  # Run tests
make clean                 # Cleanup Docker
```

### File Locations
- Environment: `.env`
- Docker config: `docker-compose.yml`
- Terraform config: `terraform/`
- Django app: `tweets/`
- Templates: `templates/tweets/`
- Tests: `tweets/tests/`

Happy coding! 🚀 