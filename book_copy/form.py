from django import forms


class DocumentForm(forms.Form):
    bfile = forms.FileField(label='Select a file')