from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from messenger.models import GroupChat , Members , Message

class group_form(forms.ModelForm):
    class Meta:
        model = GroupChat
        fields = ['name' , 'image']
        widgets = {
            "name" : forms.TextInput(attrs={"class":"form-control form-control-sm" , "id":"colFormLabelSm" }),
            "image" : forms.FileInput(attrs={"class":"form-control form-control-sm" , "id":"customFile" , "type": "file" })
        }
    def clean_name(self):
        name = self.cleaned_data.get('name')
        GroupChat.objects.filter(name=name).count()==1
        if GroupChat.objects.filter(name=name).count()==1:
            self.add_error(None, "incorect data")
            raise forms.ValidationError('Incorect data')
        else:
            return name
    def save(self):
        instance = super().save()
        user = instance.creator
        Members.objects.create(chat=instance , user =user )
        new_message = Message.objects.create(chat=instance , author =user ,warning=True)
        new_message.body = new_message.create()
        new_message.save()
        return instance
        
class join_group_form(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control form-control-sm" , "id":"colFormLabelSm" }))
