from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('signin/',views.Signin.as_view(),name='signin'),
    path('user_login/',views.UserLogin.as_view(), name='user_login'),
    path('profile/<str:pk>/',views.UserProfile.as_view(),name='profile'),

    path('add_librarian/',views.AddLibrarian.as_view(),name='add_librarian'),
    path('user_update/<str:pk>/',views.UserUpdate.as_view(),name='user_update'),
    path('user_delete/<str:pk>/',views.UserDelete.as_view(),name='user_delete'),
    path("user_logout/",views.UserLogout.as_view(), name='user_logout'),
    path("send_mail/",views.send_email, name='send_mail'),
    path('add_book/',views.AddBookView.as_view(), name='add_book'),
    path('book_detail/<str:pk>/',views.BookDetailView.as_view(),name='book_detail'),
    path('book_update/<str:pk>/',views.BookUpdateView.as_view(),name='book_update'),
    path('book_delete/<str:pk>/', views.DeleteBookView.as_view(), name='book_delete'),
    path('admin_dashboard/',views.AdminDashBoard.as_view(), name='admin_dashboard'),
    path('student_list/',views.StudentList.as_view(), name='student_list'),
    path('facutly_list/',views.FacultyList.as_view(), name='faculty_list'),
    path('librarian_list/',views.LibrarianList.as_view(), name='librarian_list'),
    path('book_list/',views.BookList.as_view(), name='book_list'),
    path('book_issue/',views.BookIssue.as_view(), name='book_issue'),
    path('book_return/',views.BookReturn.as_view(), name='book_return'),
    path('book_record/',views.BookRecords.as_view(), name='book_record'),
    path('avail_books/<str:pk>',views.AvailableBooks.as_view(), name='avail_books'),











]