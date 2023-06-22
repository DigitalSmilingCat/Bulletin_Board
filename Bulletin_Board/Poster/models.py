from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Poster(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} / {self.category} / {self.created} / {self.user}'

    def get_absolute_url(self):
        return reverse('poster_detail', args=[str(self.pk)])


class Response(models.Model):
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, null=True, choices=[('A', 'Approved'), ('R', 'Rejected')])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poster = models.ForeignKey(Poster, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.text} / {self.created} / {self.status} / {self.user} / {self.poster}'
