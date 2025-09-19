"""
Tutorial 3: Advanced Composition & Multi-Image Processing
========================================================

This tutorial demonstrates advanced composition capabilities using the Gemini API.
Perfect for combining multiple images and creating complex scenes.

Key Features:
- Multi-image composition
- Advanced scene creation
- Style blending
- Complex prompt engineering
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from ai import ImageGenerator, PromptTemplates, ImageStyle, CameraAngle


def multi_image_composition():
    """Multi-image composition example."""
    print("🎨 Multi-Image Composition")
    print("=" * 40)
    
    # Initialize the image generator
    generator = ImageGenerator()
    
    # Create individual elements first
    print("Creating individual elements...")
    
    # Element 1: Background
    bg_result = generator.generate_text_to_image(
        prompt="A mystical forest with ancient trees and soft sunlight filtering through",
        output_filename="forest_background",
        save_image=True
    )
    
    if not bg_result["success"]:
        print(f"❌ Failed to create background: {bg_result.get('error')}")
        return
    
    # Element 2: Character
    character_result = generator.generate_text_to_image(
        prompt="A wise wizard in a long robe holding a glowing staff",
        output_filename="wizard_character",
        save_image=True
    )
    
    if not character_result["success"]:
        print(f"❌ Failed to create character: {character_result.get('error')}")
        return
    
    # Element 3: Magical effect
    magic_result = generator.generate_text_to_image(
        prompt="Magical sparkles and light particles floating in the air",
        output_filename="magic_effects",
        save_image=True
    )
    
    if not magic_result["success"]:
        print(f"❌ Failed to create magic effects: {magic_result.get('error')}")
        return
    
    print("✅ All elements created successfully!")
    
    # Now compose them together
    print("Composing elements together...")
    
    result = generator.generate_with_template(
        template_type="multi_image_composition",
        images=[
            "a mystical forest background",
            "a wise wizard character",
            "magical sparkles and effects"
        ],
        composition_goal="a complete fantasy scene with the wizard in the forest surrounded by magical effects",
        blending_style="seamless and atmospheric",
        input_image=bg_result["image_path"],  # Use background as base
        output_filename="fantasy_composition",
        save_image=True
    )
    
    if result["success"]:
        print(f"✅ Multi-image composition completed successfully!")
        print(f"📁 Saved to: {result.get('image_path', 'N/A')}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")


def iterative_refinement():
    """Iterative refinement example."""
    print("\n🎨 Iterative Refinement")
    print("=" * 40)
    
    # Initialize the image generator
    generator = ImageGenerator()
    
    # Initial generation
    print("Creating initial image...")
    initial_prompt = "A modern kitchen with white cabinets and stainless steel appliances"
    
    result = generator.generate_text_to_image(
        prompt=initial_prompt,
        output_filename="kitchen_v1",
        save_image=True
    )
    
    if not result["success"]:
        print(f"❌ Failed to create initial image: {result.get('error')}")
        return
    
    print("✅ Initial image created!")
    
    # First refinement
    print("Applying first refinement...")
    refinement_1 = "Add warm, cozy lighting and a bowl of fresh fruit on the counter"
    
    refined_prompt = PromptTemplates.iterative_refinement(initial_prompt, refinement_1)
    
    result_1 = generator.generate_image_editing(
        prompt=refined_prompt,
        input_image=result["image_path"],
        output_filename="kitchen_v2",
        save_image=True
    )
    
    if not result_1["success"]:
        print(f"❌ Failed first refinement: {result_1.get('error')}")
        return
    
    print("✅ First refinement applied!")
    
    # Second refinement
    print("Applying second refinement...")
    refinement_2 = "Change the lighting to evening mood with candles and add a cat sitting on the counter"
    
    refined_prompt_2 = PromptTemplates.iterative_refinement(refined_prompt, refinement_2)
    
    result_2 = generator.generate_image_editing(
        prompt=refined_prompt_2,
        input_image=result_1["image_path"],
        output_filename="kitchen_v3",
        save_image=True
    )
    
    if result_2["success"]:
        print(f"✅ Second refinement applied successfully!")
        print(f"📁 Final image saved to: {result_2.get('image_path', 'N/A')}")
    else:
        print(f"❌ Error in second refinement: {result_2.get('error', 'Unknown error')}")


def professional_product_photography():
    """Professional product photography example."""
    print("\n🎨 Professional Product Photography")
    print("=" * 40)
    
    # Initialize the image generator
    generator = ImageGenerator()
    
    # Use professional template for product photography
    result = generator.generate_with_template(
        template_type="text_to_image",
        subject="a premium wireless headphone",
        style=ImageStyle.PHOTOREALISTIC,
        context="professional product photography for e-commerce",
        camera_angle=CameraAngle.MACRO,
        lighting="soft, professional studio lighting with subtle shadows",
        composition="clean white background with subtle gradient"
    )
    
    if result["success"]:
        print(f"✅ Professional product photo generated successfully!")
        print(f"📁 Saved to: {result.get('image_path', 'N/A')}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")


def architectural_visualization():
    """Architectural visualization example."""
    print("\n🎨 Architectural Visualization")
    print("=" * 40)
    
    # Initialize the image generator
    generator = ImageGenerator()
    
    # Create architectural visualization
    prompt = PromptTemplates.text_to_image(
        subject="a modern minimalist house with large glass windows",
        style=ImageStyle.PHOTOREALISTIC,
        context="architectural visualization for a client presentation",
        camera_angle=CameraAngle.WIDE_ANGLE,
        lighting="golden hour lighting with warm, natural illumination",
        composition="surrounded by a well-landscaped garden with a swimming pool"
    )
    
    result = generator.generate_text_to_image(
        prompt=prompt,
        output_filename="architectural_house",
        save_image=True
    )
    
    if result["success"]:
        print(f"✅ Architectural visualization generated successfully!")
        print(f"📁 Saved to: {result.get('image_path', 'N/A')}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")


def batch_generation_example():
    """Batch generation example for multiple variations."""
    print("\n🎨 Batch Generation Example")
    print("=" * 40)
    
    # Initialize the image generator
    generator = ImageGenerator()
    
    # Define multiple prompts for batch generation
    prompts = [
        "A serene mountain lake at sunrise",
        "A bustling city street at night with neon lights",
        "A peaceful garden with blooming flowers",
        "A cozy cabin in the woods during winter",
        "A tropical beach with palm trees and crystal clear water"
    ]
    
    print(f"Generating {len(prompts)} images in batch...")
    
    results = generator.batch_generate(
        prompts=prompts,
        output_prefix="batch_scene"
    )
    
    successful = sum(1 for result in results if result["success"])
    print(f"✅ Batch generation completed! {successful}/{len(prompts)} images generated successfully.")
    
    for i, result in enumerate(results):
        if result["success"]:
            print(f"  📁 Scene {i+1}: {result.get('image_path', 'N/A')}")
        else:
            print(f"  ❌ Scene {i+1}: Failed - {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    print("🚀 Gemini Image Generation - Advanced Composition Tutorial")
    print("=" * 70)
    
    try:
        # Run all examples
        multi_image_composition()
        iterative_refinement()
        professional_product_photography()
        architectural_visualization()
        batch_generation_example()
        
        print("\n🎉 All tutorials completed successfully!")
        print("Check the 'outputs' directory for generated images.")
        
    except Exception as e:
        print(f"❌ Tutorial failed: {str(e)}")
        print("Make sure you have set up your GEMINI_API_KEY in the .env file.")
