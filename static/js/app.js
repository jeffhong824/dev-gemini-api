// Main application JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initTabs();
    initForms();
    initTemplateFields();
});

// Tab functionality
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            button.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
}

// Form functionality
function initForms() {
    // Generate form
    const generateForm = document.getElementById('generateForm');
    if (generateForm) {
        generateForm.addEventListener('submit', handleGenerateSubmit);
        
        // Handle style change for custom style field
        const styleSelect = document.getElementById('generateStyle');
        const customStyleGroup = document.getElementById('customStyleGroup');
        styleSelect.addEventListener('change', () => {
            customStyleGroup.style.display = styleSelect.value === 'custom' ? 'block' : 'none';
        });
    }

    // Edit form
    const editForm = document.getElementById('editForm');
    if (editForm) {
        editForm.addEventListener('submit', handleEditSubmit);
        
        // Handle style change for custom style field
        const styleSelect = document.getElementById('editStyle');
        const customStyleGroup = document.getElementById('editCustomStyleGroup');
        styleSelect.addEventListener('change', () => {
            customStyleGroup.style.display = styleSelect.value === 'custom' ? 'block' : 'none';
        });
    }

    // Clean form
    const cleanForm = document.getElementById('cleanForm');
    if (cleanForm) {
        cleanForm.addEventListener('submit', handleCleanSubmit);
    }

    // Style form
    const styleForm = document.getElementById('styleForm');
    if (styleForm) {
        styleForm.addEventListener('submit', handleStyleSubmit);
        
        // Handle style change for custom style field
        const styleSelect = document.getElementById('targetStyle');
        const customStyleGroup = document.getElementById('styleCustomGroup');
        styleSelect.addEventListener('change', () => {
            customStyleGroup.style.display = styleSelect.value === 'custom' ? 'block' : 'none';
        });
    }

    // Composition form
    const compositionForm = document.getElementById('compositionForm');
    if (compositionForm) {
        compositionForm.addEventListener('submit', handleCompositionSubmit);
    }

    // Templates form
    const templatesForm = document.getElementById('templatesForm');
    if (templatesForm) {
        templatesForm.addEventListener('submit', handleTemplatesSubmit);
        
        // Handle template type change
        const templateTypeSelect = document.getElementById('templateType');
        templateTypeSelect.addEventListener('change', updateTemplateFields);
    }
}

// Template fields functionality
function initTemplateFields() {
    updateTemplateFields();
}

