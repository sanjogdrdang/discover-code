from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("send_opt/", views.send_opt, name="send_opt"),
    path("validate_opt/", views.validate_opt, name="validate_opt"),
    path("gettingstarted", views.gettingstarted, name="gettingstarted"),
    path("healthgoal", views.healthgoal, name="healthgoal"),
    path("general1", views.general1, name="general1"),
    path("general2", views.general2, name="general2"),
    path("yourbmi", views.yourbmi, name="yourbmi"),
    path("personaldetails1", views.personaldetails1, name="personaldetails1"),
    path("personaldetails2", views.personaldetails2, name="personaldetails2"),
    path("lifestyle1", views.lifestyle1, name="lifestyle1"),
    path("lifestyle2", views.lifestyle2, name="lifestyle2"),
    path("subgoal", views.subgoal, name="subgoal"),
    path("question1", views.question1, name="question1"),
    path("question2", views.question2, name="question2"),
    path("result", views.result, name="result"),
    path("contactus", views.contactus, name="contactus"),
    path("sample", views.sample, name="sample"),
    path("problem1", views.problem1, name="problem1"),
    path("result", views.result, name="result"),
    path("sexualspecific1", views.sexualspecific1, name="sexualspecific1"),
    path("sexualspecific2", views.sexualspecific2, name="sexualspecific2"),
    path("sexualspecific3", views.sexualspecific3, name="sexualspecific3"),
    path("sexualspecific4", views.sexualspecific4, name="sexualspecific4"),
    path("sexualspecific5", views.sexualspecific5, name="sexualspecific5"),
    path("sexualspecific6", views.sexualspecific6, name="sexualspecific6"),
    path("sexualspecific7", views.sexualspecific7, name="sexualspecific7"),
    path("sexualspecific8", views.sexualspecific8, name="sexualspecific8"),
    path("sexualspecific9", views.sexualspecific9, name="sexualspecific9"),
    path("sexualspecific10", views.sexualspecific10, name="sexualspecific10"),
    path("specific1", views.specific1, name="specific1"),
    path("specific2", views.specific2, name="specific2"),
    path("specific3", views.specific3, name="specific3"),
    path("specific4", views.specific4, name="specific4"),
    path("specific5", views.specific5, name="specific5"),
    path("specific6", views.specific6, name="specific6"),
    path("specific7", views.specific7, name="specific7"),
    path("lifestyle", views.lifestyle, name="lifestyle"),
    path("lifestylefemale", views.lifestylefemale, name="lifestylefemale"),
    path("navbar", views.navbar, name="navbar"),
]

