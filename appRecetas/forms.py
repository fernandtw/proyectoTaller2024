from django import forms
from .models import Post, Contacto, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",  # Título
            "ingredients",  # Ingredientes
            "instructions",  # Instrucciones
            "image",  # Imagen
            "tabla",  # Tabla
            "category",  # Categoría
        ]
        widgets = {
            "ingredients": forms.Textarea(attrs={"rows": 4, "cols": 40}),
            "instructions": forms.Textarea(attrs={"rows": 6, "cols": 40}),
        }

    # Hacer los campos obligatorios
    title = forms.CharField(label="Título", required=True)
    ingredients = forms.CharField(widget=forms.Textarea(attrs={"rows": 4, "cols": 40}), label="Ingredientes", required=True)
    instructions = forms.CharField(widget=forms.Textarea(attrs={"rows": 6, "cols": 40}), label="Instrucciones", required=True)
    image = forms.ImageField(label="Imagen", required=True)
    tabla = forms.ImageField(required=True)  # Tabla


    

class ContactoForm(forms.ModelForm):
    
    class Meta:
        model = Contacto
        fields = ["nombre", "correo", "tipo_consulta", "mensaje", "avisos"]
        


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escribe tu comentario...'}),
        }
