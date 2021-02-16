from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Corosel

class CoroselForm(forms.ModelForm):
    class Meta:
        model = Corosel
        fields = [
            'id',
            'name',
            'description',
            'link',
            'corosel_image',
            'is_enabled'
        ]

