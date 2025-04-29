// Function to handle image upload
function handleImageUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    // Clear any previous error messages
    document.getElementById('errorMessage').innerText = '';

    // Create an image object to load the selected file
    const reader = new FileReader();
    reader.onload = function (e) {
        const img = new Image();
        img.src = e.target.result;
        img.onload = function () {
            // Call the function to decode the message from the image
            decodeImageMessage(img);
        };
    };
    reader.readAsDataURL(file);
}

// Function to decode the message from the uploaded image
function decodeImageMessage(img) {
    // Convert the image to a canvas to read pixel data
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = img.width;
    canvas.height = img.height;
    ctx.drawImage(img, 0, 0);

    const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imgData.data;

    let binaryMessage = '';
    
    // Extract the least significant bit of each color channel
    for (let i = 0; i < data.length; i += 4) {
        for (let j = 0; j < 3; j++) {
            binaryMessage += (data[i + j] & 1);  // Extract LSB
        }
    }

    // Convert binary message back to text
    const message = binaryToText(binaryMessage);

    // Check if a message is found
    if (message) {
        document.getElementById('decodedMessage').value = message;
    } else {
        document.getElementById('errorMessage').innerText = 'No hidden message found in this image!';
    }
}

// Function to convert binary to text (ASCII)
function binaryToText(binary) {
    let message = '';
    for (let i = 0; i < binary.length; i += 8) {
        const byte = binary.slice(i, i + 8);
        message += String.fromCharCode(parseInt(byte, 2));
    }

    // Find the delimiter (*^*^*) and truncate the message
    const delimiter = '*^*^*';
    const endIdx = message.indexOf(delimiter);
    if (endIdx !== -1) {
        message = message.substring(0, endIdx);
    }

    return message;
}
