from django.shortcuts import render, redirect
from django.views import View
from django.views import generic
from django.http import HttpResponse
from .models import Student,Faculty,User,Librarian,Admin,Department,Role,Book,Category
from .forms import StudentForm,UserForm,FacultyForm,StaffForm,DepartmentForm,RoleForm, LibrarianForm, LoginForm, BookForm,CategoryForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from dev_project.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
import smtplib
# Create your views here.



def send_email(request):

    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 587
    if request.method == 'POST':
        reciver = request.POST.get('email')
        subject = 'Stipend'
        message = 'You will be given stipend shortly'
        recipent = str(reciver)

        with smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_HOST_USER,'Shazam@1998')
            server.sendmail(EMAIL_HOST_USER, reciver, message)

        # send_mail(subject,message,EMAIL_HOST_USER,[reciver],fail_silently=False)
        return HttpResponse('Mail Sent Sucessfully')

    return render(request,'library/email.html')



class HomeView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        book = Book.objects.all()[::-1]
        return render(request,'library/home.html',{'books':book})

class Signin(View):

    def get(self, request):
        roleform = RoleForm()
        userform = UserForm()
        studentform = StudentForm()
        departmentform = DepartmentForm()
        facultyform = FacultyForm()
        
        return render(request,'library/signin.html',{
            'userform': userform, 
            'studentform': studentform, 
            'departmentform': departmentform, 
            'roleform': roleform,
            'facultyform': facultyform,
            })
   
    def post(self, request):

        user_role = {
            'Student': StudentForm(request.POST),
            'Faculty': FacultyForm(request.POST)
            }
        
        roleform = RoleForm(request.POST)
        
        if roleform.is_valid():
            temp_role = roleform.cleaned_data['role']
            usertype = user_role.get(temp_role)
            
            userform = UserForm(request.POST, request.FILES)
            deptform = DepartmentForm(request.POST)

            if userform.is_valid() and usertype.is_valid():

                # saving user with department
                user = userform.save(commit=False)
                # department and Role saved
                dept = deptform.save(commit=False)

                dept1 = Department.objects.get(department=dept)
                user.department = dept1
                role1 = Role.objects.get(role=temp_role)
                user.role = role1
                user.save()

                new_user = usertype.save(commit=False)
                new_user.user = user
                new_user.save()
                # login user
                login(request, user)
                return redirect('library:profile', pk=user.id)

            else:
                return render(request,'library/signin.html',{'userform': userform,'departmentform':deptform, 'roleform':roleform})
  

class AddLibrarian(View):

    def get(self, request):
        userform = StaffForm()
        librarianform = LibrarianForm()

        return render(request, 'library/librarian_signin.html',{
            'userform': userform,
            'librarianform': librarianform,
        })
    
    def post(self, request):
        userform = StaffForm(request.POST, request.FILES)
        librarianform = LibrarianForm(request.POST)

        if userform.is_valid() and librarianform.is_valid():
            user = userform.save(commit=False)
           
            new_role = Role.objects.get(role='Librarian')
            user.role = new_role
            user.save()

            lib = librarianform.save(commit=False)
            lib.user = user
            lib.save()
            login(request,user)
            return redirect('library:profile',pk=user.id)
            
        else:
            return render(request, 'library/librarian_signin.html',{
                'userform': userform,
                'librarianform': librarianform
            })


class UserProfile(LoginRequiredMixin,View):

    login_url ='/library/user_login/'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        return render(request, 'library/user_profile.html',{'user':user})


class UserLogin(View):

    def get(self, request):
        form = LoginForm()
        return render(request,'library/login.html',{'form':form})

    def post(self, request):
        form = LoginForm(request.POST)
        
        self.uname = request.POST.get('username')
        self.pasw = request.POST.get('password')
        self.user = authenticate(request, username=self.uname,password=self.pasw)
        
        if self.user:
            if self.user.is_active:
                login(request, self.user)
                if self.user.is_staff:
                    return redirect('library:admin_dashboard')
                return redirect('library:profile', pk=self.user.id)

            else:
                return HttpResponse('Account is not Active')
        else:
            messages.info(request,'UserName or Password is Incorrect', extra_tags='alert')
            return render(request,'library/login.html',{'form':form})

class UserLogout(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self,request):
        logout(request)
        return redirect('library:user_login')


class AddBookView(LoginRequiredMixin, View):

    login_url = '/library/user_login/'

    def get(self, request):
        bookform = BookForm()
    
        return render(request,'library/add_book.html',{
            'bookform': bookform,
            })
    
    def post(self, request):
        bookform = BookForm(request.POST, request.FILES)

        if bookform.is_valid():
            book = bookform.save(commit=False)
            # category = bookform.cleaned_data['category']
            # new_category = Category.objects.get(category=category)
            # book.category = new_category
            book.save()
            return redirect('library:book_detail', pk=book.id)
        else:
            return render(request, 'library/add_book.html',{'bookform': bookform})


class BookDetailView(LoginRequiredMixin,View):
    login_url = '/library/user_login/'
    def get(self, request, pk):
        book = Book.objects.get(id=pk)
        return render(request,'library/book_detail.html',{'book': book})


class BookUpdateView(LoginRequiredMixin, View):

    login_url = '/library/user_login/'
    
    def get(self, request, pk):
        book = Book.objects.get(id=pk)
        bookform = BookForm(instance=book)
        return render(request, 'library/add_book.html',{'bookform': bookform})
    
    def post(self, request, pk):
        book = Book.objects.get(id=pk)
        bookform = BookForm(request.POST, request.FILES, instance=book)

        if bookform.is_valid():
            book = bookform.save(commit=False)
            book.save()
            return redirect('library:book_detail',pk=book.id)
        else:
            return render(request,'library/add_book.html',{'bookform':bookform})

class DeleteBookView(LoginRequiredMixin, View):
    login_url = '/library/user_login/'

    def get(self, request, pk):
        book = Book.objects.get(id=pk)
        book.delete()
        return redirect('library:home')


class AdminDashBoard(LoginRequiredMixin,View):
    login_url = '/library/user_login/'

    def get(self, request):
        return render(request,'library/admin_dashboard.html')

class StudentList(LoginRequiredMixin,View):
    login_url = '/library/user_login/'

    def get(self, request):
        student = Student.objects.all().order_by('id')
        return render(request,'library/student_list.html',{'students':student})


class FacultyList(LoginRequiredMixin,View):
    login_url = '/library/user_login/'

    def get(self, request):
        facutly = Faculty.objects.all().order_by('id')
        return render(request,'library/faculty_list.html',{'faculties':facutly})

class LibrarianList(LoginRequiredMixin,View):
    login_url = '/library/user_login/'

    def get(self, request):
        librarian = Librarian.objects.all().order_by('id')
        return render(request,'library/librarian_list.html',{'librarians':librarian})

class BookList(LoginRequiredMixin,View):
    login_url = '/library/user_login/'

    def get(self, request):
        book = Book.objects.all().order_by('id')
        return render(request,'library/book_list.html',{'books':book})

    