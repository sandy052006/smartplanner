from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Goal

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['city', 'income', 'job', 'lifestyle']
        widgets = {
            'city': forms.TextInput(attrs={
                'id': 'city-input',
                'autocomplete': 'off',
                'placeholder': 'e.g. Mumbai, Delhi, London, Dubai...',
            }),
            'income': forms.NumberInput(attrs={
                'placeholder': 'Monthly income',
                'min': '0',
                'step': '100',
            }),
            'job': forms.TextInput(attrs={
                'placeholder': 'e.g. Software Engineer, Teacher...',
            }),
            'lifestyle': forms.Select(),
        }

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'target_amount', 'current_amount', 'target_date']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Emergency Fund, Vacation...'}),
            'target_amount': forms.NumberInput(attrs={'placeholder': 'Target amount', 'min': '0', 'step': '100'}),
            'current_amount': forms.NumberInput(attrs={'placeholder': 'Amount saved so far', 'min': '0', 'step': '100'}),
            'target_date': forms.DateInput(attrs={'type': 'date'}),
        }

class SettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['theme', 'language', 'custom_primary', 'custom_bg', 'custom_surface', 'custom_text', 'custom_accent']
        widgets = {
            'theme': forms.RadioSelect(),
            'language': forms.Select(),
            'custom_primary': forms.TextInput(attrs={'type': 'color', 'class': 'color-picker'}),
            'custom_bg': forms.TextInput(attrs={'type': 'color', 'class': 'color-picker'}),
            'custom_surface': forms.TextInput(attrs={'type': 'color', 'class': 'color-picker'}),
            'custom_text': forms.TextInput(attrs={'type': 'color', 'class': 'color-picker'}),
            'custom_accent': forms.TextInput(attrs={'type': 'color', 'class': 'color-picker'}),
        }
        labels = {
            'custom_primary': 'Primary Color',
            'custom_bg': 'Background Color',
            'custom_surface': 'Card/Surface Color',
            'custom_text': 'Text Color',
            'custom_accent': 'Accent/Success Color',
        }
