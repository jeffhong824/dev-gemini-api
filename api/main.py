"""
FastAPI main application for Gemini Image Generation API
"""

import os
from pathlib import Path
from typing import List, Optional, Union
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import AI services
import sys
sys.path.append(str(Path(__file__).parent.parent))
from ai import ImageGenerator, PromptTemplates, ImageStyle, CameraAngle

# Initialize FastAPI app
app = FastAPI(
    title="Gemini Image Generation API",
    description="Professional image generation service using Google Gemini API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# Initialize AI services
image_generator = ImageGenerator()
prompt_templates = PromptTemplates()

# Pydantic models for request/response
class GenerateRequest(BaseModel):
    prompt: str
    output_filename: Optional[str] = None

class EditRequest(BaseModel):
    prompt: str
    output_filename: Optional[str] = None

class CleanRequest(BaseModel):
    objects: Optional[str] = None
    maintain_layout: bool = True
    output_filename: Optional[str] = None

class StyleRequest(BaseModel):
    target_style: str
    custom_style: Optional[str] = None
    output_filename: Optional[str] = None

class CompositionRequest(BaseModel):
    goal: str
    blending: str = "seamless"
    output_filename: Optional[str] = None

class TemplateRequest(BaseModel):
    template_type: str
    subject: Optional[str] = None
    style: Optional[str] = None
    context: Optional[str] = None
    angle: Optional[str] = None
    lighting: Optional[str] = None
    composition: Optional[str] = None
    base: Optional[str] = None
    mask: Optional[str] = None
    replace: Optional[str] = None
    source: Optional[str] = None
    target: Optional[str] = None
    text_content: Optional[str] = None
    design_style: Optional[str] = None
    steps: Optional[List[str]] = None

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
    error: Optional[str] = None

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main frontend interface"""
    return FileResponse("static/index.html")

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Gemini Image Generation API"}

# Generate endpoint
@app.post("/api/generate", response_model=APIResponse)
async def generate_image(request: GenerateRequest):
    """Generate image from text description"""
    try:
        result = image_generator.generate_text_to_image(
            prompt=request.prompt,
            output_filename=request.output_filename or "generated"
        )
        
        # Filter out binary data for JSON response
        if result.get("image_data"):
            del result["image_data"]
        
        return APIResponse(
            success=True,
            message="Image generated successfully",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Edit endpoint
@app.post("/api/edit", response_model=APIResponse)
async def edit_image(
    file: UploadFile = File(...),
    prompt: str = Form(...),
    style: Optional[str] = Form(None),
    custom_style: Optional[str] = Form(None),
    output_filename: Optional[str] = Form(None)
):
    """Edit existing image with text prompt"""
    try:
        # Save uploaded file temporarily
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Convert style string to enum
        style_enum = None
        if style:
            if style == "custom" and custom_style:
                style_enum = ImageStyle.CUSTOM
            elif style in [s.value for s in ImageStyle]:
                style_enum = ImageStyle(style)
        
        # Edit image
        result = image_generator.edit_image(
            input_image=temp_path,
            prompt=prompt,
            output_filename=output_filename or "edited"
        )
        
        # Filter out binary data for JSON response
        if result.get("image_data"):
            del result["image_data"]
        
        # Clean up temp file
        os.remove(temp_path)
        
        return APIResponse(
            success=True,
            message="Image edited successfully",
            data=result
        )
    except Exception as e:
        # Clean up temp file if it exists
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=str(e))

# Clean endpoint
@app.post("/api/clean", response_model=APIResponse)
async def clean_image(
    file: UploadFile = File(...),
    objects: Optional[str] = Form(None),
    maintain_layout: bool = Form(True),
    output_filename: Optional[str] = Form(None)
):
    """Clean room clutter and unnecessary objects"""
    try:
        # Save uploaded file temporarily
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Clean image
        result = image_generator.clean_image(
            input_image=temp_path,
            specific_objects=objects,
            maintain_layout=maintain_layout,
            output_filename=output_filename or "cleaned"
        )
        
        # Filter out binary data for JSON response
        if result.get("image_data"):
            del result["image_data"]
        
        # Clean up temp file
        os.remove(temp_path)
        
        return APIResponse(
            success=True,
            message="Image cleaned successfully",
            data=result
        )
    except Exception as e:
        # Clean up temp file if it exists
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=str(e))

# Style transfer endpoint
@app.post("/api/style", response_model=APIResponse)
async def transfer_style(
    file: UploadFile = File(...),
    target_style: str = Form(...),
    custom_style: Optional[str] = Form(None),
    output_filename: Optional[str] = Form(None)
):
    """Transfer style from one image to another"""
    try:
        # Save uploaded file temporarily
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Style mapping for the 12 predefined styles
        style_mapping = {
            "modern": "modern style, clean, neutral color, minimalistic furniture, marble tile floors, abundant natural light, sleek materials, bright color schemes",
            "minimalist": "minimalist style, monochromatic and cold tones, large flat floors, white walls, clean and uncluttered aesthetics, low-profile furniture, natural light, calming and spacious environment",
            "neoclassical": "neoclassical style, bright and elegant tone, marble floors, white paneled walls, luxurious and sophisticated materials, soft neutral-toned furniture, soft and warm lighting",
            "industrial_loft": "industrial loft, reclaimed wood, walnut floors, exposed structural elements like pipes and beams, concrete or brick walls, vintage and repurposed furniture, leather and metal accents",
            "coastal": "coastal style, weathered wood, rattan, jute furniture, natural light, cotton linen, driftwood",
            "country": "country style, natural materials like wood, and brick walls, delicate grooved details, soft pastel painted wood, and ornate metal handles, floral and plaid patterns furniture, warm tones, soft natural lighting",
            "scandinavian": "scandinavian style, crisp clean lines, cozy furniture, oak floors, soft natural light, warm natural materials, neutral palettes, airy and tranquil atmosphere",
            "japanese": "japanese style, wood bamboo stone flooring furniture, clean line, tatami, low wooden table, shoji door, bonsai, bamboo, paper lanterns, natural material pendant lights",
            "japandi": "japandi style, japanese minimalism, scandinavian coziness, natural wood, clean line, tatami, shoji, japanese aesthetic, warm",
            "modern_american": "modern american style, wood, metal, glass, timeless furniture, pendant lights, floor lamp, contemporary",
            "mid_century_modern": "mid century modern interior, warm wooden tones and rich walnut finishes, retro aesthetic furniture, a color palette with muted earth tones and pops of color",
            "modern_classic": "modern classic style, metallic accent, crown molding, wainscoting, rich fabrics, velvet, silk, linen"
        }
        
        # Get style text
        if target_style == "custom" and custom_style:
            style_text = custom_style
        elif target_style in style_mapping:
            style_text = style_mapping[target_style]
        else:
            style_text = target_style.replace("_", " ").title()
        
        prompt = prompt_templates.style_transfer(
            source_image_description="the uploaded image",
            target_style=style_text
        )
        
        result = image_generator.generate_image_editing(
            input_image=temp_path,
            prompt=prompt,
            output_filename=output_filename or "styled"
        )
        
        # Filter out binary data for JSON response
        if result.get("image_data"):
            del result["image_data"]
        
        # Clean up temp file
        os.remove(temp_path)
        
        return APIResponse(
            success=True,
            message="Style transferred successfully",
            data=result
        )
    except Exception as e:
        # Clean up temp file if it exists
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=str(e))

# Composition endpoint
@app.post("/api/composition", response_model=APIResponse)
async def compose_images(
    files: List[UploadFile] = File(...),
    goal: str = Form(...),
    output_filename: Optional[str] = Form(None)
):
    """Compose multiple images into a new scene"""
    try:
        # Save uploaded files temporarily
        temp_paths = []
        for i, file in enumerate(files):
            temp_path = f"temp_{i}_{file.filename}"
            with open(temp_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            temp_paths.append(temp_path)
        
        # Compose images using template-based generation
        prompt = prompt_templates.multi_image_composition(
            images=["the uploaded images"],
            composition_goal=goal,
            blending_style="seamless"
        )
        
        # Use the new multi-image composition method
        result = image_generator.generate_multi_image_composition(
            input_images=temp_paths,
            prompt=prompt,
            output_filename=output_filename or "composed"
        )
        
        # Filter out binary data for JSON response
        if result.get("image_data"):
            del result["image_data"]
        
        # Clean up temp files
        for temp_path in temp_paths:
            os.remove(temp_path)
        
        return APIResponse(
            success=True,
            message="Images composed successfully",
            data=result
        )
    except Exception as e:
        # Clean up temp files if they exist
        for temp_path in temp_paths:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        raise HTTPException(status_code=500, detail=str(e))

# Templates endpoint
@app.post("/api/templates", response_model=APIResponse)
async def get_template(request: TemplateRequest):
    """Get formatted prompt template"""
    try:
        # Generate template based on type
        if request.template_type == "text":
            template = prompt_templates.text_to_image(
                subject=request.subject or "image",
                style=ImageStyle(request.style) if request.style else ImageStyle.PHOTOREALISTIC,
                context=request.context,
                camera_angle=CameraAngle(request.angle) if request.angle else None,
                lighting=request.lighting,
                composition=request.composition
            )
        elif request.template_type == "inpainting":
            template = prompt_templates.inpainting(
                base_image=request.base or "image",
                mask_area=request.mask or "area",
                replacement_content=request.replace or "content"
            )
        elif request.template_type == "style":
            template = prompt_templates.style_transfer(
                source_image=request.source or "source image",
                target_style=request.target or "target style"
            )
        elif request.template_type == "composition":
            template = prompt_templates.multi_image_composition(
                goal=request.goal or "composition goal",
                blending_style=request.blending or "seamless"
            )
        elif request.template_type == "text_rendering":
            template = prompt_templates.text_rendering(
                text_content=request.text_content or "text",
                design_style=request.design_style or "modern"
            )
        elif request.template_type == "clean_room":
            template = prompt_templates.clean_room(
                specific_objects=request.objects,
                maintain_layout=request.maintain_layout
            )
        elif request.template_type == "step_by_step":
            template = prompt_templates.step_by_step(
                steps=request.steps or ["step 1", "step 2"]
            )
        else:
            raise ValueError(f"Unknown template type: {request.template_type}")
        
        return APIResponse(
            success=True,
            message="Template generated successfully",
            data={"template": template}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get available styles and angles
@app.get("/api/styles")
async def get_styles():
    """Get available image styles"""
    return {
        "styles": [style.value for style in ImageStyle],
        "angles": [angle.value for angle in CameraAngle]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
