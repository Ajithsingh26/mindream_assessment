from django.db import models


class StudentsDetails(models.Model):
    name = models.CharField(max_length = 20,db_column="Name")
    Id = models.AutoField(primary_key=True)
    date_of_birth = models.DateTimeField(db_column="D-O-B")
    father_name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

class Subjects(models.Model):
    sub_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=20)

    def __str__(self):
        return self.subject_name

class Studentmarks(models.Model):
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentsDetails, on_delete=models.CASCADE)
    marks = models.FloatField()

    

  
