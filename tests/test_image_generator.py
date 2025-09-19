"""
Tests for ImageGenerator class
"""

import pytest
import os
from unittest.mock import Mock, patch
from ai.image_generator import ImageGenerator
from ai.prompt_templates import ImageStyle, CameraAngle


class TestImageGenerator:
    """Test cases for ImageGenerator class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        # Mock the API key for testing
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
            self.generator = ImageGenerator()
    
    def test_initialization_with_api_key(self):
        """Test initialization with API key"""
        generator = ImageGenerator(api_key="test_key")
        assert generator.api_key == "test_key"
    
    def test_initialization_without_api_key(self):
        """Test initialization without API key raises error"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="GEMINI_API_KEY environment variable is required"):
                ImageGenerator()
    
    @patch('ai.image_generator.genai.Client')
    def test_generate_text_to_image_success(self, mock_client):
        """Test successful text-to-image generation"""
        # Mock the response
        mock_response = Mock()
        mock_response.candidates = [Mock()]
        mock_response.candidates[0].content.parts = [Mock()]
        mock_response.candidates[0].content.parts[0].inline_data = Mock()
        mock_response.candidates[0].content.parts[0].inline_data.data = b"fake_image_data"
        mock_response.candidates[0].content.parts[0].text = None
        
        mock_client.return_value.models.generate_content.return_value = mock_response
        
        result = self.generator.generate_text_to_image(
            prompt="test prompt",
            output_filename="test",
            save_image=False
        )
        
        assert result["success"] is True
        assert result["image_data"] == b"fake_image_data"
        assert result["metadata"]["type"] == "text_to_image"
    
    @patch('ai.image_generator.genai.Client')
    def test_generate_text_to_image_failure(self, mock_client):
        """Test text-to-image generation failure"""
        # Mock the exception
        mock_client.return_value.models.generate_content.side_effect = Exception("API Error")
        
        result = self.generator.generate_text_to_image(
            prompt="test prompt",
            save_image=False
        )
        
        assert result["success"] is False
        assert "API Error" in result["error"]
    
    def test_prompt_templates_integration(self):
        """Test integration with prompt templates"""
        # Test that the generator has access to prompt templates
        assert hasattr(self.generator, 'prompt_templates')
        assert self.generator.prompt_templates is not None
    
    def test_output_directory_creation(self):
        """Test that output directory is created"""
        assert self.generator.output_dir.exists()
        assert self.generator.output_dir.name == "outputs"


class TestPromptTemplates:
    """Test cases for PromptTemplates class"""
    
    def test_text_to_image_template(self):
        """Test text-to-image template generation"""
        from ai.prompt_templates import PromptTemplates
        
        prompt = PromptTemplates.text_to_image(
            subject="a cat",
            style=ImageStyle.PHOTOREALISTIC,
            context="a pet photo",
            camera_angle=CameraAngle.CLOSE_UP
        )
        
        assert "cat" in prompt
        assert "photorealistic" in prompt
        assert "pet photo" in prompt
        assert "close-up shot" in prompt
    
    def test_inpainting_template(self):
        """Test inpainting template generation"""
        from ai.prompt_templates import PromptTemplates
        
        prompt = PromptTemplates.inpainting(
            base_image_description="a portrait",
            mask_area="the background",
            replacement_content="a forest scene"
        )
        
        assert "portrait" in prompt
        assert "background" in prompt
        assert "forest scene" in prompt
    
    def test_style_transfer_template(self):
        """Test style transfer template generation"""
        from ai.prompt_templates import PromptTemplates
        
        prompt = PromptTemplates.style_transfer(
            source_image_description="a house",
            target_style=ImageStyle.ANIME,
            preserve_subject=True
        )
        
        assert "house" in prompt
        assert "anime" in prompt
        assert "preserving" in prompt
    
    def test_text_rendering_template(self):
        """Test text rendering template generation"""
        from ai.prompt_templates import PromptTemplates
        
        prompt = PromptTemplates.text_rendering(
            text_content="TEST",
            design_style="modern",
            context="a logo"
        )
        
        assert "TEST" in prompt
        assert "modern" in prompt
        assert "logo" in prompt
