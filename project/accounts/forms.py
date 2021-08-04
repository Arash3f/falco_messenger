from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class login_form(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control form-control-sm" , "id":"colFormLabelSm" }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control form-control-sm" , "id":"colFormLabelSm" , "type": "password" }))

class register_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' , 'password']
        widgets = {
            'username'   : forms.TextInput(attrs={"class":"form-control form-control-sm" , "id":"colFormLabelSm" }),
            'first_name' : forms.TextInput(attrs={"class":"form-control form-control-sm" , "id":"colFormLabelSm" }),
            'last_name'  : forms.TextInput(attrs={"class":"form-control form-control-sm" , "id":"colFormLabelSm" }),
            'email'      : forms.EmailInput(attrs={"class":"form-control form-control-sm" , "id":"colFormLabelSm" , "type": "email" }),
            'password'   : forms.PasswordInput(attrs={"class":"form-control form-control-sm" , "id":"colFormLabelSm" , "type": "password" }),
        }
    def save(self):
        instance = super().save()
        instance.is_active = True
        instance.is_staff = True 
        instance.is_superuser = False 
        instance.set_password(str(instance.password))
        instance.save()
        return instance

class information_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username'   :forms.TextInput  (attrs={"class":"form-control " , "aria-describedby":"inputGroup-sizing-default" , "type": "username" ,"aria-label":"Username" }),
            'first_name' : forms.TextInput (attrs={"class":"form-control " , "aria-describedby":"inputGroup-sizing-default" , "type": "text"     ,"aria-label":"First Name"}),
            'last_name'  : forms.TextInput (attrs={"class":"form-control " , "aria-describedby":"inputGroup-sizing-default" , "type": "text"     ,"aria-label":"Last Name"}),
            'email'      : forms.EmailInput(attrs={"class":"form-control " , "aria-describedby":"inputGroup-sizing-default" , "type": "email"    ,"aria-label":"Email"}),
        }