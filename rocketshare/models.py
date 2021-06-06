from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SharedFile(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    actual_file = models.FileField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name