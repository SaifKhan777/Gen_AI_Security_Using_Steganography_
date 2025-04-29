import os
import json
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from PIL import Image
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from stego.stego_utils.image_decoder import decode_image_stego

# === Load AI detection model and processor once ===
model_name = "Smogy/SMOGY-Ai-images-detector"
processor = AutoImageProcessor.from_pretrained(model_name)
model = AutoModelForImageClassification.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

# === Utility function for AI detection ===
def detect_ai_generated(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            pred_class = torch.argmax(logits, dim=-1).item()
            label = model.config.id2label[pred_class]
            confidence = torch.softmax(logits, dim=-1)[0][pred_class].item()

        if confidence >= 0.5:
            return "AI GENERATED"
        else:
            return "NOT AI GENERATED"
    except Exception as e:
        return f"Detection Error: {str(e)}"

# === Image Upload View ===
def decode_uploaded_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        path = os.path.join(upload_dir, image.name)
        with open(path, 'wb+') as dest:
            for chunk in image.chunks():
                dest.write(chunk)

    image_folder = os.path.join(settings.MEDIA_ROOT, 'uploads')
    images = [
        {'url': os.path.join(settings.MEDIA_URL, 'uploads', f).replace('\\', '/')}
        for f in os.listdir(image_folder)
        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]
    return render(request, 'social/index.html', {'images': images})

# === AJAX Decode and AI Detection View ===


@csrf_exempt
def ajax_decode_image(request):
    if request.method == "POST":
        data = json.loads(request.body)
        url = data['image_url']
        filename = os.path.basename(url)
        path = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)

        try:
            # Decode image for stego
            message = decode_image_stego(path).strip()

            # Check for valid stego message or suspicious content
            if not message or all(c in "01" for c in message) or len(message) < 5 or message == "Original Content":
                print("⚠️ No valid stego message found or Original Content. Running AI detector...")
                message = detect_ai_generated(path)
            else:
                print("✅ Stego message found:", message)

        except Exception as e:
            message = f"Error decoding stego: {str(e)}"
            print("❌ Stego decoding error:", str(e))

        return JsonResponse({'message': message})

