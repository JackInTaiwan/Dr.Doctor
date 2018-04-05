from django.db import models

# Create your models here.
class Message(models.Model):
    nickname = models.CharField(max_length=20)
    text = models.CharField(max_length=225)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname


class Users(models.Model) :
    #values = ["nickname", "gender", "height", "weight", "password"]
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    height = models.IntegerField(max_length=5)
    weight = models.IntegerField(max_length=5)
    password = models.CharField(max_length=20)