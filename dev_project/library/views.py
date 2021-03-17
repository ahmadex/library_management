from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views import generic
from django.http import HttpResponse, JsonResponse
from .models import Student,Faculty,User,Librarian,Admin,Department,Role,Book,Category
from .forms import StudentForm,UserForm,FacultyForm,StaffForm,LibrarianForm, LoginForm, BookForm,UserUpdateForm
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

    if request.method == 'POST':
        reciver = request.POST.get('email')
        print(type(reciver))
        subject = 'Mail Check'
        message = 'Mail Eception can not be trace'
        recepient = str(reciver)
        
        try:
            send_mail(subject, 
                message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

        return HttpResponse('Mail Sent Sucessfully')

    return render(request,'library/email.html')



class HomeView(LoginRequiredMixin, View):

    login_url = '/library/user_login/'
    
    def get(self, request):
        book = Book.objects.all()[::-1]
        return render(request,'library/home.html',{'books':book})

class Signin(View):

    def get(self, request):
        userform = UserForm()
        studentform = StudentForm()
        facultyform = FacultyForm()
        
        return render(request,'library/signin.html',{
            'userform': userform, 
            'studentform': studentform, 
            'facultyform': facultyform,
            })
   
    def post(self, request):

        user_role = {
            '1': StudentForm(request.POST),
            '2': FacultyForm(request.POST)
            }
        
        temp_role = request.POST.get('role')
        usertype = user_role.get(temp_role)
        userform = UserForm(request.POST, request.FILES)

        if userform.is_valid() and usertype.is_valid():
            user = userform.save()
            new_user = usertype.save(commit=False)
            new_user.user = user
            new_user.save()
            # login user
            login(request, user)
            return redirect('library:profile', pk=user.id)

        else:
            return render(request,'library/signin.html',{'userform': userform})


class UserUpdate(LoginRequiredMixin, View):
    login_url = '/library/user_login/'

    def get(self,request,pk):
        user = User.objects.get(id=pk)
        userform = UserUpdateForm(instance=user)

        return render(request,'library/update.html',{'userform': userform,})

    def post(self,request,pk):
        user = User.objects.get(id=pk)
        userform = UserUpdateForm(request.POST, request.FILES, instance=user)

        if userform.is_valid():
            user1 = userform.save(commit=False)
            user1.save()
            messages.success(request,'User Updated Successfully')
            return redirect('library:user_update',pk=user1.id)
        else:
            return render(request,'library/signin.html',{'userform':userform})


class UserDelete(LoginRequiredMixin, View):
    login_url = '/library/user_login/'

    def get(self,request,pk):
        user = User.objects.get(id=pk)
        new_role = user.role.role
        user.delete()

        if new_role == 'Student':
            return redirect('library:student_list')
        elif new_role == 'Faculty':
            return redirect('library:faculty_list')
        else:
            return redirect('library:librarian_list')
        

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
            user = userform.save()
           
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

    def get(self, request, pk=None):
        book_form = BookForm()
        return render(request,'library/add_book.html',{
            'bookform': book_form,
        })
        
    def post(self, request):
        book_form = BookForm(request.POST, request.FILES)
        if book_form.is_valid():
            book = book_form.save(commit=False)
            # category = book_form.cleaned_data['category']
            # new_category = Category.objects.get(category=category)
            # book.category = new_category
            book.save()
            return redirect('library:book_detail', pk=book.id)
        else:
            return render(request, 'library/add_book.html',{'bookform': book_form})


class BookDetailView(LoginRequiredMixin,View):
    login_url = '/library/user_login/'
    def get(self, request, pk):
        book = Book.objects.get(id=pk)
        return render(request,'library/book_detail.html',{'book': book})


class BookUpdateView(LoginRequiredMixin, View):

    login_url = '/library/user_login/'
    
    def get(self, request, pk):
        book = Book.objects.get(id=pk)
        book_form = BookForm(instance=book)
        return render(request, 'library/book_update.html',{'bookform': book_form,'books':book})
    
    def post(self, request, pk):
        book = Book.objects.get(id=pk)
        book_form = BookForm(request.POST, request.FILES, instance=book)

        if book_form.is_valid():
            book = book_form.save(commit=False)
            book.save()
            return redirect('library:book_detail',pk=book.id)
        else:
            return render(request,'library/book_update.html',{'bookform':book_form})


class DeleteBookView(LoginRequiredMixin, View):
    login_url = '/library/user_login/'

    def get(self, request, pk):
        book = Book.objects.get(id=pk)
        book.delete()
        return redirect('library:book_list')


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


class CopyIncrmt(View):

    def post(self,request):
        pk = request.POST.get('id') 
        sign = request.POST.get('sign')       
        book = Book.objects.get(id=pk)

        if sign == 'plus':
            book.no_of_copy += 1
            book.available_copy += 1
        else:
            book.no_of_copy -= 1
            book.available_copy -= 1
        
        book.save()
        return JsonResponse({'status':1, 'book_copy':book.no_of_copy,'avail':book.available_copy})


    
