
from django.db.models.aggregates import Avg
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from django.db.models import F
from .models import Students,Subjects
#from .serializers import StudentSerializer
from django.db.models import Sum
# Create your views here.

class StudentCreateMark(APIView):
    
    def post(self,request):
        try:
            data= request.data
            student_name = (data.get("name"))
            dob = (data.get("date"))
            father_name = (data.get("father_name"))
            english = (data.get("english"))
            tamil   = (data.get("tamil"))
            maths   = (data.get("maths"))
            science = (data.get("science"))
            social  = (data.get("social"))
            
            student_new, created = Students.objects.update_or_create(name=student_name,date_of_birth = dob,father_name = father_name)
            student_id = Students.objects.filter(pk = student_new.pk).first()
            Subjects.objects.create(
                student = student_id,
                english  = english,
                tamil = tamil,
                maths = maths,
                science = science,
                social = social
                ).save()                                       

            return Response(
                    status=status.HTTP_200_OK,
                    data={'data':"Created Successfully",
                    'status':status.HTTP_200_OK}
                )

        except Exception as e:
            print(str(e))
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error':str(e)}
            )


class GetStudentsMark(APIView):
    
    def get(self,request):
        try:
            student_obj = Students.objects.all() 
            all_students_marks = []           
            marks = []
            for student in student_obj:
                mark = Subjects.objects.get(pk = student.pk)
                all_students_marks.append({
                    'student_name':student.name,
                    'english':mark.english,
                    'tamil': mark.tamil,
                    'maths': mark.maths,
                    'science': mark.science,
                    'social': mark.social

                })
               
            return Response(
                    status=status.HTTP_200_OK,
                    data= all_students_marks
                )

        except Exception as e:
            print(str(e))
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error':str(e)}
            )

class GetStudentTotalMark(APIView):
    
    def get(self,request):
        try:
            student_obj = Students.objects.all() 
            all_students_marks = []           
            for student in student_obj:
                total = Subjects.objects.filter(pk=student.pk).annotate(total=F('english') + F('tamil') + F('maths') + F('science') + F('social')).values('total')[0].get('total')
                all_students_marks.append({
                    'student_name':student.name,
                    'total_marks':total
                    
                })
            
            return Response(
                    status=status.HTTP_200_OK,
                    data=all_students_marks
                )   
            
        except Exception as e:
            print(str(e))
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error':str(e)}
            )

class GetAverageMark(APIView):
    
    def get(self,request):
        try:
            average_marks = []
            subject_name =  [field.name for field in Subjects._meta.get_fields()]
            for sub in subject_name[2::]:
                average_marks.append({
                    sub:Subjects.objects.aggregate(a = Avg(sub)).get('a')
                })
                   
            return Response(
                    status=status.HTTP_200_OK,
                    data= average_marks
                )
            
            
        except Exception as e:
            print(str(e))
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error':str(e)}
            )