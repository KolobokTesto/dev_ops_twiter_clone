#!/bin/bash
# Reset script to test fresh installation experience

set -e

echo "🧹 Resetting Twitter Clone for fresh installation testing..."

# Stop and destroy Terraform infrastructure
echo "📦 Destroying Terraform infrastructure..."
cd terraform 2>/dev/null && terraform destroy -auto-approve 2>/dev/null || echo "No Terraform state found"
cd ..

# Stop Docker Compose if running
echo "🐳 Stopping Docker Compose..."
docker compose down -v 2>/dev/null || echo "No Docker Compose services running"

# Clean up all Docker resources
echo "🗑️  Cleaning up Docker resources..."
docker system prune -af --volumes

# Remove generated files (but keep source code)
echo "🔧 Removing generated files..."
rm -f .env
rm -f terraform/terraform.tfvars
rm -f terraform/terraform.tfstate*
rm -f terraform/.terraform.lock.hcl
rm -rf terraform/.terraform/

# Clean Python cache
echo "🐍 Cleaning Python cache..."
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Verify clean state
echo
echo "✅ Reset complete! Current state:"
echo "   - Docker containers: $(docker ps -aq | wc -l | tr -d ' ') running"
echo "   - Git status: $(git status --porcelain | wc -l | tr -d ' ') changes"
echo "   - Essential files present:"
echo "     - .env.example: $([ -f .env.example ] && echo '✅' || echo '❌')"
echo "     - migrations: $([ -d tweets/migrations ] && echo '✅' || echo '❌')"
echo "     - terraform.tfvars.example: $([ -f terraform/terraform.tfvars.example ] && echo '✅' || echo '❌')"

echo
echo "🚀 Ready for fresh installation testing!"
echo
echo "Test options:"
echo "  1. Docker Compose: make up"
echo "  2. Terraform:      make tf-init && make tf-apply"
echo "  3. Local dev:      make venv && source venv/bin/activate && make run"
echo 