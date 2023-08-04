from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Bank(models.Model):
    name = models.CharField(max_length=100, null=False)
    swift_code = models.CharField(max_length=100, null=False)
    institution_number = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=100, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return 'Bank Name is: '+str(self.name)


class Branch(models.Model):
    name = models.CharField(max_length=100, null=False)
    transit_number = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=100, null=False)
    email = models.EmailField(default='admin@utoronto.ca')
    capacity = models.IntegerField(blank=True, null=True)
    last_modified = models.TimeField()
    bank_name=models.ForeignKey(Bank,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return 'Branch Name is: '+str(self.name)
