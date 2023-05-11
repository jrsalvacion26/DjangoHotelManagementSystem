from django import forms
from Hotel_managements.Employee_model import Employee_Member


class EmployeeForm(forms.ModelForm):
    Employees_Name = forms.CharField()
    emp_username = forms.EmailField(widget=forms.EmailInput())
    payment_method = forms.ChoiceField(choices=[('cheque', 'Cheque'), ('bank transfer', 'Bank Transfer')])
    emp_password = forms.CharField(widget=forms.PasswordInput())
    status = forms.CharField()
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')])
    level = forms.ChoiceField(choices=[('junior level', 'Junior Level'), ('mid level', 'Mid Level'), ('senior level', 'Senior Level')])
    
    type_job = forms.ChoiceField(choices=[('hotel manager', 'Hotel Manager'), ('front desk manager', 'Front Desk Manager'),
    ('housekeeping manager','Housekeeping Manager'),('food and beverage manager','Food and Beverage Manager'),
    ('maintenance manager','Maintenance Manager'), ('human resources manager','Human Resources Manager')])
    class Meta:
        model = Employee_Member
        fields = "__all__"   
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data["emp_password"])
        
        if commit:
            instance.save()
        return instance
        