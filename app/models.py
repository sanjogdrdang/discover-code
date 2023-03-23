from django.db import models


class Bmi(models.Model):
    height=models.IntegerField()
    weight=models.IntegerField()



class OtpMobile(models.Model):
    phone_number=models.CharField(max_length=180)
    otp=models.CharField(max_length=180)
    verified=models.BooleanField(default=False)

class Contactus(models.Model):
    name=models.CharField(max_length=50)
    email=models. EmailField()
    number=models.IntegerField()

    def __str__(self):
        return self.name


class Patient(models.Model):
    patient_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=100, default="none")
    number=models.CharField(max_length=50)
    healthgoal=models.CharField(max_length=50, default="not chosen")
    gender=models.CharField(max_length=50, default="not specified")
    age=models.IntegerField(default=0)
    height=models.IntegerField(default=0)
    weight=models.IntegerField(default=0)
    bmi=models.IntegerField(default=0)
    bmi_result=models.CharField(max_length=50,default="Normal")
    diet_answer=models.CharField(max_length=50, default="none")
    workout_answer=models.CharField(max_length=50, default="none")
    smoking_answer=models.CharField(max_length=50, default="none")
    drinking_answer=models.CharField(max_length=50, default="none")
    history_question=models.CharField(max_length=200, default="none")
    history_answer=models.CharField(max_length=1000, default="none")
    historyfemale_question=models.CharField(max_length=200, default="none")
    historyfemale_answer=models.CharField(max_length=500, default="none")
    subgoal=models.CharField(max_length=50,default="none")
    question1=models.CharField(max_length=100,default="none")
    answer1=models.CharField(max_length=200,default="none")
    question2=models.CharField(max_length=100,default="none")
    answer2=models.CharField(max_length=400,default="none")
    specificquestion1=models.CharField(max_length=100,default="non")
    specificanswer1=models.CharField(max_length=200,default="non")
    specificquestion2=models.CharField(max_length=100,default="non")
    specificanswer2=models.CharField(max_length=100,default="non")
    specificquestion3=models.CharField(max_length=100,default="non")
    specificanswer3=models.CharField(max_length=100,default="non")
    specificquestion4=models.CharField(max_length=100,default="non")
    specificanswer4=models.CharField(max_length=100,default="non")
    specificquestion5=models.CharField(max_length=100,default="non")
    specificanswer5=models.CharField(max_length=100,default="non")
    specificquestion6=models.CharField(max_length=100,default="non")
    specificanswer6=models.CharField(max_length=100,default="non")
    specificquestion7=models.CharField(max_length=100,default="non")
    specificanswer7=models.CharField(max_length=100,default="non")
    specificquestion8=models.CharField(max_length=100,default="non")
    specificanswer8=models.CharField(max_length=100,default="non")
    specificquestion9=models.CharField(max_length=100,default="non")
    specificanswer9=models.CharField(max_length=100,default="non")
    specificquestion10=models.CharField(max_length=100,default="non")
    specificanswer10=models.CharField(max_length=100,default="non")
    tests=models.CharField(max_length=1000,default="none")
    testlink=models.CharField(max_length=1000,default="none")
    buttons_clear=models.CharField(max_length=100,default="none")
    healthgoal_clear=models.CharField(max_length=100,default="none")
    tests_clear=models.CharField(max_length=100,default="none")
    questions_clear=models.CharField(max_length=100,default="none")
    rating=models.CharField(max_length=100,default="none")
    comments=models.CharField(max_length=1000,default="none")
    contacted=models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Test(models.Model):
    test=models.CharField(max_length=50,default="")
    test_price=models.IntegerField(default=0)
    test_description=models.CharField(max_length=1000,default="non")
    test_reason=models.CharField(max_length=500,default="non")
    test_link=models.CharField(max_length=500,default="non")


    def __str__(self):
        return self.test

class HealthGoal(models.Model):
    healthgoal=models.CharField(max_length=50,default="")


    def __str__(self):
        return self.healthgoal

class Option(models.Model):
    option=models.CharField(max_length=50,default="")
    particulartest=models.CharField(max_length=50,default="")


    def __str__(self):
        return self.option

    
