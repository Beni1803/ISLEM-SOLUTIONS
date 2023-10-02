from django.db import models

class Block(models.Model):
    start_frequency = models.FloatField()
    end_frequency = models.FloatField()
    center_frequency = models.FloatField()
    block_code = models.CharField(max_length=100)

    def __str__(self):
        return self.block_code
