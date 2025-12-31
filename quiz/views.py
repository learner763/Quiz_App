from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
# Create your views here.
def login_page(request):
    if request.method=='POST':
        context={}
        context['email']=request.POST.get('email')
        context['password']=request.POST.get('password')
        user=authenticate(username=request.POST['email'],password=request.POST['password'])
        if user is not None:
            if user.is_superuser:
                login(request,user)
                request.session['email']=request.POST['email']
                return render(request,'dashboard.html',{'email':request.session['email']})
            else:
                context['login_error']='You are not a super_user'
                return render(request,'login.html',context)
        else:
            context['login_error']='Invalid Credentials'
            return render(request,'login.html',context)
    return render(request,'login.html')
def dashboard(request):
    return render(request,'dashboard.html')
def parent_dashboard(request):
    return render(request,'parent_dashboard.html')
def student(request):
    return render(request,'student.html')
def index(request):
    return redirect('parent_dashboard')
def student_dashboard(request):
    if request.method=='POST':
        print(request.POST)
        request.session['course']=request.POST['course']
        return redirect('student_subjects')
    course=Courses.objects.all()
    print(course)
    return render(request,'student_dashboard.html',{'courses':course,'email':request.session.get('email')})
def student_subjects(request):
    if request.method=='POST':
        print(request.POST)
        request.session['subject']=request.POST['subject']
        return redirect('student_exam')
    course=Courses.objects.get(id=request.session['course'])
    subject=Subjects.objects.filter(courses_id=course)
    return render(request,'student_subjects.html',{'subjects':subject})
def student_exam(request):
    if request.method=='POST':
        correct=request.POST.getlist('correct')
        answer=request.POST.getlist('answer')
        score=0
        for i in range(len(answer)):
            if answer[i]==correct[i]:
                score+=5
        student=Students.objects.get(email=request.session.get('email'))
        course=Courses.objects.get(id=request.session['course'])
        subject=Subjects.objects.get(id=request.session['subject'])

        result=Scores.objects.create(score=f"{score}/{len(correct)*5}",
                                    student=student,courses=course,
                                    subjects=subject)
        return render(request,'student_exam.html',{'score':f"{score}/{len(correct)*5}"})
    course=Courses.objects.get(id=request.session['course'])
    subject=Subjects.objects.get(id=request.session['subject'])
    question=Question.objects.filter(subjects_id=subject)
    return render(request,'student_exam.html',{'questions':question,'courses':course,'subjects':subject})
def student_login(request):
    if request.method=='POST':
        context={}
        context['email']=request.POST.get('email')
        context['password']=request.POST.get('password')
        try:
            student=Students.objects.get(email=request.POST['email'])
            if check_password(request.POST['password'],student.password):
                request.session['email']=request.POST.get('email')
                request.session['email']=request.POST.get('email')

                print(request.session['email'])
                return render(request,'student.html',{'email':request.session['email']})
            else:
                context['login_error']='Invalid Credentials'
                return render(request,'student_login.html',context)
        except Students.DoesNotExist:
            context['login_error']='Invalid Credentials'
            return render(request,'student_login.html',context)
        
    return render(request,'student_login.html')

def student_signup(request):
    if request.method=='POST':
        print(request.POST)
        context={}
        context['email']=request.POST['email']
        context['password']=request.POST['password']
        context['confirmpassword']=request.POST['confirmpassword']
        context['firstname']=request.POST['firstname']
        context['lastname']=request.POST['lastname']
        context['phone']=request.POST['phone']
        # print(request.FILES['image'])
        try:
            validate_email(request.POST['email'])
        except ValidationError:
            context['signup_error']='Invalid Email'
            return render(request,'student_signup.html',context)
        if request.POST['password']!=request.POST['confirmpassword']:
            context['password_error']='Passwords should match!'
            return render(request,'student_signup.html',context)
        elif len(list(Students.objects.filter(email=request.POST['email'])))>0:
            context['signup_error']='Email already choosen!'
            return render(request,'student_signup.html',context)

        else:
            student=Students(email=request.POST['email'],password=make_password( request.POST['password']),firstname=request.POST['firstname'],lastname=request.POST['lastname'],phone=request.POST['phone'])
            student.save()
            request.session['email']=request.POST['email']
            request.session['password']=request.POST['password']
            return redirect('student_login')

    return render(request,'student_signup.html')
def view_results(request):
    score=Scores.objects.all()
    score=list(score.values())
    for i in range(len(score)):
        student=Students.objects.get(id=score[i]['student_id'])
        course=Courses.objects.get(id=score[i]['courses_id'])
        subject=Subjects.objects.get(id=score[i]['subjects_id'])
        score[i]['student_email']=student.email
        score[i]['course_name']=course.course_name
        score[i]['subject_name']=subject.subject_name
    return render(request,'view_results.html',{'scores':score})
def view_courses(request):
    if request.method=='POST':
        if 'edit' in request.POST:
            print(request.POST.get('edit'))
            request.session['edit']=request.POST.get('edit')
            return redirect('edit_course')
        else:
            course=Courses.objects.get(id=request.POST.get('delete'))
            course.delete()
            return redirect('view_courses')

    try:
        print(9)
        print(request.session.get('email'))
        teacher=Teacher.objects.get(email=request.session.get('email'))
        print(teacher)
        courses=Courses.objects.filter(teacher=teacher)
        return render(request,'view_courses.html',{'courses':courses})
    except Teacher.DoesNotExist:
        return redirect('admin_login')
