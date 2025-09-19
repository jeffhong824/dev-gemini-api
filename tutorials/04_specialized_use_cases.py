"""
Tutorial 4: Specialized Use Cases
=================================

This tutorial demonstrates specialized use cases and professional applications
using the Gemini API for image generation.

Key Features:
- Logo and brand design
- Interior design visualization
- Character design
- Text rendering and typography
- Professional photography styles
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from ai import ImageGenerator, PromptTemplates, ImageStyle, CameraAngle


def logo_design_workflow():
    """Complete logo design workflow example."""
    print("🎨 Logo Design Workflow")
    print("=" * 40)
    
    # Initialize the image generator
    generator = ImageGenerator()
    
    # Logo design with professional template
    logo_prompts = [
        "Create a minimalist logo for a tech startup called 'NEXUS' with geometric elements and blue color scheme",
        "Design a modern logo for 'NEXUS' with clean typography and a subtle tech-inspired icon",
        "Create a professional logo for 'NEXUS' with a futuristic feel and gradient effects"
    ]
    
    print("Generating logo variations...")
    
    for i, prompt in enumerate(logo_prompts, 1):
        result = generator.generate_text_to_image(
            prompt=prompt,
            output_filename=f"nexus_logo_v{i}",
            save_image=True
        )
        
        if result["success"]:
            print(f"✅ Logo variation {i} generated successfully!")
            print(f"📁 Saved to: {result.get('image_path', 'N/A')}")
        else:
            print(f"❌ Logo variation {i} failed: {result.get('error', 'Unknown error')}")


def interior_design_visualization():
    """Interior design visualization example."""
    print("\n🎨 Interior Design Visualization")
    print("=" * 40)
    
    # Initialize the image generator
    generator = ImageGenerator()
    
    # Different room designs
    room_designs = [
        {
            "room": "modern living room",
            "style": "contemporary",
            "elements": "sleek furniture, large windows, neutral colors",
            "lighting": "natural light with modern pendant lights"
        },
        {
            "room": "cozy bedroom",
            "style": "scandinavian",
            "elements": "wooden furniture, soft textiles, plants",
            "lighting": "warm, soft lighting"
        },
        {
            "room": "industrial kitchen",
            "style": "modern industrial",
            "elements": "exposed brick, stainless steel, concrete countertops",
            "lighting": "track lighting and pendant lights"
        }
    ]
    
    for i, design in enumerate(room_designs, 1):
        prompt = PromptTemplates.text_to_image(
            subject=f"a {design['room']}",
            style=ImageStyle.PHOTOREALISTIC,
            context="interior design visualization for a client",
            camera_angle=CameraAngle.WIDE_ANGLE,
            lighting=design["lighting"],
            composition=f"with {design['elements']} in {design['style']} style"
        )
        
        result = generator.generate_text_to_image(
            prompt=prompt,
            output_filename=f"interior_design_{i}",
            save_image=True
        )
        
        if result["success"]:
            print(f"✅ {design['room'].title()} design generated successfully!")
            print(f"📁 Saved to: {result.get('image_path', 'N/A')}")
        else:
            print(f"❌ {design['room'].title()} design failed: {result.get('error', 'Unknown error')}")


def character_design_series():
    """Character design series example."""
    print("\n🎨 Character Design Series")
    print("=" * 40)
    
    # Initialize the image generator
    generator = ImageGenerator()
    
    # Character design prompts
    characters = [
        {
            "name": "Fantasy Warrior",
            "description": "a heroic fantasy warrior with ornate armor, wielding a magical sword",
            "style": ImageStyle.ARTISTIC,
            "setting": "mystical forest background"
        },
        {
            "name": "Cyberpunk Hacker",
            "description": "a futuristic hacker with cybernetic implants and neon accessories",
            "style": ImageStyle.ANIME,
            "setting": "neon-lit cityscape background"
        },
        {
            "name": "Steampunk Inventor",
            "description": "a Victorian-era inventor with brass goggles and mechanical gadgets",
            "style": ImageStyle.PAINTING,
            "setting": "steam-powered workshop background"
        }
    ]
    
    for character in characters:
        prompt = PromptTemplates.text_to_image(
            subject=character["description"],
            style=character["style"],
            context="character design for a video game",
            camera_angle=CameraAngle.CLOSE_UP,
            lighting="dramatic character lighting",
            composition=f"with {character['setting']}"
        )
        
        result = generator.generate_text_to_image(
            prompt=prompt,
            output_filename=f"character_{character['name'].lower().replace(' ', '_')}",
            save_image=True
        )
        
        if result["success"]:
            print(f"✅ {character['name']} generated successfully!")
            print(f"📁 Saved to: {result.get('image_path', 'N/A')}")
        else:
            print(f"❌ {character['name']} failed: {result.get('error', 'Unknown error')}")


def text_rendering_examples():
    """Text rendering and typography examples."""
    print("\n🎨 Text Rendering Examples")
    print("=" * 40)
    
    # Initialize the image generator
    generator = ImageGenerator()
    
    # Different text rendering scenarios
    text_examples = [
        {
            "text": "INNOVATION",
            "style": "bold, modern typography with geometric elements",
            "context": "a tech company logo"
        },
        {
            "text": "Grand Opening",
            "style": "elegant, decorative script with gold accents",
            "context": "a restaurant banner"
        },
        {
            "text": "SUMMER SALE",
            "style": "bold, attention-grabbing display font with bright colors",
            "context": "a retail store poster"
        }
    ]
    
    for i, example in enumerate(text_examples, 1):
        prompt = PromptTemplates.text_rendering(
            text_content=example["text"],
            design_style=example["style"],
            context=example["context"]
        )
        
        result = generator.generate_text_to_image(
            prompt=prompt,
            output_filename=f"text_rendering_{i}",
            save_image=True
        )
        
        if result["success"]:
            print(f"✅ Text rendering {i} generated successfully!")
            print(f"📁 Saved to: {result.get('image_path', 'N/A')}")
        else:
            print(f"❌ Text rendering {i} failed: {result.get('error', 'Unknown error')}")


def professional_photography_styles():
    """Professional photography style examples."""
    print("\n🎨 Professional Photography Styles")
    print("=" * 40)
    
    # Initialize the image generator
    generator = ImageGenerator()
    
    # Different photography styles
    photo_styles = [
        {
            "subject": "a luxury watch",
            "style": "product photography",
            "lighting": "soft, professional studio lighting",
            "angle": CameraAngle.MACRO,
            "background": "clean white background with subtle shadows"
        },
        {
            "subject": "a fashion model in elegant clothing",
            "style": "fashion photography",
            "lighting": "dramatic, high-contrast lighting",
            "angle": CameraAngle.CLOSE_UP,
            "background": "sophisticated urban background"
        },
        {
            "subject": "a chef preparing gourmet food",
            "style": "food photography",
            "lighting": "warm, appetizing lighting",
            "angle": CameraAngle.MACRO,
            "background": "restaurant kitchen setting"
        }
    ]
    
    for i, style in enumerate(photo_styles, 1):
        prompt = PromptTemplates.text_to_image(
            subject=style["subject"],
            style=ImageStyle.PHOTOREALISTIC,
            context=f"professional {style['style']}",
            camera_angle=style["angle"],
            lighting=style["lighting"],
            composition=f"with {style['background']}"
        )
        
        result = generator.generate_text_to_image(
            prompt=prompt,
            output_filename=f"photo_style_{i}",
            save_image=True
        )
        
        if result["success"]:
            print(f"✅ {style['style'].title()} generated successfully!")
            print(f"📁 Saved to: {result.get('image_path', 'N/A')}")
        else:
            print(f"❌ {style['style'].title()} failed: {result.get('error', 'Unknown error')}")


def creative_art_styles():
    """Creative art style examples."""
    print("\n🎨 Creative Art Styles")
    print("=" * 40)
    
    # Initialize the image generator
    generator = ImageGenerator()
    
    # Different art styles
    art_styles = [
        {
            "subject": "a serene landscape with mountains and lake",
            "style": ImageStyle.PAINTING,
            "description": "impressionist painting style with visible brushstrokes"
        },
        {
            "subject": "a futuristic cityscape",
            "style": ImageStyle.ANIME,
            "description": "anime art style with vibrant colors and clean lines"
        },
        {
            "subject": "a portrait of a person",
            "style": ImageStyle.SKETCH,
            "description": "detailed pencil sketch with shading and texture"
        }
    ]
    
    for i, art in enumerate(art_styles, 1):
        prompt = PromptTemplates.text_to_image(
            subject=art["subject"],
            style=art["style"],
            context=f"artistic {art['description']}",
            camera_angle=CameraAngle.WIDE_ANGLE,
            lighting="artistic lighting",
            composition="with artistic composition and visual appeal"
        )
        
        result = generator.generate_text_to_image(
            prompt=prompt,
            output_filename=f"art_style_{i}",
            save_image=True
        )
        
        if result["success"]:
            print(f"✅ {art['style'].value.title()} art generated successfully!")
            print(f"📁 Saved to: {result.get('image_path', 'N/A')}")
        else:
            print(f"❌ {art['style'].value.title()} art failed: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    print("🚀 Gemini Image Generation - Specialized Use Cases Tutorial")
    print("=" * 70)
    
    try:
        # Run all examples
        logo_design_workflow()
        interior_design_visualization()
        character_design_series()
        text_rendering_examples()
        professional_photography_styles()
        creative_art_styles()
        
        print("\n🎉 All tutorials completed successfully!")
        print("Check the 'outputs' directory for generated images.")
        
    except Exception as e:
        print(f"❌ Tutorial failed: {str(e)}")
        print("Make sure you have set up your GEMINI_API_KEY in the .env file.")
