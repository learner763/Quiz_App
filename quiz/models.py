from django.db import models

# Create your models here.
class Teacher(models.Model):
    email=models.EmailField()
    password=models.CharField(max_length=15)
    def __str__(self):
        return self.email
class Courses(models.Model):
    course_name=models.CharField(max_length=15,default='')
    course_code=models.CharField(max_length=15,default='')
    domain=models.CharField(max_length=15,default='')

    teacher=models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    def __str__(self):
        return self.course_name
class Subjects(models.Model):
    subject_name=models.CharField(max_length=15,default='')
    subject_code=models.CharField(max_length=15,default='')
    credit_hours=models.CharField(default='0',max_length=1)

    teacher=models.ForeignKey(
    Teacher,
    on_delete=models.CASCADE,
    related_name='subjects'
)
    courses=models.ForeignKey(
        Courses,
        on_delete=models.CASCADE,
        related_name='subjects'
    )
    
    def __str__(self):
        return self.subject_name
class Question(models.Model):
    statement=models.CharField(max_length=100)
    teacher=models.ForeignKey(
    Teacher,
    on_delete=models.CASCADE,
    related_name='question'
)
    courses=models.ForeignKey(
        Courses,
        on_delete=models.CASCADE,
        related_name='question'
    )
    subjects=models.ForeignKey(
        Subjects,
        on_delete=models.CASCADE,
        related_name='question'
    )
    option_1=models.CharField(default='',max_length=20)
    option_2=models.CharField(default='',max_length=20)
    option_3=models.CharField(default='',max_length=20)
    option_4=models.CharField(default='',max_length=20)
    correct=models.CharField(default='0',max_length=1)
    def __str__(self):
        return self.statement
    
class Students(models.Model):
    email=models.EmailField()
    password=models.CharField(max_length=128)
    firstname=models.CharField(max_length=15)
    lastname=models.CharField(max_length=15)
    phone=models.CharField(max_length=11)
    # image=models.CharField(max_length=100)
    def __str__(self):
        return self.email
class Scores(models.Model):
    score=models.CharField(max_length=15)
    student=models.ForeignKey(
        Students,
        on_delete=models.CASCADE,
        related_name='scores'
    )
    courses=models.ForeignKey(
        Courses,
        on_delete=models.CASCADE,
        related_name='scores'
    )  
    subjects=models.ForeignKey(
        Subjects,
        on_delete=models.CASCADE,
        related_name='scores'
    )   
    def __str__(self):
        return self.score
