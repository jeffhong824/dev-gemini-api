"""
Tutorial 1: Text-to-Image Generation
====================================

This tutorial demonstrates basic text-to-image generation using the Gemini API.
Perfect for creating images from simple text descriptions.

Key Features:
- Simple text-to-image generation
- Professional prompt templates
- Automatic image saving
- Error handling
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from ai import ImageGenerator, PromptTemplates, ImageStyle, CameraAngle


def basic_text_to_image():
    """Basic text-to-image generation example."""
    print("🎨 Basic Text-to-Image Generation")
    print("=" * 40)
    
    # Initialize the image generator
    generator = ImageGenerator()
    
    # Simple prompt
    prompt = "A beautiful sunset over a mountain landscape with a lake in the foreground"
    
    # Generate image
    result = generator.generate_text_to_image(
        prompt=prompt,
        output_filename="sunset_mountain",
        save_image=True
    )
    
    if result["success"]:
        print(f"✅ Image generated successfully!")
        print(f"📁 Saved to: {result.get('image_path', 'N/A')}")
        if result.get("text_content"):
            print(f"📝 Generated text: {result['text_content']}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")


def professional_text_to_image():
    """Professional text-to-image generation with templates."""
    print("\n🎨 Professional Text-to-Image Generation")
    print("=" * 40)
    
    # Initialize the image generator
    generator = ImageGenerator()
    
    # Use professional template
    result = generator.generate_with_template(
        template_type="text_to_image",
        subject="a futuristic city skyline",
        style=ImageStyle.PHOTOREALISTIC,
        context="a concept art for a sci-fi movie",
        camera_angle=CameraAngle.WIDE_ANGLE,
        lighting="dramatic neon lighting at night",
        composition="with flying cars and holographic displays"
    )
    
    if result["success"]:
        print(f"✅ Professional image generated successfully!")
        print(f"📁 Saved to: {result.get('image_path', 'N/A')}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")


def logo_design_example():
    """Logo design example using professional templates."""
    print("\n🎨 Logo Design Example")
    print("=" * 40)
    
    # Initialize the image generator
    generator = ImageGenerator()
    
    # Logo design prompt
    prompt = PromptTemplates.text_rendering(
        text_content="TECHNOVA",
        design_style="modern minimalist with geometric elements",
        context="a professional logo"
    )
    
    result = generator.generate_text_to_image(
        prompt=prompt,
        output_filename="technova_logo",
        save_image=True
    )
    
    if result["success"]:
        print(f"✅ Logo generated successfully!")
        print(f"📁 Saved to: {result.get('image_path', 'N/A')}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")


def step_by_step_generation():
    """Step-by-step image generation example."""
    print("\n🎨 Step-by-Step Generation")
    print("=" * 40)
    
    # Initialize the image generator
    generator = ImageGenerator()
    
    # Step-by-step instructions
    steps = [
        "Create a background of a serene, misty forest at dawn",
        "Add a moss-covered ancient stone altar in the foreground",
        "Place a single, glowing sword on top of the altar",
        "Add mystical lighting effects around the sword"
    ]
    
    prompt = PromptTemplates.step_by_step_instructions(steps)
    
    result = generator.generate_text_to_image(
        prompt=prompt,
        output_filename="mystical_forest_scene",
        save_image=True
    )
    
    if result["success"]:
        print(f"✅ Step-by-step image generated successfully!")
        print(f"📁 Saved to: {result.get('image_path', 'N/A')}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    print("🚀 Gemini Image Generation - Text-to-Image Tutorial")
    print("=" * 60)
    
    try:
        # Run all examples
        basic_text_to_image()
        professional_text_to_image()
        logo_design_example()
        step_by_step_generation()
        
        print("\n🎉 All tutorials completed successfully!")
        print("Check the 'outputs' directory for generated images.")
        
    except Exception as e:
        print(f"❌ Tutorial failed: {str(e)}")
        print("Make sure you have set up your GEMINI_API_KEY in the .env file.")
