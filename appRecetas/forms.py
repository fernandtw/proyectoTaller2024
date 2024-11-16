from django import forms
from .models import Post, Contacto, Comment
from utils.custom_image import customize_image


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

    def save(self, commit=True):
        post = super().save(commit=False)  # Obtenemos el objeto sin guardarlo aún

        # Personalizar la imagen si existe
        if post.image:
            post.image = customize_image(post.image, size=(450, 550), quality=85)
        
        # Personalizar la tabla si existe
        if post.tabla:
            post.tabla = customize_image(post.tabla, size=(450, 550), quality=85)

        if commit:
            post.save()  # Guardamos el post con las imágenes personalizadas
        
        return post


    

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
