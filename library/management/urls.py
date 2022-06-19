from django.urls import path
from . import views 
#from .views import BookListView, UpdateView


urlpatterns=[
   path('', views.home),
   path('login/', views.login_user, name='login'),
   path('logoutUser/', views.logoutUser, name='logoutUser'),
   path('AdminProfile/', views.AdminProfile, name='AdminProfile'),
   path('Editprofile/', views.Editprofile, name='Editprofile'),
   path('AddBook/', views.AddBook, name='AddBook'),
   path('BookViewAndSearch/', views.BookViewAndSearch, name='BookViewAndSearch'),
   path('updatebook/<int:pk>/', views.updatebook, name='updatebook'),
   path('DeleteBook/<int:pk>/', views.DeleteBook, name='DeleteBook'),
   path('BookDetail/<int:pk>/', views.BookDetail, name='Detail'),
   path('BookSearch/', views.BookSearch, name='BookSearch'),
   path('IssuedDetails/', views.IssuedDetails, name='IssuedDetails'),
   path('IssuedBookDetails/', views.IssuedBookDetails, name='IssuedBookDetails'),
   path('IssuedSearch/', views.IssuedSearch, name='IssuedSearch'),
   path('StudentDetails/', views.StudentDetails, name='StudentDetails'),
   path('StudentSearch/', views.StudentSearch, name='StudentSearch'),
   path('PlaceBook/', views.PlaceBook, name='PlaceBook'),
   path('IssuedBookSearch/', views.IssuedBookSearch, name='IssuedBookSearch'),
   path('ReturnBook/(?P<pid>[0-9]+)', views.ReturnBook, name='ReturnBook'),
   path('AdminFine/(?P<pid>[0-9]+)',views.AdminFine,name='AdminFine'),
   path('StudentRegister/', views.StudentRegister, name='StudentRegister'),
   path('StudentLogin/', views.StudentLogin, name='StudentLogin'),
   path('StudentProfiles/', views.StudentProfiles, name='StudentProfiles'),
   path('EditStudentprofile/', views.EditStudentprofile, name='EditStudentprofile'),
   path('StudentBookSearch/', views.StudentBookSearch, name='StudentBookSearch'),
   path('StudentBookView/', views.StudentBookView, name='StudentBookView'),
   path('StudentIssueBook/', views.StudentIssueBook, name='StudentIssueBook'),
   path('StudentIssuedDetail/', views.StudentIssuedDetail, name='StudentIssuedDetail'),
   path('StudentFine/(?P<pid>[0-9]+)',views.StudentFine,name='StudentFine'),
]