.PHONY: help venv run test build up down tf-init tf-apply tf-destroy clean reset

# Default target
help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@egrep '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

# Development targets
venv: ## Create and activate virtual environment, install dependencies
	python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt
	@echo "Virtual environment created. Activate with: source venv/bin/activate"

run: ## Run Django development server locally
	python manage.py migrate
	python manage.py runserver

test: ## Run Django tests
	python manage.py test

# Docker targets
build: ## Build Docker image for web application
	docker build -t tweets-web:dev .

up: ## Start services with Docker Compose
	cp .env.example .env 2>/dev/null || true
	docker compose up --build -d
	@echo "Services started. Visit http://localhost:8000"

down: ## Stop and remove Docker Compose services
	docker compose down -v

# Terraform targets  
tf-init: ## Initialize Terraform
	cd terraform && terraform init

tf-apply: ## Apply Terraform configuration
	cp terraform/terraform.tfvars.example terraform/terraform.tfvars 2>/dev/null || true
	docker build -t tweets-web:dev .
	cd terraform && terraform apply -auto-approve

tf-destroy: ## Destroy Terraform infrastructure
	cd terraform && terraform destroy -auto-approve

# Utility targets
clean: ## Clean up Docker resources and Python cache
	docker system prune -f
	docker volume prune -f
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete

reset: ## Complete reset for fresh installation testing
	@echo "🧹 Resetting for fresh installation testing..."
	@./scripts/reset.sh

# Quick setup targets
setup-compose: ## Quick setup with Docker Compose
	make up
	@echo "Setup complete! Visit http://localhost:8000"

setup-terraform: ## Quick setup with Terraform
	make tf-init
	make tf-apply
	@echo "Setup complete! Visit http://localhost:8000" 