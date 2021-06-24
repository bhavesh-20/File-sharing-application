from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class SharedFile(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    actual_file = models.FileField()
    description = models.TextField(blank=True)

    def delete(self, *args, **kwargs):
        path = self.actual_file.url
        print(path[1:])
        os.remove(path[1:])

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name