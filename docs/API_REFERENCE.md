# API Reference

## ImageGenerator Class

The main class for image generation using the Gemini API.

### Constructor

```python
ImageGenerator(api_key: Optional[str] = None)
```

**Parameters:**
- `api_key` (Optional[str]): Gemini API key. If None, uses `GEMINI_API_KEY` environment variable.

### Methods

#### generate_text_to_image

Generate an image from a text prompt.

```python
generate_text_to_image(
    prompt: str,
    output_filename: Optional[str] = None,
    save_image: bool = True
) -> Dict[str, Any]
```

**Parameters:**
- `prompt` (str): Text description for image generation
- `output_filename` (Optional[str]): Output filename without extension
- `save_image` (bool): Whether to save the image to disk

**Returns:**
- `Dict[str, Any]`: Result dictionary with success status, image data, and metadata

**Example:**
```python
generator = ImageGenerator()
result = generator.generate_text_to_image(
    prompt="A beautiful sunset over mountains",
    output_filename="sunset",
    save_image=True
)
```

#### generate_image_editing

Edit an existing image with a text prompt.

```python
generate_image_editing(
    prompt: str,
    input_image: Union[str, Path, Image.Image],
    output_filename: Optional[str] = None,
    save_image: bool = True
) -> Dict[str, Any]
```

**Parameters:**
- `prompt` (str): Text description for image editing
- `input_image` (Union[str, Path, Image.Image]): Input image (path, PIL Image, or base64 string)
- `output_filename` (Optional[str]): Output filename without extension
- `save_image` (bool): Whether to save the image to disk

**Returns:**
- `Dict[str, Any]`: Result dictionary with success status, image data, and metadata

**Example:**
```python
result = generator.generate_image_editing(
    prompt="Add a cat sleeping on the sofa",
    input_image="path/to/image.png",
    output_filename="edited_image"
)
```

#### generate_with_template

Generate an image using predefined professional templates.

```python
generate_with_template(
    template_type: str,
    **kwargs
) -> Dict[str, Any]
```

**Parameters:**
- `template_type` (str): Type of template to use
- `**kwargs`: Template-specific parameters

**Template Types:**
- `text_to_image`: Basic text-to-image generation
- `inpainting`: Semantic masking and element replacement
- `style_transfer`: Apply artistic styles
- `multi_image_composition`: Combine multiple images
- `text_rendering`: High-fidelity text generation

**Example:**
```python
result = generator.generate_with_template(
    template_type="text_to_image",
    subject="a futuristic city",
    style=ImageStyle.PHOTOREALISTIC,
    context="concept art for a sci-fi movie"
)
```

#### batch_generate

Generate multiple images in batch.

```python
batch_generate(
    prompts: List[str],
    output_prefix: str = "batch"
) -> List[Dict[str, Any]]
```

**Parameters:**
- `prompts` (List[str]): List of text prompts
- `output_prefix` (str): Prefix for output filenames

**Returns:**
- `List[Dict[str, Any]]`: List of generation results

**Example:**
```python
prompts = ["A mountain", "A city", "A garden"]
results = generator.batch_generate(prompts, "scenes")
```

## PromptTemplates Class

Professional prompt templates following Gemini API best practices.

### Methods

#### text_to_image

Generate a professional text-to-image prompt.

```python
text_to_image(
    subject: str,
    style: ImageStyle = ImageStyle.PHOTOREALISTIC,
    context: Optional[str] = None,
    camera_angle: Optional[CameraAngle] = None,
    lighting: Optional[str] = None,
    composition: Optional[str] = None,
    negative_prompt: Optional[str] = None
) -> str
```

**Parameters:**
- `subject` (str): Main subject of the image
- `style` (ImageStyle): Visual style of the image
- `context` (Optional[str]): Purpose and context of the image
- `camera_angle` (Optional[CameraAngle]): Camera composition angle
- `lighting` (Optional[str]): Lighting description
- `composition` (Optional[str]): Compositional elements
- `negative_prompt` (Optional[str]): What to avoid (use positive descriptions)

