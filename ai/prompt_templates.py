"""
Professional prompt templates for different image generation use cases.
Based on Gemini API best practices for optimal results.
Uses external prompt files from resources/prompts directory.
"""

from typing import Dict, List, Optional
from enum import Enum
from .prompt_loader import PromptLoader


class ImageStyle(Enum):
    """Supported image styles for generation"""
    PHOTOREALISTIC = "photorealistic"
    ARTISTIC = "artistic"
    CARTOON = "cartoon"
    ANIME = "anime"
    SKETCH = "sketch"
    PAINTING = "painting"
    MINIMALIST = "minimalist"
    CUSTOM = "custom"


class CameraAngle(Enum):
    """Camera angles for composition control"""
    WIDE_ANGLE = "wide-angle shot"
    MACRO = "macro shot"
    LOW_ANGLE = "low-angle perspective"
    HIGH_ANGLE = "high-angle perspective"
    CLOSE_UP = "close-up shot"
    BIRD_EYE = "bird's eye view"
    DUTCH_ANGLE = "dutch angle"


class PromptTemplates:
    """Professional prompt templates following Gemini API best practices"""
    
    def __init__(self):
        """Initialize prompt templates with loader."""
        self.loader = PromptLoader()
        # Clear cache to ensure fresh prompts are loaded
        self.loader.reload_cache()
    
    def text_to_image(
        self,
        subject: str,
        style: ImageStyle = ImageStyle.PHOTOREALISTIC,
        context: Optional[str] = None,
        camera_angle: Optional[CameraAngle] = None,
        lighting: Optional[str] = None,
        composition: Optional[str] = None,
        negative_prompt: Optional[str] = None
    ) -> str:
        """
        Generate a professional text-to-image prompt following best practices.
        
        Args:
            subject: Main subject of the image
            style: Visual style of the image
            context: Purpose and context of the image
            camera_angle: Camera composition angle
            lighting: Lighting description
            composition: Compositional elements
            negative_prompt: What to avoid (use positive descriptions instead)
        
        Returns:
            Formatted prompt string
        """
        # Format optional parameters
        angle_text = f", using {camera_angle.value}" if camera_angle else ""
        lighting_text = f", with {lighting}" if lighting else ""
        composition_text = f", and {composition}" if composition else ""
        negative_text = f", ensuring {negative_prompt}" if negative_prompt else ""
        
        return self.loader.format_prompt(
            "text_to_image",
            context=context or "image",
            subject=subject,
            style=style.value,
            angle=angle_text,
            lighting=lighting_text,
            composition=composition_text,
            negative_prompt=negative_text
        )
    
    def inpainting(
        self,
        base_image_description: str,
        mask_area: str,
        replacement_content: str,
        style_consistency: bool = True
    ) -> str:
        """
        Generate inpainting prompt for semantic masking and element replacement.
        
        Args:
            base_image_description: Description of the base image
            mask_area: Area to be modified
            replacement_content: What to replace it with
            style_consistency: Whether to maintain style consistency
        
        Returns:
            Formatted inpainting prompt
        """
        style_text = " while maintaining visual consistency and style" if style_consistency else ""
        
        return self.loader.format_prompt(
            "inpainting",
            base_image_description=base_image_description,
            mask_area=mask_area,
            replacement_content=replacement_content,
            style_consistency=style_text
        )
    
    def style_transfer(
        self,
        source_image_description: str,
        target_style: str,
        preserve_subject: bool = True
    ) -> str:
        """
        Generate style transfer prompt.
        
        Args:
            source_image_description: Description of source image
            target_style: Target style to apply (string)
            preserve_subject: Whether to preserve the main subject
        
        Returns:
            Formatted style transfer prompt
        """
        preserve_text = " while preserving the main subject and composition" if preserve_subject else ""
        
        return self.loader.format_prompt(
            "style_transfer",
            source_image_description=source_image_description,
            target_style=target_style,
            preserve_subject=preserve_text
        )
    
    def multi_image_composition(
        self,
        images: List[str],
        composition_goal: str,
        blending_style: str = "seamless"
    ) -> str:
        """
        Generate multi-image composition prompt.
        
        Args:
            images: List of image descriptions
            composition_goal: Goal of the composition
            blending_style: How to blend the images
        
        Returns:
            Formatted composition prompt
        """
        images_str = ", ".join(images)
        
        return self.loader.format_prompt(
            "multi_image_composition",
            images=images_str,
            composition_goal=composition_goal,
            blending_style=blending_style
        )
    
    def iterative_refinement(
        self,
        base_prompt: str,
        refinement_instruction: str
    ) -> str:
        """
        Generate iterative refinement prompt.
        
        Args:
            base_prompt: Original prompt
            refinement_instruction: Specific refinement to apply
        
        Returns:
            Formatted refinement prompt
        """
        return f"Based on the previous image: {base_prompt}, {refinement_instruction}."
    
    def text_rendering(
        self,
        text_content: str,
        design_style: str,
        context: str
    ) -> str:
        """
        Generate high-fidelity text rendering prompt.
        
        Args:
            text_content: Text to render
            design_style: Design style for the text
            context: Context for the text (logo, poster, etc.)
        
        Returns:
            Formatted text rendering prompt
        """
        return self.loader.format_prompt(
            "text_rendering",
            text_content=text_content,
            design_style=design_style,
            context=context
        )
    
    def step_by_step_instructions(self, steps: List[str]) -> str:
        """
        Generate step-by-step instruction prompt.
        
        Args:
            steps: List of step descriptions
        
        Returns:
            Formatted step-by-step prompt
        """
        step_instructions = []
        for i, step in enumerate(steps, 1):
            step_instructions.append(f"Step {i}: {step}")
        
        steps_text = " ".join(step_instructions)
        
        return self.loader.format_prompt(
            "step_by_step",
            steps=steps_text
        )
    
    def clean_room(
        self,
        specific_objects: Optional[str] = None,
        maintain_layout: bool = True
    ) -> str:
        """
        Generate room cleaning prompt.
        
        Args:
            specific_objects: Specific objects to remove (if None, removes general clutter)
            maintain_layout: Whether to maintain the room layout
        
        Returns:
            Formatted cleaning prompt
        """
        if specific_objects:
            remove_instruction = f"Remove the {specific_objects}"
        else:
            remove_instruction = "Clean up this room by removing all clutter and unnecessary objects"
        
        maintain_text = " while maintaining the original room layout and structure" if maintain_layout else ""
        
        return self.loader.format_prompt(
            "clean_room",
            remove_instruction=remove_instruction,
            maintain_layout=maintain_text
        )


# Pre-defined professional prompts for common use cases
PROFESSIONAL_PROMPTS = {
    "logo_design": {
        "template": "Create a {style} logo for a {industry} company with the text '{company_name}' in {color_scheme} colors, {design_elements}",
        "variables": ["style", "industry", "company_name", "color_scheme", "design_elements"]
    },
    "product_photography": {
        "template": "Professional product photography of {product} on {background} with {lighting} lighting, {camera_angle}",
        "variables": ["product", "background", "lighting", "camera_angle"]
    },
    "interior_design": {
        "template": "Interior design rendering of a {room_type} in {style} style with {furniture} and {lighting} lighting, {camera_angle}",
        "variables": ["room_type", "style", "furniture", "lighting", "camera_angle"]
    },
    "character_design": {
        "template": "Character design of a {character_type} with {physical_features} wearing {clothing} in {setting}, {art_style} style",
        "variables": ["character_type", "physical_features", "clothing", "setting", "art_style"]
    }
}
