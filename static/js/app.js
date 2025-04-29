// TanzoGlyph Application JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
    
    // Animate the sample glyph on the homepage
    animateHomeGlyph();
    
    // Add copy-to-clipboard functionality
    setupClipboardButtons();
    
    // Add file input enhancement
    enhanceFileInputs();
});

// Function to animate the glyph on the homepage
function animateHomeGlyph() {
    const sampleGlyph = document.querySelector('.sample-glyph');
    if (!sampleGlyph) return;
    
    // Get the original text
    const originalText = sampleGlyph.textContent;
    const chars = originalText.split('');
    
    // Animation interval
    setInterval(() => {
        // Randomly choose a character to highlight
        const randomIndex = Math.floor(Math.random() * chars.length);
        
        // Create a span with highlighted style
        const highlightedText = chars.map((char, i) => 
            i === randomIndex ? `<span style="color:#fff;text-shadow:0 0 20px #fff,0 0 30px #0f0;">${char}</span>` : char
        ).join('');
        
        // Update the text
        sampleGlyph.innerHTML = highlightedText;
        
        // Reset after a short delay
        setTimeout(() => {
            sampleGlyph.innerHTML = originalText;
        }, 300);
    }, 1000);
}

// Function to set up clipboard copy buttons
function setupClipboardButtons() {
    // This is handled inline in the HTML for simplicity
}

// Function to enhance file inputs with better UI
function enhanceFileInputs() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', (e) => {
            const fileName = e.target.files[0]?.name || 'No file chosen';
            const fileNameElement = document.createElement('span');
            fileNameElement.classList.add('selected-file-name', 'ms-2');
            fileNameElement.textContent = fileName;
            
            // Remove any previous filename display
            const parent = input.parentElement;
            const existingName = parent.querySelector('.selected-file-name');
            if (existingName) {
                parent.removeChild(existingName);
            }
            
            // Add the new filename display
            parent.appendChild(fileNameElement);
        });
    });
}

// Analytics for character usage - helps improve the mapping system
function trackCharacterUsage(glyph) {
    // This would connect to an analytics endpoint in a production environment
    // For this prototype, we're just logging to console
    if (!glyph) return;
    
    const categories = {
        traits: /[A-Za-z]/g,
        archetypes: /[А-Яа-я]/g,
        spiritualArcs: /[Α-Ωα-ω]/g,
        mood: /[ｦ-ﾝ]/g,
        scars: /[⠀-⣿]/g,
        projection: /[▀-▟█-░]/g
    };
    
    const stats = {};
    
    for (const [category, regex] of Object.entries(categories)) {
        const matches = glyph.match(regex) || [];
        stats[category] = {
            count: matches.length,
            characters: matches.join('')
        };
    }
    
    console.log('Glyph Character Statistics:', stats);
}
