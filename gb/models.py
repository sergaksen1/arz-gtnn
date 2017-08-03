from django.db import models
from django.utils import timezone
# Create your models here.
class mesage (models.Model):
    tema = models.CharField (max_length=32, null=False, blank = False)
    otzyv = models.CharField(max_length=1024, null=False, blank=False)
    ot_date = models.DateTimeField(null=False, default=timezone.now)

