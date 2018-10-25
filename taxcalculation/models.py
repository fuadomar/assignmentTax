import os

from django.db import models


# Create your models here.
from django.urls import reverse


class File(models.Model):
    upload = models.FileField(upload_to='uploads/%Y/%m/%d/')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def filename(self):
        return os.path.basename(self.upload.name)

    def get_absolute_url(self):
        return reverse('taxcalculation:file_detail', args=[self.id,])

    def populatePersonFromFile(self):
        pass

class Person(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=15)

    fest_bonus = models.IntegerField()
    pf = models.IntegerField()
    total_income = models.IntegerField()
    file = models.ForeignKey(File, related_name="persons", on_delete=models.CASCADE)
