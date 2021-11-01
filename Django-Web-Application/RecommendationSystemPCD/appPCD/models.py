from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email', 'password1','password2']



class scholarship(models.Model):
	id = models.IntegerField(primary_key=True)
	ScholarshipName=models.CharField(max_length=150)
	University=models.CharField(max_length=100)
	ScholarshipValue=models.FloatField(null=True, blank=True, default=None)
	Deadline=models.CharField(max_length=20)
	Location=models.CharField(max_length=50)
	Level=models.CharField(max_length=50)
	Description=models.CharField(max_length=2000)
	Link=models.CharField(max_length=100)
	Program=models.CharField(max_length=300,default="")
	Rank=models.FloatField(null=True, blank=True, default=None)
	Class=models.CharField(max_length=3)
	def __str__(self):
		return self.ScholarshipName

class Historique(models.Model):
    username=models.CharField(max_length=100)
    date=models.CharField(max_length=100)
    classe=models.CharField(max_length=3)

    def __str__(self):
        return self.date
