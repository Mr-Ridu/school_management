from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('', views.wisdomwave, name="wisdomwave"),
    path('login', views.UserLogin, name="userlogin"),
    path('logout', views.UserLogout, name="userlogout"),
    path('Dashboard', views.dashboard, name="dashboard"),
    path('create_user', views.add_user, name="add_user"),
    path('create_student', views.add_student, name="add_student"),
    path('teachersprofile', views.teachersprofile, name="teachersprofile"),
    path('all_student', views.all_student, name="all_student"),
    path('all_user', views.user_list, name="all_user"),
    path('Upate_Profile', views.update_teacher_profile, name="update_teacher_profile"),
    path('teacher_list', views.teacher_list, name="teacher_list"),
    path('other_teacher_profile/<int:id>', views.otp, name="otp"),
    path('add_exam', views.add_exam, name="add_exam"),
    path('all_exam', views.all_exam, name="all_exam"),
    path('add_marks/<int:id>', views.add_marks, name="add_marks"),
    path('makeCT', views.makeCT, name="makeCT"),
    path('subjects', views.subjects, name="subjects"),
    path('getresult', views.getresult, name="getresult"),
    path('addclass', views.addclass, name="addclass"),
]