**Example:**
```python
prompt = PromptTemplates.text_to_image(
    subject="a futuristic city",
    style=ImageStyle.PHOTOREALISTIC,
    context="concept art for a sci-fi movie",
    camera_angle=CameraAngle.WIDE_ANGLE,
    lighting="dramatic neon lighting"
)
```

#### inpainting

Generate inpainting prompt for semantic masking.

```python
inpainting(
    base_image_description: str,
    mask_area: str,
    replacement_content: str,
    style_consistency: bool = True
) -> str
```

**Parameters:**
- `base_image_description` (str): Description of the base image
- `mask_area` (str): Area to be modified
- `replacement_content` (str): What to replace it with
- `style_consistency` (bool): Whether to maintain style consistency

**Example:**
```python
prompt = PromptTemplates.inpainting(
    base_image_description="a professional portrait",
    mask_area="the plain white background",
    replacement_content="a modern office environment"
)
```

#### style_transfer

Generate style transfer prompt.

```python
style_transfer(
    source_image_description: str,
    target_style: ImageStyle,
    preserve_subject: bool = True
) -> str
```

**Parameters:**
- `source_image_description` (str): Description of source image
- `target_style` (ImageStyle): Target style to apply
- `preserve_subject` (bool): Whether to preserve the main subject

**Example:**
```python
prompt = PromptTemplates.style_transfer(
    source_image_description="a simple house",
    target_style=ImageStyle.ANIME,
    preserve_subject=True
)
```

#### multi_image_composition

Generate multi-image composition prompt.

```python
multi_image_composition(
    images: List[str],
    composition_goal: str,
    blending_style: str = "seamless"
) -> str
```

**Parameters:**
- `images` (List[str]): List of image descriptions
- `composition_goal` (str): Goal of the composition
- `blending_style` (str): How to blend the images

**Example:**
```python
prompt = PromptTemplates.multi_image_composition(
    images=["a forest background", "a wizard character", "magical effects"],
    composition_goal="a complete fantasy scene",
    blending_style="seamless and atmospheric"
)
```

#### text_rendering

Generate high-fidelity text rendering prompt.

```python
text_rendering(
    text_content: str,
    design_style: str,
    context: str
) -> str
```

**Parameters:**
- `text_content` (str): Text to render
- `design_style` (str): Design style for the text
- `context` (str): Context for the text (logo, poster, etc.)

**Example:**
```python
prompt = PromptTemplates.text_rendering(
    text_content="TECHNOVA",
    design_style="modern minimalist with geometric elements",
    context="a professional tech company logo"
)
```

## Enums

### ImageStyle

Visual styles for image generation.

```python
class ImageStyle(Enum):
    PHOTOREALISTIC = "photorealistic"
    ARTISTIC = "artistic"
    CARTOON = "cartoon"
    ANIME = "anime"
    SKETCH = "sketch"
    PAINTING = "painting"
    MINIMALIST = "minimalist"
```

### CameraAngle

Camera angles for composition control.

```python
class CameraAngle(Enum):
    WIDE_ANGLE = "wide-angle shot"
    MACRO = "macro shot"
    LOW_ANGLE = "low-angle perspective"
    HIGH_ANGLE = "high-angle perspective"
    CLOSE_UP = "close-up shot"
    BIRD_EYE = "bird's eye view"
    DUTCH_ANGLE = "dutch angle"
```

## Error Handling

All methods return a dictionary with the following structure:

```python
{
    "success": bool,           # Whether the operation succeeded
    "text_content": str,       # Generated text (if any)
    "image_data": bytes,       # Raw image data (if any)
    "image_path": str,         # Path to saved image (if saved)
    "error": str,              # Error message (if failed)
    "metadata": {              # Additional metadata
        "model": str,
        "prompt": str,
        "type": str
    }
}
```

## Best Practices

1. **Always check the success flag** before accessing image data
2. **Use professional templates** for better results
3. **Provide specific, detailed prompts** with context
4. **Handle errors gracefully** and provide user feedback
5. **Use appropriate image styles** for your use case
6. **Consider batch processing** for multiple images
