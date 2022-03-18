from .models import UploadImage
from django.forms import ModelForm
from django import forms

class ImageUpload(ModelForm):

    class Meta:

        model = UploadImage
        fields = '__all__'

        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
