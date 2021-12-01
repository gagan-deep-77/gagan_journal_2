from django.db import models
from django.db.models.deletion import CASCADE
from datetime import datetime
from django.utils.timezone import now

class User(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField(max_length=400)
    password = models.CharField(max_length=200)



    def __str__(self):
        return self.name





class Post(models.Model):
    title = models.CharField(max_length=240)
    body = models.TextField()
    user = models.ForeignKey(User,on_delete=CASCADE)
    pub_date = models.DateTimeField(default=now,editable=False)
    likes = models.IntegerField(default=0)
    def __str__(self):
        return self.title[:20]


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE)
    pub_date = models.DateTimeField(default=now,editable=False)
    likes = models.IntegerField(default=0)
    body = models.TextField(max_length=1024)
    post = models.ForeignKey(Post, on_delete=CASCADE,default=None)
    def __str__(self):
        return self.body[:64]


