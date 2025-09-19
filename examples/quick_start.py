"""
Quick Start Example
==================

A simple example to get started with the Gemini Image Generation API.
This demonstrates the most common use cases in a single script.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from ai import ImageGenerator, ImageStyle, CameraAngle


def main():
    """Quick start example with common use cases."""
    print("🚀 Gemini Image Generation - Quick Start")
    print("=" * 50)
    
    # Initialize the image generator
    try:
        generator = ImageGenerator()
        print("✅ Image generator initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        print("Make sure you have set up your GEMINI_API_KEY in the .env file.")
        return
    
    # Example 1: Simple text-to-image
    print("\n1. Simple Text-to-Image Generation")
    print("-" * 40)
    
    result = generator.generate_text_to_image(
        prompt="A beautiful sunset over a calm ocean with sailboats",
        output_filename="quick_start_sunset",
        save_image=True
    )
    
    if result["success"]:
        print(f"✅ Sunset image generated: {result.get('image_path', 'N/A')}")
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    # Example 2: Professional product photography
    print("\n2. Professional Product Photography")
    print("-" * 40)
    
    result = generator.generate_with_template(
        template_type="text_to_image",
        subject="a premium coffee mug",
        style=ImageStyle.PHOTOREALISTIC,
        context="professional product photography for e-commerce",
        camera_angle=CameraAngle.MACRO,
        lighting="soft, professional studio lighting",
        composition="clean white background with subtle shadows"
    )
    
    if result["success"]:
        print(f"✅ Product photo generated: {result.get('image_path', 'N/A')}")
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    # Example 3: Logo design
    print("\n3. Logo Design")
    print("-" * 40)
    
    from ai.prompt_templates import PromptTemplates
    
    logo_prompt = PromptTemplates.text_rendering(
        text_content="TECHNOVA",
        design_style="modern minimalist with geometric elements",
        context="a professional tech company logo"
    )
    
    result = generator.generate_text_to_image(
        prompt=logo_prompt,
        output_filename="quick_start_logo",
        save_image=True
    )
    
    if result["success"]:
        print(f"✅ Logo generated: {result.get('image_path', 'N/A')}")
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    # Example 4: Batch generation
    print("\n4. Batch Generation")
    print("-" * 40)
    
    prompts = [
        "A serene mountain landscape at dawn",
        "A bustling city street at night",
        "A peaceful garden with flowers"
    ]
    
    results = generator.batch_generate(
        prompts=prompts,
        output_prefix="quick_start_batch"
    )
    
    successful = sum(1 for r in results if r["success"])
    print(f"✅ Batch generation: {successful}/{len(prompts)} images generated successfully")
    
    print("\n🎉 Quick start completed!")
    print("Check the 'outputs' directory for all generated images.")


if __name__ == "__main__":
    main()
