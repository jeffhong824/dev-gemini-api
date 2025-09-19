"""
Prompt template loader for loading system prompts from resources directory.
"""

import os
from pathlib import Path
from typing import Dict, Optional


class PromptLoader:
    """Load and manage system prompts from resources directory."""
    
    def __init__(self, resources_dir: Optional[str] = None):
        """
        Initialize the prompt loader.
        
        Args:
            resources_dir: Path to resources directory. If None, uses default path.
        """
        if resources_dir is None:
            # Get the directory containing this file, then look for resources/prompts in the same directory
            current_dir = Path(__file__).parent
            resources_dir = current_dir / "resources" / "prompts"
        else:
            resources_dir = Path(resources_dir)
        
        self.resources_dir = resources_dir
        self._cache: Dict[str, str] = {}
    
    def load_prompt(self, prompt_name: str) -> str:
        """
        Load a prompt template from file.
        
        Args:
            prompt_name: Name of the prompt file (without .txt extension)
        
        Returns:
            Prompt template string
        
        Raises:
            FileNotFoundError: If prompt file doesn't exist
        """
        if prompt_name in self._cache:
            return self._cache[prompt_name]
        
        prompt_file = self.resources_dir / f"{prompt_name}.txt"
        
        if not prompt_file.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
        
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        self._cache[prompt_name] = content
        return content
    
    def format_prompt(self, prompt_name: str, **kwargs) -> str:
        """
        Load and format a prompt template with given parameters.
        
        Args:
            prompt_name: Name of the prompt file
            **kwargs: Parameters to format the template with
        
        Returns:
            Formatted prompt string
        """
        template = self.load_prompt(prompt_name)
        
        # Handle optional parameters by providing defaults
        formatted_kwargs = {}
        for key, value in kwargs.items():
            if value is not None:
                formatted_kwargs[key] = value
            else:
                formatted_kwargs[key] = ""
        
        try:
            return template.format(**formatted_kwargs)
        except KeyError as e:
            raise ValueError(f"Missing required parameter for prompt '{prompt_name}': {e}")
    
    def list_available_prompts(self) -> list:
        """
        List all available prompt files.
        
        Returns:
            List of prompt names (without .txt extension)
        """
        if not self.resources_dir.exists():
            return []
        
        prompt_files = list(self.resources_dir.glob("*.txt"))
        return [f.stem for f in prompt_files]
    
    def reload_cache(self):
        """Reload all cached prompts from files."""
        self._cache.clear()
    
    def get_prompt_info(self, prompt_name: str) -> Dict[str, str]:
        """
        Get information about a prompt template.
        
        Args:
            prompt_name: Name of the prompt file
        
        Returns:
            Dictionary with prompt information
        """
        template = self.load_prompt(prompt_name)
        
        # Extract placeholders from template
        import re
        placeholders = re.findall(r'\{([^}]+)\}', template)
        
        return {
            "name": prompt_name,
            "template": template,
            "placeholders": list(set(placeholders)),
            "file_path": str(self.resources_dir / f"{prompt_name}.txt")
        }
