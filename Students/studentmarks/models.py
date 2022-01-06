from django.db import models
from django.db.models.fields import FloatField,CharField,DateTimeField,AutoField
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class Students(models.Model):
    name = models.CharField(max_length = 20,db_column="Name")
    Id = models.AutoField(primary_key=True)
    date_of_birth = models.DateTimeField(db_column="D-O-B")
    father_name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

class Subjects(models.Model):
    student = models.ForeignKey(Students,on_delete=models.CASCADE)
    english = models.FloatField(db_column="English")
    tamil = models.FloatField(db_column="Tamil")
    maths = models.FloatField(db_column="Maths")
    science = models.FloatField(db_column="Science")
    social = models.FloatField(db_column="Social")

    