from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class Hotel(models.Model):
    Employee_Name = models.CharField(max_length=200) 
    username = models.EmailField()
    password = models.CharField(max_length=100)

    def set_password(self,raw_password):
        self.password = make_password(raw_password)
        
    def check_password(self, raw_password):
        return check_password(raw_password,self.password)
        
    class Meta:
        db_table = 'register'
        
        
        
