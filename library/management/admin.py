from django.contrib import admin
from .models import Book, IssuedBook, UserProfile,StudentProfile,Category


class BookAdmin(admin.ModelAdmin):
    list_display=('id', 'book_title', 'book_author', 'book_category',
    'book_publisher', 'book_quantity', 'created_at' 
    )
    list_display_links = ('id', 'book_title')
    ordering = ('id',)


# Register your models here.
admin.site.register(UserProfile)
#admin.site.register(User)
admin.site.register(Book, BookAdmin)
admin.site.register(StudentProfile)
admin.site.register(IssuedBook)
admin.site.register(Category)