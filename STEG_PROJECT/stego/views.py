from django.shortcuts import render
from django.http import JsonResponse
from .stego_utils.image_encoder import encode_image_stego
from .stego_utils.image_decoder import decode_image_stego  # Assuming you have this function

def encode_image_view(request):
    if request.method == 'POST':
        image_file = request.FILES['image']
        secret_text = request.POST['secret_text']
        
        # Call the steganography encoding function
        encoded_image_path = encode_image_stego(image_file, secret_text)
        
        # Respond with the encoded image path or URL
        return JsonResponse({'encoded_image_url': encoded_image_path})

def decode_image_view(request):
    if request.method == 'POST':
        image_file = request.FILES['image']
        
        # Call the steganography decoding function
        decoded_text = decode_image_stego(image_file)
        
        return JsonResponse({'decoded_text': decoded_text})
