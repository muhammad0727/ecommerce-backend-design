from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    isbn = models.CharField(max_length=13, unique = True)
    publishedDate = models.DateField()#auto_now=False, auto_now_add=False)


    def __str__(self):
        return self.title
    