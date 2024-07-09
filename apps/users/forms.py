from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Widget, Field

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","password1","password2"]
    

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        username: Field = self.fields['username']
        username.help_text = ' '
        username.widget.attrs.update({
            "hx-post":"/check-username/", 
            "hx-target":"#id_username_helptext", 
            "hx-trigger": "keyup changed delay:1s", 
            "class":"text-dark"
        })

        password1: Field = self.fields['password1']
        password1.help_text = ''

        password2: Field = self.fields['password2']
        password2.help_text = ''