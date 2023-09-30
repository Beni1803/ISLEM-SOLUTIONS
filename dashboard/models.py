from django.db import models

class WebApp(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()
