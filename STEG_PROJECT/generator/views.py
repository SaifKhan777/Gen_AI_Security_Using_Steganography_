# stego/views.py or wherever your view is located
import os
import random
from django.shortcuts import render
from django.utils import timezone
from django.conf import settings
from stego.stego_utils.image_encoder import encode_image_stego


def generate_and_stego_image(request):
    if request.method == "POST":
        images_dir = os.path.join(settings.MEDIA_ROOT, 'random_images')
        image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if image_files:
            image_name = random.choice(image_files)
            image_path = os.path.join(images_dir, image_name)

            metadata = {
                "date": timezone.now().strftime("%Y-%m-%d"),
                "time": timezone.now().strftime("%H:%M:%S"),
                "model": "ChatGPT-ImageGen"
            }
            message = f"{metadata['date']}|{metadata['time']}|{metadata['model']}"

            output_dir = os.path.join(settings.MEDIA_ROOT, "generated_images")
            os.makedirs(output_dir, exist_ok=True)

            generated_name = f"stego_{timezone.now().strftime('%Y%m%d%H%M%S')}_{image_name}"
            generated_path = os.path.join(output_dir, generated_name)

            encode_image_stego(
                image_path=image_path,
                message=message,
                output_path=generated_path
            )

            image_url = os.path.join(settings.MEDIA_URL, "generated_images", generated_name)
            return render(request, "generator/generate.html", {"image_url": image_url})

    return render(request, "generator/generate.html")
