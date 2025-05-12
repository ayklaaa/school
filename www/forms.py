from django import forms
from .models import ContactMessage
from django import forms
from .models import ContactMessage

class ContactMessageResponseForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['admin_response', 'status']
        widgets = {
            'admin_response': forms.Textarea(attrs={'rows': 4}),
        }
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
        }

