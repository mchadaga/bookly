from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext

from .models import CustomUser


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(label=gettext("Email"), required=True)
    language = forms.ChoiceField(label=gettext('Language'))

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'language')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if settings.USE_I18N and len(settings.LANGUAGES) > 1:
            language = self.fields.get('language')
            language.choices = settings.LANGUAGES
        else:
            self.fields.pop('language')


class UploadAvatarForm(forms.Form):
    avatar = forms.FileField()


class CustomSocialSignupForm(SocialSignupForm):
    """Custom social signup form to work around this issue:
    https://github.com/pennersr/django-allauth/issues/3266"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prevent_enumeration = False