function updateTemplateFields() {
    const templateType = document.getElementById('templateType').value;
    const fieldsContainer = document.getElementById('templateFields');
    
    let fieldsHTML = '';
    
    switch (templateType) {
        case 'text':
            fieldsHTML = `
                <div class="template-field">
                    <label for="templateSubject">Subject *</label>
                    <input type="text" id="templateSubject" name="subject" placeholder="e.g., modern sofa" required>
                </div>
                <div class="template-field">
                    <label for="templateStyle">Style</label>
                    <select id="templateStyle" name="style">
                        <option value="photorealistic">Photorealistic</option>
                        <option value="artistic">Artistic</option>
                        <option value="cartoon">Cartoon</option>
                        <option value="oil_painting">Oil Painting</option>
                        <option value="watercolor">Watercolor</option>
                        <option value="sketch">Sketch</option>
                    </select>
                </div>
                <div class="template-field">
                    <label for="templateContext">Context</label>
                    <input type="text" id="templateContext" name="context" placeholder="e.g., product photography">
                </div>
                <div class="template-field">
                    <label for="templateAngle">Camera Angle</label>
                    <select id="templateAngle" name="angle">
                        <option value="">Select angle</option>
                        <option value="wide_angle">Wide Angle</option>
                        <option value="close_up">Close Up</option>
                        <option value="low_angle">Low Angle</option>
                        <option value="high_angle">High Angle</option>
                        <option value="bird_eye">Bird's Eye</option>
                    </select>
                </div>
                <div class="template-field">
                    <label for="templateLighting">Lighting</label>
                    <input type="text" id="templateLighting" name="lighting" placeholder="e.g., soft natural lighting">
                </div>
                <div class="template-field">
                    <label for="templateComposition">Composition</label>
                    <input type="text" id="templateComposition" name="composition" placeholder="e.g., rule of thirds">
                </div>
            `;
            break;
            
        case 'inpainting':
            fieldsHTML = `
                <div class="template-field">
                    <label for="templateBase">Base Image Description *</label>
                    <input type="text" id="templateBase" name="base" placeholder="e.g., living room with sofa" required>
                </div>
                <div class="template-field">
                    <label for="templateMask">Mask Area *</label>
                    <input type="text" id="templateMask" name="mask" placeholder="e.g., coffee table area" required>
                </div>
                <div class="template-field">
                    <label for="templateReplace">Replacement Content *</label>
                    <input type="text" id="templateReplace" name="replace" placeholder="e.g., modern glass table" required>
                </div>
            `;
            break;
            
        case 'style':
            fieldsHTML = `
                <div class="template-field">
                    <label for="templateSource">Source Image Description *</label>
                    <input type="text" id="templateSource" name="source" placeholder="e.g., modern living room" required>
                </div>
                <div class="template-field">
                    <label for="templateTarget">Target Style *</label>
                    <input type="text" id="templateTarget" name="target" placeholder="e.g., vintage oil painting style" required>
                </div>
            `;
            break;
            
        case 'composition':
            fieldsHTML = `
                <div class="template-field">
                    <label for="templateGoal">Composition Goal *</label>
                    <textarea id="templateGoal" name="goal" placeholder="e.g., modern living room with person" required></textarea>
                </div>
                <div class="template-field">
                    <label for="templateBlending">Blending Style</label>
                    <select id="templateBlending" name="blending">
                        <option value="seamless">Seamless</option>
                        <option value="artistic">Artistic</option>
                        <option value="collage">Collage</option>
                        <option value="overlay">Overlay</option>
                    </select>
                </div>
            `;
            break;
            
        case 'text_rendering':
            fieldsHTML = `
                <div class="template-field">
                    <label for="templateTextContent">Text Content *</label>
                    <input type="text" id="templateTextContent" name="text_content" placeholder="e.g., Welcome Home" required>
                </div>
                <div class="template-field">
                    <label for="templateDesignStyle">Design Style</label>
                    <input type="text" id="templateDesignStyle" name="design_style" placeholder="e.g., modern minimalist">
                </div>
            `;
            break;
            
        case 'clean_room':
            fieldsHTML = `
                <div class="template-field">
                    <label for="templateObjects">Objects to Remove</label>
                    <input type="text" id="templateObjects" name="objects" placeholder="e.g., books, magazines (leave empty for all clutter)">
                </div>
                <div class="template-field">
                    <label class="checkbox-label">
                        <input type="checkbox" id="templateMaintainLayout" name="maintain_layout" checked>
                        <span class="checkmark"></span>
                        Maintain original room layout
                    </label>
                </div>
            `;
            break;
            
        case 'step_by_step':
            fieldsHTML = `
                <div class="template-field">
                    <label>Steps *</label>
                    <div id="stepsContainer">
                        <div class="step-input">
                            <input type="text" name="steps" placeholder="Step 1" required>
                            <button type="button" class="remove-step" onclick="removeStep(this)" style="display: none;">Remove</button>
                        </div>
                        <div class="step-input">
                            <input type="text" name="steps" placeholder="Step 2" required>
                            <button type="button" class="remove-step" onclick="removeStep(this)">Remove</button>
                        </div>
                    </div>
                    <button type="button" class="add-step" onclick="addStep()">Add Step</button>
                </div>
            `;
            break;
    }
    
    fieldsContainer.innerHTML = fieldsHTML;
}

// Step management for step-by-step template
function addStep() {
    const container = document.getElementById('stepsContainer');
    const stepCount = container.children.length + 1;
    
    const stepDiv = document.createElement('div');
    stepDiv.className = 'step-input';
    stepDiv.innerHTML = `
        <input type="text" name="steps" placeholder="Step ${stepCount}" required>
        <button type="button" class="remove-step" onclick="removeStep(this)">Remove</button>
    `;
    
    container.appendChild(stepDiv);
    updateStepButtons();
}

function removeStep(button) {
    const container = document.getElementById('stepsContainer');
    if (container.children.length > 1) {
        button.parentElement.remove();
        updateStepButtons();
    }
}

function updateStepButtons() {
    const container = document.getElementById('stepsContainer');
    const removeButtons = container.querySelectorAll('.remove-step');
    removeButtons.forEach((button, index) => {
        button.style.display = container.children.length > 1 ? 'block' : 'none';
    });
}

