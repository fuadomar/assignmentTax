import os

from django.db import models
import openpyxl

# Create your models here.
from django.urls import reverse

# these values depend on the data formation of file
STARTING_ROW_INDEX = 15
NAME_COL_INDEX = 0
GENDER_COL_INDEX = 1
FEST_BONUS_COL_INDEX = 67
PF_COL_INDEX = 70
TOTAL_INCOME_COL_INDEX = 71
EMP_ID_COL_INDEX = 87
DEPARTMENT_COL_INDEX = 88
DESIGNATION_COL_INDEX = 89
JOINTING_DATE_COL_INDEX = 90
INCOME_YEAR_COL_INDEX = 91
ASSESSMENT_YEAR_COL_INDEX = 92


# TODO add validation check for file type
# todo delete files from media when model object is deleted

class File(models.Model):
    upload = models.FileField(upload_to='uploads/%Y/%m/%d/')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def get_filename(self):
        return os.path.basename(self.upload.name)

    def get_absolute_url(self):
        return reverse('taxcalculation:file_detail', args=[self.id, ])

    def __str__(self):
        return self.get_filename()

    def populate_person_from_file(self):

        book = openpyxl.load_workbook(self.upload.file, data_only=True)
        sheet = book.active

        for row in sheet.iter_rows(min_row=15):  # starting row 15
            if row[0].value is None:  # if name field is empty stop iteration
                break
            print("hm")
            Person.objects.create(name=row[NAME_COL_INDEX].value,
                                  gender=row[GENDER_COL_INDEX].value,
                                  fest_bonus=row[FEST_BONUS_COL_INDEX].value,
                                  pf=row[PF_COL_INDEX].value,
                                  total_income=row[TOTAL_INCOME_COL_INDEX].value,
                                  file=self)
            print("done")
            # print(p.name + "fest: "+ str(p.fest_bonus) + "pf:"+ str(p.pf) + "total:"+str(p.total_income))


class Person(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=15)

    fest_bonus = models.IntegerField()
    pf = models.IntegerField()
    total_income = models.IntegerField()



    file = models.ForeignKey(File, related_name="persons", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('taxcalculation:individual_pdf', args=[self.id])
