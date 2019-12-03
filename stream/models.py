from django.db import models


class User(models.Model):
    token = models.CharField(max_length=100, primary_key=True)
    category = models.CharField(max_length=10)
    sketch = models.ImageField()
    pattern = models.ImageField()
    segment = models.ImageField()
    texture_output = models.ImageField()
    disco_output = models.ImageField()
