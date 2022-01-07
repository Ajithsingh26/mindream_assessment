
from django.db.models.aggregates import Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Sum
from .models import StudentsDetails,Subjects,Studentmarks

class StudentCreateMark(APIView):
    
    def post(self,request):
        try:
            data= request.data
            student_name = (data.get("name"))
            dob = (data.get("date"))
            father_name = (data.get("father_name"))
            
            
            student_new, created = StudentsDetails.objects.update_or_create(name=student_name,date_of_birth = dob,father_name = father_name)
            # using update or create to check if the student details are alread there in db.
            # if its there then it only add marks and link it with the existing student data
            if created:
                student_id = StudentsDetails.objects.filter(pk = student_new.pk).first()
            else:
                student_id = StudentsDetails.objects.get(name=student_name,date_of_birth = dob,father_name = father_name)
            
            for i in Subjects.objects.values_list('subject_name',flat = True):
                Studentmarks.objects.create(
                    student = student_id,
                    subject = Subjects.objects.get(subject_name=i),
                    marks = data.get(i)
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
            student_obj = StudentsDetails.objects.all() 
            all_students_marks = []           
            for student in student_obj:
                sub_marks = {}
                for sub in Subjects.objects.values_list('subject_name',flat = True): 
                    sub_id = Subjects.objects.get(subject_name= sub)
                    sub_marks[sub] = Studentmarks.objects.values_list('marks',flat = True).get(student_id =student.pk,subject_id =sub_id)

                all_students_marks.append({
                    'student_name':student.name,
                    'english': sub_marks.get('english'),
                    'tamil': sub_marks.get('tamil'),
                    'maths': sub_marks.get('maths'),
                    'science': sub_marks.get('science'),
                    'social': sub_marks.get('social')
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
            student_obj = StudentsDetails.objects.all() 
            all_students_marks = []           
            for student in student_obj:
                total = Studentmarks.objects.filter(pk=student.pk).annotate(total =Sum('marks')).values('total')[0].get('total')
                
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
            for sub in Subjects.objects.values_list('subject_name',flat = True):
                sub_id = Subjects.objects.get(subject_name= sub)
                avg_marks = Studentmarks.objects.filter(subject_id=sub_id).aggregate(mark = Avg("marks")).get('mark')
                average_marks.append({
                    sub:str(round(avg_marks, 2))
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