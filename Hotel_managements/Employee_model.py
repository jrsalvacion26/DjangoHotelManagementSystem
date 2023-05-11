from django.db import models
from django.contrib.auth.hashers import make_password, check_password



class Employee_Member(models.Model):
    emp_id = models.AutoField(primary_key=True)
    Employees_Name = models.CharField(max_length=200) 
    emp_username = models.EmailField()
    emp_password = models.CharField(max_length=100)
    type_job = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    salary = models.IntegerField()
    payment_method = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    def set_password(self,raw_password):
            self.emp_password = make_password(raw_password)
        
    def check_password(self, raw_password):
        return check_password(raw_password,self.emp_password)
    
    
    class Meta:
        db_table = 'employee'
    