from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import auth,User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser,StudentDetails,TeacherDetails , SchoolInfo,ExamDetails,class_Grade,sections,subject,Mark
from .form import StudentForm,Teacherform,Examform,subjectform
from .custom_decorator import user_is_admin_or_superuser,admin_required,only_teacher_required
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def wisdomwave(request):
    return render (request, 'index.html')


def UserLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Congratulations! You logged in.")
            urole = request.user.role
            if urole=='teacher' or urole=='principal':
                return redirect('teachersprofile')
            else:
                return redirect("wisdomwave")
        else:
            messages.error(request,"Sorry! Username or password Dosen't match")
            print("Sorry! Username or password Dosen't match")
            return redirect("wisdomwave")
    else:
        print('else part')
        return render(request, 'index.html')

@login_required
def UserLogout(request):
    auth.logout(request)
    messages.success(request,"You Logged Out")
    return redirect ("wisdomwave")

@login_required
def dashboard(request):
    theuser= request.user
    therole= theuser.role
    all_student = StudentDetails.objects.count()
    all_teacher = CustomUser.objects.filter(role='teacher').count()
    tdet = TeacherDetails.objects.get(username=theuser) if therole=='teacher' else None
    context = {'theuser':theuser,'therole':therole,'all_student':all_student,'all_teacher':all_teacher,'tdet':tdet}
    return render(request, 'dash/dashbord.html',context)


        
@login_required
@admin_required
def add_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST['role']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        profile_picture = request.FILES.get('profile_picture') 
        if password != confirm_password:
            messages.error(request, "Enter Both password same")
            return redirect("add_user")  # Update with the actual registration URL
        elif len(password)<8:
            messages.error(request, "Password is too short")
            return redirect("add_user") 
        else:
            CustomUser.objects.create_user(username=username, email=email, password=password, role=role,first_name=first_name,last_name=last_name,profile_picture=profile_picture)
            return redirect("dashboard") 

    return render(request, "dash/add_user.html")



@admin_required
def user_list(request):
    all_u_data = CustomUser.objects.all()
    return render (request, 'dash/user_list.html',{'all_u_data':all_u_data})


@admin_required
def teacher_list(request):
    all_t_data = CustomUser.objects.filter(role='teacher')
    return render (request, 'dash/teacher_list.html',{'all_t_data':all_t_data})




@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            return redirect("dashboard")
        else:
            print(form.errors)
    else:
        form = StudentForm()
    return render(request, 'dash/add_student.html', {'form': form})



@login_required
def update_teacher_profile(request):
    if request.method == 'POST':
        teacher_details, created = TeacherDetails.objects.get_or_create(username=request.user)
        form = Teacherform(request.POST)
        if form.is_valid():
            teacher_details = form.save(commit=False)
            teacher_details.username = request.user
            teacher_details.employee_id=request.user.employee_id
            teacher_details.save()
            messages.success(request, "Profile updated successfully")
            return redirect("teachersprofile")
        else:
            messages.error(request, "Form validation failed")
            print(form.errors)
    else:
        form = Teacherform()

    return render(request, 'updateteachersprofile.html', {'form': form})


@login_required
def all_student(request):
    all_s_data = StudentDetails.objects.all()
    return render (request, 'dash/all_student.html',{'all_s_data':all_s_data})





@login_required
def teachersprofile(request):
    try:
        techardata = TeacherDetails.objects.get(username=request.user)
        return render(request, 'teachersprofile.html',{'techardata':techardata})
    except ObjectDoesNotExist:
        if request.user.role=='teacher':
            messages.warning(request,"Update Your Profile First!")
            return redirect('update_teacher_profile')
        else:
            messages.error(request,"Sorry , You have no permission")
            return redirect ("wisdomwave")



def otp(request,id):
    try:
        otheruser = CustomUser.objects.get(id=id)
        techardata=TeacherDetails.objects.get(username=otheruser)
        return render(request, 'otp.html',{'techardata':techardata,'otheruser':otheruser})

    except ObjectDoesNotExist:
        messages.error(request,"Sorry , Teacher Not found")
        return redirect ("wisdomwave")