def edit_course(request):
    if request.method=='POST':
        course=Courses.objects.get(id=request.session.get('edit'))
        course.course_name=request.POST.get('course_name')
        course.course_code=request.POST.get('course_code')
        course.domain=request.POST.get('domain')
        course.save()
        return redirect('view_courses')
    course=Courses.objects.get(id=request.session.get('edit'))
    return render(request,'edit_course.html',{'course':course})
def edit_subject(request):
    if request.method=='POST':
        subject=Subjects.objects.get(id=request.session.get('edit'))
        subject.subject_name=request.POST.get('subject_name')
        subject.subject_code=request.POST.get('subject_code')
        subject.credit_hours=request.POST.get('credit_hours')
        subject.save()
        return redirect('view_subjects')
    subject=Subjects.objects.get(id=request.session.get('edit'))
    course=Courses.objects.get(id=request.session.get('course'))
    print(subject)
    print(course)
    return render(request,'edit_subject.html',{'subject':subject,'course':course})
def edit_subject(request):
    if request.method=='POST':
        subject=Subjects.objects.get(id=request.session.get('edit'))
        subject.subject_name=request.POST.get('subject_name')
        subject.subject_code=request.POST.get('subject_code')
        subject.credit_hours=request.POST.get('credit_hours')
        subject.save()
        return redirect('view_subjects')
    subject=Subjects.objects.get(id=request.session.get('edit'))
    course=Courses.objects.get(id=request.session.get('course'))
    print(subject)
    print(course)
    return render(request,'edit_subject.html',{'subject':subject,'course':course})
def edit_question(request):
    if request.method=='POST':
        question=Question.objects.get(id=request.session.get('edit'))
        question.statement=request.POST.get('statement')
        question.option_1=request.POST.get('option_1')
        question.option_2=request.POST.get('option_2')
        question.option_3=request.POST.get('option_3')
        question.option_4=request.POST.get('option_4')
        question.correct=request.POST.get('correct')
        question.save()
        return redirect('view_questions')
    question=Question.objects.get(id=request.session.get('edit'))
    course=Courses.objects.get(id=request.session.get('course'))
    subject=Subjects.objects.get(id=request.session.get('subject'))
    return render(request,'edit_question.html',{'subjects':subject,'courses':course,'question':question})
def view_subjects(request):
    if request.method=='POST':
        if 'edit' in request.POST:
            print(request.POST.get('edit'))
            request.session['edit']=request.POST.get('edit')
            print(request.POST.get('course'))
            request.session['course']=request.POST.get('course')
            return redirect('edit_subject')
        else:
            subject=Subjects.objects.get(id=request.POST.get('delete'))
            subject.delete()
            return redirect('view_subjects')

    teacher=Teacher.objects.get(email=request.session.get('email'))
    course=Courses.objects.filter(teacher=teacher)
    subject=Subjects.objects.filter(courses__in=course)
    print(f"{list(subject.values())}")
    print(f"{list(course.values())}")
    return render(request,'view_subjects.html',{'subjects':subject,'courses':course})
def view_questions(request):
    if request.method=='POST':
        if 'edit' in request.POST:
            request.session['edit']=request.POST.get('edit')
            request.session['course']=request.POST.get('course')
            request.session['subject']=request.POST.get('subject')
            return redirect('edit_question')
        elif 'delete' in request.POST:
            question=Question.objects.get(id=request.POST.get('delete'))
            question.delete()
            return redirect('view_questions')
        else:
            request.session['course']=request.POST.get('course')
            request.session['subject']=request.POST.get('subject')
            return redirect('add_question')

    teacher=Teacher.objects.get(email=request.session.get('email'))
    course=Courses.objects.filter(teacher=teacher)
    subject=Subjects.objects.filter(courses__in=course)
    question=Question.objects.filter(subjects__in=subject)
    print(question)
    return render(request,'view_questions.html',{'courses':course,'subjects':subject,'questions':question})

def add_course(request):
    if request.method=='POST':
        try:
            teacher=Teacher.objects.get(email=request.POST.get('email'))
            course=Courses.objects.create(course_name=request.POST.get('course_name'),course_code=request.POST.get('course_code'),domain=request.POST.get('domain'),teacher=teacher)
            return redirect('view_courses')
        except Teacher.DoesNotExist:
            return redirect('admin_login')
    return render(request,'add_course.html')
def add_subject(request):
    if request.method=='POST':
        teacher=Teacher.objects.get(email=request.POST.get('email'))
        course=Courses.objects.get(id=request.POST.get('available_courses'))
        subject=Subjects.objects.create(subject_name=request.POST.get('subject_name'),subject_code=request.POST.get('subject_code'),credit_hours=request.POST.get('credit_hours'),courses=course,teacher=teacher)
        return redirect('view_subjects')
    teacher=Teacher.objects.get(email=request.session.get('email'))
    course=Courses.objects.filter(teacher=teacher)
    return render(request,'add_subject.html',{'courses':course})
def add_question(request):    
    if request.method=='POST':  
        print(request.POST['correct'])
        teacher=Teacher.objects.get(email=request.POST['email'])
        course=Courses.objects.get(id=request.session['course'])
        subject=Subjects.objects.get(id=request.session['subject'])
        question=Question.objects.create(statement=request.POST['statement'],
                                        option_1=request.POST['option_1'],
                                        option_2=request.POST['option_2'],
                                        option_3=request.POST['option_3'],
                                        option_4=request.POST['option_4'],
                                        teacher=teacher,courses=course,subjects=subject,
                                        correct=request.POST['correct'])
        return redirect('view_questions')
    course=Courses.objects.get(id=request.session.get('course'))
    subject=Subjects.objects.get(id=request.session.get('subject'))
    return render(request,'add_question.html',{'subjects':subject,'courses':course})