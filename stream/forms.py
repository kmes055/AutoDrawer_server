from django import forms
from .models import UploadModel, DownloadModel


class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadModel
        fields = ('uid', 'name', 'file')

    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)


class DownloadForm(forms.Form):
    class Meta:
        model = DownloadModel
        fields = ('uid', 'name', 'file')

    def __init__(self, *args, **kwargs):
        super(DownloadForm, self).__init__(*args, **kwargs)
