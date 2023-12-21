from django import forms

from utils.django_forms import add_attr
from recipes.models import Recipe


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_attr(self.fields.get("preparation_steps"), "class", "span-2")

    class Meta:
        model = Recipe
        fields = [
            "title",
            "description",
            "preparation_time",
            "preparation_time_unit",
            "servings",
            "servings_unit",
            "preparation_steps",
            "cover",
            "category",
        ]

        widgets = {
            "cover": forms.FileInput(attrs={"class": "span-2"}),
            "servings_unit": forms.Select(
                choices=(
                    ("Porções", "Porções"),
                    ("Pedaços", "Pedaços"),
                    ("Pessoas", "Pessoas"),
                )
            ),
            "preparation_time_unit": forms.Select(
                choices=(
                    ("Minutos", "Minutos"),
                    ("Horas", "Horas"),
                )
            ),
        }
