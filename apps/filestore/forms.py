from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'topbar__upload-hidden',
                                                         'id': 'upload-hidden', 
                                                         'onchange':'this.form.submit()'}),
                                                         label='')