# forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from project.models import Profile
from django.utils.translation import gettext_lazy as _

class RegisterForm(forms.ModelForm):

    profile = forms.ImageField(
        label="Profile Picture Url (options)",
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label=_("Password"),
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Enter password')})
    )
    confirm_password = forms.CharField(
        label=_("Confirm Password"),
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Enter Confirm password')})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        labels = {
            'username': "Username",
            'email': "Email",
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}), 
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address','required': 'required'}), 
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)  # Ignore current user
        if qs.exists():
            raise ValidationError(_("This email is already registered!"))
        return email

    def clean_profile(self):
        profile = self.cleaned_data.get('profile')

        if profile:
            allowed_extensions = ['png', 'jpg', 'jpeg']
            ext = profile.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError("Only PNG, JPG, and JPEG images are allowed.")
            if profile.content_type not in ['image/png', 'image/jpg', 'image/jpeg', 'image/pjpeg']:
                raise forms.ValidationError("Invalid image format.")
            if profile.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file must be under 5MB.")

        return profile


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password or confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', _("Passwords do not match!"))
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")

        if password: 
            user.set_password(password)

        if commit:
            user.save()
            profile = self.cleaned_data.get('profile')

            Profile.objects.update_or_create(
                user=user,
                defaults={'profile': profile}
            )
        return user

