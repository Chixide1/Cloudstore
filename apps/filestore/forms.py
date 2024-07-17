from django import forms

class UploadForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'hidden': '', 'id': 'upload-hidden'}), label='')

class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control topbar__input text-dark','style': 'border-left: none;',
        'type':'text', 'placeholder':'Search All Files...', 'id': 'searchInput',
        "hx-post":"/search/",
        'hx-swap': 'outerHTML',
        "hx-target":"#content", 
        "hx-trigger": "keyup changed delay:1s", 
        }), label='')
    
    # def __init__(self, *args, **kwargs):
    #     super(forms.Form, self).__init__(*args, **kwargs)

    #     self.fields['query']