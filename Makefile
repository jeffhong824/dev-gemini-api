# Gemini Image Generation API - Makefile
# 模組化圖片生成服務管理

.PHONY: help install setup clean run docker-build docker-run docker-stop

# Default target
help:
	@echo "🚀 Gemini Image Generation API - 可用命令"
	@echo "=========================================="
	@echo ""
	@echo "設置與安裝:"
	@echo "  make install     - 安裝 Python 依賴"
	@echo "  make setup       - 完整專案設置"
	@echo ""
	@echo "運行服務:"
	@echo "  make run         - 運行模組化服務"
	@echo "  make api         - 啟動 FastAPI 後端服務"
	@echo "  make test        - 測試所有功能"
	@echo "  make test-api    - 測試 API 服務"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build - 構建 Docker 鏡像"
	@echo "  make docker-run   - 使用 Docker Compose 運行"
	@echo "  make docker-stop  - 停止 Docker 容器"
	@echo ""
	@echo "清理:"
	@echo "  make clean       - 清理臨時文件"
	@echo ""

# Installation
install:
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt

setup: install
	@echo "🔧 Setting up project..."
	@if [ ! -f .env ]; then \
		echo "📝 Creating .env file from template..."; \
		cp .env.example .env; \
		echo "⚠️  Please edit .env file and add your GEMINI_API_KEY"; \
	fi
	@mkdir -p outputs assets/images logs data/raw data/processed artifacts results
	@echo "✅ Project setup complete!"
	@echo "📝 Next steps:"
	@echo "   1. Edit .env file and add your GEMINI_API_KEY"
	@echo "   2. Run 'make test' to verify installation"
	@echo "   3. Run 'make run' to start the service"

# Development
run:
	@echo "🚀 Running modular service..."
	python gemini_api.py --help

api:
	@echo "🌐 Starting FastAPI server..."
	python api_server.py

test:
	@echo "🧪 Testing all functionality..."
	python gemini_api.py --help
	python gemini_api.py generate --prompt "test image" --output test_make
	python gemini_api.py templates --type text --subject "test" --style photorealistic
	@echo "✅ All tests completed successfully"

test-api:
	@echo "🧪 Testing API service..."
	@echo "⚠️  Make sure API service is running (make api) before running this test"
	python test_api.py

lint:
	@echo "🔍 Running linting checks..."
	ruff check ai/ tutorials/ --fix
	black --check ai/ tutorials/

format:
	@echo "🎨 Formatting code..."
	black ai/ tutorials/
	isort ai/ tutorials/
	ruff check ai/ tutorials/ --fix

clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/

# Running services
run:
	@echo "🚀 運行模組化服務..."
	python gemini_api.py --help

# 移除 run-server 命令

# Testing commands (moved to Development section)

# Docker commands
docker-build:
	@echo "🐳 Building Docker image..."
	docker-compose build

docker-run: docker-build
	@echo "🐳 Running with Docker Compose..."
	docker-compose up

docker-stop:
	@echo "🐳 Stopping Docker containers..."
	docker-compose down

# Development with Jupyter
jupyter:
	@echo "📓 Starting Jupyter notebook..."
	docker-compose --profile development up jupyter

# API service
api:
	@echo "🌐 Starting API service..."
	docker-compose --profile api up api

# Production deployment
deploy:
	@echo "🚀 Deploying to production..."
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Backup outputs
backup:
	@echo "💾 Backing up outputs..."
	tar -czf outputs_backup_$(shell date +%Y%m%d_%H%M%S).tar.gz outputs/

# Show project status
status:
	@echo "📊 Project Status"
	@echo "================="
	@echo "Python version: $(shell python --version)"
	@echo "Docker version: $(shell docker --version 2>/dev/null || echo 'Docker not installed')"
	@echo "Outputs directory: $(shell ls -la outputs/ 2>/dev/null | wc -l) files"
	@echo "Environment file: $(shell [ -f .env ] && echo '✅ Present' || echo '❌ Missing')"
