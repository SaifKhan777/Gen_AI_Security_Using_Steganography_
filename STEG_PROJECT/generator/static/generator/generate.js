// generator/static/generator/js/generate.js
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('generateForm');
    const generatedImageContainer = document.querySelector('.image-container');
    const generateButton = form.querySelector('button');
    const loadingMessage = document.createElement('p');
    loadingMessage.textContent = 'Generating image... Please wait.';
    loadingMessage.classList.add('loading');

    form.addEventListener('submit', function (e) {
        e.preventDefault(); // Prevents the default form submission behavior

        // Show the loading message
        generatedImageContainer.appendChild(loadingMessage);

        // Disable the button to prevent multiple submissions
        generateButton.disabled = true;

        // Use Fetch API to make the POST request to the backend
        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ prompt: "" })  // Send an empty prompt since we're selecting a random image
        })
        .then(response => response.json())
        .then(data => {
            if (data.image_url) {
                // Update the image source with the new generated image URL
                const image = document.createElement('img');
                image.src = data.image_url;
                image.alt = 'Generated Image';
                generatedImageContainer.innerHTML = ''; // Clear loading message
                generatedImageContainer.appendChild(image);
            } else {
                generatedImageContainer.innerHTML = '<p>Error generating image.</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            generatedImageContainer.innerHTML = '<p>Error generating image.</p>';
        })
        .finally(() => {
            // Enable the button again after the process is finished
            generateButton.disabled = false;
        });
    });
});
