from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinLengthValidator, RegexValidator


# Create your models here.

class CustomUser(AbstractUser):
    contact=models.CharField(max_length=10,blank=True,null=True)
    groups=models.ManyToManyField('auth.Group', related_name='account_user_set',blank=True)
    user_permissions=models.ManyToManyField('auth.Permission', related_name='account_user_permission_set',blank=True)
    
    def __str__(self):
        return self.username

    class Meta:
        indexes=[
            models.Index(fields=['username']),
            models.Index(fields=['email'])
        
        ]

class Customer(CustomUser):
    
    profile_picture=models.ImageField(upload_to='profile_pics/',null=True,blank=True)
    dob = models.DateField()
    gender = models.CharField(max_length=10,choices=(('male','Male'),('female','Female'),('others','Others')))

    def __str__(self):
        return f'Customer : {self.first_name} {self.last_name}'

    class Meta:
        db_table = 'Customer'




class contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
