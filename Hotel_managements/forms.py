from django import forms
from Hotel_managements.models import Hotel

class HotelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Hotel
        fields = "__all__"   
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data["password"])
        
        if commit:
            instance.save()
        return instance
        