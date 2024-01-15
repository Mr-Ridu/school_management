from django.contrib import admin
from .models import CustomUser,SchoolInfo, StudentDetails,TeacherDetails,ExamDetails,class_Grade,sections,subject,Mark



admin.site.register(CustomUser)
admin.site.register(StudentDetails)
admin.site.register(TeacherDetails)
admin.site.register(SchoolInfo)
admin.site.register(ExamDetails)
admin.site.register(class_Grade)
admin.site.register(sections)
admin.site.register(subject)
admin.site.register(Mark)
