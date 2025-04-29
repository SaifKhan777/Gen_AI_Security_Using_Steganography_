from PIL import Image
import numpy as np

def encode_image_stego(image_path, message, output_path):
    delimiter = "####"
    full_message = message + delimiter
    binary_message = ''.join(format(ord(char), '08b') for char in full_message)

    image = Image.open(image_path).convert("RGB")
    image_data = np.array(image)

    flat_image = image_data.flatten()

    if len(binary_message) > len(flat_image):
        raise ValueError("Message too long to encode in image.")

    # Safe bit embedding in LSB
    for i, bit in enumerate(binary_message):
        current_pixel = int(flat_image[i])  # Cast to int before bitwise operations
        new_pixel = (current_pixel & ~1) | int(bit)  # Set LSB to bit
        flat_image[i] = np.uint8(new_pixel)  # Cast back to uint8 safely

    encoded_image_data = flat_image.reshape(image_data.shape)
    encoded_image = Image.fromarray(encoded_image_data.astype('uint8'), 'RGB')
    encoded_image.save(output_path)
    return output_path
