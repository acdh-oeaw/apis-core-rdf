from django.db import models


class Person(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_default_uri(self):
        return f"https://www.example.org/id/{self.pk}"


class Dummy(models.Model):
    pass
