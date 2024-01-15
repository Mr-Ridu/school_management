from django.contrib.auth.models import AbstractUser, BaseUserManager,User
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Max


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    ROLES = (
        ('superuser', 'Superuser'),
        ('teacher', 'Teacher'),
        ('principal', 'Principal'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLES)
    profile_picture = models.ImageField(upload_to='pp',null=True,blank=True)
    objects = CustomUserManager()
    employee_id = models.CharField(max_length=20, unique=True,default='') #remove default option when site is ready

    def save(self, *args, **kwargs):
        if not self.employee_id:
            session = str(self.date_joined.strftime('%Y'))
            self.employee_id = f'em{session}0{CustomUser.objects.last().id}'  
        super().save(*args, **kwargs)


    def is_teacher(self):
        return self.role == 'teacher'

    def is_admin(self):
        return self.role == 'admin'

    def is_principal(self):
        return self.role == 'primcipal'





class SchoolInfo(models.Model):
    school_name = models.CharField(max_length=100)
    school_logo = models.ImageField(upload_to='logo',null=True,blank=True)
    school_location = models.CharField(max_length=255)
    school_slogan = models.CharField(max_length=500)
    school_email = models.EmailField()
    school_contacts = models.CharField(max_length=100)
    about_school = models.TextField(blank=True, null=True)

    # Social Media Links
    facebook_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    youtube_link = models.URLField(blank=True, null=True)
    whatsapp_link = models.URLField(blank=True, null=True)


    def __str__(self):
        return self.school_name

    @classmethod
    def get_singleton(cls):
        instance, created = cls.objects.get_or_create(pk=1)
        return instance

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)




class StudentDetails(models.Model):
    # Personal Information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    nationality = models.CharField(max_length=50)
    address = models.TextField()
    contact_number = models.CharField(max_length=20)
    student_email= models.EmailField(blank=True)
    # Parent/Guardian Information
    parent_name = models.CharField(max_length=100)
    relationship_to_student = models.CharField(max_length=50)
    parent_contact_number = models.CharField(max_length=20)
    parent_nid = models.CharField(max_length=50)
    parent_email = models.EmailField()
    parent_address = models.TextField()
    # Academic Information
    student_id = models.CharField(max_length=20, unique=True)
    admission_date = models.DateField()
    graduation_date = models.DateField(null=True, blank=True)
    class_grade = models.CharField(max_length=50) #class have to change in onetomany fields
    section = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=10)
    profile_p = models.FileField(upload_to='documents/', null=True, blank=True) #Profile Picture
    # Medical Information
    allergies = models.TextField(null=True, blank=True)
    medications = models.TextField(null=True, blank=True)
    emergency_contact_medical = models.CharField(max_length=20, null=True, blank=True)
    blood_group = models.CharField(max_length=20, null=True, blank=True)
    doctor_contact_info = models.TextField(null=True, blank=True)
    # Behavioral Information
    conduct_grades = models.CharField(max_length=50, null=True, blank=True)
    disciplinary_records = models.TextField(null=True, blank=True)
    # Extracurricular Activities
    clubs_and_societies = models.TextField(null=True, blank=True)
    sports_participation = models.TextField(null=True, blank=True)
    achievements = models.TextField(null=True, blank=True)
    # Document Information
    birth_certificate = models.FileField(upload_to='documents/', null=True, blank=True)



    def save(self, *args, **kwargs):
        if not self.student_id:
            last_student_id = StudentDetails.objects.aggregate(Max('id'))['id__max'] or 0
            session = str(self.admission_date.strftime('%Y'))
            roll = str(self.roll_number).zfill(3)
            self.student_id = f'st{session}{roll}{last_student_id + 1}'
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.student_id}- {self.class_grade}-{self.roll_number}-{self.section}"


class TeacherDetails(models.Model):
    username = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    employee_id = models.CharField(max_length=20, unique=True,default='')

    classteacher = models.CharField(max_length=50,blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField()
    address = models.TextField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    qualifications = models.TextField()
    subjects_taught = models.CharField(max_length=255)#extra
    years_of_experience = models.PositiveIntegerField()
    joining_date = models.DateField()
    department = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    job_role = models.CharField(max_length=50)  # extra
    profile_picture = models.ImageField(upload_to='teacher_profiles/', null=True, blank=True)
    facebook = models.CharField(max_length=50, blank=True)
    twitter = models.CharField(max_length=50,blank=True)
    instagrame = models.CharField(max_length=50,blank=True)
    whatsapp = models.CharField(max_length=50,blank=True)
    youtube = models.CharField(max_length=50,blank=True)

    def __str__(self):
        return f'{self.username}   &   {self.employee_id}'



class ExamDetails(models.Model):
    main_exam_name = models.CharField(max_length=100)
    exam_name = models.CharField(max_length=100)
    exam_date = models.DateField()
    exam_time = models.TimeField()
    exams_availability = models.BooleanField(default=True)
    details_of_exam = models.TextField()
    registration_start_date = models.DateField()
    registration_end_date = models.DateField()

    def __str__(self):
        return f"{self.main_exam_name} - {self.exam_name}"


class class_Grade(models.Model):
    classess = models.CharField(max_length=50)
    
    def __str__(self):
        return self.classess


class sections(models.Model):
    sec = models.CharField(max_length=100)
    class_grade = models.ForeignKey(class_Grade, on_delete=models.CASCADE, related_name='sections')

    def __str__(self):
        return self.sec
    

class subject(models.Model):
    subject_name = models.CharField(max_length=100)
    class_grade = models.ManyToManyField(class_Grade,  related_name='subject_name')

    def __str__(self):
        return self.subject_name
    

class Mark(models.Model):
    student = models.ForeignKey(StudentDetails, on_delete=models.CASCADE)
    subject = models.ForeignKey(subject, on_delete=models.CASCADE)
    exam = models.ForeignKey(ExamDetails, on_delete=models.CASCADE)
    marks_obtained = models.PositiveIntegerField()
    stu_class = models.CharField()
    stu_section = models.CharField()
    stu_roll = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.exam} - Marks: {self.marks_obtained}"
