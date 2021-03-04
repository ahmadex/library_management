from phonenumber_field.formfields import PhoneNumberField
from .models import Student,Faculty,Librarian,Book,BookRecord,Admin,Role,User,Department,Category
from django import forms
from django.contrib.auth.forms import UserCreationForm

class DepartmentForm(forms.ModelForm):
    CHOICES = (('Computer', 'Computer'),
                ('IT', 'IT'),
                ('Mechanical','Mechanical'),
                ('Civil','Civil'),
                ('Electrical','Electrical'),
                ('Environmental','Environmental')
                )
    department = forms.ChoiceField(choices=CHOICES,)
    class Meta:
        model = Department
        fields = '__all__'


class RoleForm(forms.ModelForm):

    CHOICES = (('Student', 'Student'),('Faculty', 'Faculty'),)
    role = forms.ChoiceField(choices=CHOICES,)
    class Meta:
        model = Role
        fields = ('role',)


class UserForm(UserCreationForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    phone_no = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Contact'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))

    class Meta:
        model = User
        fields = ('first_name','last_name','phone_no','username','password1','password2','profile_pic')


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        exclude = ('user',)


class FacultyForm(forms.ModelForm):
    
    class Meta:
        model = Faculty
        exclude = ('user',)


class StaffForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    phone_no = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Contact'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password1'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))

    class Meta:
        model = User
        fields = ['first_name','last_name','phone_no','username','password1','password2','profile_pic',]


class LibrarianForm(forms.ModelForm):

    class Meta:
        model = Librarian
        exclude = ('user',)

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password'}))


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'

class BookForm(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Title'}))
    author = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Author'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Desciption'}))
    no_of_copy = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'No of Copies'}))
    available_copy = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Available Copies'}))

    class Meta:
        model = Book
        fields = '__all__'


class BookRecordForm(forms.ModelForm):

    class Meta:
        model = BookRecord
        fields = '__all__'