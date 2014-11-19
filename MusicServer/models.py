from django.db import models


class Track(models.Model):
    name = models.CharField(max_length=30, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    # track_path = models.FileField(upload_to='/%Y/%m/%d')
    source_path = models.FileField(upload_to='/source/%Y/%m/%d', null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class User(models.Model):
    email = models.EmailField()
    login = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    tracks = models.ManyToManyField(Track, null=True)

    def __str__(self):
        return self.login