// Form submission handlers
async function handleGenerateSubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    showLoading('generateResult');
    
    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        showResult('generateResult', result);
    } catch (error) {
        showError('generateResult', error.message);
    }
}

async function handleEditSubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    // Store original image path for comparison
    const fileInput = document.getElementById('editImage');
    if (fileInput.files[0]) {
        // Create a temporary URL for the original image
        window.originalImagePath = URL.createObjectURL(fileInput.files[0]);
    }
    
    showLoading('editResult');
    
    try {
        const response = await fetch('/api/edit', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        showResult('editResult', result);
    } catch (error) {
        showError('editResult', error.message);
    }
}

async function handleCleanSubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    // Store original image path for comparison
    const fileInput = document.getElementById('cleanImage');
    if (fileInput.files[0]) {
        // Create a temporary URL for the original image
        window.originalImagePath = URL.createObjectURL(fileInput.files[0]);
    }
    
    showLoading('cleanResult');
    
    try {
        const response = await fetch('/api/clean', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        showResult('cleanResult', result);
    } catch (error) {
        showError('cleanResult', error.message);
    }
}

async function handleStyleSubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    // Store original image path for comparison
    const fileInput = document.getElementById('styleImage');
    if (fileInput.files[0]) {
        // Create a temporary URL for the original image
        window.originalImagePath = URL.createObjectURL(fileInput.files[0]);
    }
    
    showLoading('styleResult');
    
    try {
        const response = await fetch('/api/style', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        showResult('styleResult', result);
    } catch (error) {
        showError('styleResult', error.message);
    }
}

async function handleCompositionSubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    // Store original images for comparison
    const fileInput = document.getElementById('compositionImages');
    if (fileInput.files.length > 0) {
        // Create temporary URLs for the original images
        window.originalImages = [];
        for (let i = 0; i < fileInput.files.length; i++) {
            window.originalImages.push(URL.createObjectURL(fileInput.files[i]));
        }
    }
    
    showLoading('compositionResult');
    
    try {
        const response = await fetch('/api/composition', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        showResult('compositionResult', result);
    } catch (error) {
        showError('compositionResult', error.message);
    }
}

async function handleTemplatesSubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    // Handle steps array for step-by-step template
    if (data.template_type === 'step_by_step') {
        const steps = Array.from(formData.getAll('steps')).filter(step => step.trim());
        data.steps = steps;
    }
    
    showLoading('templatesResult');
    
    try {
        const response = await fetch('/api/templates', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        showTemplateResult('templatesResult', result);
    } catch (error) {
        showError('templatesResult', error.message);
    }
}

// Utility functions
function showLoading(resultId) {
    const resultDiv = document.getElementById(resultId);
    resultDiv.innerHTML = '<div class="loading"></div> Processing...';
    resultDiv.className = 'result';
    resultDiv.style.display = 'block';
}

function showResult(resultId, result) {
    const resultDiv = document.getElementById(resultId);
    
    if (result.success) {
        let html = `<div class="result success">
            <h3><i class="fas fa-check-circle"></i> ${result.message}</h3>`;
        
        if (result.data) {
            if (result.data.image_path) {
                // Handle both direct path and nested path
                let imagePath = result.data.image_path;
                if (imagePath.startsWith('outputs/')) {
                    imagePath = imagePath.substring(8); // Remove 'outputs/' prefix
                }
                
        // Check if this is an edit, clean, or style operation (has original image)
        const isEditOrClean = resultId.includes('edit') || resultId.includes('clean') || resultId.includes('style');
        const isComposition = resultId.includes('composition');
                
                if (isEditOrClean && window.originalImagePath) {
                    // Show comparison view for edit/clean/style operations
                    html += createImageComparisonView(window.originalImagePath, imagePath);
                } else if (isComposition && window.originalImages && window.originalImages.length > 0) {
                    // Show composition view for composition operations
                    html += createCompositionView(window.originalImages, imagePath);
                } else {
                    // Show single image for generate operations
                    html += `<img src="/outputs/${imagePath}" alt="Generated image" class="result-image">`;
                }
                
                html += `<a href="/outputs/${imagePath}" class="download-link" download>
                    <i class="fas fa-download"></i> Download Image
                </a>`;
            }
            
            if (result.data.prompt) {
                html += `<h4>Generated Prompt:</h4>
                <pre>${result.data.prompt}</pre>`;
            }
            
            if (result.data.metadata) {
                html += `<h4>Metadata:</h4>
                <pre>${JSON.stringify(result.data.metadata, null, 2)}</pre>`;
            }
        }
        
        html += '</div>';
        resultDiv.innerHTML = html;
        
        // Initialize image comparison slider if it exists
        initializeImageComparison();
    } else {
        showError(resultId, result.error || 'Unknown error occurred');
    }
}

