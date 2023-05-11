from django import forms
from Hotel_managements.reservation_model import Reservation

class ReservationForm(forms.ModelForm):
    user_update = forms.ChoiceField(choices=[('checkin', 'Check-In')])
    room_type = forms.ChoiceField(choices=[('single', 'Single'), ('double', 'Double'), ('triple', 'Triple')])
    Quantity = forms.IntegerField()
    

    class Meta:
        model = Reservation
        fields = ('user_update', 'room_type', 'Quantity')
        
        
class BookingCheckout(forms.ModelForm):
    user_update = forms.ChoiceField(choices=[('checkout', 'Check-Out')])
    Quantity = forms.IntegerField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    
    
    class Meta:
        model = Reservation
        fields = ('user_update','Quantity')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Quantity'].initial = 0
