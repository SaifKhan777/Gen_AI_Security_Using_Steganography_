from PIL import Image
import numpy as np

def decode_image_stego(image_path):
    image = Image.open(image_path).convert("RGB")
    image_data = np.array(image)
    flat_image = image_data.flatten()

    binary_data = ''.join([str(pixel & 1) for pixel in flat_image])

    chars = []
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if len(byte) < 8:
            break
        char = chr(int(byte, 2))
        chars.append(char)
        
        # Check for the end of the embedded message (####)
        if ''.join(chars[-4:]) == "####":
            return ''.join(chars).replace("####", "")

    # If no valid steganographic data found, return "NOT AI GENERATED"
    return "Original Content"

