"""
Tutorial 2: Image Editing (Text + Image to Image)
=================================================

This tutorial demonstrates image editing capabilities using the Gemini API.
Perfect for modifying existing images with text prompts.

Key Features:
- Image editing with text prompts
- Inpainting and semantic masking
- Style transfer
- Element addition and removal
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from ai import ImageGenerator, PromptTemplates, ImageStyle
from PIL import Image


def basic_image_editing():
    """Basic image editing example."""
    print("🎨 Basic Image Editing")
    print("=" * 40)
    
    # Initialize the image generator
    generator = ImageGenerator()
    
    # First, generate a base image
    base_prompt = "A modern living room with white walls, a sofa, and a coffee table"
    print("Creating base image...")
    
    base_result = generator.generate_text_to_image(
        prompt=base_prompt,
        output_filename="base_living_room",
        save_image=True
    )
    
    if not base_result["success"]:
        print(f"❌ Failed to create base image: {base_result.get('error')}")
        return
    
    print("✅ Base image created successfully!")
    
    # Now edit the image
    edit_prompt = "Add a cat sleeping on the sofa and change the lighting to warm golden hour"
    print("Editing image...")
    
    edit_result = generator.generate_image_editing(
        prompt=edit_prompt,
        input_image=base_result["image_path"],
        output_filename="edited_living_room",
        save_image=True
    )
    
    if edit_result["success"]:
        print(f"✅ Image edited successfully!")
        print(f"📁 Saved to: {edit_result.get('image_path', 'N/A')}")
    else:
        print(f"❌ Error: {edit_result.get('error', 'Unknown error')}")


def inpainting_example():
    """Inpainting example for semantic masking."""
    print("\n🎨 Inpainting Example")
    print("=" * 40)
    
    # Initialize the image generator
    generator = ImageGenerator()
    
    # Create a base image first
    base_prompt = "A portrait of a person in a business suit standing in front of a plain white background"
    print("Creating base portrait...")
    
    base_result = generator.generate_text_to_image(
        prompt=base_prompt,
        output_filename="base_portrait",
        save_image=True
    )
    
    if not base_result["success"]:
        print(f"❌ Failed to create base image: {base_result.get('error')}")
        return
    
    # Use inpainting template
    result = generator.generate_with_template(
        template_type="inpainting",
        base_image_description="a professional portrait",
        mask_area="the plain white background",
        replacement_content="a modern office environment with city skyline visible through windows",
        input_image=base_result["image_path"],
        output_filename="inpainted_portrait",
        save_image=True
    )
    
    if result["success"]:
        print(f"✅ Inpainting completed successfully!")
        print(f"📁 Saved to: {result.get('image_path', 'N/A')}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")


def style_transfer_example():
    """Style transfer example."""
    print("\n🎨 Style Transfer Example")
    print("=" * 40)
    
    # Initialize the image generator
    generator = ImageGenerator()
    
    # Create a base image
    base_prompt = "A simple house with a garden"
    print("Creating base house image...")
    
    base_result = generator.generate_text_to_image(
        prompt=base_prompt,
        output_filename="base_house",
        save_image=True
    )
    
    if not base_result["success"]:
        print(f"❌ Failed to create base image: {base_result.get('error')}")
        return
    
    # Apply style transfer
    result = generator.generate_with_template(
        template_type="style_transfer",
        source_image_description="a simple house with a garden",
        target_style=ImageStyle.ANIME,
        preserve_subject=True,
        input_image=base_result["image_path"],
        output_filename="anime_house",
        save_image=True
    )
    
    if result["success"]:
        print(f"✅ Style transfer completed successfully!")
        print(f"📁 Saved to: {result.get('image_path', 'N/A')}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")


def adding_elements_example():
    """Example of adding elements to an image."""
    print("\n🎨 Adding Elements Example")
    print("=" * 40)
    
    # Initialize the image generator
    generator = ImageGenerator()
    
    # Create a base image
    base_prompt = "An empty park with trees and a walking path"
    print("Creating base park image...")
    
    base_result = generator.generate_text_to_image(
        prompt=base_prompt,
        output_filename="base_park",
        save_image=True
    )
    
    if not base_result["success"]:
        print(f"❌ Failed to create base image: {base_result.get('error')}")
        return
    
    # Add elements
    edit_prompt = "Add a family having a picnic on the grass, children playing with a ball, and a dog running around"
    
    result = generator.generate_image_editing(
        prompt=edit_prompt,
        input_image=base_result["image_path"],
        output_filename="park_with_family",
        save_image=True
    )
    
    if result["success"]:
        print(f"✅ Elements added successfully!")
        print(f"📁 Saved to: {result.get('image_path', 'N/A')}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")


def removing_elements_example():
    """Example of removing elements from an image."""
    print("\n🎨 Removing Elements Example")
    print("=" * 40)
    
    # Initialize the image generator
    generator = ImageGenerator()
    
    # Create a base image with elements to remove
    base_prompt = "A busy street with cars, people, and street vendors"
    print("Creating busy street image...")
    
    base_result = generator.generate_text_to_image(
        prompt=base_prompt,
        output_filename="busy_street",
        save_image=True
    )
    
    if not base_result["success"]:
        print(f"❌ Failed to create base image: {base_result.get('error')}")
        return
    
    # Remove elements
    edit_prompt = "Remove all the cars and people, keeping only the empty street and buildings"
    
    result = generator.generate_image_editing(
        prompt=edit_prompt,
        input_image=base_result["image_path"],
        output_filename="empty_street",
        save_image=True
    )
    
    if result["success"]:
        print(f"✅ Elements removed successfully!")
        print(f"📁 Saved to: {result.get('image_path', 'N/A')}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    print("🚀 Gemini Image Generation - Image Editing Tutorial")
    print("=" * 60)
    
    try:
        # Run all examples
        basic_image_editing()
        inpainting_example()
        style_transfer_example()
        adding_elements_example()
        removing_elements_example()
        
        print("\n🎉 All tutorials completed successfully!")
        print("Check the 'outputs' directory for generated images.")
        
    except Exception as e:
        print(f"❌ Tutorial failed: {str(e)}")
        print("Make sure you have set up your GEMINI_API_KEY in the .env file.")
