from django.db import models

# Create your models here.
class tower(models.Model):
    predicted_Usage=models.CharField(max_length=10000)
    actual_Usage=models.CharField(max_length=10000)
    difference=models.CharField(max_length=10000)
    class Meta:
        db_table = 'tower_model'