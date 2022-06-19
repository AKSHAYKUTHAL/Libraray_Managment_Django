from django.db import models
from django.contrib.auth.models import Group  
from django.core.paginator import Paginator
from datetime import datetime,date
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from .decorators import allowed_users
from .forms import (UserAdminUpdateForm,  UserProfileAdminUpdateForm, BookForm, 
                    StudentUserRegisterForm, UserStudentUpdateForm,StudentProfileUpdateForm,
                    )
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Book, IssuedBook, StudentIssuedBook,StudentProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from . import models
import datetime



#Create your views here.

def home(request):
    return render(request, 'index.html')


def login_user(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('AdminProfile')
            else:
                messages.error(request,'Username or Password is Incorrect')
        else:
            messages.error(request,'Fill out all the fields')
    return render(request, 'registration/login.html', {})


@login_required(login_url='/')
@allowed_users(allowed_roles=['admin'])
def AdminProfile(request):

    return render(request, 'admin/AdminProfile.html' )
    
def Editprofile(request):
    if request.method == 'POST':
        adminform = UserAdminUpdateForm(request.POST, instance=request.user)
        profileform =  UserProfileAdminUpdateForm(request.POST, 
                                                  request.FILES, 
                                                  instance=request.user.userprofile)
        if adminform.is_valid() and profileform.is_valid():
            adminform.save()
            profileform.save()
            messages.success(request, f'You are Updated!')
            return redirect('AdminProfile')
    else:
            adminform = UserAdminUpdateForm(instance=request.user)
            profileform = UserProfileAdminUpdateForm(instance=request.user.userprofile)
    context ={
        'adminform': adminform, 
        'profileform': profileform,
    }
    return render(request, 'admin/Editprofile.html',context)

@login_required(login_url='/')
@allowed_users(allowed_roles=['admin'])
def AddBook(request):
    if request.method=='POST':
        addform = BookForm(request.POST, request.FILES )
        
        if addform.is_valid():
            addform.save()
            messages.success(request, f'Book Added Successfully')
            return redirect('AddBook')
    else:
        addform = BookForm()
    context = {
        'addform':addform
    }
    return render(request, 'admin/AddBook.html', context)

@login_required(login_url='/')
@allowed_users(allowed_roles=['admin'])    
def BookViewAndSearch(request):
    addbooks = Book.objects.all()
    paginator=Paginator(Book.objects.all(), 6)
    page = request.GET.get('page')
    books = paginator.get_page(page)
    nums = "a" * books.paginator.num_pages
    try:
        book=paginator.page(page)
    except PageNotAnInteger:
        book=paginator.page(1)
    except EmptyPage:
        book=paginator.page(paginator.num_pages)
    return render(request, 'admin/BookViewAndSearch.html',{'addbooks':addbooks, 'books':books, 'nums':nums})

@login_required(login_url='/')
@allowed_users(allowed_roles=['admin'])
def updatebook(request, pk):
    book = Book.objects.get(id=pk)
    form = BookForm(instance=book)

    if request.method == 'POST':
        form =BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('BookViewAndSearch')
    context={
        "form":form
    }
    return render(request, 'admin/updatebook.html', context)

@login_required(login_url='/')
@allowed_users(allowed_roles=['admin'])
def DeleteBook(request, pk):
    book = Book.objects.get(id=pk)
    book.delete()
    return redirect ('BookViewAndSearch')

@login_required(login_url='/')
@allowed_users(allowed_roles=['admin'])
def BookDetail(request, pk):
    eachbook =Book.objects.get(id=pk)
    context={
        'eachbook':eachbook
    }
    return render(request, 'admin/BookDetail.html', context)

@login_required(login_url='/')
@allowed_users(allowed_roles=['admin'])
def ViewDateInfo(request):
    return render(request, 'admin/ViewDateInfo.html')

@login_required(login_url='/')
@allowed_users(allowed_roles=['admin'])
def BookSearch(request):
    if request.method =='GET':
        query = request.GET.get('query')
        if query:
            books = Book.objects.filter(book_title__icontains=query)
            return render(request, 'admin/BookSearch.html', {'books': books})
        else:
            print("No Information....")
            return request(request, 'admin/BookSearch.html', {})

@login_required(login_url='/')
@allowed_users(allowed_roles=['admin'])
def StudentSearch(request):
    if request.method =='GET':
        query = request.GET.get('query')
        if query:
            items = StudentProfile.objects.filter(enrollment__icontains=query)
            return render(request, 'admin/StudentSearch.html', {'items': items})
        else:
            print("No Information....")
            return request(request, 'admin/IssuedSearch.html', {})

@login_required(login_url='/')
@allowed_users(allowed_roles=['admin'])
def StudentDetails(request):
    data= StudentProfile.objects.all()
    p=Paginator(StudentProfile.objects.all(),4)
    page = request.GET.get('page')
    data2 = p.get_page(page)
    nums = "a" * data2.paginator.num_pages
    contex={
        'studentprofile':data,
        'data2':data2,
        'nums':nums,
    }
    return render(request, 'admin/StudentDetails.html',contex)

@login_required(login_url='/')
@allowed_users(allowed_roles=['admin'])
def IssuedSearch(request):
    if request.method =='GET':
        query = request.GET.get('query')
        if query:
            items = IssuedBook.objects.filter(enrollment__icontains=query)
            items = IssuedBook.objects.filter(enrollment__icontains=query)
            return render(request, 'admin/IssuedSearch.html', {'items': items})
        else:
            print("No Information....")
            return request(request, 'admin/IssuedSearch.html', {})

@login_required(login_url='/')
@allowed_users(allowed_roles=['admin'])
def IssuedDetails(request):
     issuedbooks=models.IssuedBook.objects.all()
     items=[]
     for obj in issuedbooks:
        issdate=str(obj.issue_date.day)+'-'+str(obj.issue_date.month)+'-'+str(obj.issue_date.year)
        expdate=str(obj.expire_date.day)+'-'+str(obj.expire_date.month)+'-'+str(obj.expire_date.year)
        #fine calculation
        days=(date.today()-obj.issue_date)
        print(date.today())
        d=days.days
        fine=0
        if d>1:
            day = d-1
            fine=day*10

        books=list(models.Book.objects.filter(book_title=obj.book_title))
        students=list(models.StudentProfile.objects.filter(enrollment=obj.enrollment))
        i=0
        for li in books:
            t = (students[i].get_name,students[i].enrollment,books[i].book_title,issdate,expdate,fine)
            i=i+1
            items.append(t)
     paginator =Paginator(items, 7)
     page = request.GET.get('pg')
     items = paginator.get_page(page)
    
     return render(request, 'admin/IssuedDetails.html',{'items':items})

@login_required(login_url='/')
@allowed_users(allowed_roles=['admin'])
def PlaceBook(request):
    data = StudentProfile.objects.all()
    data1 = Book.objects.all()
    if request.method =='POST':
        bo = request.POST['book']
        e=request.POST['enroll']
        tday=datetime.date.today()
        tdelta = datetime.timedelta(days=30)
        ex=tday+tdelta
        stu=StudentProfile.objects.filter(enrollment=e).first()
        book1 = Book.objects.filter(book_title=bo).first()
        StudentIssuedBook.objects.create(studentprofile=stu, book=book1, issue_date=tday, expire_date=ex)
        book1.book_quantity-=1
        if book1.book_quantity == -1:
            messages.success(request, f'Book is Not available at the moment')
        else:
            book1.save()
            messages.success(request, f'Book Issued Successfully !')
            return redirect('PlaceBook')
    d={
        'studentprofile':data,
        'book':data1
    }
    return render(request, 'admin/PlaceBook.html',d)

@login_required(login_url='/')
@allowed_users(allowed_roles=['admin'])
def IssuedBookDetails(request):
    order1 = StudentIssuedBook.objects.all()
    p=Paginator(StudentIssuedBook.objects.all(), 4)
    page = request.GET.get('page')
    data = p.get_page(page)
    nums = "a" * data.paginator.num_pages
    contex={
        'data1':order1,
        'data':data,
        'nums':nums
    }
    return render(request, 'admin/IssuedBookDetail.html',contex)

@login_required(login_url='/')
@allowed_users(allowed_roles=['admin'])
def IssuedBookSearch(request):
    if request.method =='GET':
        query = request.GET.get('query')
        if query:
            items = StudentIssuedBook.objects.filter(studentprofile_enrollment__icontains=query)
            return render(request, 'admin/IssuedBookSearch.html', {'items': items})
        else:
            print("No Information....")
            return request(request, 'admin/IssuedBookSearch.html', {})

@login_required(login_url='/')
@allowed_users(allowed_roles=['admin'])
def ReturnBook(request,pid):
    data1=StudentIssuedBook.objects.get(id=pid)
    book = data1.book.id
    data = Book.objects.get(id=book)
    data1.delete()
    data.book_quantity+=1
    data.save()
    return redirect('IssuedBookDetails')

@login_required(login_url='/')
@allowed_users(allowed_roles=['admin'])
def AdminFine(request,pid):
    data = StudentIssuedBook.objects.get(id=pid)
    tday = datetime.date.today()
    d1 = data.expire_date
    f1 = 0
    d2 = 0
    if tday > d1:
        total_day = tday - d1
        f1 = int(str(total_day)[:-14]) * 5
        d2 = int(str(total_day)[:-14])
    else:
        f1 = 0
        d2 = 0
    context={
        'fine':f1,
        'late':d2
    }
    return render(request, 'admin/AdminFine.html',context)

         #Student Section below........................................................

def StudentRegister(request):
    if request.method =='POST':
        form1 = StudentUserRegisterForm(request.POST)
        if form1.is_valid():
            user = form1.save()
            username = form1.cleaned_data.get('username')

            group = Group.objects.get(name='student')
            user.groups.add(group)

            messages.success(request, f'Account created for {username}')
            return redirect('StudentLogin')
    else:
        form1 = StudentUserRegisterForm()
    return render(request, 'student/StudentRegister.html', {'form1':form1})

def StudentLogin(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('StudentProfiles')
            else:
                messages.error(request,'Username or Password is Incorrect')
        else:
            messages.error(request,'Fill out all the fields')
    return render(request, 'student/StudentLogin.html')

@login_required(login_url='/')
@allowed_users(allowed_roles=['student'])
def StudentProfiles(request):
  
    return render(request, 'Student/StudentProfiles.html')

@login_required(login_url='/')
@allowed_users(allowed_roles=['student'])
def EditStudentprofile(request):
    if request.method == 'POST':
        studentform = UserStudentUpdateForm(request.POST, instance=request.user)
        studentprofileform =  StudentProfileUpdateForm(request.POST, 
                                                  request.FILES, 
                                                  instance=request.user.studentprofile)
        if studentform.is_valid() and studentprofileform.is_valid():
            studentform.save()
            studentprofileform.save()
            messages.success(request, f'You are Updated!')
            return redirect('StudentProfiles')
    else:
        studentform = UserStudentUpdateForm(instance=request.user)
        studentprofileform = StudentProfileUpdateForm(instance=request.user.studentprofile)
    context ={
        'studentform': studentform, 
        'studentprofileform': studentprofileform,
    }
    return render(request, 'Student/EditStudentprofile.html', context)

@login_required(login_url='/')
@allowed_users(allowed_roles=['student'])
def StudentBookView(request):
    addbooks = Book.objects.all().order_by('created_at',)
    paginator=Paginator(Book.objects.all(), 6)
    page = request.GET.get('page')
    books = paginator.get_page(page)
    nums = "a" * books.paginator.num_pages
    try:
        book=paginator.page(page)
    except PageNotAnInteger:
        book=paginator.page(1)
    except EmptyPage:
        book=paginator.page(paginator.num_pages)
    return render(request, 'student/StudentBookView.html',{'addbooks':addbooks, 'books':books, 'nums':nums})

@login_required(login_url='/')
@allowed_users(allowed_roles=['student'])
def StudentBookSearch(request):
    if request.method =='GET':
        items = request.GET.get('items')
        if items:
            books = Book.objects.filter(book_title__icontains=items)
            return render(request, 'student/StudentBookSearch.html', {'books': books})
        else:
            print("No Information....")
            return request(request, 'student/StudentBookSearch.html', {})
 
@login_required(login_url='/')
@allowed_users(allowed_roles=['student'])
def StudentIssueBook(request):
    data = models.StudentProfile.objects.filter(user_id=request.user.id)
    data1 = Book.objects.all()
    if request.method =='POST':
        bo = request.POST['book']
        e=request.POST['enroll']
        tday=datetime.date.today()
        tdelta = datetime.timedelta(days=30)
        ex=tday+tdelta
        stu=StudentProfile.objects.filter(enrollment=e).first()
        book1 = Book.objects.filter(book_title=bo).first()
        StudentIssuedBook.objects.create(studentprofile=stu, book=book1, issue_date=tday, expire_date=ex)
        book1.book_quantity-=1
        if book1.book_quantity == -1:
            messages.success(request, f'Book is Not available at the moment')
        else:
            book1.save()
            messages.success(request, f'Book Issued Successfully ! You can collect it from Library')
            return redirect('StudentIssueBook')
    d={
        'studentprofile':data,
        'book':data1
    }
    return render(request, 'student/StudentIssueBook.html',d)

@login_required(login_url='/')
@allowed_users(allowed_roles=['student'])
def StudentIssuedDetail(request):
    data=StudentProfile.objects.filter(user=request.user.id).first()
    order1 = StudentIssuedBook.objects.filter(studentprofile=data)
    p=Paginator(StudentIssuedBook.objects.filter(studentprofile=data), 4)
    page = request.GET.get('page')
    data3 = p.get_page(page)
    nums = "a" * data3.paginator.num_pages
    context={
        'data1':order1,
        'data3':data3,
        'nums':nums
    }
    return render(request, 'student/StudentIssuedDetail.html',context)

@login_required(login_url='/')
@allowed_users(allowed_roles=['student'])
def StudentFine(request,pid):
    order1= StudentProfile.objects.filter(user=request.user.id).first()
    data = StudentIssuedBook.objects.filter(studentprofile=order1, id=pid).first()
    tday = datetime.date.today()
    mon1= data.expire_date.month
    d1 = data.expire_date.month
    f1=0
    d2=0
    if mon1 == tday.month:
        if d1 < tday.day:
            d2 = tday.day
            f1=d2*5
        else:
            pass
    elif mon1 < tday.month:
        m2 = tday.month-mon1
        d3=(30*m2)+tday.day
        d2=d3-d1
        f1=d2*5
    else:
        f1=0
        d2=0
    context={
        'fine':f1,
        'late':d2
    }
    return render(request, 'student/StudentFine.html',context)

def logoutUser(request):
    logout(request)
    messages.sucess(request,"Logout Sucess")
    return redirect('login')



