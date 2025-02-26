from django import forms
from .models import Class, Student, Instructor, Course

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['students', 'instructor', 'course', 'class_date', 'study_material', 'class_joining_link']

    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple,
#        required=True,
        label='Students'
    )
    instructor = forms.ModelChoiceField(
        queryset=Instructor.objects.all(),
#        required=True,
        label='Instructor'
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
#        required=True,
        label='Course'
    )
    class_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=True,
        label='Class Date'
    )
    study_material = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter study material'}),
#        required=False,
        label='Study Material'
    )
    class_joining_link = forms.URLField(
        widget=forms.URLInput(attrs={'placeholder': 'Enter class joining link'}),
#        required=False,
        label='Class Joining Link'
    )
