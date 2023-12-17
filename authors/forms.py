from django import forms
from django.contrib.auth.models import User

class RegisterForm (forms.ModelForm):
    class Meta():
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password',
            'email',
        ]

        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }

        help_texts = {
            'email': 'The e-mail must be valid.',
        }

        error_messages = {
            'username': {
                'required': 'This field must be filled',
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your name here',
                'class': 'input text-input other-class',
            }),
            'password': forms.PasswordInput(),
        }