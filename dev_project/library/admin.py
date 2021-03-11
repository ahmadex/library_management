from django.contrib import admin
from . import models
# Register your models here.

# admin.site.register(models.User)
admin.site.register(models.Faculty)
admin.site.register(models.Librarian)
admin.site.register(models.Student)
admin.site.register(models.Role)
admin.site.register(models.Department)
admin.site.register(models.Category)
admin.site.register(models.Book)
admin.site.register(models.Admin)
admin.site.register(models.BookRecord)




# Register your models here.
admin.site.site_header = "Library Adminn"
admin.site.site_title = "Library admin area"
admin.site.index_title = "Welcome to Library Management System"

# admin.site.register(Department)
# admin.site.register(Category)
# admin.site.register(Role)


# admin.site.register(Student)

# admin.site.register(Faculty)
# admin.site.register(Librarian)
# admin.site.register(Book)
# admin.site.register(BookRecord)

class UserAdmin(admin.ModelAdmin):
  list_display = ('first_name', 'last_name', 'username', 'phone_no', 'profile_pic', 'role', 'department')
admin.site.register(models.User, UserAdmin)
