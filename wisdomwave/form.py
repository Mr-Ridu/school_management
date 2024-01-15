# forms.py
from django import forms
from .models import StudentDetails,TeacherDetails,ExamDetails,subject

class StudentForm(forms.ModelForm):
    class Meta:
        model = StudentDetails
        fields = '__all__'
        exclude = ['student_id']  # Exclude student_id from the form, as it will be auto-generated

    def clean_student_id(self):
        if 'student_id' in self.cleaned_data:
            raise forms.ValidationError("Student ID is automatically generated and cannot be manually set.")
        return self.cleaned_data['student_id']



class Teacherform(forms.ModelForm):
    class Meta:
        model = TeacherDetails
        fields = '__all__'
        exclude = ['employee_id','classteacher']  

    def clean_employee_id(self):
        if 'employee_id' in self.cleaned_data:
            raise forms.ValidationError("Emplayee ID is automatically generated and cannot be manually set.")
        return self.cleaned_data['employee_id']


class Examform(forms.ModelForm):
    class Meta:
        model = ExamDetails
        fields = '__all__'
        exclude = ['exams_availability']

class subjectform(forms.ModelForm):
    class Meta:
        model = subject
        fields = '__all__'