function createImageComparisonView(originalPath, newPath) {
    // Handle both temporary URLs and server paths
    const originalSrc = originalPath.startsWith('blob:') ? originalPath : `/outputs/${originalPath}`;
    const newSrc = newPath.startsWith('outputs/') ? `/outputs/${newPath}` : `/outputs/${newPath}`;

    return `
        <div class="image-comparison-container">
            <h4>Image Comparison</h4>

            <!-- Side by side comparison -->
            <div class="side-by-side-comparison">
                <div class="image-container">
                    <h5>Original</h5>
                    <img src="${originalSrc}" alt="Original image" class="comparison-image">
                </div>
                <div class="image-container">
                    <h5>Result</h5>
                    <img src="${newSrc}" alt="Result image" class="comparison-image">
                </div>
            </div>

            <!-- Interactive slider comparison -->
            <div class="slider-comparison">
                <h5>Interactive Comparison (Drag to compare)</h5>
                <div class="slider-container">
                    <div class="slider-image-container">
                        <img src="${originalSrc}" alt="Original" class="slider-original">
                        <img src="${newSrc}" alt="Result" class="slider-result">
                        <div class="slider-handle">
                            <div class="slider-line"></div>
                            <div class="slider-button">
                                <i class="fas fa-grip-vertical"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function createCompositionView(originalImages, resultPath) {
    // Handle server path
    const resultSrc = resultPath.startsWith('outputs/') ? `/outputs/${resultPath}` : `/outputs/${resultPath}`;
    
    // Create HTML for original images
    let originalImagesHtml = '';
    originalImages.forEach((imgSrc, index) => {
        originalImagesHtml += `
            <div class="image-container">
                <h5>Input ${index + 1}</h5>
                <img src="${imgSrc}" alt="Input image ${index + 1}" class="comparison-image">
            </div>
        `;
    });

    return `
        <div class="image-comparison-container">
            <h4>Composition Result</h4>

            <!-- Input images -->
            <div class="input-images-section">
                <h5>Input Images</h5>
                <div class="side-by-side-comparison">
                    ${originalImagesHtml}
                </div>
            </div>

            <!-- Result image -->
            <div class="result-section">
                <h5>Composed Result</h5>
                <div class="image-container">
                    <img src="${resultSrc}" alt="Composed image" class="result-image">
                </div>
            </div>
        </div>
    `;
}

function initializeImageComparison() {
    const sliderContainer = document.querySelector('.slider-image-container');
    if (!sliderContainer) {
        console.log('No slider container found');
        return;
    }
    
    const handle = sliderContainer.querySelector('.slider-handle');
    const originalImg = sliderContainer.querySelector('.slider-original');
    const resultImg = sliderContainer.querySelector('.slider-result');
    
    if (!handle || !originalImg || !resultImg) {
        console.log('Missing slider elements:', { handle: !!handle, originalImg: !!originalImg, resultImg: !!resultImg });
        return;
    }
    
    console.log('Initializing image comparison slider');
    
    let isDragging = false;
    
    // Ensure both images have the same dimensions
    function syncImageDimensions() {
        function updateDimensions() {
            if (!originalImg.naturalWidth || !resultImg.naturalWidth) return;
            
            // Use the smaller image's dimensions as reference for consistency
            const originalAspect = originalImg.naturalWidth / originalImg.naturalHeight;
            const resultAspect = resultImg.naturalWidth / resultImg.naturalHeight;
            
            // Use the average aspect ratio for consistency
            const avgAspect = (originalAspect + resultAspect) / 2;
            
            const containerHeight = sliderContainer.offsetHeight;
            const containerWidth = sliderContainer.offsetWidth;
            
            // Calculate the best fit dimensions
            let imgWidth, imgHeight;
            if (containerWidth / containerHeight > avgAspect) {
                imgHeight = containerHeight;
                imgWidth = containerHeight * avgAspect;
            } else {
                imgWidth = containerWidth;
                imgHeight = containerWidth / avgAspect;
            }
            
            // Apply the same dimensions to both images
            originalImg.style.width = imgWidth + 'px';
            originalImg.style.height = imgHeight + 'px';
            resultImg.style.width = imgWidth + 'px';
            resultImg.style.height = imgHeight + 'px';
            
            // Center the images
            originalImg.style.left = (containerWidth - imgWidth) / 2 + 'px';
            originalImg.style.top = (containerHeight - imgHeight) / 2 + 'px';
            resultImg.style.left = (containerWidth - imgWidth) / 2 + 'px';
            resultImg.style.top = (containerHeight - imgHeight) / 2 + 'px';
        }
        
        // Update dimensions when both images are loaded
        let loadedCount = 0;
        function onImageLoad() {
            loadedCount++;
            if (loadedCount === 2) {
                updateDimensions();
            }
        }
        
        originalImg.onload = onImageLoad;
        resultImg.onload = onImageLoad;
        
        // If images are already loaded
        if (originalImg.complete && resultImg.complete) {
            updateDimensions();
        }
        
        // Force update after a short delay to ensure images are rendered
        setTimeout(() => {
            if (originalImg.naturalWidth > 0 && resultImg.naturalWidth > 0) {
                updateDimensions();
            }
        }, 100);
        
        // Additional fallback for slow-loading images
        setTimeout(() => {
            if (originalImg.naturalWidth > 0 && resultImg.naturalWidth > 0) {
                updateDimensions();
            }
        }, 500);
    }
    
    // Sync dimensions when images load
    syncImageDimensions();
    
    // Set initial position
    updateSliderPosition(50);
    
    // Mouse events for dragging
    handle.addEventListener('mousedown', startDrag);
    document.addEventListener('mousemove', drag);
    document.addEventListener('mouseup', stopDrag);
    
    // Mouse events for hover effect
    sliderContainer.addEventListener('mousemove', handleHover);
    sliderContainer.addEventListener('mouseleave', handleLeave);
    
    // Touch events for mobile
    handle.addEventListener('touchstart', startDrag);
    document.addEventListener('touchmove', drag);
    document.addEventListener('touchend', stopDrag);
    
    function startDrag(e) {
        isDragging = true;
        e.preventDefault();
        sliderContainer.style.cursor = 'grabbing';
    }
    
    function drag(e) {
        if (!isDragging) return;
        
        const rect = sliderContainer.getBoundingClientRect();
        const x = (e.clientX || e.touches[0].clientX) - rect.left;
        const percentage = Math.max(0, Math.min(100, (x / rect.width) * 100));
        
        updateSliderPosition(percentage);
    }
    
    function stopDrag() {
        isDragging = false;
        sliderContainer.style.cursor = 'grab';
    }
    
    function handleHover(e) {
        if (isDragging) return;
        
        const rect = sliderContainer.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const percentage = Math.max(0, Math.min(100, (x / rect.width) * 100));
        
        updateSliderPosition(percentage);
    }
    
    function handleLeave() {
        if (isDragging) return;
        // Reset to center when mouse leaves
        updateSliderPosition(50);
    }
    
    function updateSliderPosition(percentage) {
        handle.style.left = percentage + '%';
        originalImg.style.clipPath = `inset(0 ${100 - percentage}% 0 0)`;
        resultImg.style.clipPath = `inset(0 0 0 ${percentage}%)`;
    }
}

function showTemplateResult(resultId, result) {
    const resultDiv = document.getElementById(resultId);
    
    if (result.success) {
        let html = `<div class="result success">
            <h3><i class="fas fa-check-circle"></i> ${result.message}</h3>`;
        
        if (result.data && result.data.template) {
            html += `<h4>Generated Template:</h4>
            <pre>${result.data.template}</pre>`;
        }
        
        html += '</div>';
        resultDiv.innerHTML = html;
    } else {
        showError(resultId, result.error || 'Unknown error occurred');
    }
}

function showError(resultId, message) {
    const resultDiv = document.getElementById(resultId);
    resultDiv.innerHTML = `<div class="result error">
        <h3><i class="fas fa-exclamation-circle"></i> Error</h3>
        <p>${message}</p>
    </div>`;
    resultDiv.className = 'result error';
    resultDiv.style.display = 'block';
}
