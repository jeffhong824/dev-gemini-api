"""
Gemini Image Generation API - Modular Entry Point
Usage: python gemini_api.py <command> [options]

A modular image generation service supporting:
- Text-to-Image: Generate high-quality images from text descriptions
- Image + Text-to-Image (Editing): Edit existing images with text prompts
- Multi-Image to Image (Composition & Style Transfer): Compose multiple images
- Iterative Refinement: Progressively refine images
- High-Fidelity Text Rendering: Generate images with legible text
- Room Cleaning: Specialized editing for room clutter removal

All system prompts are externalized to ai/resources/prompts/ directory.
"""

import sys
import argparse
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from ai import ImageGenerator, ImageStyle, CameraAngle
from ai.prompt_templates import PromptTemplates


def cmd_generate(args):
    """Generate images from text descriptions (Text-to-Image)"""
    generator = ImageGenerator()
    
    # Determine style
    if args.style == 'custom' and args.custom_style:
        style = args.custom_style
    elif args.style:
        style = args.style
    else:
        style = 'photorealistic'
    
    # Build prompt with optional parameters
    prompt_parts = [args.prompt]
    
    if args.context:
        prompt_parts.insert(0, f"Create a {args.context} featuring")
        prompt_parts.append("")
    
    if args.angle:
        angle_map = {
            'wide_angle': 'wide-angle shot',
            'close_up': 'close-up shot', 
            'bird_eye': "bird's eye view",
            'dutch_angle': 'dutch angle'
        }
        prompt_parts.append(f"using {angle_map[args.angle]}")
    
    if args.lighting:
        prompt_parts.append(f"with {args.lighting}")
    
    if args.composition:
        prompt_parts.append(f"and {args.composition}")
    
    # Join and clean up prompt
    full_prompt = " ".join(filter(None, prompt_parts))
    if not full_prompt.endswith('.'):
        full_prompt += f" in {style} style."
    else:
        full_prompt += f" in {style} style."
    
    result = generator.generate_text_to_image(
        prompt=full_prompt,
        output_filename=args.output,
        save_image=True
    )
    
    if result["success"]:
        print(f"✅ Image generated successfully: {result.get('image_path', 'N/A')}")
    else:
        print(f"❌ Generation failed: {result.get('error', 'Unknown error')}")


def cmd_edit(args):
    """Edit existing images with text prompts (Image + Text-to-Image)"""
    generator = ImageGenerator()
    
    # Determine style
    if args.style == 'custom' and args.custom_style:
        style_text = f" in {args.custom_style} style"
    elif args.style:
        style_text = f" in {args.style} style"
    else:
        style_text = ""
    
    # Build edit prompt
    edit_prompt = f"{args.prompt}{style_text}"
    
    result = generator.edit_image(
        input_image=args.input,
        prompt=edit_prompt,
        output_filename=args.output,
        save_image=True
    )
    
    if result["success"]:
        print(f"✅ Image edited successfully: {result.get('image_path', 'N/A')}")
    else:
        print(f"❌ Editing failed: {result.get('error', 'Unknown error')}")


def cmd_clean(args):
    """Clean room clutter and unnecessary objects"""
    generator = ImageGenerator()
    
    result = generator.clean_image(
        input_image=args.input,
        specific_objects=args.objects,
        maintain_layout=not args.no_layout,
        output_filename=args.output,
        save_image=True
    )
    
    if result["success"]:
        print(f"✅ Image cleaned successfully: {result.get('image_path', 'N/A')}")
    else:
        print(f"❌ Cleaning failed: {result.get('error', 'Unknown error')}")


def cmd_style(args):
    """Transfer style from one image to another (Style Transfer)"""
    generator = ImageGenerator()
    
    # Determine target style
    if args.target_style == 'custom' and args.custom_style:
        target_style = args.custom_style
    elif args.target_style:
        target_style = args.target_style
    else:
        target_style = 'artistic'
    
    # Build style transfer prompt
    preserve_text = " while preserving the main subject and composition" if args.preserve_subject else ""
    style_prompt = f"Apply {target_style} style to this image{preserve_text}"
    
    result = generator.edit_image(
        input_image=args.input,
        prompt=style_prompt,
        output_filename=args.output,
        save_image=True
    )
    
    if result["success"]:
        print(f"✅ Style transfer completed: {result.get('image_path', 'N/A')}")
    else:
        print(f"❌ Style transfer failed: {result.get('error', 'Unknown error')}")


