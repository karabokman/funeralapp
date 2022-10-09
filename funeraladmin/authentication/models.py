from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee_no = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    identity_no = models.CharField(max_length=13)
    gender = models.CharField(max_length=15)
    contacts = models.CharField(max_length=15)
    email = models.CharField(max_length=150)
    role = models.CharField(max_length=150,default='STAFF')
    #img = models.ImageField(upload_to='employee_img', default='placeholder.jpeg')

    def __str__(self):
        return self.employee_no

class EmployeeAddress(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.city
