from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views import generic
from django.http import HttpResponse, JsonResponse
from library.models import Student,Faculty,User,Librarian,Admin,Department,Role,Book,Category,BookRecord
from library.forms import StudentForm,UserForm,FacultyForm,LibrarianForm, LoginForm, BookForm, UserUpdateForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core import serializers
from dev_project.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
import smtplib
from django.db.models import Q
import datetime

# Create your views here.



class HomeView(LoginRequiredMixin,View):

    login_url = '/library/user_login/'

    def get(self, request):
        book = Book.objects.all()[::-1]

        page = request.GET.get('page',1)
        paginator = Paginator(book, 8)
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)

        return render(request,'library/home.html',{'books':books})


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
        # userform = StaffForm()
        userform = UserForm()
        librarianform = LibrarianForm()

        return render(request, 'library/librarian_signin.html',{
            'userform': userform,
            'librarianform': librarianform,
        })
    
    def post(self, request):

        # userform = StaffForm(request.POST, request.FILES)
        userform = UserForm(request.POST, request.FILES)
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
        user_books_issued = BookRecord.objects.filter(
            Q(user__username__iexact=user.username) &
            Q(return_date=None)
            )
        return render(request, 'library/user_profile.html',{'user':user,'user_books_issued':user_books_issued})


class UserLogin(View):

    def get(self, request):
        form = LoginForm()
        return render(request,'library/login.html',{'form':form})

    def post(self, request):
        form = LoginForm(request.POST)
        
        self.uname = request.POST.get('username')
        self.pasw = request.POST.get('password')
        self.user = authenticate(request, username=self.uname,password=self.pasw)
        # import pdb
        # pdb.set_trace()
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


class BookIssue(View):

    def post(self, request):
        user_pk = request.POST.get('user_id')
        book_pk = request.POST.get('book_id')
        user = User.objects.get(id=user_pk)
        book = Book.objects.get(id=book_pk)
        
        # getting all the records from BookRecord for requested book
        all_book_records = BookRecord.objects.filter(
            Q(book__title__iexact=book.title) &
            Q(return_date=None)
            )
        
        # check if current_user with requested Book is already in BookRecords or Not
        # or check if book title is occupied by any other user 
        for current_user in all_book_records: 
            if current_user.user.username == user.username and current_user.return_date == None:
                print('Book Already Issued')
                return JsonResponse({'status':0, 'msg':'Book Already Issued by You'}) 
        
        # getting all the user from BookRecord for current user
        all_user_records = BookRecord.objects.filter(
            Q(user__username__iexact=user.username) &
            Q(return_date=None)
            )
        # check if user has issued book more than 3 or not
        if all_user_records.count() > 2:
            print('Can NOt Issue Book More Than 3')
            return JsonResponse({'status':2,'msg':'You Can Not Issue Book More than 3'})
        
        record = BookRecord.objects.create(book=book,user=user)
        record.book_due_date()
        record.save()
        book.available_copy -= 1
        book.save()

        return JsonResponse({'status':1,'book':book.title,'user':user.username,'avail':book.available_copy})


class BookReturn(View):
    def post(self,request):
        title = request.POST.get('book')
        username = request.POST.get('user')
        book = Book.objects.get(title=title)
        # getting a particular record from BookRecord to set its return_date
        returned_book = BookRecord.objects.get(
            Q(book__title__iexact=title)&
            Q(return_date=None)&
            Q(user__username=username)
            )

        today = datetime.date.today()

        returned_book.return_date = today
        returned_book.save()
        book.available_copy += 1
        book.save()

        return JsonResponse({'book':title,'user':username})


class BookRecords(View):

    def get(self,request):
        books = BookRecord.objects.all()[::-1]
        print(len(books))
        return render(request,'library/book_records.html',{'books':books})


class AvailableBooks(View):

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        except_books = []
        
        issue_book_records = BookRecord.objects.filter(
            Q(user__username__iexact=user.username) &
            Q(return_date=None)
            )
        
        for book in issue_book_records:
            except_books.append(book) 

        avail_books = Book.objects.exclude(
            Q(title__in=except_books) |
            Q(available_copy__lte=0)
            )

        return render(request,'library/avail_books.html',{'avail_books':avail_books})


class RecordSearch(LoginRequiredMixin,View):
    login_url = '/library/user_login/'

    def get(self, request):
        title = request.GET.get('title')
        book_record = BookRecord.objects.filter(book__title__icontains=title)
        search_record = []

        for record in book_record:
            details = {
                'id':record.id,
                'book':record.book.title,
                'user':record.user.username,
                'isuue_date':record.issue_date,
                'due_date':record.due_date,
                'return_date':record.return_date
            }
            search_record.append(details)
        
        return JsonResponse({'records':search_record})


class Usernamevalid(View):

    # check for username already exist or not
    def post(self,request):
        username = request.POST.get('uname')
        data = {
            'taken': User.objects.filter(username__iexact=username).exists()
        }
        if data['taken']:
            return JsonResponse(data)


class SearchTitle(LoginRequiredMixin,View):
    login_url = '/library/user_login/'

    def get(self, request):
        title = request.GET.get('query')
        book = Book.objects.filter(title__icontains=title)
        print(book)
        return render(request,'library/search.html',{'books':book})