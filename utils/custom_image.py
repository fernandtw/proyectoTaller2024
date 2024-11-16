from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import uuid
import os

def customize_image(image, size=(450, 550), output_format=None, quality=95, optimize=True):
    """
    Personaliza la imagen: redimensiona y reduce el peso.
    """
    # Redimensionar la imagen
    img = Image.open(image)
    
    # Si la imagen tiene un canal alfa (transparencia), convertir a RGB
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    img = img.resize(size)

    # Ajustar el formato de salida
    output_format = output_format or img.format or "JPEG"
    
    # Guardar la imagen en memoria para convertirla en un archivo
    img_io = BytesIO()
    img.save(img_io, format=output_format, quality=quality, optimize=optimize)
    img_io.seek(0)
    
    # Generar un nombre único para la imagen usando UUID
    unique_filename = f"{uuid.uuid4().hex}.jpg"  # Se usa el uuid para el nombre del archivo
    
    # Crear un archivo InMemoryUploadedFile a partir de los datos en memoria
    image_file = InMemoryUploadedFile(
        img_io, None, unique_filename, 'image/jpeg', img_io.tell(), None
    )
    
    return image_file

