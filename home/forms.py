from django import forms
from .models import ContactMessage, Newsletter


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'autofocus': 'autofocus'
            }),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'maxlength': 1000
            }),
        }


class NewsletterForm(forms.ModelForm):
    """
    Form for users to subscribe to the newsletter.
    Only requires a valid, unique email address.
    """
    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Email Address',
                    'class': 'form-control',
                    'id': 'id_newsletter_email',
                }
            ),
        }

    labels = {
        'email': '',
    }
