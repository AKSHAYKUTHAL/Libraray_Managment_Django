from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey
#from django.db.models.fields.related import OneToOneField
from django.urls import reverse
from PIL import Image
from datetime import datetime,timedelta

# Create your models here.

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=200, null=True)
    enrollment = CharField(max_length=100)
    branch = models.CharField(max_length=40)
    image = models.ImageField(default='default.jpg', upload_to='student_pics')

    def __str__(self):
        return self.user.username+'['+str(self.enrollment)+']'

    @property
    def get_name(self):
        return self.user.student
    @property
    def getuserid(self):
        return self.user.id
    
    def save(self, *args, **kwargs):
        super(StudentProfile,self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width >300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    address = models.CharField(max_length=200, null=True)
    contact = models.CharField(max_length=20, null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    

    def __str__(self):
        return f'{self.user.username} UserProfile'
    
    def save(self, *args, **kwargs):
        super(UserProfile,self).save(*args, **kwargs)
        
        img = Image.open(self.image.path)

        if img.height > 300 or img.width >300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length = 200)

    def __str__(self):
        return self.name
    

class Book(models.Model):
    book_title = models.CharField(max_length=200, unique=True)
    isbn = models.IntegerField(null=True)
    book_author = models.CharField(max_length=200)
    book_category = models.CharField(max_length=100)
    book_publisher = models.CharField(max_length=200)
    book_quantity = models.IntegerField(null=True)
    book_cover = models.ImageField(default='default.jpg', upload_to='book_pics')
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    
    class Meta:
        ordering = ('-id',)
        

    def __str__(self):
        return self.book_title
    
    
    
    
    def save(self, *args, **kwargs):
        super(Book,self).save(*args, **kwargs)
   
        img = Image.open(self.book_cover.path)

        if img.height > 300 or img.width >300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.book_cover.path)

def get_expiry():
    date =  datetime.today() + timedelta(days=1)
    return date.date()

class IssuedBook(models.Model):
    enrollment = models.CharField(max_length=20)
    book_title = models.CharField(max_length=200)
    issue_date = models.DateField(auto_now=True)
    expire_date = models.DateField(default = get_expiry)

    def __str__(self):
        return self.enrollment

class StudentIssuedBook(models.Model):
    studentprofile = models.ForeignKey(StudentProfile, null=True, on_delete=models.SET_NULL)
    book = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL)
    issue_date = models.DateField(auto_now=True)
    expire_date = models.DateField(default = get_expiry)

    class Meta:
        ordering = ('-issue_date',)

    def __str__(self):
        return self.username