@login_required
@admin_required
def add_exam(request):
    if request.method == 'POST':
        form = Examform(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            return redirect("all_exam")
        else:
            print(form.errors)
    else:
        form = Examform()
    return render (request, 'dash/add_exam.html')



@login_required
def all_exam(request):
    exams= ExamDetails.objects.all().order_by('-id')
    return render (request, 'dash/all_exam.html',{'exams':exams})


@login_required
@only_teacher_required
def add_marks(request,id):
    exam = ExamDetails.objects.get(id=id)
    teacher = TeacherDetails.objects.get(username=request.user)
    clas = teacher.classteacher.rsplit(',', 1)[0].strip()
    sec = teacher.classteacher.rsplit(',', 1)[1].strip()
    sub = subject.objects.filter(class_grade__classess=clas)
    stu = StudentDetails.objects.filter(class_grade=clas,section=sec).exclude(mark__exam=exam).order_by('roll_number') 
    try:
        if request.method == 'POST':
            st = request.POST.get('stdetail')
            student = StudentDetails.objects.get(id=st)
            for s in sub:
                marks_obtained = request.POST.get(f'marks_{s.id}')
                if marks_obtained and  marks_obtained.isdigit() and 0<= int(marks_obtained) <=100:
                    mark, created = Mark.objects.get_or_create(student=student, subject=s,stu_class=student.class_grade,stu_section=student.section,stu_roll=student.roll_number, exam=exam, defaults={'marks_obtained': marks_obtained})
                    messages.success(request, f'Marked {"saved" if created else "updated"} for {student.student_id}')
                else:
                    messages.error(request,'Use valid Number and select excet student')
            return redirect('add_marks',id)
    except (ObjectDoesNotExist, ValueError) as e:
        messages.error(request, str(e))
    context={'exam':exam,'student':stu,'teacher':teacher,'clas':clas,'sub':sub}
    return render (request, 'dash/add_marks.html',context)



@login_required
@admin_required
def makeCT(request):
    teacher = TeacherDetails.objects.all()
    stclass= class_Grade.objects.all()
    section= sections.objects.all()

    if request.method == 'POST':
        id = request.POST.get('tuser')
        cassec = request.POST.get('section')
        gettheteacher=TeacherDetails.objects.get(id=id)
        gettheteacher.classteacher=cassec
        gettheteacher.save()
        messages.success(request,f"{gettheteacher.last_name} added as Classteacher")
        return redirect('makeCT')
    
    context = {'teacher':teacher,'stclass':stclass,'section':section}
    return render (request, 'dash/makeCT.html',context)



@login_required
@admin_required
def subjects(request):
    if request.method == 'POST':
        subject_name = request.POST.get('subject_name')
        selected_class_grades = request.POST.getlist('class_grade')
        existing_subject = subject.objects.filter(subject_name__icontains=subject_name).first()

        if existing_subject:
            #existing_subject.class_grade.set(selected_class_grades)
            messages.error(request, f'"{existing_subject}" is already exist!')
        else:
            new_subject = subject.objects.create(subject_name=subject_name)
            new_subject.class_grade.set(selected_class_grades)
            messages.success(request, f'New Subject "{new_subject}" added!')
        return redirect("subjects")

    subs = subject.objects.all()
    class_grades = class_Grade.objects.all()
    return render(request, 'dash/subject.html', {'subs': subs, 'class_grades': class_grades})




def getresult(request):
    exm = ExamDetails.objects.all().order_by('-id')
    cls = class_Grade.objects.all()
    sec = sections.objects.all()

    if request.method == 'POST':
        exam_name = request.POST.get('exam_name')
        stu_id = request.POST.get('stu_id')  
        class_name = request.POST.get('class_name')  
        section = request.POST.get('section')  
        Class_roll = request.POST.get('class_roll')  
        try:
            if stu_id:
                the_marks = Mark.objects.filter(exam__exam_name=exam_name, student__student_id__iexact=stu_id)
                frst_obj = the_marks.first()
                return render(request, 'showresult.html', {'marks': the_marks,'exam_name':exam_name,'frst_obj':frst_obj})
            elif class_name and section and Class_roll:
                print(class_name,section,Class_roll)
                the_marks = Mark.objects.filter(exam__exam_name=exam_name, stu_class=class_name,stu_section=section,stu_roll=Class_roll)
                frst_obj = the_marks.first()
                return render(request, 'showresult.html', {'marks': the_marks,'exam_name':exam_name,'frst_obj':frst_obj})
            else:
               messages.error(request, f"No records found for student : {Class_roll} ")
        except Mark.DoesNotExist:
            messages.info(request, f"No records found for student ID: {stu_id}")
    return render(request, 'getresult.html', {'exm': exm, 'cls': cls, 'sec': sec})


# def showresult(request,the_marks):

#     return render(request, 'showresult.html', {'marks': the_marks})
