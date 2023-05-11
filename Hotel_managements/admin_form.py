from django import forms
from Hotel_managements.admin_model import Administration


class AdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')])
    class Meta:
        model = Administration
        fields = "__all__"   
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data["password"])
        
        if commit:
            instance.save()
        return instance
        