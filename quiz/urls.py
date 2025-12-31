from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin_login', views.login_page, name='login'),
    path('student_login', views.student_login, name='student_login'),
    path('student_signup', views.student_signup, name='student_signup'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('parent_dashboard', views.parent_dashboard, name='parent_dashboard'),
    path('student_dashboard', views.student_dashboard, name='student_dashboard'),
    path('student_subjects', views.student_subjects, name='student_subjects'),
    path('student_exam', views.student_exam, name='student_exam'),
    path('view_results', views.view_results, name='view_results'),
    path('view_courses', views.view_courses, name='view_courses'),
    path('view_subjects', views.view_subjects, name='view_subjects'),
    path('view_questions', views.view_questions, name='view_questions'),
    path('add_course', views.add_course, name='add_course'),
    path('add_subject', views.add_subject, name='add_subject'),
    path('add_question', views.add_question, name='add_question'),
    path('edit_course', views.edit_course, name='edit_course'),
    path('edit_subject', views.edit_subject, name='edit_subject'),
    path('edit_question', views.edit_question, name='edit_question')


]
