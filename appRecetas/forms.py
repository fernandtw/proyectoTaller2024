from django import forms
from .models import Post, Contacto

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            "title",
            "ingredients",
            "instructions",
            "image",
            "tabla",
            "published",
            "category",
        ]
        widgets = {
            "ingredients": forms.Textarea(attrs={"rows": 4, "cols": 40}),
            "instructions": forms.Textarea(attrs={"rows": 6, "cols": 40}),
        }


    

class ContactoForm(forms.ModelForm):
    
    class Meta:
        model = Contacto
        fields = ["nombre", "correo", "tipo_consulta", "mensaje", "avisos"]
        