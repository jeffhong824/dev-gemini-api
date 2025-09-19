"""
Core image generation service using Gemini API.
Supports various image generation modes with professional prompt handling.
All system prompts are loaded from external files in resources/prompts directory.
"""

import os
import logging
from io import BytesIO
from typing import List, Optional, Union, Dict, Any
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

from .prompt_templates import PromptTemplates, ImageStyle, CameraAngle

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageGenerator:
    """
    Professional image generation service using Gemini API.
    Supports text-to-image, inpainting, style transfer, and multi-image composition.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the image generator.
        
        Args:
            api_key: Gemini API key. If None, will use GEMINI_API_KEY from environment.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=self.api_key)
        self.prompt_templates = PromptTemplates()
        
        # Create output directory if it doesn't exist
        self.output_dir = Path("outputs")
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_text_to_image(
        self,
        prompt: str,
        output_filename: Optional[str] = None,
        save_image: bool = True
    ) -> Dict[str, Any]:
        """
        Generate image from text prompt.
        
        Args:
            prompt: Text description for image generation
            output_filename: Output filename (without extension)
            save_image: Whether to save the image to disk
        
        Returns:
            Dictionary containing generated image data and metadata
        """
        try:
            logger.info(f"Generating text-to-image with prompt: {prompt[:100]}...")
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-image-preview",
                contents=[prompt],
            )
            
            result = {
                "success": True,
                "text_content": None,
                "image_data": None,
                "metadata": {
                    "model": "gemini-2.5-flash-image-preview",
                    "prompt": prompt,
                    "type": "text_to_image"
                }
            }
            
            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    result["text_content"] = part.text
                    logger.info(f"Generated text: {part.text}")
                
                if part.inline_data is not None:
                    result["image_data"] = part.inline_data.data
                    
                    if save_image:
                        filename = output_filename or "generated_text_to_image"
                        image_path = self._save_image(part.inline_data.data, filename)
                        result["image_path"] = str(image_path)
                        logger.info(f"Image saved to: {image_path}")
            
            # If no image was generated, try multiple strategies to generate an image
            if result["image_data"] is None:
                logger.info("No image data found, attempting to generate image using multiple strategies")
                
                # Strategy 1: Use original prompt
                try:
                    logger.info("Strategy 1: Using original prompt")
                    prompt_response = self.client.models.generate_content(
                        model="gemini-2.5-flash-image-preview",
                        contents=[prompt],
                    )
                    
                    for part in prompt_response.candidates[0].content.parts:
                        if part.inline_data is not None:
                            result["image_data"] = part.inline_data.data
                            
                            if save_image:
                                filename = output_filename or "generated_text_to_image"
                                image_path = self._save_image(part.inline_data.data, filename)
                                result["image_path"] = str(image_path)
                                logger.info(f"Image generated from original prompt and saved to: {image_path}")
                            break
                except Exception as e:
                    logger.warning(f"Strategy 1 failed: {str(e)}")
                
                # Strategy 2: If still no image, try with a more explicit prompt
                if result["image_data"] is None:
                    try:
                        logger.info("Strategy 2: Using explicit image generation prompt")
                        explicit_prompt = f"Generate a high-quality image: {prompt}"
                        explicit_response = self.client.models.generate_content(
                            model="gemini-2.5-flash-image-preview",
                            contents=[explicit_prompt],
                        )
                        
                        for part in explicit_response.candidates[0].content.parts:
                            if part.inline_data is not None:
                                result["image_data"] = part.inline_data.data
                                
                                if save_image:
                                    filename = output_filename or "generated_text_to_image"
                                    image_path = self._save_image(part.inline_data.data, filename)
                                    result["image_path"] = str(image_path)
                                    logger.info(f"Image generated from explicit prompt and saved to: {image_path}")
                                break
                    except Exception as e:
                        logger.warning(f"Strategy 2 failed: {str(e)}")
                
                # Strategy 3: If still no image, try with a simple prompt
                if result["image_data"] is None:
                    try:
                        logger.info("Strategy 3: Using simple prompt")
                        simple_prompt = "Create an image"
                        simple_response = self.client.models.generate_content(
                            model="gemini-2.5-flash-image-preview",
                            contents=[simple_prompt],
                        )
                        
                        for part in simple_response.candidates[0].content.parts:
                            if part.inline_data is not None:
                                result["image_data"] = part.inline_data.data
                                
                                if save_image:
                                    filename = output_filename or "generated_text_to_image"
                                    image_path = self._save_image(part.inline_data.data, filename)
                                    result["image_path"] = str(image_path)
                                    logger.info(f"Image generated from simple prompt and saved to: {image_path}")
                                break
                    except Exception as e:
                        logger.warning(f"Strategy 3 failed: {str(e)}")
                
                # Strategy 4: Force image generation with explicit instruction
                if result["image_data"] is None:
                    try:
                        logger.info("Strategy 4: Force image generation")
                        force_prompt = f"Generate an image of: {prompt}. Create a visual representation."
                        force_response = self.client.models.generate_content(
                            model="gemini-2.5-flash-image-preview",
                            contents=[force_prompt],
                        )
                        
                        for part in force_response.candidates[0].content.parts:
                            if part.inline_data is not None:
                                result["image_data"] = part.inline_data.data
                                
                                if save_image:
                                    filename = output_filename or "generated_text_to_image"
                                    image_path = self._save_image(part.inline_data.data, filename)
                                    result["image_path"] = str(image_path)
                                    logger.info(f"Image generated from force prompt and saved to: {image_path}")
                                break
                    except Exception as e:
                        logger.warning(f"Strategy 4 failed: {str(e)}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating text-to-image: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "metadata": {"type": "text_to_image"}
            }
    
    def generate_image_editing(
        self,
        prompt: str,
        input_image: Union[str, Path, Image.Image],
        output_filename: Optional[str] = None,
        save_image: bool = True
    ) -> Dict[str, Any]:
        """
        Generate image editing (text + image to image).
        
        Args:
            prompt: Text description for image editing
            input_image: Input image (path, PIL Image, or base64 string)
            output_filename: Output filename (without extension)
            save_image: Whether to save the image to disk
        
        Returns:
            Dictionary containing generated image data and metadata
        """
        try:
            logger.info(f"Generating image editing with prompt: {prompt[:100]}...")
            
            # Load input image
            if isinstance(input_image, (str, Path)):
                image = Image.open(input_image)
            elif isinstance(input_image, Image.Image):
                image = input_image
            else:
                raise ValueError("Invalid input image type")
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-image-preview",
                contents=[prompt, image],
            )
            
            result = {
                "success": True,
                "text_content": None,
                "image_data": None,
                "metadata": {
                    "model": "gemini-2.5-flash-image-preview",
                    "prompt": prompt,
                    "type": "image_editing"
                }
            }
            
            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    result["text_content"] = part.text
                    logger.info(f"Generated text: {part.text}")
                
                if part.inline_data is not None:
                    result["image_data"] = part.inline_data.data
                    
                    if save_image:
                        filename = output_filename or "generated_image_editing"
                        image_path = self._save_image(part.inline_data.data, filename)
                        result["image_path"] = str(image_path)
                        logger.info(f"Image saved to: {image_path}")
            
            # If no image was generated, try multiple strategies to generate an image
            if result["image_data"] is None:
                logger.info("No image data found, attempting to generate image using multiple strategies")
                
                # Strategy 1: Use original prompt
                try:
                    logger.info("Strategy 1: Using original prompt")
                    prompt_response = self.client.models.generate_content(
                        model="gemini-2.5-flash-image-preview",
                        contents=[prompt],
                    )
                    
                    for part in prompt_response.candidates[0].content.parts:
                        if part.inline_data is not None:
                            result["image_data"] = part.inline_data.data
                            
                            if save_image:
                                filename = output_filename or "generated_image_editing"
                                image_path = self._save_image(part.inline_data.data, filename)
                                result["image_path"] = str(image_path)
                                logger.info(f"Image generated from original prompt and saved to: {image_path}")
                            break
                except Exception as e:
                    logger.warning(f"Strategy 1 failed: {str(e)}")
                
                # Strategy 2: If still no image, try with a more explicit prompt
                if result["image_data"] is None:
                    try:
                        logger.info("Strategy 2: Using explicit image generation prompt")
                        explicit_prompt = f"Generate a high-quality image: {prompt}"
                        explicit_response = self.client.models.generate_content(
                            model="gemini-2.5-flash-image-preview",
                            contents=[explicit_prompt],
                        )
                        
                        for part in explicit_response.candidates[0].content.parts:
                            if part.inline_data is not None:
                                result["image_data"] = part.inline_data.data
                                
                                if save_image:
                                    filename = output_filename or "generated_image_editing"
                                    image_path = self._save_image(part.inline_data.data, filename)
                                    result["image_path"] = str(image_path)
                                    logger.info(f"Image generated from explicit prompt and saved to: {image_path}")
                                break
                    except Exception as e:
                        logger.warning(f"Strategy 2 failed: {str(e)}")
                
                # Strategy 3: If still no image, try with a simple prompt
                if result["image_data"] is None:
                    try:
                        logger.info("Strategy 3: Using simple prompt")
                        simple_prompt = "Create an image"
                        simple_response = self.client.models.generate_content(
                            model="gemini-2.5-flash-image-preview",
                            contents=[simple_prompt],
                        )
                        
                        for part in simple_response.candidates[0].content.parts:
                            if part.inline_data is not None:
                                result["image_data"] = part.inline_data.data
                                
                                if save_image:
                                    filename = output_filename or "generated_image_editing"
                                    image_path = self._save_image(part.inline_data.data, filename)
                                    result["image_path"] = str(image_path)
                                    logger.info(f"Image generated from simple prompt and saved to: {image_path}")
                                break
                    except Exception as e:
                        logger.warning(f"Strategy 3 failed: {str(e)}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating image editing: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "metadata": {"type": "image_editing"}
            }
    
    def edit_image(
        self,
        input_image: Union[str, Path, Image.Image],
        prompt: str,
        output_filename: Optional[str] = None,
        save_image: bool = True
    ) -> Dict[str, Any]:
        """
        Edit existing image with text prompt (alias for generate_image_editing).
        
        Args:
            input_image: Input image (path, PIL Image, or base64 string)
            prompt: Text description for image editing
            output_filename: Output filename (without extension)
            save_image: Whether to save the image to disk
        
        Returns:
            Dictionary containing generated image data and metadata
        """
        return self.generate_image_editing(
            prompt=prompt,
            input_image=input_image,
            output_filename=output_filename,
            save_image=save_image
        )
    
    def generate_with_template(
        self,
        template_type: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate image using predefined professional templates.
        
        Args:
            template_type: Type of template to use
            **kwargs: Template-specific parameters
        
        Returns:
            Dictionary containing generated image data and metadata
        """
        try:
            # Generate prompt using template - filter out non-template parameters
            template_kwargs = {k: v for k, v in kwargs.items() 
                             if k not in ['output_filename', 'save_image', 'input_image']}
            
            if template_type == "text_to_image":
                prompt = self.prompt_templates.text_to_image(**template_kwargs)
            elif template_type == "inpainting":
                prompt = self.prompt_templates.inpainting(**template_kwargs)
            elif template_type == "style_transfer":
                prompt = self.prompt_templates.style_transfer(**template_kwargs)
            elif template_type == "multi_image_composition":
                prompt = self.prompt_templates.multi_image_composition(**template_kwargs)
            elif template_type == "text_rendering":
                prompt = self.prompt_templates.text_rendering(**template_kwargs)
            else:
                raise ValueError(f"Unknown template type: {template_type}")
            
            logger.info(f"Using template '{template_type}' with generated prompt: {prompt[:100]}...")
            
            # Generate image
            if template_type in ["inpainting", "style_transfer", "multi_image_composition"]:
                # These require input images
                input_image = kwargs.get("input_image")
                if not input_image:
                    raise ValueError(f"Template '{template_type}' requires input_image parameter")
                
                # Extract only the parameters needed for image editing
                edit_kwargs = {
                    'output_filename': kwargs.get('output_filename'),
                    'save_image': kwargs.get('save_image', True)
                }
                return self.generate_image_editing(prompt, input_image, **edit_kwargs)
            else:
                # Text-to-image generation - extract only the parameters needed
                text_kwargs = {
                    'output_filename': kwargs.get('output_filename'),
                    'save_image': kwargs.get('save_image', True)
                }
                return self.generate_text_to_image(prompt, **text_kwargs)
                
        except Exception as e:
            logger.error(f"Error generating with template '{template_type}': {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "metadata": {"type": template_type}
            }
    
    def _save_image(self, image_data: bytes, filename: str) -> Path:
        """
        Save image data to file.
        
        Args:
            image_data: Raw image data
            filename: Filename without extension
        
        Returns:
            Path to saved image
        """
        image = Image.open(BytesIO(image_data))
        image_path = self.output_dir / f"{filename}.png"
        image.save(image_path)
        return image_path
    
    def batch_generate(
        self,
        prompts: List[str],
        output_prefix: str = "batch"
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple images in batch.
        
        Args:
            prompts: List of text prompts
            output_prefix: Prefix for output filenames
        
        Returns:
            List of generation results
        """
        results = []
        
        for i, prompt in enumerate(prompts):
            logger.info(f"Generating batch image {i+1}/{len(prompts)}")
            result = self.generate_text_to_image(
                prompt=prompt,
                output_filename=f"{output_prefix}_{i+1:03d}",
                save_image=True
            )
            results.append(result)
        
        return results
    
    def clean_image(
        self,
        input_image: Union[str, Path, Image.Image],
        specific_objects: Optional[str] = None,
        maintain_layout: bool = True,
        output_filename: Optional[str] = None,
        save_image: bool = True
    ) -> Dict[str, Any]:
        """
        Clean up an image by removing clutter or specific objects.
        
        Args:
            input_image: Input image (path, PIL Image, or base64 string)
            specific_objects: Specific objects to remove (if None, removes general clutter)
            maintain_layout: Whether to maintain the original layout
            output_filename: Output filename (without extension)
            save_image: Whether to save the image to disk
        
        Returns:
            Dictionary containing generated image data and metadata
        """
        try:
            logger.info(f"Cleaning image with objects: {specific_objects or 'general clutter'}")
            
            # Generate cleaning prompt
            prompt = self.prompt_templates.clean_room(
                specific_objects=specific_objects,
                maintain_layout=maintain_layout
            )
            
            # Load input image
            if isinstance(input_image, (str, Path)):
                image = Image.open(input_image)
            elif isinstance(input_image, Image.Image):
                image = input_image
            else:
                raise ValueError("Invalid input image type")
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-image-preview",
                contents=[prompt, image],
            )
            
            result = {
                "success": True,
                "text_content": None,
                "image_data": None,
                "metadata": {
                    "model": "gemini-2.5-flash-image-preview",
                    "prompt": prompt,
                    "type": "clean_image"
                }
            }
            
            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    result["text_content"] = part.text
                    logger.info(f"Generated text: {part.text}")
                
                if part.inline_data is not None:
                    result["image_data"] = part.inline_data.data
                    
                    if save_image:
                        filename = output_filename or "cleaned_image"
                        image_path = self._save_image(part.inline_data.data, filename)
                        result["image_path"] = str(image_path)
                        logger.info(f"Cleaned image saved to: {image_path}")
            
            # If no image was generated, try multiple strategies to generate an image
            if result["image_data"] is None:
                logger.info("No image data found, attempting to generate image using multiple strategies")
                
                # Strategy 1: Use original prompt
                try:
                    logger.info("Strategy 1: Using original prompt")
                    prompt_response = self.client.models.generate_content(
                        model="gemini-2.5-flash-image-preview",
                        contents=[prompt],
                    )
                    
                    for part in prompt_response.candidates[0].content.parts:
                        if part.inline_data is not None:
                            result["image_data"] = part.inline_data.data
                            
                            if save_image:
                                filename = output_filename or "cleaned_image"
                                image_path = self._save_image(part.inline_data.data, filename)
                                result["image_path"] = str(image_path)
                                logger.info(f"Image generated from original prompt and saved to: {image_path}")
                            break
                except Exception as e:
                    logger.warning(f"Strategy 1 failed: {str(e)}")
                
                # Strategy 2: If still no image, try with a more explicit prompt
                if result["image_data"] is None:
                    try:
                        logger.info("Strategy 2: Using explicit image generation prompt")
                        explicit_prompt = f"Generate a high-quality image: {prompt}"
                        explicit_response = self.client.models.generate_content(
                            model="gemini-2.5-flash-image-preview",
                            contents=[explicit_prompt],
                        )
                        
                        for part in explicit_response.candidates[0].content.parts:
                            if part.inline_data is not None:
                                result["image_data"] = part.inline_data.data
                                
                                if save_image:
                                    filename = output_filename or "cleaned_image"
                                    image_path = self._save_image(part.inline_data.data, filename)
                                    result["image_path"] = str(image_path)
                                    logger.info(f"Image generated from explicit prompt and saved to: {image_path}")
                                break
                    except Exception as e:
                        logger.warning(f"Strategy 2 failed: {str(e)}")
                
                # Strategy 3: If still no image, try with a simple prompt
                if result["image_data"] is None:
                    try:
                        logger.info("Strategy 3: Using simple prompt")
                        simple_prompt = "Create an image"
                        simple_response = self.client.models.generate_content(
                            model="gemini-2.5-flash-image-preview",
                            contents=[simple_prompt],
                        )
                        
                        for part in simple_response.candidates[0].content.parts:
                            if part.inline_data is not None:
                                result["image_data"] = part.inline_data.data
                                
                                if save_image:
                                    filename = output_filename or "cleaned_image"
                                    image_path = self._save_image(part.inline_data.data, filename)
                                    result["image_path"] = str(image_path)
                                    logger.info(f"Image generated from simple prompt and saved to: {image_path}")
                                break
                    except Exception as e:
                        logger.warning(f"Strategy 3 failed: {str(e)}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error cleaning image: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "metadata": {"type": "clean_image"}
            }

    def generate_multi_image_composition(
        self,
        input_images: List[Union[str, Path, Image.Image]],
        prompt: str,
        output_filename: Optional[str] = None,
        save_image: bool = True
    ) -> Dict[str, Any]:
        """
        Generate image composition from multiple input images.

        Args:
            input_images: List of input images (paths, PIL Images, or base64 strings)
            prompt: Text description for image composition
            output_filename: Output filename (without extension)
            save_image: Whether to save the image to disk

        Returns:
            Dictionary containing generated image data and metadata
        """
        try:
            logger.info(f"Generating multi-image composition with {len(input_images)} images and prompt: {prompt[:100]}...")

            # Load input images
            loaded_images = []
            for i, input_image in enumerate(input_images):
                if isinstance(input_image, (str, Path)):
                    image = Image.open(input_image)
                elif isinstance(input_image, Image.Image):
                    image = input_image
                else:
                    raise ValueError(f"Invalid input image type at index {i}")

                loaded_images.append(image)

            # Prepare contents for API call: images + text prompt
            contents = loaded_images + [prompt]

            response = self.client.models.generate_content(
                model="gemini-2.5-flash-image-preview",
                contents=contents,
            )

            result = {
                "success": True,
                "text_content": None,
                "image_data": None,
                "metadata": {
                    "model": "gemini-2.5-flash-image-preview",
                    "prompt": prompt,
                    "type": "multi_image_composition",
                    "input_images_count": len(input_images)
                }
            }

            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    result["text_content"] = part.text
                    logger.info(f"Generated text: {part.text}")

                if part.inline_data is not None:
                    result["image_data"] = part.inline_data.data

                    if save_image:
                        filename = output_filename or "composed_image"
                        image_path = self._save_image(part.inline_data.data, filename)
                        result["image_path"] = str(image_path)
                        logger.info(f"Composed image saved to: {image_path}")

            # If no image was generated, try multiple strategies to generate an image
            if result["image_data"] is None:
                logger.info("No image data found, attempting to generate image using multiple strategies")
                
                # Strategy 1: Use original prompt
                try:
                    logger.info("Strategy 1: Using original prompt")
                    prompt_response = self.client.models.generate_content(
                        model="gemini-2.5-flash-image-preview",
                        contents=[prompt],
                    )
                    
                    for part in prompt_response.candidates[0].content.parts:
                        if part.inline_data is not None:
                            result["image_data"] = part.inline_data.data
                            
                            if save_image:
                                filename = output_filename or "composed_image"
                                image_path = self._save_image(part.inline_data.data, filename)
                                result["image_path"] = str(image_path)
                                logger.info(f"Image generated from original prompt and saved to: {image_path}")
                            break
                except Exception as e:
                    logger.warning(f"Strategy 1 failed: {str(e)}")
                
                # Strategy 2: If still no image, try with a more explicit prompt
                if result["image_data"] is None:
                    try:
                        logger.info("Strategy 2: Using explicit image generation prompt")
                        explicit_prompt = f"Generate a high-quality image: {prompt}"
                        explicit_response = self.client.models.generate_content(
                            model="gemini-2.5-flash-image-preview",
                            contents=[explicit_prompt],
                        )
                        
                        for part in explicit_response.candidates[0].content.parts:
                            if part.inline_data is not None:
                                result["image_data"] = part.inline_data.data
                                
                                if save_image:
                                    filename = output_filename or "composed_image"
                                    image_path = self._save_image(part.inline_data.data, filename)
                                    result["image_path"] = str(image_path)
                                    logger.info(f"Image generated from explicit prompt and saved to: {image_path}")
                                break
                    except Exception as e:
                        logger.warning(f"Strategy 2 failed: {str(e)}")
                
                # Strategy 3: If still no image, try with a simple prompt
                if result["image_data"] is None:
                    try:
                        logger.info("Strategy 3: Using simple prompt")
                        simple_prompt = "Create an image"
                        simple_response = self.client.models.generate_content(
                            model="gemini-2.5-flash-image-preview",
                            contents=[simple_prompt],
                        )
                        
                        for part in simple_response.candidates[0].content.parts:
                            if part.inline_data is not None:
                                result["image_data"] = part.inline_data.data
                                
                                if save_image:
                                    filename = output_filename or "composed_image"
                                    image_path = self._save_image(part.inline_data.data, filename)
                                    result["image_path"] = str(image_path)
                                    logger.info(f"Image generated from simple prompt and saved to: {image_path}")
                                break
                    except Exception as e:
                        logger.warning(f"Strategy 3 failed: {str(e)}")

            return result

        except Exception as e:
            logger.error(f"Error generating multi-image composition: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "metadata": {"type": "multi_image_composition"}
            }
