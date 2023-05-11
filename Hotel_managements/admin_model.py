from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Administration(models.Model):
    admin_id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=200) 
    admin_username = models.EmailField()
    password = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    
    
    def set_password(self,raw_password):
            self.password = make_password(raw_password)
        
    def check_password(self, raw_password):
        return check_password(raw_password,self.password)
    
    
    class Meta:
        db_table = 'admin'