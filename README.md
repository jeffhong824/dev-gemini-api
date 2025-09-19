# Gemini Image Generation API

A modular Gemini image generation service supporting text-to-image, image editing, style transfer, and room cleaning with external prompt templates.

## 🚀 Core Features

- **Text-to-Image**: Generate high-quality images from text descriptions
- **Image + Text-to-Image (Editing)**: Edit existing images with text prompts (add, remove, modify elements)
- **Multi-Image to Image (Composition & Style Transfer)**: Compose multiple images or transfer styles
- **Iterative Refinement**: Progressively refine images through conversation
- **High-Fidelity Text Rendering**: Generate images with legible and well-placed text
- **Room Cleaning**: Specialized editing for removing clutter and unnecessary objects
- **Externalized Prompts**: All system prompts stored in `ai/resources/prompts/` directory for easy customization
- **Modular Design**: Support for `python gemini_api.py` command calls

## 📁 Project Structure

```
gemini-api/
├── ai/                          # Core AI services
│   ├── resources/               # Externalized resources
│   │   └── prompts/            # System prompt templates
│   │       ├── text_to_image.txt
│   │       ├── inpainting.txt
│   │       ├── style_transfer.txt
│   │       ├── clean_room.txt
│   │       ├── multi_image_composition.txt
│   │       ├── text_rendering.txt
│   │       ├── step_by_step.txt
│   │       └── style_options.txt
│   ├── __init__.py
│   ├── image_generator.py      # Main image generation service
│   ├── prompt_templates.py     # Professional prompt templates
│   └── prompt_loader.py        # Prompt loader
├── assets/images/               # Sample images
├── outputs/                     # Generated images
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker configuration
├── docker-compose.yml          # Docker Compose settings
├── Makefile                    # Project management commands
├── gemini_api.py               # Modular entry point
└── README.md                   # Usage guide
```

## 🛠️ Quick Start

### Method 1: Using Make (Recommended)
```bash
# Clone project
git clone <repository-url>
cd dev-gemini-api

# Complete setup with Make
make setup

# This will:
# - Install Python dependencies
# - Create .env file from template
# - Set up directories
# - Run basic tests

# Edit .env and add your GEMINI_API_KEY
nano .env

# Test the installation
make test

# Run services
make run    # CLI service
make api    # Web API service with frontend (http://localhost:8000)
```

### Method 2: Manual Installation
```bash
# Clone project
git clone <repository-url>
cd dev-gemini-api

# Install Python dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Create necessary directories
mkdir -p outputs assets/images
```

### Method 3: Using Docker
```bash
# Clone project
git clone <repository-url>
cd dev-gemini-api

# Create .env file
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Build and run with Docker Compose
make docker-run

# Or manually with Docker
docker-compose up --build

# Note: If you encounter network issues, try:
# 1. Ensure Docker Desktop is running
# 2. Check your internet connection
# 3. Try building with a different base image
```

### 2. Web API Service

The project now includes a complete FastAPI backend with a web frontend for easy testing and usage.

#### Starting the API Service

```bash
# Start the FastAPI server
make api

# Or run directly
python api_server.py
```

The service will be available at:
- **Frontend Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

#### Frontend Features

The web interface provides:
- **Generate Tab**: Text-to-image generation with style options
- **Edit Tab**: Upload and edit images with text prompts
- **Clean Tab**: Remove objects or clutter from room images
- **Style Tab**: Transfer artistic styles between images
- **Composition Tab**: Combine multiple images into new scenes
- **Templates Tab**: Generate professional prompt templates

#### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Frontend interface |
| `/health` | GET | Health check |
| `/api/generate` | POST | Text-to-image generation |
| `/api/edit` | POST | Image editing |
| `/api/clean` | POST | Room cleaning |
| `/api/style` | POST | Style transfer |
| `/api/composition` | POST | Multi-image composition |
| `/api/templates` | POST | Prompt template generation |
| `/api/styles` | GET | Available styles and angles |

### 3. CLI Usage
```bash
# Text-to-Image generation
python gemini_api.py generate --prompt "a modern living room with minimalist design"

# Image editing
python gemini_api.py edit --input assets/images/living_room.png --prompt "add a cat on the sofa"

# Room cleaning
python gemini_api.py clean --input assets/images/living_room.png --objects "books and magazines"

# Style transfer
python gemini_api.py style --input assets/images/living_room.png --target_style oil_painting

# Multi-image composition
python gemini_api.py composition --inputs assets/images/living_room.png assets/images/model.png --goal "modern living room with person"
```

## 🔧 Installation & Deployment

