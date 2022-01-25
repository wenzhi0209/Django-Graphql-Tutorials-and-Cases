from django.db import models

# Create your models here.
class Author(models.Model):
    family_name=models.CharField(max_length=200)
    given_name=models.CharField(max_length=200)

    def __str__(self):
        return self.given_name
    
class Book(models.Model):
    title=models.CharField(max_length=200)
    subtitle=models.CharField(max_length=200)
    author=models.ForeignKey(Author, verbose_name=("author"), on_delete=models.CASCADE)
    published=models.DateField()