// Loader animation
window.addEventListener('load', () => {
    const loader = document.querySelector('.loader');
    loader.style.opacity = '0';
    setTimeout(() => {
        loader.style.display = 'none';
        document.querySelector('header').style.display = 'block';
        document.querySelector('main').style.display = 'block';
    }, 500);
});

// Handle form submission for plant image upload
document.getElementById('scan-form').onsubmit = async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById('plant-image');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/api/identify-plant', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        // Redirect to result page with plant info
        window.location.href = `result.html?name=${encodeURIComponent(result.name)}&info=${encodeURIComponent(result.info)}&medicinalUse=${encodeURIComponent(result.medicinalUse)}`;
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while processing your request. Please try again.');
    }
};

// Image preview functionality
document.getElementById('plant-image').onchange = function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.className = 'preview-image';
            const previewContainer = document.getElementById('image-preview');
            previewContainer.innerHTML = '';
            previewContainer.appendChild(img);
        }
        reader.readAsDataURL(file);
    }
};

// Handle displaying plant info on result page
if (window.location.pathname.includes('result.html')) {
    document.addEventListener('DOMContentLoaded', () => {
        const urlParams = new URLSearchParams(window.location.search);
        const name = urlParams.get('name');
        const info = urlParams.get('info');
        const medicinalUse = urlParams.get('medicinalUse');

        const plantInfoDiv = document.getElementById('plant-info');
        
        if (name && info && medicinalUse) {
            plantInfoDiv.innerHTML = `
                <h2>${name}</h2>
                <p><strong>Info:</strong> ${info}</p>
                <p><strong>Medicinal Use:</strong> ${medicinalUse}</p>
            `;
        } else {
            plantInfoDiv.innerHTML = '<p>No plant information available.</p>';
        }
    });
}