### Prerequisites
- Python 3.11+ (for local installation)
- Docker & Docker Compose (for containerized deployment)
- Make (optional, for convenience commands)
- Gemini API Key (get from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation Methods

#### 1. Make Commands (Recommended)
```bash
# Show all available commands
make help

# Complete project setup
make setup

# Install Python dependencies only
make install

# Run basic functionality test
make test

# Run the service
make run
```

#### 2. Docker Deployment
```bash
# Build Docker image
make docker-build
# or: docker-compose build

# Run with Docker Compose
make docker-run
# or: docker-compose up

# Run in background
docker-compose up -d

# Stop containers
make docker-stop
# or: docker-compose down

# View logs
docker-compose logs -f

# Execute commands in container
docker-compose exec gemini-api python gemini_api.py --help
```

#### 3. Manual Python Installation
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Create directories
mkdir -p outputs assets/images

# Test installation
python gemini_api.py --help
```

### Environment Configuration
```bash
# .env file configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Set custom output directory
OUTPUT_DIR=outputs

# Optional: Set custom prompt templates directory
PROMPTS_DIR=ai/resources/prompts
```

### Production Deployment

#### Using Docker Compose
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  gemini-api:
    build: .
    container_name: gemini-api-prod
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - ./outputs:/app/outputs
      - ./assets:/app/assets
    ports:
      - "8000:8000"
    restart: unless-stopped
```

#### Using Docker Swarm
```bash
# Deploy to Docker Swarm
docker stack deploy -c docker-compose.prod.yml gemini-stack

# Scale the service
docker service scale gemini-stack_gemini-api=3
```

#### Using Kubernetes
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gemini-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gemini-api
  template:
    metadata:
      labels:
        app: gemini-api
    spec:
      containers:
      - name: gemini-api
        image: gemini-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: GEMINI_API_KEY
          valueFrom:
            secretKeyRef:
              name: gemini-secrets
              key: api-key
```

## 📖 Command Reference

### Generate - Text-to-Image
Generate high-quality images from text descriptions.

```bash
# Basic generation
python gemini_api.py generate --prompt "a beautiful sunset over mountains"

# With style and context
python gemini_api.py generate --prompt "coffee cup" --style artistic --context "product photography"

# With camera angle and lighting
python gemini_api.py generate --prompt "modern sofa" --angle close_up --lighting "soft studio lighting"

# Custom style
python gemini_api.py generate --prompt "vintage car" --style custom --custom_style "vintage sepia tone with film grain"
```

**Available Styles**: photorealistic, artistic, cartoon, anime, oil_painting, watercolor, sketch, digital_art, custom

### Edit - Image + Text-to-Image
Edit existing images with text prompts.

```bash
# Add elements
python gemini_api.py edit --input assets/images/living_room.png --prompt "add a cat sitting on the sofa"

# Remove elements
python gemini_api.py edit --input assets/images/living_room.png --prompt "remove the books from the table"

# Change style
python gemini_api.py edit --input assets/images/living_room.png --prompt "change to night scene" --style custom --custom_style "dark moody lighting"

# Modify elements
python gemini_api.py edit --input assets/images/living_room.png --prompt "change the wall color to blue"
```

### Clean - Room Cleaning
Specialized editing for removing clutter and unnecessary objects.

```bash
# Clean specific objects
python gemini_api.py clean --input assets/images/living_room.png --objects "books and magazines"

# Clean all clutter
python gemini_api.py clean --input assets/images/living_room.png

# Clean without maintaining layout
python gemini_api.py clean --input assets/images/living_room.png --objects "decorations" --no-layout
```

### Style - Style Transfer
Transfer style from one image to another.

```bash
# Transfer to artistic style
python gemini_api.py style --input assets/images/living_room.png --target_style oil_painting

# Custom style transfer
python gemini_api.py style --input assets/images/living_room.png --target_style custom --custom_style "cyberpunk neon aesthetic"

# Preserve subject during transfer
python gemini_api.py style --input assets/images/living_room.png --target_style watercolor --preserve_subject
```

### Composition - Multi-Image to Image
Compose multiple images into a new scene.

```bash
# Compose living room with person
python gemini_api.py composition --inputs assets/images/living_room.png assets/images/model.png --goal "modern living room with person"

# Product showcase composition
python gemini_api.py composition --inputs assets/images/dress.png assets/images/living_room.png --goal "fashion product showcase"

# Artistic blending
python gemini_api.py composition --inputs assets/images/living_room.png assets/images/model.png --goal "surreal living room scene" --blending artistic
```

### Templates - Show Available Templates
Display available prompt templates and examples.

```bash
# Show text-to-image template
python gemini_api.py templates --type text --subject "modern sofa" --style photorealistic

# Show editing examples
python gemini_api.py templates --type edit

# Show style transfer options
python gemini_api.py templates --type style

# Show composition examples
python gemini_api.py templates --type composition

# Show cleaning options
python gemini_api.py templates --type clean
```

## 🎯 Real-World Use Cases

### E-commerce Product Photography
```bash
# Generate product images
python gemini_api.py generate --prompt "premium wireless headphones" --style photorealistic --context "product photography" --angle close_up --lighting "soft studio lighting"

# Edit product images
python gemini_api.py edit --input assets/images/dress.png --prompt "change background to white studio backdrop"
```

### Interior Design
```bash
# Clean room for staging
python gemini_api.py clean --input assets/images/living_room.png --objects "personal items and clutter"

# Style transfer for mood boards
python gemini_api.py style --input assets/images/living_room.png --target_style watercolor
```

### Logo and Brand Design
```bash
# Generate logo concepts
python gemini_api.py generate --prompt "modern minimalist logo for tech company" --style custom --custom_style "clean geometric design"

# Text rendering
python gemini_api.py generate --prompt "logo with text 'TECHNOVA' in modern sans-serif font" --context "logo design"
```

### Multi-Image Composition
```bash
# Compose furniture layout
python gemini_api.py composition --inputs assets/images/living_room.png assets/images/model.png --goal "modern living room layout with person"

# Product showcase
python gemini_api.py composition --inputs assets/images/dress.png assets/images/living_room.png --goal "fashion product showcase"
```

## 🔧 Customize Prompts

All system prompts are stored in `ai/resources/prompts/` directory for easy customization:

### Available Prompt Templates
- `text_to_image.txt` - Text-to-image template
- `inpainting.txt` - Image editing template
- `style_transfer.txt` - Style transfer template
- `clean_room.txt` - Room cleaning template
- `multi_image_composition.txt` - Multi-image composition template
- `text_rendering.txt` - Text rendering template
- `step_by_step.txt` - Step-by-step instruction template
- `style_options.txt` - Available style options

### Customization Method
1. Edit the corresponding `.txt` file
2. Use `{variable_name}` syntax to define replaceable parameters
3. Restart the service to take effect

### Example: Customize Text-to-Image Template
```txt
# Original template
Create a {context} featuring {subject}, in {style} style{angle}{lighting}{composition}{negative_prompt}.

# Customized template
Generate a professional {context} showcasing {subject} in {style} style{angle}{lighting}{composition}{negative_prompt}. Focus on high-quality details and commercial appeal.
```

## 🚨 Limitations

- Best language support: EN, es-MX, ja-JP, zh-CN, hi-IN
- Maximum 3 input images per request
- Maximum 1 output image per request
- All generated images contain SynthID watermark
- Uploading images of children not supported in EEA, CH, and UK

## 🆘 Troubleshooting

### Common Issues
1. **Invalid API key**: Check `GEMINI_API_KEY` in `.env` file
2. **Image generation failed**: Try simplifying prompts, provide more context
3. **Memory issues**: Reduce batch generation quantity
4. **Permission errors**: Ensure `outputs` directory has write permissions

### Getting Help
```bash
# Show all commands
python gemini_api.py --help

# Show specific command help
python gemini_api.py generate --help
python gemini_api.py edit --help
python gemini_api.py clean --help
python gemini_api.py style --help
python gemini_api.py composition --help
```

## 🐳 Docker Support

### Quick Docker Usage
```bash
# Build and run with Docker Compose
make docker-run

# Run in background
docker-compose up -d

# Stop containers
make docker-stop
```

### Docker Commands
```bash
# Build Docker image
make docker-build
# or: docker-compose build

# Run with Docker Compose
make docker-run
# or: docker-compose up

# Execute commands in container
docker-compose exec gemini-api python gemini_api.py --help
docker-compose exec gemini-api python gemini_api.py generate --prompt "test image"

# View logs
docker-compose logs -f

# Stop and remove containers
docker-compose down
```

### Docker Environment Variables
```bash
# Set environment variables for Docker
export GEMINI_API_KEY=your_api_key_here
docker-compose up
```

### Docker Troubleshooting

#### Common Issues
1. **Docker daemon not running**
   ```bash
   # Start Docker Desktop
   open -a Docker  # macOS
   # or restart Docker service
   sudo systemctl start docker  # Linux
   ```

2. **Network timeout during build**
   ```bash
   # Check internet connection
   ping google.com
   
   # Try with different DNS
   docker build --dns=8.8.8.8 -t gemini-api .
   ```

3. **Permission denied errors**
   ```bash
   # Fix permissions
   sudo chown -R $USER:$USER .
   chmod +x gemini_api.py
   ```

4. **Large build context**
   ```bash
   # Use .dockerignore to reduce context size
   # Check what's being sent to Docker
   docker build --no-cache --progress=plain .
   ```

#### Alternative Docker Setup
If you encounter issues with the main Dockerfile, try the simplified version:

```bash
# Use simplified Dockerfile
docker build -f Dockerfile.simple -t gemini-api-simple .

# Run the container
docker run --rm -v $(pwd)/outputs:/app/outputs gemini-api-simple
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.