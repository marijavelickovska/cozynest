from django import forms
from .models import UserProfile
from django.contrib.auth.models import User


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating the built-in User model's username, email,
    and full name (first and last name combined).
    """
    full_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        """
        Initialize form and set initial value for full_name
        from first and last name.
        """
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['full_name'].initial = (
                f"{self.instance.first_name} {self.instance.last_name}"
            )

    def save(self, commit=True):
        """
        Save the User instance, splitting full_name
        into first_name and last_name.
        """
        user = super().save(commit=False)
        full_name = self.cleaned_data.get('full_name', '')
        if full_name:
            parts = full_name.split(' ', 1)
            user.first_name = parts[0]
            user.last_name = parts[1] if len(parts) > 1 else ''
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """
    Form for updating the UserProfile model, excluding the linked User field.
    """
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = (
                'border-black rounded-0 profile-form-input'
            )
            self.fields[field].label = False