def cmd_composition(args):
    """Compose multiple images into a new scene (Multi-Image to Image)"""
    generator = ImageGenerator()
    
    if len(args.inputs) < 2 or len(args.inputs) > 3:
        print("❌ Composition requires 2-3 input images")
        return
    
    # Build composition prompt
    images_text = ", ".join([f"image {i+1}" for i in range(len(args.inputs))])
    composition_prompt = f"Combine {images_text} to create {args.goal} with {args.blending} blending"
    
    # For now, use the first image as base and edit with composition prompt
    # In a full implementation, this would handle multiple images
    result = generator.edit_image(
        input_image=args.inputs[0],
        prompt=composition_prompt,
        output_filename=args.output,
        save_image=True
    )
    
    if result["success"]:
        print(f"✅ Composition completed: {result.get('image_path', 'N/A')}")
    else:
        print(f"❌ Composition failed: {result.get('error', 'Unknown error')}")


def cmd_templates(args):
    """Show available prompt templates"""
    templates = PromptTemplates()
    
    if args.type == 'text':
        if args.subject and args.style:
            style_enum = getattr(ImageStyle, args.style.upper(), ImageStyle.PHOTOREALISTIC)
            prompt = templates.text_to_image(
                subject=args.subject,
                style=style_enum,
                context=args.context or "image"
            )
            print(f"Generated prompt: {prompt}")
        else:
            print("Text-to-Image template:")
            print("Usage: --subject 'main subject' --style 'style_name' --context 'purpose'")
            print("Available styles: photorealistic, artistic, cartoon, anime, oil_painting, watercolor, sketch, digital_art")
    
    elif args.type == 'edit':
        print("Image Editing template:")
        print("Usage: Provide --input image and --prompt 'edit instruction'")
        print("Example: 'Add a cat sitting on the sofa' or 'Change the background to a beach scene'")
    
    elif args.type == 'style':
        print("Style Transfer template:")
        print("Usage: Provide --input image and --target_style 'style_name'")
        print("Available styles: photorealistic, artistic, cartoon, anime, oil_painting, watercolor, sketch, digital_art")
    
    elif args.type == 'composition':
        print("Multi-Image Composition template:")
        print("Usage: Provide --inputs 'image1 image2 image3' and --goal 'composition goal'")
        print("Example: 'modern living room layout' or 'product showcase'")
    
    elif args.type == 'clean':
        print("Room Cleaning template:")
        print("Usage: Provide --input image and optionally --objects 'specific items'")
        print("Example: 'books and magazines' or leave empty for general clutter removal")
    
    else:
        print("Available template types: text, edit, style, composition, clean")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Gemini Image Generation API - Modular Image Generation Service',
        epilog="""
Examples:
  # Text-to-Image generation
  python gemini_api.py generate --prompt "a modern living room with minimalist design"
  python gemini_api.py generate --prompt "coffee cup" --style artistic --context "product photography"
  
  # Image editing
  python gemini_api.py edit --input assets/images/living_room.png --prompt "add a cat on the sofa"
  python gemini_api.py edit --input assets/images/living_room.png --prompt "change to night scene" --style custom --custom_style "dark moody lighting"
  
  # Room cleaning
  python gemini_api.py clean --input assets/images/living_room.png --objects "books and magazines"
  python gemini_api.py clean --input assets/images/living_room.png  # clean all clutter
  
  # Style transfer
  python gemini_api.py style --input assets/images/living_room.png --target_style oil_painting
  python gemini_api.py style --input assets/images/living_room.png --target_style custom --custom_style "vintage sepia tone"
  
  # Multi-image composition
  python gemini_api.py composition --inputs assets/images/living_room.png assets/images/model.png --goal "modern living room with person"
  
  # Show templates
  python gemini_api.py templates --type text --subject "modern sofa" --style photorealistic
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command - Text-to-Image
    generate_parser = subparsers.add_parser('generate', help='Generate images from text descriptions')
    generate_parser.add_argument('--prompt', required=True, help='Text prompt for image generation')
    generate_parser.add_argument('--style', choices=['photorealistic', 'artistic', 'cartoon', 'anime', 'oil_painting', 'watercolor', 'sketch', 'digital_art', 'custom'], default='photorealistic', help='Image style (use custom for free-form style description)')
    generate_parser.add_argument('--custom_style', help='Custom style description (when style=custom)')
    generate_parser.add_argument('--context', help='Context or purpose (e.g., product photography, logo design)')
    generate_parser.add_argument('--angle', choices=['wide_angle', 'close_up', 'bird_eye', 'dutch_angle'], help='Camera angle')
    generate_parser.add_argument('--lighting', help='Lighting description')
    generate_parser.add_argument('--composition', help='Composition elements')
    generate_parser.add_argument('--output', '-o', default='generated', help='Output filename')
    generate_parser.set_defaults(func=cmd_generate)
    
    # Edit command - Image + Text-to-Image (Editing)
    edit_parser = subparsers.add_parser('edit', help='Edit existing images with text prompts')
    edit_parser.add_argument('--input', '-i', required=True, help='Input image path')
    edit_parser.add_argument('--prompt', required=True, help='Edit instruction (add, remove, modify elements)')
    edit_parser.add_argument('--style', choices=['photorealistic', 'artistic', 'cartoon', 'anime', 'oil_painting', 'watercolor', 'sketch', 'digital_art', 'custom'], help='Target style for editing')
    edit_parser.add_argument('--custom_style', help='Custom style description (when style=custom)')
    edit_parser.add_argument('--output', '-o', default='edited', help='Output filename')
    edit_parser.set_defaults(func=cmd_edit)
    
    # Clean command - Specialized editing for room cleaning
    clean_parser = subparsers.add_parser('clean', help='Clean room clutter and unnecessary objects')
    clean_parser.add_argument('--input', '-i', required=True, help='Input image path')
    clean_parser.add_argument('--objects', help='Specific objects to remove (optional, removes general clutter if not specified)')
    clean_parser.add_argument('--no-layout', action='store_true', help='Do not maintain original room layout')
    clean_parser.add_argument('--output', '-o', default='cleaned', help='Output filename')
    clean_parser.set_defaults(func=cmd_clean)
    
    # Style command - Style Transfer
    style_parser = subparsers.add_parser('style', help='Transfer style from one image to another')
    style_parser.add_argument('--input', '-i', required=True, help='Input image path')
    style_parser.add_argument('--target_style', choices=['photorealistic', 'artistic', 'cartoon', 'anime', 'oil_painting', 'watercolor', 'sketch', 'digital_art', 'custom'], default='artistic', help='Target style')
    style_parser.add_argument('--custom_style', help='Custom style description (when target_style=custom)')
    style_parser.add_argument('--preserve_subject', action='store_true', default=True, help='Preserve main subject and composition')
    style_parser.add_argument('--output', '-o', default='styled', help='Output filename')
    style_parser.set_defaults(func=cmd_style)
    
    # Composition command - Multi-Image to Image
    composition_parser = subparsers.add_parser('composition', help='Compose multiple images into a new scene')
    composition_parser.add_argument('--inputs', '-i', nargs='+', required=True, help='Input image paths (2-3 images)')
    composition_parser.add_argument('--goal', required=True, help='Composition goal (e.g., "modern living room layout", "product showcase")')
    composition_parser.add_argument('--blending', choices=['seamless', 'artistic', 'collage', 'overlay'], default='seamless', help='Blending style')
    composition_parser.add_argument('--output', '-o', default='composition', help='Output filename')
    composition_parser.set_defaults(func=cmd_composition)
    
    # Templates command - Show available templates
    templates_parser = subparsers.add_parser('templates', help='Show available prompt templates')
    templates_parser.add_argument('--type', choices=['text', 'edit', 'style', 'composition', 'clean'], help='Template type')
    templates_parser.add_argument('--subject', help='Subject for template preview')
    templates_parser.add_argument('--style', choices=['photorealistic', 'artistic', 'cartoon', 'anime', 'oil_painting', 'watercolor', 'sketch', 'digital_art'], help='Style for template preview')
    templates_parser.add_argument('--context', help='Context for template preview')
    templates_parser.set_defaults(func=cmd_templates)
    
    # Parse arguments and execute command
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        args.func(args)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()