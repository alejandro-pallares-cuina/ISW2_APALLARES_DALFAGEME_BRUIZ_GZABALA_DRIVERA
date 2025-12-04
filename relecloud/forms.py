from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """
    Formulario para crear/editar reviews.

    T5 PBI PT3 - Crear Formulario:
    Este formulario se usará en las vistas para enviar las reviews.
    """

    class Meta:
        model = Review
        fields = ["rating", "title", "comment"]

        labels = {
            "rating": "Rating (1–5)",
            "title": "Título",
            "comment": "Comentario",
        }

        help_texts = {
            "rating": "Indica una puntuación entre 1 y 5 estrellas.",
            "title": "Opcional: un título corto para tu opinión.",
            "comment": "Opcional: descripción de tu experiencia.",
        }

        widgets = {
            "rating": forms.NumberInput(
                attrs={
                    "min": 1,
                    "max": 5,
                    "class": "form-control",
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Título de tu review (opcional)",
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Escribe aquí tu comentario (opcional)",
                }
            ),
        }
