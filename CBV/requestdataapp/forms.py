from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile


class UserBioForm(forms.Form):
    name = forms.CharField()
    age = forms.IntegerField(label='Your age')
    bio = forms.CharField(label='Biography', widget=forms.Textarea)


def validate_file_name(file: InMemoryUploadedFile) -> None:
    if 'virus' in file.name:
        raise ValidationError('File name should not contain `virus`')


class FileUploadForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name])
