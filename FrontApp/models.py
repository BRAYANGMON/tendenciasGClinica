from django.db import models

# Create your models here.
class Sesion(models.Model):
    id=models.IntegerField(primary_key=True)
    token=models.CharField(max_length=200, null=False, default="")

    def __str__(self):
        return f"id: {self.id}, token: {self.token}"    