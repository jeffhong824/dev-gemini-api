"""
AI Services for Gemini Image Generation

This module provides core AI services for image generation using the Gemini API.
All system prompts are externalized to resources/prompts directory for better
maintainability and customization.
"""

from .image_generator import ImageGenerator
from .prompt_templates import PromptTemplates, ImageStyle, CameraAngle
from .prompt_loader import PromptLoader

__all__ = ["ImageGenerator", "PromptTemplates", "ImageStyle", "CameraAngle", "PromptLoader"]
