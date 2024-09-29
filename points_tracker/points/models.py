from django.db import models

class Transaction(models.Model):
    payer = models.CharField(max_length=256)
    points = models.IntegerField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.payer} = {self.points}"