from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from django.forms import widgets
from django.forms.models import ModelForm
from django.http import request
from .models import StudentIssuedBook, UserProfile,Book,User,StudentProfile,IssuedBook,Category
from .import models


choices = Category.objects.all().values_list('name','name')

choice_list = []

for item in choices:
   choice_list.append(item)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        
class UserAdminUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class UserProfileAdminUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address', 'contact', 'image']

    
class StudentUserRegisterForm(UserCreationForm):
   email = forms.EmailField()
    
   class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class UserStudentUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class StudentProfileUpdateForm(forms.ModelForm):
   class Meta:
       model = StudentProfile
       fields = ['name','enrollment', 'branch', 'image']

class StudentIssueBookForm(forms.Form):
    book_title2= forms.ModelChoiceField(queryset=models.Book.objects.all(),
                                           empty_label="book_title",
                                           to_field_name="book_title",
                                           label='book_title'
                                        )
    enrollment2= forms.ModelChoiceField(queryset=models.StudentProfile.objects.all(),
                                          empty_label="enrollment and user",
                                          to_field_name="enrollment",
                                          label='enrollment and username'
                                        )       

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_title','isbn', 'book_author', 'book_category', 'book_publisher', 'book_quantity', 'book_cover']
        widgets = {
            'book_title': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'book_author': forms.TextInput(attrs={'class': 'form-control'}),
            'book_category': forms.Select(choices=choice_list,attrs={'class': 'form-control-plaintext'}),
            'book_publisher': forms.TextInput(attrs={'class': 'form-control'}),
            'book_quantity': forms.TextInput(attrs={'class': 'form-control'}),
            'book_cover': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'Book Title*': 'Book Title',
            'Isbn*': 'Isbn',
            'Book Author*': 'Book Author',
            'Book Category*': 'Book Category',
            'Book Publisher*': 'Book Publisher',
            'Book Quantity*': 'Book Quantity',
            'Book Cover*': 'Book Cover',
        }

class IssuedStuForm(ModelForm):
    class Meta:
        model = IssuedBook
        fields = '__all__'
    #enrollment= forms.ModelChoiceField(queryset=models.StudentProfile.objects.all()
    def __init__(self, *args, **kwargs):
        enrollment = kwargs.pop('enrollment', None)
        super(IssuedStuForm, self).__init__(*args, **kwargs)
        if enrollment is not None:
            # update queryset for exercise field
            self.fields['enrollment'].queryset = StudentProfile.objects.filter(enrollment)
        else:
            # UserExercises.objects.none() will return an empty queryset
            self.fields['enrollment'].queryset = StudentProfile.objects.none()