from django.db import models


class Director(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField(default=2000)
    director = models.ForeignKey(Director, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.year})"
