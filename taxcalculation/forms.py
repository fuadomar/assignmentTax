from django import forms

from taxcalculation.models import File


class FileUploaderForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ('upload',)
