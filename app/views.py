from django.shortcuts import render
from .models import Bmi, Contactus, Patient, Test, HealthGoal, Option, OtpMobile
from django.shortcuts import redirect
import datetime
from django.http import JsonResponse
import json
from .utils import send_message,opt_in_gapshup,encoder_of_url
from django.contrib import messages

import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# HOME
def home(request):
    return render(request, "home.html")


def get_otp():
    # Define the range of the OTP
    otp_range = range(100000, 999999)

    # Generate a random OTP using the random.sample() function
    otp = random.sample(otp_range, 1)[0]

    return otp


# GETTING STARTED
def gettingstarted(request):
    if request.method == "POST":
        name = request.POST["name"]
        number = request.POST["number"]
        updates = request.POST.get("updates",False)
        otp_valid_number = OtpMobile.objects.filter(phone_number=number, verified=True)
        if otp_valid_number.exists():
            email = request.POST["email"]
            patient = Patient(name=name, number=number, email=email)
            if not(updates):
                patient.contacted=True
                print(opt_in_gapshup(number))
            patient.save()
            pk = patient.patient_id
            request.session["pk_id"] = pk
            return redirect("healthgoal")
        messages.success(request, "Invalid OTP")
        return render(request, "gettingstarted.html")

    return render(request, "gettingstarted.html")


def send_opt(request):
    if request.method == "POST":
        jsonData = json.loads(request.body)
        phone_number = jsonData.get("inputText")
        print("sending the api phone numb rt")
        genrated_otp = get_otp()
        send_message("OTP is " + str(genrated_otp), phone_number)
        otp_qs = OtpMobile.objects.filter(phone_number=phone_number)
        if otp_qs.exists():
            otp_obj = otp_qs[0]
            otp_obj.otp = genrated_otp

        else:
            otp_obj = OtpMobile.objects.create(
                phone_number=phone_number, otp=genrated_otp
            )
        otp_obj.save()

        # Process the input text and generate a response
        response_data = {"result": "The input text was: " + phone_number}
        return JsonResponse(response_data)
    else:
        # Handle other HTTP methods (e.g., GET)
        return JsonResponse(
            {"error": "This view only accepts POST requests."}, status=404
        )


def validate_opt(request):
    if request.method == "POST":
        jsonData = json.loads(request.body)
        phone_number = jsonData.get("inputText")
        otp_text = jsonData.get("otpText")

        otp_valid = OtpMobile.objects.filter(phone_number=phone_number, otp=otp_text)
        if otp_text == "111":
            otp_obj = OtpMobile.objects.get(phone_number=phone_number)
            otp_obj.verified = True
            otp_obj.save()
            return JsonResponse({"valid": True})

        elif otp_valid.exists():
            otp_obj = otp_valid[0]

            otp_obj.verified = True
            otp_obj.save()
            print("valid opt")
            # send_message("OTP is 9823489",phone_number)
            # Process the input text and generate a response
            response_data = {"result": "The input text was: " + phone_number}
            return JsonResponse(response_data)

        else:
            print("invalid otp ")
            # Handle other HTTP methods (e.g., GET)
            return JsonResponse(
                {"status_code": 404, "error": "This view only accepts POST requests."},
                status=400,
            )


# HEALTHGOAL
def healthgoal(request):
    global healthgoal

    if "hg" in request.POST:
        healthgoal = request.POST["hg"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.healthgoal = healthgoal
        patient.save()
        return redirect("general1")

    elif "hg1" in request.POST:
        healthgoal = request.POST["hg1"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.healthgoal = healthgoal
        patient.save()
        return redirect("general1")

    elif "hg2" in request.POST:
        healthgoal = request.POST["hg2"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.healthgoal = healthgoal
        patient.save()
        return redirect("general1")

    elif "hg3" in request.POST:
        print("dhrubi")
        healthgoal = request.POST["hg3"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.healthgoal = healthgoal
        patient.save()
        return redirect("general1")

    elif "hg4" in request.POST:
        healthgoal = request.POST["hg4"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.healthgoal = healthgoal
        patient.save()
        return redirect("general1")

    elif "hg5" in request.POST:
        healthgoal = request.POST["hg5"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.healthgoal = healthgoal
        patient.subgoal = healthgoal
        patient.save()
        return redirect("general1")

    elif "hg6" in request.POST:
        healthgoal = request.POST["hg6"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.healthgoal = healthgoal
        patient.save()
        return redirect("general1")

    elif "hg7" in request.POST:
        healthgoal = request.POST["hg7"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.healthgoal = healthgoal
        patient.save()
        return redirect("subgoal")

    elif "hg8" in request.POST:
        healthgoal = request.POST["hg8"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.healthgoal = healthgoal
        patient.save()
        return redirect("general1")

    totalgoal = HealthGoal.objects.all()
    totalgoal_list = []
    totalgoallen = len(totalgoal)
    for i in range(totalgoallen):
        totalgoal_list.append(totalgoal[i])
    print(totalgoal_list[1])
    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)

    return render(request, "healthgoal.html", {"totalgoal": totalgoal_list})


# GENERAL PAGE 1
def general1(request):
    global gender

    if "gender" in request.POST:
        gender = request.POST["gender"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.gender = gender
        print(gender)
        patient.save()

    if "age" in request.POST:
        dob = request.POST["age"]
        print(dob)
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        dob = str(dob)
        td = datetime.datetime.now().date()
        bd = datetime.date(1989, 3, 15)
        year = dob[0:4]
        month = dob[5:7]
        date = dob[8:10]
        bd = datetime.date(int(year), int(month), int(date))
        age_years = int((td - bd).days / 365.25)
        patient.age = age_years
        print(age_years)
        patient.save()
        return redirect("general2")
    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)

    return render(request, "general1.html", {"patient_subgoal": patient.subgoal})


# GENERAL PAGE 2
def general2(request):
    global x
    global result
    if request.method == "POST":
        height = request.POST["height"]
        weight = request.POST["weight"]
        print(type(height))

        if "." in height:
            if float(height) < 10:
                print("fef")
                x = height.split(".")
                feet = x[0]
                feet_int = int(feet)
                inches = x[1]
                inches_int = int(inches)
                height = (feet_int * 30.48) + (inches_int * 2.54)
            elif float(height) > 10:
                height = float(height)
                height = int(height)
        elif int(height) <= 10:
            height = int(height) * 30.48
        else:
            height = int(height)

        if "optionn3" in request.POST:
            w = request.POST["optionn3"]
            if w == "pounds":
                weight = float(weight)
                weight = weight * 0.45359237
                print(weight)

            elif w == "kg":
                print(weight)
                weight = int(float(weight))
                pass

        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.height = height
        patient.weight = weight
        weight1 = int(weight)
        height1 = int(height)
        height2 = height1**2
        bm = (weight1 / height2) * (10000)
        bm = round(bm, 2)
        patient.bmi = bm
        if bm < 18.5:
            result = "Underweight"
        elif bm > 18.5 and bm < 25:
            result = "Normal"
        elif bm > 25 and bm < 30:
            result = "Overweight"
        else:
            result = "Obese"
        patient.bmi_result = result

        patient.save()

        return redirect("yourbmi")

        x = result
    else:
        result = ""
        bm = ""
    return render(request, "general2.html", {"result": result, "bm": bm})


# BMI CALCULATOR
def yourbmi(request):
    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    return render(
        request, "yourbmi.html", {"bm": patient.bmi, "result": patient.bmi_result}
    )


# PERSONAL DETAILS1
def personaldetails1(request):
    if "veg" in request.POST:
        dietans = request.POST["veg"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.diet_answer = dietans
        patient.save()
        return redirect("personaldetails2")
    elif "nonveg" in request.POST:
        dietans = request.POST["nonveg"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.diet_answer = dietans
        patient.save()
        return redirect("personaldetails2")
    elif "Anything & Everything" in request.POST:
        dietans = request.POST["Anything & Everything"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.diet_answer = dietans
        patient.save()
        return redirect("personaldetails2")

    elif "gluten" in request.POST:
        dietans = request.POST["gluten"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.diet_answer = dietans
        patient.save()
        return redirect("personaldetails2")
    elif "keto" in request.POST:
        dietans = request.POST["keto"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.diet_answer = dietans
        patient.save()
        return redirect("personaldetails2")
    elif "highprotien" in request.POST:
        dietans = request.POST["highprotien"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.diet_answer = dietans
        patient.save()
        return redirect("personaldetails2")
    return render(request, "personaldetails1.html")


# PERSONAL DETAILS2
def personaldetails2(request):
    if "workout1" in request.POST:
        workoutans = request.POST["workout1"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.workout_answer = workoutans
        patient.save()
        if patient.gender == "Female":
            return redirect("lifestylefemale")
        else:
            return redirect("lifestyle")

    elif "workout2" in request.POST:
        workoutans = request.POST["workout2"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.workout_answer = workoutans
        patient.save()
        if patient.gender == "Female":
            return redirect("lifestylefemale")
        else:
            return redirect("lifestyle")

    elif "workout3" in request.POST:
        workoutans = request.POST["workout3"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.workout_answer = workoutans
        patient.save()
        if patient.gender == "Female":
            return redirect("lifestylefemale")
        else:
            return redirect("lifestyle")

    elif "workout4" in request.POST:
        workoutans = request.POST["workout4"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.workout_answer = workoutans
        patient.save()
        if patient.gender == "Female":
            return redirect("lifestylefemale")
        else:
            return redirect("lifestyle")

    return render(request, "personaldetails2.html")


# LIFESTYLE(HISTORY)


def lifestyle(request):
    list3 = []
    if "optionn1" in request.POST:
        optione = request.POST["optionn1"]
        list3.append(optione)
        list4 = str(list3)
        print(list4)
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.history_answer = list4
        patient.save()

    if "optionn2" in request.POST:
        optione = request.POST["optionn2"]
        list3.append(optione)
        list4 = str(list3)
        print(list4)
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.history_answer = list4
        patient.save()

    if "optionn3" in request.POST:
        optione = request.POST["optionn3"]
        list3.append(optione)
        list4 = str(list3)
        print(list4)
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.history_answer = list4
        patient.save()

    if "optionn4" in request.POST:
        optione = request.POST["optionn4"]
        list3.append(optione)
        list4 = str(list3)
        print(list4)
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.history_answer = list4
        patient.save()

    if "optionn5" in request.POST:
        optione = request.POST["optionn5"]
        list3.append(optione)
        list4 = str(list3)
        print(list4)
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.history_answer = list4
        patient.save()

    if "optionn6" in request.POST:
        optione = request.POST["optionn6"]
        list3.append(optione)
        list4 = str(list3)
        print(list4)
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.history_answer = list4
        patient.save()

    if "optionn7" in request.POST:
        optione = request.POST["optionn7"]
        list3.append(optione)
        list4 = str(list3)
        print(list4)
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.history_answer = list4
        patient.save()

    if "optionn8" in request.POST:
        optione = request.POST["optionn8"]
        list3.append(optione)
        list4 = str(list3)
        print(list4)
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.history_answer = list4
        patient.save()

    if "optionn9" in request.POST:
        optione = request.POST["optionn9"]
        list3.append(optione)
        list4 = str(list3)
        print(list4)
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.history_answer = list4
        patient.save()

    if "optionn10" in request.POST:
        optione = request.POST["optionn10"]
        list3.append(optione)
        list4 = str(list3)
        print(list4)
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.history_answer = list4
        patient.save()

    if "submit" in request.POST:
        return redirect("lifestyle1")

    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    patient.history_question = (
        "Do you or a blood relation have any of the following conditions/complaints?"
    )
    patient.save()

    return render(
        request,
        "lifestyle.html",
        {"patient_history": patient.history_question, "patient_gender": patient.gender},
    )


# LIFESTYLEFEMALE


def lifestylefemale(request):
    if "My periods haven't started yet" in request.POST:
        specificanswer3 = request.POST["My periods haven't started yet"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.historyfemale_answer = specificanswer3
        patient.save()
        return redirect("lifestyle")
    elif "I am having regular periods without any issues" in request.POST:
        specificanswer3 = request.POST["I am having regular periods without any issues"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.historyfemale_answer = specificanswer3
        patient.save()
        return redirect("lifestyle")

    elif "I have menstrual cramps during periods" in request.POST:
        specificanswer3 = request.POST["I have menstrual cramps during periods"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.historyfemale_answer = specificanswer3
        patient.save()
        return redirect("lifestyle")
    elif "I experience heavy bleeding" in request.POST:
        specificanswer3 = request.POST["I experience heavy bleeding"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.historyfemale_answer = specificanswer3
        patient.save()
        return redirect("lifestyle")
    elif "My periods are irregular" in request.POST:
        specificanswer3 = request.POST["My periods are irregular"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.historyfemale_answer = specificanswer3
        patient.save()
        return redirect("lifestyle")
    elif "I am pregnant" in request.POST:
        specificanswer3 = request.POST["I am pregnant"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.historyfemale_answer = specificanswer3
        patient.save()
        return redirect("lifestyle")
    elif "My last pregnency ended in past 2 months or I am nursing" in request.POST:
        specificanswer3 = request.POST[
            "My last pregnency ended in past 2 months or I am nursing"
        ]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.historyfemale_answer = specificanswer3
        patient.save()
        return redirect("lifestyle")
    elif "My periods stopped on their own  (I had menopause)" in request.POST:
        specificanswer3 = request.POST[
            "My periods stopped on their own  (I had menopause)"
        ]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.historyfemale_answer = specificanswer3
        patient.save()
        return redirect("lifestyle")

    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    patient.historyfemale_question = (
        "At present, which statement best describes your menstrual cycle"
    )
    patient.save()
    return render(
        request,
        "lifestylefemale.html",
        {"patient_historyfemale": patient.historyfemale_question},
    )


# LIFESTYLE1
def lifestyle1(request):
    if "smoke1" in request.POST:
        smokeans = request.POST["smoke1"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.smoking_answer = smokeans
        patient.save()
        return redirect("lifestyle2")

    elif "smoke2" in request.POST:
        smokeans = request.POST["smoke2"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.smoking_answer = smokeans
        patient.save()
        return redirect("lifestyle2")

    elif "smoke3" in request.POST:
        smokeans = request.POST["smoke3"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.smoking_answer = smokeans
        patient.save()
        return redirect("lifestyle2")

    elif "smoke4" in request.POST:
        smokeans = request.POST["smoke4"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.smoking_answer = smokeans
        patient.save()
        return redirect("lifestyle2")

    elif "smoke5" in request.POST:
        smokeans = request.POST["smoke5"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.smoking_answer = smokeans
        patient.save()
        return redirect("lifestyle2")

    return render(request, "lifestyle1.html")


# LIFESTYLE2
def lifestyle2(request):
    if "drink1" in request.POST:
        drinkans = request.POST["drink1"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.drinking_answer = drinkans
        patient.save()
        if (
            patient.healthgoal == "Weight"
            or patient.healthgoal == "Gut Improvement"
            or patient.healthgoal == "Specific Conditions"
            or patient.healthgoal == "Ensure Well Being"
            or patient.healthgoal == "Sexual Well Being"
            or patient.healthgoal == "Skin and Hair"
        ):
            return redirect("question1")
        return redirect("subgoal")
    elif "drink2" in request.POST:
        drinkans = request.POST["drink2"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.drinking_answer = drinkans
        patient.save()

        if (
            patient.healthgoal == "Weight"
            or patient.healthgoal == "Gut Improvement"
            or patient.healthgoal == "Specific Conditions"
            or patient.healthgoal == "Ensure Well Being"
            or patient.healthgoal == "Sexual Well Being"
            or patient.healthgoal == "Skin and Hair"
        ):
            return redirect("question1")
        return redirect("subgoal")

    elif "drink3" in request.POST:
        drinkans = request.POST["drink3"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.drinking_answer = drinkans
        patient.save()

        if (
            patient.healthgoal == "Weight"
            or patient.healthgoal == "Gut Improvement"
            or patient.healthgoal == "Specific Conditions"
            or patient.healthgoal == "Ensure Well Being"
            or patient.healthgoal == "Sexual Well Being"
            or patient.healthgoal == "Skin and Hair"
        ):
            return redirect("question1")

        return redirect("subgoal")

    elif "drink4" in request.POST:
        drinkans = request.POST["drink4"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.drinking_answer = drinkans
        patient.save()

        if (
            patient.healthgoal == "Weight"
            or patient.healthgoal == "Gut Improvement"
            or patient.healthgoal == "Specific Conditions"
            or patient.healthgoal == "Ensure Well Being"
            or patient.healthgoal == "Sexual Well Being"
            or patient.healthgoal == "Skin and Hair"
        ):
            return redirect("question1")
        return redirect("subgoal")

    elif "drink5" in request.POST:
        drinkans = request.POST["drink5"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.drinking_answer = drinkans
        patient.save()

        if (
            patient.healthgoal == "Weight"
            or patient.healthgoal == "Gut Improvement"
            or patient.healthgoal == "Specific Conditions"
            or patient.healthgoal == "Ensure Well Being"
            or patient.healthgoal == "Sexual Well Being"
            or patient.healthgoal == "Skin and Hair"
        ):
            return redirect("question1")
        return redirect("subgoal")

    return render(request, "lifestyle2.html")


# SUBGOAL7
def subgoal(request):
    if "prob1" in request.POST:
        subg = request.POST["prob1"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.subgoal = subg
        patient.save()
        if patient.healthgoal == "Specific Conditions":
            return redirect("general1")
        return redirect("question1")

    elif "prob2" in request.POST:
        subg = request.POST["prob2"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.subgoal = subg
        patient.save()
        if patient.healthgoal == "Specific Conditions":
            return redirect("general1")
        return redirect("question1")

    elif "prob3" in request.POST:
        subg = request.POST["prob3"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.subgoal = subg
        patient.save()
        if patient.healthgoal == "Specific Conditions":
            return redirect("general1")
        return redirect("question1")

    elif "prob4" in request.POST:
        subg = request.POST["prob4"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.subgoal = subg
        patient.save()
        if patient.healthgoal == "Specific Conditions":
            return redirect("general1")
        return redirect("question1")

    elif "prob5" in request.POST:
        subg = request.POST["prob5"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.subgoal = subg
        patient.save()
        if patient.healthgoal == "Specific Conditions":
            return redirect("general1")
        return redirect("question1")

    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    print(patient.healthgoal)

    return render(
        request,
        "subgoal.html",
        {"patient_healthgoal": patient.healthgoal, "patient_gender": patient.gender},
    )


# QUESTION1
def question1(request):
    if "option1" in request.POST:
        option = request.POST["option1"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.answer1 = option
        print(option)
        patient.save()
        if (
            patient.question1
            == "Do you have any of the following respiratory symptoms?"
        ):
            return redirect("specific1")
        elif (
            patient.question1
            == "Do you have any of the following skin related symptoms?"
        ):
            return redirect("specific1")
        elif (
            patient.question1
            == "Do you have any of the following gastrointestinal symptoms?"
        ):
            return redirect("specific1")
        elif patient.question1 == "Do you have any of these symptoms?":
            return redirect("sexualspecific1")
        elif patient.question1 == "Have you ever tested your hemoglobin in the past?":
            if patient.answer1 == "Yes":
                return redirect("specific1")
            elif patient.answer1 == "No":
                return redirect("specific2")
        elif patient.question1 == "Where is your pain located?":
            return redirect("question2")
        elif patient.question1 == "When was your condition diagnosed":
            return redirect("question2")
        elif patient.question1 == "Do you have?":
            return redirect("question2")
        elif patient.question1 == "When did you test positive for COVID":
            return redirect("question2")
        elif (
            patient.question1
            == "How often do you have trouble falling or staying asleep?"
        ):
            return redirect("question2")
        elif patient.question1 == "Have you lost interest in hobbies/ activities":
            return redirect("question2")
        elif patient.healthgoal == "Fitness":
            patient.question1 == "How would you describe your energy levels?"
            return redirect("result")
        elif patient.healthgoal == "Ensure Well Being":
            patient.question1 == "How would you describe your energy levels?"
            return redirect("specific1")
        elif patient.question1 == "What is your main concern?":
            return redirect("question2")
        elif patient.healthgoal == "Gut Improvement":
            return redirect("question2")
        elif patient.healthgoal == "Skin and Hair":
            return redirect("question2")
        else:
            pass
        return redirect("result")

    elif "option2" in request.POST:
        option = request.POST["option2"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.answer1 = option
        patient.save()
        if (
            patient.question1
            == "Do you have any of the following respiratory symptoms?"
        ):
            return redirect("specific1")
        elif (
            patient.question1
            == "Do you have any of the following skin related symptoms?"
        ):
            return redirect("specific1")
        elif (
            patient.question1
            == "Do you have any of the following gastrointestinal symptoms?"
        ):
            return redirect("specific1")
        elif patient.question1 == "Do you have any of these symptoms?":
            return redirect("sexualspecific1")
        elif patient.question1 == "Have you ever tested your hemoglobin in the past?":
            if patient.answer1 == "Yes":
                return redirect("specific1")
            elif patient.answer1 == "No":
                return redirect("specific2")
        elif patient.question1 == "When was your condition diagnosed":
            return redirect("question2")
        elif patient.question1 == "Do you have?":
            return redirect("question2")
        elif patient.question1 == "When did you test positive for COVID":
            return redirect("question2")
        elif (
            patient.question1
            == "How often do you have trouble falling or staying asleep?"
        ):
            return redirect("question2")
        elif patient.question1 == "Have you lost interest in hobbies/ activities":
            return redirect("question2")
        elif patient.healthgoal == "Fitness":
            patient.question1 == "How would you describe your energy levels?"
            return redirect("result")
        elif patient.healthgoal == "Ensure Well Being":
            patient.question1 == "How would you describe your energy levels?"
            return redirect("specific1")
        elif patient.question1 == "What is your main concern?":
            return redirect("question2")
        elif patient.question1 == "Where is your pain located?":
            return redirect("question2")
        elif patient.healthgoal == "Gut Improvement":
            return redirect("question2")
        elif patient.healthgoal == "Skin and Hair":
            return redirect("question2")
        else:
            pass
        return redirect("result")

    elif "option3" in request.POST:
        option = request.POST["option3"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.answer1 = option
        patient.save()
        if (
            patient.question1
            == "Do you have any of the following respiratory symptoms?"
        ):
            return redirect("specific1")
        elif (
            patient.question1
            == "Do you have any of the following skin related symptoms?"
        ):
            return redirect("specific1")
        elif (
            patient.question1
            == "Do you have any of the following gastrointestinal symptoms?"
        ):
            return redirect("specific1")
        elif patient.question1 == "Do you have any of these symptoms?":
            return redirect("sexualspecific1")

        elif patient.question1 == "When was your condition diagnosed":
            return redirect("question2")
        elif patient.question1 == "Do you have?":
            return redirect("question2")
        elif patient.question1 == "When did you test positive for COVID":
            return redirect("question2")
        elif (
            patient.question1
            == "How often do you have trouble falling or staying asleep?"
        ):
            return redirect("question2")
        elif patient.question1 == "What is your main concern?":
            return redirect("question2")
        elif patient.healthgoal == "Fitness":
            patient.question1 == "How would you describe your energy levels?"
            return redirect("result")
        elif patient.healthgoal == "Ensure Well Being":
            patient.question1 == "How would you describe your energy levels?"
            return redirect("specific1")
        elif patient.question1 == "Where is your pain located?":
            return redirect("question2")
        elif patient.healthgoal == "Gut Improvement":
            return redirect("question2")
        elif patient.healthgoal == "Skin and Hair":
            return redirect("question2")
        else:
            pass
        return redirect("result")

    elif "option4" in request.POST:
        option = request.POST["option4"]

        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.answer1 = option
        patient.save()
        if (
            patient.question1
            == "Do you have any of the following respiratory symptoms?"
        ):
            return redirect("specific1")
        elif (
            patient.question1
            == "Do you have any of the following skin related symptoms?"
        ):
            return redirect("specific1")
        elif (
            patient.question1
            == "Do you have any of the following gastrointestinal symptoms?"
        ):
            return redirect("specific1")
        elif patient.question1 == "Do you have any of these symptoms?":
            return redirect("sexualspecific1")
        elif patient.question1 == "When did you test positive for COVID":
            return redirect("question2")
        elif (
            patient.question1
            == "How often do you have trouble falling or staying asleep?"
        ):
            return redirect("question2")
        elif patient.question1 == "What is your main concern?":
            return redirect("question2")
        elif patient.question1 == "Where is your pain located?":
            return redirect("question2")
        elif patient.healthgoal == "Fitness":
            patient.question1 == "How would you describe your energy levels?"
            return redirect("result")
        elif patient.healthgoal == "Ensure Well Being":
            patient.question1 == "How would you describe your energy levels?"
            return redirect("specific1")
        elif patient.healthgoal == "Gut Improvement":
            return redirect("question2")
        elif patient.healthgoal == "Skin and Hair":
            return redirect("question2")
        else:
            pass
        return redirect("result")

    elif "option5" in request.POST:
        option = request.POST["option5"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.answer1 = option
        patient.save()
        if (
            patient.question1
            == "Do you have any of the following respiratory symptoms?"
        ):
            return redirect("specific1")
        elif (
            patient.question1
            == "Do you have any of the following skin related symptoms?"
        ):
            return redirect("specific1")
        elif (
            patient.question1
            == "Do you have any of the following gastrointestinal symptoms?"
        ):
            return redirect("specific1")
        elif patient.question1 == "Do you have any of these symptoms?":
            return redirect("sexualspecific1")
        elif (
            patient.question1
            == "How often do you have trouble falling or staying asleep?"
        ):
            return redirect("question2")
        elif patient.question1 == "What is your main concern?":
            return redirect("question2")
        elif patient.question1 == "Where is your pain located?":
            return redirect("question2")
        elif patient.healthgoal == "Gut Improvement":
            return redirect("question2")
        elif patient.healthgoal == "Skin and Hair":
            return redirect("question2")
        elif patient.healthgoal == "Ensure Well Being":
            return redirect("specific1")

        else:
            pass
        return redirect("result")

    elif "option6" in request.POST:
        option = request.POST["option6"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.answer1 = option
        patient.save()
        if (
            patient.question1
            == "Do you have any of the following respiratory symptoms?"
        ):
            return redirect("specific1")
        elif (
            patient.question1
            == "Do you have any of the following skin related symptoms?"
        ):
            return redirect("specific1")
        elif (
            patient.question1
            == "Do you have any of the following gastrointestinal symptoms?"
        ):
            return redirect("specific1")
        elif patient.question1 == "Do you have any of these symptoms?":
            return redirect("sexualspecific1")
        elif (
            patient.question1
            == "How often do you have trouble falling or staying asleep?"
        ):
            return redirect("question2")
        elif patient.healthgoal == "Fitness":
            patient.question1 == "How would you describe your energy levels?"
            return redirect("result")
        elif patient.healthgoal == "Ensure Well Being":
            patient.question1 == "How would you describe your energy levels?"
            return redirect("question2")
        elif patient.healthgoal == "Gut Improvement":
            return redirect("question2")
        elif patient.healthgoal == "Skin and Hair":
            return redirect("question2")

        else:
            pass
        return redirect("result")

    elif "option7" in request.POST:
        option = request.POST["option7"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.answer1 = option
        patient.save()
        if (
            patient.question1
            == "Do you have any of the following respiratory symptoms?"
        ):
            return redirect("specific1")
        elif (
            patient.question1
            == "Do you have any of the following skin related symptoms?"
        ):
            return redirect("specific1")
        elif (
            patient.question1
            == "Do you have any of the following gastrointestinal symptoms?"
        ):
            return redirect("specific1")
        elif patient.question1 == "Do you have any of these symptoms?":
            return redirect("sexualspecific1")
        elif patient.healthgoal == "Gut Improvement":
            return redirect("question2")
        elif patient.healthgoal == "Skin and Hair":
            return redirect("question2")
        else:
            pass
        return redirect("result")

    elif "option8" in request.POST:
        option = request.POST["option8"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.answer1 = option
        patient.save()
        if (
            patient.question1
            == "Do you have any of the following respiratory symptoms?"
        ):
            return redirect("specific1")
        elif (
            patient.question1
            == "Do you have any of the following skin related symptoms?"
        ):
            return redirect("specific1")
        elif (
            patient.question1
            == "Do you have any of the following gastrointestinal symptoms?"
        ):
            return redirect("specific1")
        elif patient.question1 == "Do you have any of these symptoms?":
            return redirect("sexualspecific1")
        elif patient.healthgoal == "Skin and Hair":
            return redirect("question2")
        else:
            pass
        return redirect("result")

    elif "option9" in request.POST:
        option = request.POST["option9"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.answer1 = option
        patient.save()
        if (
            patient.question1
            == "Do you have any of the following respiratory symptoms?"
        ):
            return redirect("specific1")
        elif (
            patient.question1
            == "Do you have any of the following skin related symptoms?"
        ):
            return redirect("specific1")
        elif (
            patient.question1
            == "Do you have any of the following gastrointestinal symptoms?"
        ):
            return redirect("specific1")
        elif patient.question1 == "Do you have any of these symptoms?":
            return redirect("sexualspecific1")

        else:
            pass
        return redirect("result")

    elif "option10" in request.POST:
        option = request.POST["option10"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.answer1 = option
        patient.save()
        if (
            patient.question1
            == "Do you have any of the following respiratory symptoms?"
        ):
            return redirect("specific1")
        elif (
            patient.question1
            == "Do you have any of the following skin related symptoms?"
        ):
            return redirect("specific1")
        elif (
            patient.question1
            == "Do you have any of the following gastrointestinal symptoms?"
        ):
            return redirect("specific1")
        elif patient.question1 == "Do you have any of these symptoms?":
            return redirect("sexualspecific1")

        else:
            pass
        return redirect("result")

    elif "option11" in request.POST:
        option = request.POST["option11"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.answer1 = option
        patient.save()
        if (
            patient.question1
            == "Do you have any of the following respiratory symptoms?"
        ):
            return redirect("specific1")
        elif (
            patient.question1
            == "Do you have any of the following skin related symptoms?"
        ):
            return redirect("specific1")
        elif (
            patient.question1
            == "Do you have any of the following gastrointestinal symptoms?"
        ):
            return redirect("specific1")
        elif patient.question1 == "Do you have any of these symptoms?":
            return redirect("sexualspecific1")
        if patient.healthgoal == "Gut Improvement":
            return redirect("question2")

        else:
            pass
        return redirect("result")

    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    if patient.subgoal == "Hair":
        patient.question1 = "Hair Problem"
        patient.save()
    elif patient.subgoal == "Skin":
        patient.question1 = "Skin Problem"
        patient.save()
    elif patient.subgoal == "Respiratory":
        patient.question1 = "Do you have any of the following respiratory symptoms?"
        patient.save()
    elif patient.subgoal == "Skin Allergy":
        patient.question1 = "Do you have any of the following skin related symptoms?"
        patient.save()
    elif patient.subgoal == "Food":
        print("yes")
        patient.question1 = (
            "Do you have any of the following gastrointestinal symptoms?"
        )
        patient.save()
    elif patient.subgoal == "Sexual Well Being":
        print("yes")
        patient.question1 = "Do you have any of these symptoms?"
        patient.save()
    elif patient.subgoal == "PCOS":
        patient.question1 = "Are you facing any of the following issues:"
        patient.save()
        list3 = []
        global count
        count = 0
        if "optionn1" in request.POST:
            optione = request.POST["optionn1"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer1 = list4
            patient.save()
            count = count + 1

        if "optionn2" in request.POST:
            optione = request.POST["optionn2"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer1 = list4
            patient.save()
            count = count + 1

        if "optionn3" in request.POST:
            optione = request.POST["optionn3"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer1 = list4
            patient.save()
            count = count + 1

        if "optionn4" in request.POST:
            optione = request.POST["optionn4"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer1 = list4
            patient.save()
            count = count + 1

        if "optionn5" in request.POST:
            optione = request.POST["optionn5"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer1 = list4
            patient.save()
            count = count + 1

        if "optionn6" in request.POST:
            optione = request.POST["optionn6"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer1 = list4
            patient.save()
            count = count + 1

        if "submit" in request.POST:
            return redirect("result")
    elif patient.subgoal == "Anemia":
        patient.question1 = "Have you ever tested your hemoglobin in the past?"
        patient.save()
    elif patient.subgoal == "Bone Pain":
        patient.question1 = "Where is your pain located?"
        patient.save()
    elif patient.subgoal == "Hypertension and Diabetes":
        patient.question1 = "Do you have?"
        patient.save()
    elif patient.subgoal == "Post Covid":
        print("hi")
        patient.question1 = "When did you test positive for COVID"
        patient.save()
    elif patient.subgoal == "Sleep":
        patient.question1 = "How often do you have trouble falling or staying asleep?"
        patient.save()
    elif patient.subgoal == "Mood":
        patient.question1 = "Have you lost interest in hobbies/ activities"
        patient.save()
    elif patient.healthgoal == "Gut Improvement":
        patient.question1 = (
            "Which of the following symptoms best describe your problem?"
        )
        patient.save()
    elif patient.healthgoal == "Weight":
        patient.question1 = "What is your main concern?"
        patient.save()
    elif patient.healthgoal == "Ensure Well Being":
        patient.question1 = "How would you describe your energy levels?"
        patient.save()

    elif patient.healthgoal == "Skin and Hair":
        patient.question1 = "Skin Problem"
        patient.save()

    return render(
        request,
        "question1.html",
        {
            "patient_subgoal": patient.subgoal,
            "patient_question1": patient.question1,
            "patient_healthgoal": patient.healthgoal,
            "patient_gender": patient.gender,
            "patient_name": patient.name,
        },
    )


# QUESTION2
def question2(request):
    if "option1" in request.POST:
        answer2 = request.POST["option1"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.answer2 = answer2
        patient.save()
        if patient.healthgoal == "Weight" or patient.healthgoal == "Skin and Hair":
            return redirect("result")
        elif patient.healthgoal == "Gut Improvement":
            return redirect("result")
        return redirect("specific1")
    if "option2" in request.POST:
        answer2 = request.POST["option2"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.answer2 = answer2
        patient.save()
        if patient.healthgoal == "Weight" or patient.healthgoal == "Skin and Hair":
            return redirect("result")
        elif patient.healthgoal == "Gut Improvement":
            return redirect("result")
        return redirect("specific1")
    if "option3" in request.POST:
        answer2 = request.POST["option3"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.answer2 = answer2
        patient.save()
        if (
            patient.healthgoal == "Weight"
            or patient.healthgoal == "Skin and Hair"
            or patient.healthgoal == "Gut Improvement"
        ):
            return redirect("result")
        return redirect("specific1")
    if "option4" in request.POST:
        answer2 = request.POST["option4"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.answer2 = answer2
        patient.save()
        if (
            patient.healthgoal == "Weight"
            or patient.healthgoal == "Skin and Hair"
            or patient.healthgoal == "Gut Improvement"
        ):
            return redirect("result")
        return redirect("specific1")
    if "option5" in request.POST:
        answer2 = request.POST["option5"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.answer2 = answer2
        patient.save()
        if (
            patient.healthgoal == "Weight"
            or patient.healthgoal == "Skin and Hair"
            or patient.healthgoal == "Gut Improvement"
        ):
            return redirect("result")
        return redirect("specific1")
    if "option6" in request.POST:
        answer2 = request.POST["option6"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.answer2 = answer2
        patient.save()
        if (
            patient.healthgoal == "Weight"
            or patient.healthgoal == "Skin and Hair"
            or patient.healthgoal == "Gut Improvement"
        ):
            return redirect("result")
        return redirect("specific1")
    if "option7" in request.POST:
        answer2 = request.POST["option7"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.answer2 = answer2
        patient.save()
        if (
            patient.healthgoal == "Weight"
            or patient.healthgoal == "Skin and Hair"
            or patient.healthgoal == "Gut Improvement"
        ):
            return redirect("result")
        return redirect("specific1")
    if "option8" in request.POST:
        answer2 = request.POST["option8"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.answer2 = answer2
        patient.save()
        return redirect("specific1")
    if "option8" in request.POST:
        answer2 = request.POST["option8"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.answer2 = answer2
        patient.save()
        return redirect("specific1")
    if "option9" in request.POST:
        answer2 = request.POST["option9"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.answer2 = answer2
        patient.save()
        return redirect("specific1")
    if "option10" in request.POST:
        answer2 = request.POST["option10"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.answer2 = answer2
        patient.save()
        return redirect("specific1")
    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    if patient.subgoal == "Bone Pain":
        patient.question2 = "Which sides are involved"
    elif patient.subgoal == "Hypertension and Diabetes":
        patient.question2 = "When was your condition diagnosed"
    elif patient.subgoal == "Post Covid":
        patient.question2 = "Do you have any of the following?"
        patient.save()
        list3 = []
        global count1
        count1 = 0
        if "optionn1" in request.POST:
            optione = request.POST["optionn1"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer2 = list4
            patient.save()
            print("hi")
            count1 = count1 + 1
        if "optionn2" in request.POST:
            optione = request.POST["optionn2"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer2 = list4
            patient.save()
            count1 = count1 + 1
        if "optionn3" in request.POST:
            optione = request.POST["optionn3"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer2 = list4
            patient.save()
            count1 = count1 + 1
        if "optionn4" in request.POST:
            optione = request.POST["optionn4"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer2 = list4
            patient.save()
            count1 = count1 + 1
        if "optionn5" in request.POST:
            optione = request.POST["optionn5"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer2 = list4
            patient.save()
            count1 = count1 + 1
        if "optionn6" in request.POST:
            optione = request.POST["optionn6"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer2 = list4
            patient.save()
            count1 = count1 + 1
        if "optionn7" in request.POST:
            optione = request.POST["optionn7"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer2 = list4
            patient.save()
            count1 = count1 + 1
        if "optionn8" in request.POST:
            optione = request.POST["optionn8"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer2 = list4
            patient.save()
            count1 = count1 + 1
        if "optionn9" in request.POST:
            optione = request.POST["optionn9"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer2 = list4
            patient.save()
            count1 = count1 + 1
        if "optionn10" in request.POST:
            optione = request.POST["optionn10"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer2 = list4
            patient.save()
            count1 = count1 + 1
        if "submit" in request.POST:
            return redirect("specific1")

    elif patient.subgoal == "Sleep":
        patient.question2 = "Do you take anything to help you sleep"
    elif patient.subgoal == "Mood":
        patient.question2 = "Do you feel sad/ irritable or hopeless"
    elif patient.healthgoal == "Ensure Well Being":
        patient.question2 = (
            "Do you or a blood relation suffer from any of the following?"
        )
        patient.save()
        list3 = []
        if "optionn1" in request.POST:
            optione = request.POST["optionn1"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer2 = list4
            patient.save()

        if "optionn2" in request.POST:
            optione = request.POST["optionn2"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer2 = list4
            patient.save()

        if "optionn3" in request.POST:
            optione = request.POST["optionn3"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer2 = list4
            patient.save()

        if "optionn4" in request.POST:
            optione = request.POST["optionn4"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer2 = list4
            patient.save()

        if "optionn5" in request.POST:
            optione = request.POST["optionn5"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer2 = list4
            patient.save()

        if "optionn6" in request.POST:
            optione = request.POST["optionn6"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer2 = list4
            patient.save()

        if "optionn7" in request.POST:
            optione = request.POST["optionn7"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer2 = list4
            patient.save()

        if "optionn8" in request.POST:
            optione = request.POST["optionn8"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer2 = list4
            patient.save()

        if "optionn9" in request.POST:
            optione = request.POST["optionn9"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer2 = list4
            patient.save()

        if "optionn10" in request.POST:
            optione = request.POST["optionn10"]
            list3.append(optione)
            list4 = str(list3)
            print(list4)
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.answer2 = list4
            patient.save()

        if "submit" in request.POST:
            if patient.healthgoal == "Ensure Well Being":
                return redirect("specific1")
            else:
                return redirect("result")

    elif patient.healthgoal == "Gut Improvement":
        patient.question2 = "Please choose any of the following FIT profiles"

    elif patient.healthgoal == "Weight":
        patient.question2 = "How would you describe your energy levels?"
        patient.save()

    elif patient.healthgoal == "Skin and Hair":
        patient.question2 = "Hair Problem"
        patient.save()

    patient.save()
    return render(
        request,
        "question2.html",
        {
            "patient_subgoal": patient.subgoal,
            "patient_question2": patient.question2,
            "patient_healthgoal": patient.healthgoal,
        },
    )


# SEXUALS
def sexualspecific1(request):
    if "Never" in request.POST:
        specificanswer1 = request.POST["Never"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer1 = specificanswer1
        patient.save()
        return redirect("sexualspecific2")
    elif "Rarely" in request.POST:
        specificanswer1 = request.POST["Rarely"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer1 = specificanswer1
        patient.save()
        return redirect("sexualspecific2")
    elif "Almost" in request.POST:
        specificanswer1 = request.POST["Almost"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer1 = specificanswer1
        patient.save()
        return redirect("sexualspecific2")
    elif "Often" in request.POST:
        specificanswer1 = request.POST["Often"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer1 = specificanswer1
        patient.save()
        return redirect("sexualspecific2")
    elif "Everyday" in request.POST:
        specificanswer1 = request.POST["Everyday"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer1 = specificanswer1
        patient.save()
        return redirect("sexualspecific2")

    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    patient.specificquestion1 = (
        "How often do you wake to urinate 2 or more times at night"
    )
    patient.save()

    return render(
        request,
        "sexualspecific1.html",
        {
            "patient_specificquestion1": patient.specificquestion1,
            "patient_healthgoal": patient.healthgoal,
            "patient_gender": patient.gender,
        },
    )


def sexualspecific2(request):
    if "Poor flow of urine or slow stream" in request.POST:
        specificanswer2 = request.POST["Poor flow of urine or slow stream"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer2 = specificanswer2
        patient.save()
        return redirect("sexualspecific3")
    elif "Feeling incomplete bladder emptying" in request.POST:
        specificanswer2 = request.POST["Feeling incomplete bladder emptying"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer2 = specificanswer2
        patient.save()
        return redirect("sexualspecific3")
    elif "Straining to pass urine" in request.POST:
        specificanswer2 = request.POST["Straining to pass urine"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer2 = specificanswer2
        patient.save()
        return redirect("sexualspecific3")
    elif "None" in request.POST:
        specificanswer2 = request.POST["None"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer2 = specificanswer2
        patient.save()
        return redirect("sexualspecific3")
    elif "Never" in request.POST:
        specificanswer2 = request.POST["Never"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer2 = specificanswer2
        patient.save()
        return redirect("sexualspecific7")
    elif "Recently" in request.POST:
        specificanswer2 = request.POST["Recently"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer2 = specificanswer2
        patient.save()
        return redirect("sexualspecific7")
    elif "More than 3 years back" in request.POST:
        specificanswer2 = request.POST["More than 3 years back"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer2 = specificanswer2
        patient.save()
        return redirect("sexualspecific7")

    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    if patient.gender == "Male":
        patient.specificquestion2 = "Do you have any of these symptoms"
    else:
        patient.specificquestion2 = "When was the last time you got your PAP smear done"
    patient.save()

    return render(
        request,
        "sexualspecific2.html",
        {
            "patient_specificquestion2": patient.specificquestion2,
            "patient_gender": patient.gender,
        },
    )


def sexualspecific3(request):
    if "Low" in request.POST:
        specificanswer3 = request.POST["Low"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer3 = specificanswer3
        patient.save()
        return redirect("sexualspecific4")
    elif "Moderate" in request.POST:
        specificanswer3 = request.POST["Moderate"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer3 = specificanswer3
        patient.save()
        return redirect("sexualspecific4")
    elif "High" in request.POST:
        specificanswer3 = request.POST["High"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer3 = specificanswer3
        patient.save()
        return redirect("sexualspecific4")
    elif "I am having regular periods without any issues" in request.POST:
        specificanswer3 = request.POST["I am having regular periods without any issues"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer3 = specificanswer3
        patient.save()
        return redirect("sexualspecific7")
    elif "I have menstrual cramps during periods" in request.POST:
        specificanswer3 = request.POST["I have menstrual cramps during periods"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer3 = specificanswer3
        patient.save()
        return redirect("sexualspecific7")
    elif "I experience heavy bleeding" in request.POST:
        specificanswer3 = request.POST["I experience heavy bleeding"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer3 = specificanswer3
        patient.save()
        return redirect("sexualspecific7")
    elif "My periods are irregular" in request.POST:
        specificanswer3 = request.POST["My periods are irregular"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer3 = specificanswer3
        patient.save()
        return redirect("sexualspecific7")
    elif "I am pregnant" in request.POST:
        specificanswer3 = request.POST["I am pregnant"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer3 = specificanswer3
        patient.save()
        return redirect("sexualspecific7")
    elif "My last pregnency ended in past 2 months or I am nursing" in request.POST:
        specificanswer3 = request.POST[
            "My last pregnency ended in past 2 months or I am nursing"
        ]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer3 = specificanswer3
        patient.save()
        return redirect("sexualspecific7")
    elif "My periods stopped on their own  (I had menopause)" in request.POST:
        specificanswer3 = request.POST[
            "My periods stopped on their own  (I had menopause)"
        ]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer3 = specificanswer3
        patient.save()
        return redirect("sexualspecific7")

    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    if patient.gender == "Male":
        patient.specificquestion3 = "How would you rate your sexual desire?"
    else:
        patient.specificquestion3 = (
            "At present, which statement best describes your menstrual cycle"
        )
    patient.save()

    return render(
        request,
        "sexualspecific3.html",
        {
            "patient_specificquestion3": patient.specificquestion3,
            "patient_gender": patient.gender,
        },
    )


def sexualspecific4(request):
    if "Yes" in request.POST:
        specificanswer4 = request.POST["Yes"]
        print("his")
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer4 = specificanswer4
        patient.save()
        return redirect("sexualspecific5")
    elif "No" in request.POST:
        specificanswer4 = request.POST["No"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer4 = specificanswer4
        patient.save()
        return redirect("sexualspecific7")
    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    patient.specificquestion4 = "Are you sexually active?"
    patient.save()

    return render(
        request,
        "sexualspecific4.html",
        {
            "patient_specificquestion4": patient.specificquestion4,
            "patient_gender": patient.gender,
        },
    )


def sexualspecific5(request):
    if "Can't achieve full erection" in request.POST:
        specificanswer5 = request.POST["Can't achieve full erection"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer5 = specificanswer5
        patient.save()
        return redirect("sexualspecific6")
    elif "Can you achieve orgasm" in request.POST:
        specificanswer5 = request.POST["Can you achieve orgasm"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer5 = specificanswer5
        patient.save()
        return redirect("sexualspecific6")
    elif "Do you have premature ejaculation" in request.POST:
        specificanswer5 = request.POST["Do you have premature ejaculation"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer5 = specificanswer5
        patient.save()
        return redirect("sexualspecific6")
    elif "None" in request.POST:
        specificanswer5 = request.POST["None"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer5 = specificanswer5
        patient.save()
        return redirect("sexualspecific6")

    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    patient.specificquestion5 = "During sexual intercourse"
    patient.save()

    return render(
        request,
        "sexualspecific5.html",
        {
            "patient_specificquestion5": patient.specificquestion5,
            "patient_question1": patient.question1,
            "patient_gender": patient.gender,
        },
    )


def sexualspecific6(request):
    if "Yes" in request.POST:
        specificanswer6 = request.POST["Yes"]
        print("his")
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer6 = specificanswer6
        patient.save()
        return redirect("sexualspecific7")
    elif "No" in request.POST:
        specificanswer6 = request.POST["No"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer6 = specificanswer6
        patient.save()
        return redirect("sexualspecific7")

    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    patient.specificquestion6 = "Do you think there is emotional cause to any of these"
    patient.save()

    return render(
        request,
        "sexualspecific6.html",
        {
            "patient_specificquestion6": patient.specificquestion6,
            "patient_question1": patient.question1,
            "patient_gender": patient.gender,
        },
    )


def sexualspecific7(request):
    if "Unusual itching or swelling of the genital area" in request.POST:
        specificanswer7 = request.POST[
            "Unusual itching or swelling of the genital area"
        ]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer7 = specificanswer7
        patient.save()
        return redirect("sexualspecific8")
    elif "Soreness or discharge from penis" in request.POST:
        specificanswer7 = request.POST["Soreness or discharge from penis"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer7 = specificanswer7
        patient.save()
        return redirect("sexualspecific8")
    elif "Burning or itching sensation while urinating" in request.POST:
        specificanswer7 = request.POST["Burning or itching sensation while urinating"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer7 = specificanswer7
        patient.save()
        return redirect("sexualspecific8")
    elif "Strong unusual genital odour" in request.POST:
        specificanswer7 = request.POST["Strong unusual genital odour"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer7 = specificanswer7
        patient.save()
        return redirect("sexualspecific8")

    elif "Any ulcers in genital area" in request.POST:
        specificanswer7 = request.POST["Any ulcers in genital area"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer7 = specificanswer7
        patient.save()
        return redirect("sexualspecific8")

    elif "Soreness or discharge from penis" in request.POST:
        specificanswer7 = request.POST["Soreness or discharge from penis"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer7 = specificanswer7
        patient.save()
        return redirect("sexualspecific8")
    elif "Soreness or discharge from vagina" in request.POST:
        specificanswer7 = request.POST["Soreness or discharge from vagina"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer7 = specificanswer7
        patient.save()
        return redirect("sexualspecific8")
    elif "None" in request.POST:
        specificanswer7 = request.POST["None"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer7 = specificanswer7
        patient.save()
        return redirect("sexualspecific8")
    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    patient.specificquestion7 = "Do you have any of the following symptoms"
    patient.save()

    return render(
        request,
        "sexualspecific7.html",
        {
            "patient_specificquestion7": patient.specificquestion7,
            "patient_question1": patient.question1,
            "patient_gender": patient.gender,
        },
    )


def sexualspecific8(request):
    if "Yes" in request.POST:
        specificanswer8 = request.POST["Yes"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer8 = specificanswer8
        patient.save()
        return redirect("sexualspecific9")
    elif "No" in request.POST:
        specificanswer8 = request.POST["No"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer8 = specificanswer8
        patient.save()
        return redirect("sexualspecific9")

    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    patient.specificquestion8 = (
        "Have you had unprotected sexual act in past 6  months (other than partner)"
    )
    patient.save()

    return render(
        request,
        "sexualspecific8.html",
        {
            "patient_specificquestion8": patient.specificquestion8,
            "patient_gender": patient.gender,
        },
    )


def sexualspecific9(request):
    if "Yes" in request.POST:
        specificanswer9 = request.POST["Yes"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer9 = specificanswer9
        patient.save()
        return redirect("sexualspecific10")
    elif "No" in request.POST:
        specificanswer9 = request.POST["No"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer9 = specificanswer9
        patient.save()
        return redirect("result")

    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    patient.specificquestion9 = "Are you planning a family soon?"
    patient.save()

    return render(
        request,
        "sexualspecific9.html",
        {
            "patient_specificquestion9": patient.specificquestion9,
            "patient_gender": patient.gender,
        },
    )


def sexualspecific10(request):
    if "6months" in request.POST:
        specificanswer10 = request.POST["6months"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer10 = specificanswer10
        patient.save()
        return redirect("result")
    elif "6months to 1 year" in request.POST:
        specificanswer10 = request.POST["6months to 1 year"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer10 = specificanswer10
        patient.save()
        return redirect("result")
    elif "1 year" in request.POST:
        specificanswer10 = request.POST["1 year"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer10 = specificanswer10
        patient.save()
        return redirect("result")

    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    patient.specificquestion10 = "How long have you and your partner been trying to concieve with unprotected intercourse?"
    patient.save()

    return render(
        request,
        "sexualspecific10.html",
        {
            "patient_specificquestion10": patient.specificquestion10,
            "patient_gender": patient.gender,
        },
    )


# SPECIFIC1
def specific1(request):
    if "option1" in request.POST:
        specificanswer1 = request.POST["option1"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer1 = specificanswer1
        patient.save()
        if patient.subgoal == "Bone Pain":
            return redirect("specific2")
        if patient.healthgoal == "Augment Quality of Sleep and Elevate Mood":
            return redirect("specific2")
        if patient.healthgoal == "Allergy and Intolerance":
            return redirect("specific2")
        if patient.subgoal == "Respiratory":
            return redirect("specific2")
        if patient.subgoal == "Skin Allergy":
            return redirect("specific2")
        if patient.subgoal == "Food":
            return redirect("specific2")

        if patient.subgoal == "Anemia":
            return redirect("specific2")
        else:
            return redirect("result")
    if "option2" in request.POST:
        specificanswer1 = request.POST["option2"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer1 = specificanswer1
        patient.save()
        if patient.subgoal == "Bone Pain":
            return redirect("specific2")
        if patient.healthgoal == "Augment Quality of Sleep and Elevate Mood":
            return redirect("specific2")
        if patient.subgoal == "Respiratory":
            return redirect("specific2")
        if patient.subgoal == "Skin Allergy":
            return redirect("specific2")
        if patient.subgoal == "Food":
            return redirect("specific2")
        if patient.subgoal == "Anemia":
            return redirect("specific2")
        else:
            return redirect("result")
    if "option3" in request.POST:
        specificanswer1 = request.POST["option3"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer1 = specificanswer1
        patient.save()
        if patient.subgoal == "Bone Pain":
            return redirect("specific2")
        if patient.healthgoal == "Augument Quality of Sleep and Elevate Mood":
            return redirect("specific2")
        if patient.subgoal == "Respiratory":
            return redirect("specific2")
        if patient.subgoal == "Skin Allergy":
            return redirect("specific2")
        if patient.subgoal == "Food":
            return redirect("specific2")
        if patient.subgoal == "Anemia":
            return redirect("specific2")
        else:
            return redirect("result")
    if "option4" in request.POST:
        specificanswer1 = request.POST["option4"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer1 = specificanswer1
        patient.save()
        if patient.subgoal == "Bone Pain":
            return redirect("specific2")
        if patient.healthgoal == "Augument Quality of Sleep and Elevate Mood":
            return redirect("specific2")
        if patient.subgoal == "Respiratory":
            return redirect("specific2")
        if patient.subgoal == "Skin Allergy":
            return redirect("specific2")
        if patient.subgoal == "Food":
            return redirect("specific2")
        if patient.subgoal == "Anemia":
            return redirect("specific2")
        else:
            return redirect("result")
    if "option5" in request.POST:
        specificanswer1 = request.POST["option5"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer1 = specificanswer1
        patient.save()
        if patient.subgoal == "Bone Pain":
            return redirect("specific2")
        if patient.healthgoal == "Augument Quality of Sleep and Elevate Mood":
            return redirect("specific2")
        if patient.subgoal == "Respiratory":
            return redirect("specific2")
        if patient.subgoal == "Skin Allergy":
            return redirect("specific2")
        if patient.subgoal == "Food":
            return redirect("specific2")
        else:
            return redirect("result")
    if "option6" in request.POST:
        specificanswer1 = request.POST["option6"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer1 = specificanswer1
        patient.save()
        if patient.subgoal == "Bone Pain":
            return redirect("specific2")
        if patient.healthgoal == "Augument Quality of Sleep and Elevate Mood":
            return redirect("specific2")
        if patient.subgoal == "Respiratory":
            return redirect("specific2")
        if patient.subgoal == "Skin Allergy":
            return redirect("specific2")
        if patient.subgoal == "Food":
            return redirect("specific2")
        else:
            return redirect("result")

    if "option7" in request.POST:
        specificanswer1 = request.POST["option7"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer1 = specificanswer1
        patient.save()
        if patient.subgoal == "Bone Pain":
            return redirect("specific2")
        if patient.healthgoal == "Augument Quality of Sleep and Elevate Mood":
            return redirect("specific2")
        if patient.subgoal == "Respiratory":
            return redirect("specific2")
        if patient.subgoal == "Skin Allergy":
            return redirect("specific2")
        if patient.subgoal == "Food":
            return redirect("specific2")
        else:
            return redirect("result")

    if "option8" in request.POST:
        specificanswer1 = request.POST["option8"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer1 = specificanswer1
        patient.save()
        if patient.subgoal == "Bone Pain":
            return redirect("specific2")
        if patient.healthgoal == "Augument Quality of Sleep and Elevate Mood":
            return redirect("specific2")
        if patient.subgoal == "Respiratory":
            return redirect("specific2")
        if patient.subgoal == "Skin Allergy":
            return redirect("specific2")
        if patient.subgoal == "Food":
            return redirect("specific2")
        else:
            return redirect("result")

    if "option9" in request.POST:
        specificanswer1 = request.POST["option9"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer1 = specificanswer1
        patient.save()
        if patient.subgoal == "Bone Pain":
            return redirect("specific2")
        if patient.healthgoal == "Augument Quality of Sleep and Elevate Mood":
            return redirect("specific2")
        if patient.subgoal == "Respiratory":
            return redirect("specific2")
        if patient.subgoal == "Skin Allergy":
            return redirect("specific2")
        if patient.subgoal == "Food":
            return redirect("specific2")
        else:
            return redirect("result")

    if "option10" in request.POST:
        specificanswer1 = request.POST["option10"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer1 = specificanswer1
        patient.save()
        if patient.subgoal == "Bone Pain":
            return redirect("specific2")
        if patient.healthgoal == "Augument Quality of Sleep and Elevate Mood":
            return redirect("specific2")
        if patient.subgoal == "Respiratory":
            return redirect("specific2")
        if patient.subgoal == "Skin Allergy":
            return redirect("specific2")
        if patient.subgoal == "Food":
            return redirect("specific2")
        else:
            return redirect("result")
    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    if patient.subgoal == "Bone Pain":
        patient.specificquestion1 = "How long you had symptoms"
    elif patient.subgoal == "Hypertension and Diabetes":
        patient.specificquestion1 = "Are you taking medicine for diabetes/ hypertension"
    elif patient.subgoal == "Post Covid":
        patient.specificquestion1 = "Please tick the most appropriate option "
    elif patient.subgoal == "Sleep":
        patient.specificquestion1 = (
            "Are you a shift worker/ have irregular sleep schedule?"
        )
    elif patient.subgoal == "Mood":
        patient.specificquestion1 = "Do you feel nervous or worried"
    elif patient.subgoal == "Respiratory":
        patient.specificquestion1 = "Choose any of the following which seems to trigger or cause the above symptoms"
    elif patient.subgoal == "Skin Allergy":
        patient.specificquestion1 = "Choose any of the following which seems to trigger or cause the above symptoms"
    elif patient.subgoal == "Food":
        patient.specificquestion1 = (
            "Are you suffering from any chronic/ autoimmune condition"
        )
    elif patient.subgoal == "Anemia":
        patient.specificquestion1 = " what was your Hb"
    elif patient.healthgoal == "Ensure Well Being":
        patient.specificquestion1 = (
            "Do you have any of the following sleep related issues?"
        )
    patient.save()

    return render(
        request,
        "specific1.html",
        {
            "patient_subgoal": patient.subgoal,
            "patient_specificquestion1": patient.specificquestion1,
            "patient_healthgoal": patient.healthgoal,
            "patient_gender": patient.gender,
        },
    )


def specific2(request):
    if "pain" in request.POST:
        pain = request.POST["pain"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificquestion2 = "On a scale of 1 to 10 ( 1 being minimal and 10 being severe), what is your level of pain"
        patient.specificanswer2 = pain
        patient.save()
        return redirect("result")
    elif "option1" in request.POST:
        specificanswer2 = request.POST["option1"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer2 = specificanswer2
        patient.save()
        if patient.subgoal == "Sleep":
            return redirect("specific3")
        elif patient.subgoal == "Mood":
            return redirect("result")
        if patient.subgoal == "Respiratory":
            return redirect("result")
        if patient.subgoal == "Skin Allergy":
            return redirect("result")
        if patient.subgoal == "Anemia":
            return redirect("specific3")
        else:
            return redirect("result")
    elif "option2" in request.POST:
        specificanswer2 = request.POST["option2"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer2 = specificanswer2
        patient.save()
        if patient.subgoal == "Sleep":
            return redirect("specific3")
        elif patient.subgoal == "Mood":
            return redirect("result")
        if patient.subgoal == "Respiratory":
            return redirect("result")
        if patient.subgoal == "Skin Allergy":
            return redirect("result")
        if patient.subgoal == "Anemia":
            return redirect("specific3")
        else:
            return redirect("result")

    elif "option3" in request.POST:
        specificanswer2 = request.POST["option3"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer2 = specificanswer2
        patient.save()
        if patient.subgoal == "Sleep":
            return redirect("specific3")
        elif patient.subgoal == "Mood":
            return redirect("result")
        if patient.subgoal == "Anemia":
            return redirect("specific3")
        else:
            return redirect("result")

    elif "option4" in request.POST:
        specificanswer2 = request.POST["option4"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer2 = specificanswer2
        patient.save()
        if patient.subgoal == "Sleep":
            return redirect("specific3")
        elif patient.subgoal == "Mood":
            return redirect("result")
        else:
            return redirect("result")
    elif "option5" in request.POST:
        specificanswer2 = request.POST["option5"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer2 = specificanswer2
        patient.save()
        if patient.subgoal == "Sleep":
            return redirect("specific3")
        elif patient.subgoal == "Mood":
            return redirect("result")
        else:
            return redirect("result")
    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    if patient.subgoal == "Bone Pain":
        patient.specificquestion2 = "On a scale of 1 to 10 ( 1 being minimal and 10 being severe), what is your level of pain"
    if patient.subgoal == "Sleep":
        patient.specificquestion2 = (
            "Do you have any unusual behavior/ movements during sleep?"
        )
    if patient.subgoal == "Mood":
        patient.specificquestion2 = "Has there ever been a period of time when you"
    elif patient.subgoal == "Respiratory":
        patient.specificquestion2 = (
            "Do other people in your family have a similar condition?"
        )
    elif patient.subgoal == "Skin Allergy":
        patient.specificquestion2 = (
            "Do other people in your family have a similar condition?"
        )
    elif patient.subgoal == "Food":
        patient.specificquestion2 = "Do you feel that your symptoms appear"
    elif patient.subgoal == "Anemia":
        patient.specificquestion2 = "Are you taking  Fe, Vit B12 or folate supplements?"
    patient.save()

    return render(
        request,
        "specific2.html",
        {
            "patient_subgoal": patient.subgoal,
            "patient_healthgoal": patient.healthgoal,
            "patient_specificquestion2": patient.specificquestion2,
        },
    )


def specific3(request):
    if "option1" in request.POST:
        specificanswer3 = request.POST["option1"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer3 = specificanswer3
        patient.save()
        if patient.healthgoal == "Augment Quality of Sleep and Elevate Mood":
            return redirect("specific4")
        if patient.subgoal == "Anemia":
            return redirect("result")
        else:
            return redirect("result")
    elif "option2" in request.POST:
        specificanswer3 = request.POST["option2"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer3 = specificanswer3
        patient.save()
        if patient.healthgoal == "Augment Quality of Sleep and Elevate Mood":
            return redirect("specific4")
        if patient.subgoal == "Anemia":
            return redirect("result")
        else:
            return redirect("result")

    elif "option3" in request.POST:
        specificanswer3 = request.POST["option3"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer3 = specificanswer3
        patient.save()
        if patient.healthgoal == "Augment Quality of Sleep and Elevate Mood":
            return redirect("specific4")
        else:
            return redirect("result")

    elif "option4" in request.POST:
        specificanswer3 = request.POST["option4"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer3 = specificanswer3
        patient.save()
        if patient.healthgoal == "Augment Quality of Sleep and Elevate Mood":
            return redirect("specific4")
        else:
            return redirect("result")
    elif "option5" in request.POST:
        specificanswer3 = request.POST["option5"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer3 = specificanswer3
        patient.save()
        if patient.healthgoal == "Augment Quality of Sleep and Elevate Mood":
            return redirect("specific4")
        else:
            return redirect("result")

    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    if patient.subgoal == "Sleep":
        patient.specificquestion3 = "Do you snore during sleep?"
    if patient.subgoal == "Mood":
        patient.specificquestion3 = "Has there ever been a period of time when you"
    if patient.subgoal == "Anemia":
        patient.specificquestion3 = (
            "Do you have anyone in your family who has thallesemia minor"
        )
    patient.save()

    return render(
        request,
        "specific3.html",
        {
            "patient_subgoal": patient.subgoal,
            "patient_healthgoal": patient.healthgoal,
            "patient_specificquestion3": patient.specificquestion3,
        },
    )


def specific4(request):
    if "option1" in request.POST:
        specificanswer5 = request.POST["option1"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer5 = specificanswer5
        patient.save()
        if patient.healthgoal == "Augment Quality of Sleep and Elevate Mood":
            return redirect("specific5")
        else:
            return redirect("result")
    elif "option2" in request.POST:
        specificanswer5 = request.POST["option2"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer5 = specificanswer5
        patient.save()
        if patient.healthgoal == "Augment Quality of Sleep and Elevate Mood":
            return redirect("specific5")
        else:
            return redirect("result")

    elif "option3" in request.POST:
        specificanswer5 = request.POST["option3"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer5 = specificanswer5
        patient.save()
        if patient.healthgoal == "Augment Quality of Sleep and Elevate Mood":
            return redirect("specific5")
        else:
            return redirect("result")

    elif "option4" in request.POST:
        specificanswer5 = request.POST["option4"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer5 = specificanswer5
        patient.save()
        if patient.healthgoal == "Augment Quality of Sleep and Elevate Mood":
            return redirect("specific5")
        else:
            return redirect("result")

    elif "option5" in request.POST:
        specificanswer5 = request.POST["option5"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer5 = specificanswer5
        patient.save()
        if patient.healthgoal == "Augment Quality of Sleep and Elevate Mood":
            return redirect("specific5")
        else:
            return redirect("result")

    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    if patient.healthgoal == "Augment Quality of Sleep and Elevate Mood":
        patient.specificquestion5 = (
            "Do you have difficulty in staying awake during the day?"
        )
    patient.save()

    return render(
        request,
        "specific4.html",
        {
            "patient_subgoal": patient.subgoal,
            "patient_healthgoal": patient.healthgoal,
            "patient_specificquestion5": patient.specificquestion5,
        },
    )


def specific5(request):
    if "option1" in request.POST:
        specificanswer6 = request.POST["option1"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer6 = specificanswer6
        patient.save()
        return redirect("specific6")
    elif "option2" in request.POST:
        specificanswer6 = request.POST["option2"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer6 = specificanswer6
        patient.save()
        return redirect("specific6")

    elif "option3" in request.POST:
        specificanswer6 = request.POST["option3"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer6 = specificanswer6
        patient.save()
        return redirect("specific6")

    elif "option4" in request.POST:
        specificanswer6 = request.POST["option4"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer6 = specificanswer6
        patient.save()
        return redirect("specific6")
    elif "option5" in request.POST:
        specificanswer6 = request.POST["option5"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer6 = specificanswer6
        patient.save()
        return redirect("specific6")

    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    if patient.healthgoal == "Augment Quality of Sleep and Elevate Mood":
        patient.specificquestion6 = (
            "Are your legs restless or uncomfortable before bed?"
        )
    patient.save()

    return render(
        request,
        "specific5.html",
        {
            "patient_subgoal": patient.subgoal,
            "patient_healthgoal": patient.healthgoal,
            "patient_specificquestion6": patient.specificquestion6,
        },
    )


def specific6(request):
    if "option1" in request.POST:
        specificanswer7 = request.POST["option1"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer7 = specificanswer7
        patient.save()
        return redirect("specific7")
    elif "option2" in request.POST:
        specificanswer7 = request.POST["option2"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer7 = specificanswer7
        patient.save()
        return redirect("specific7")

    elif "option3" in request.POST:
        specificanswer7 = request.POST["option3"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer7 = specificanswer7
        patient.save()
        return redirect("specific7")

    elif "option4" in request.POST:
        specificanswer7 = request.POST["option4"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer7 = specificanswer7
        patient.save()
        return redirect("specific7")
    elif "option5" in request.POST:
        specificanswer7 = request.POST["option5"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer7 = specificanswer7
        patient.save()
        return redirect("specific7")

    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    if patient.healthgoal == "Augment Quality of Sleep and Elevate Mood":
        patient.specificquestion7 = (
            "How often do you wake to urinate 2 or more times at night"
        )
    patient.save()

    return render(
        request,
        "specific6.html",
        {
            "patient_subgoal": patient.subgoal,
            "patient_healthgoal": patient.healthgoal,
            "patient_specificquestion7": patient.specificquestion7,
        },
    )


def specific7(request):
    if "option1" in request.POST:
        specificanswer8 = request.POST["option1"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer8 = specificanswer8
        patient.save()
        return redirect("result")
    elif "option2" in request.POST:
        specificanswer8 = request.POST["option2"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer8 = specificanswer8
        patient.save()
        return redirect("result")

    elif "option3" in request.POST:
        specificanswer8 = request.POST["option3"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer8 = specificanswer8
        patient.save()
        return redirect("result")

    elif "option4" in request.POST:
        specificanswer8 = request.POST["option4"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer8 = specificanswer8
        patient.save()
        return redirect("result")
    elif "option5" in request.POST:
        specificanswer8 = request.POST["option5"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.specificanswer8 = specificanswer8
        patient.save()
        return redirect("result")

    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    if patient.healthgoal == "Augment Quality of Sleep and Elevate Mood":
        patient.specificquestion8 = (
            "How likely are you to doze off or fall asleep in following situations:"
        )
    patient.save()

    return render(
        request,
        "specific7.html",
        {
            "patient_subgoal": patient.subgoal,
            "patient_healthgoal": patient.healthgoal,
            "patient_specificquestion8": patient.specificquestion8,
        },
    )


# RESULT
def result(request):
    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    test = Test.objects.order_by("id")
    list = []
    test_link = []
    subg = []
    # HAIR PROBLEM
    if patient.question2 == "Hair Problem":
        subg.append("HAIR PROBLEM")
        if patient.answer2 == "Hairfall":
            list.append(str(test[4]))
            list.append(str(test[21]))
            list.append(str(test[30]))
            list.append(str(test[31]))
            list.append(str(test[43]))
            list.append(str(test[33]))
            list.append(str(test[11]))
            list.append(str(test[34]))
            list.append(str(test[9]))
            list.append(str(test[114]))
            list.append(str(test[38]))
            list.append(str(test[36]))
            list.append(str(test[39]))
            list.append(str(test[29]))
            list.append(str(test[32]))
            list.append(str(test[35]))
            list.append(str(test[37]))
            list.append(str(test[8]))
            test_link.append(
                {"GOAL SPECIFIC": ["CBC", "https://pubmed.ncbi.nlm.nih.gov/31502748/"]}
            )
            test_link.append(
                {"GOAL SPECIFIC": ["TFT", "https://pubmed.ncbi.nlm.nih.gov/34455910/"]}
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Iron:",
                        "https://pubmed.ncbi.nlm.nih.gov/20888066/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Vit&Min",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6380979/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Hormones1",
                        "https://pubmed.ncbi.nlm.nih.gov/33130791/ ",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Hormones2",
                        "https://pubmed.ncbi.nlm.nih.gov/14758568/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Insulin",
                        "https://pubmed.ncbi.nlm.nih.gov/25781062/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Sex Hormones",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5817427/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "ANA",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4377414/",
                    ]
                }
            )
            test_link.append(
                {"GOAL SPECIFIC": ["CRP", "https://pubmed.ncbi.nlm.nih.gov/25484412/"]}
            )
            if patient.gender == "Female":
                list.append(str(test[102]))
                list.append(str(test[40]))
                list.append(str(test[41]))
                list.append(str(test[42]))
                test_link.append(
                    {
                        "GOAL SPECIFIC": [
                            "Female Hormones",
                            "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7432488/",
                        ]
                    }
                )
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.tests = list
            patient.save()
        if patient.answer2 == "Premature Graying":
            list.append(str(test[4]))
            list.append(str(test[21]))
            list.append(str(test[30]))
            list.append(str(test[43]))
            list.append(str(test[85]))
            list.append(str(test[114]))
            list.append(str(test[38]))
            list.append(str(test[39]))
            list.append(str(test[29]))
            list.append(str(test[32]))
            list.append(str(test[46]))
            list.append(str(test[11]))
            test_link.append(
                {"GOAL SPECIFIC": ["CBC", "https://pubmed.ncbi.nlm.nih.gov/31502748/"]}
            )
            test_link.append(
                {"GOAL SPECIFIC": ["TFT", "https://pubmed.ncbi.nlm.nih.gov/34455910/"]}
            )
            test_link.append(
                {"GOAL SPECIFIC": ["Iron", "https://pubmed.ncbi.nlm.nih.gov/20888066/"]}
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Vit&Min",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6380979/",
                    ]
                }
            )

            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.tests = list
            patient.save()
        if patient.answer2 == "Dandruff/Split Ends":
            list.append(str(test[30]))
            list.append(str(test[43]))
            list.append(str(test[85]))
            list.append(str(test[114]))
            list.append(str(test[38]))
            list.append(str(test[39]))
            list.append(str(test[29]))
            list.append(str(test[32]))
            list.append(str(test[11]))
            test_link.append(
                {"GOAL SPECIFIC": ["Iron", "https://pubmed.ncbi.nlm.nih.gov/20888066/"]}
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Vit&Min",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6380979/",
                    ]
                }
            )
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.tests = list
            patient.save()
    # SKIN PROBLEM
    if patient.question1 == "Skin Problem":
        subg.append("SKIN")
        if patient.answer1 == "Acne":
            list.append(str(test[102]))
            list.append(str(test[33]))
            list.append(str(test[26]))
            list.append(str(test[36]))
            list.append(str(test[40]))
            list.append(str(test[41]))
            list.append(str(test[42]))
            list.append(str(test[44]))
            list.append(str(test[45]))
            list.append(str(test[46]))
            test_link.append(
                {"GOAL SPECIFIC": ["DHEAS", "https://pubmed.ncbi.nlm.nih.gov/2426899/"]}
            )
            test_link.append(
                {"GOAL SPECIFIC": ["SHBG", "https://pubmed.ncbi.nlm.nih.gov/6458423/"]}
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Lipid Profile",
                        "https://pubmed.ncbi.nlm.nih.gov/32021370/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Testosterone",
                        "https://pubmed.ncbi.nlm.nih.gov/6258368/",
                    ]
                }
            )

            if patient.gender == "Female":
                test_link.append(
                    {
                        "GOAL SPECIFIC": [
                            "Female Hormone",
                            "https://pubmed.ncbi.nlm.nih.gov/2151388/",
                        ]
                    }
                )

            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.tests = list
            patient.save()
        if patient.answer1 == "Eczema":
            list.append(str(test[47]))
            list.append(str(test[48]))
            if patient.age <= 13:
                list.append(str(test[49]))
            list.append(str(test[46]))
            test_link.append(
                {"GOAL SPECIFIC": ["IgE", "https://pubmed.ncbi.nlm.nih.gov/14998387/"]}
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Intolerance",
                        "https://pubmed.ncbi.nlm.nih.gov/16782524/",
                    ]
                }
            )

            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.tests = list
            patient.save()
        if patient.answer1 == "Hives or Uticaria":
            list.append(str(test[47]))
            list.append(str(test[48]))
            if patient.age <= 13:
                list.append(str(test[49]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Allergy",
                        "https://pubmed.ncbi.nlm.nih.gov/35362938/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Intolerance",
                        "https://pubmed.ncbi.nlm.nih.gov/33601370/",
                    ]
                }
            )

            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.tests = list
            patient.save()
        if patient.answer1 == "Rashes":
            list.append(str(test[47]))
            list.append(str(test[48]))
            if patient.age <= 13:
                list.append(str(test[49]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Allergy",
                        "https://pubmed.ncbi.nlm.nih.gov/28319560/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Intolerance",
                        "https://pubmed.ncbi.nlm.nih.gov/16782524/",
                    ]
                }
            )

            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.tests = list
            patient.save()
        if patient.answer1 == "Vitiligo":
            list.append(str(test[47]))
            list.append(str(test[48]))
            if patient.age <= 13:
                list.append(str(test[49]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Anti TPO",
                        "https://pubmed.ncbi.nlm.nih.gov/25653881/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Anti TG",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3121018/",
                    ]
                }
            )
            test_link.append(
                {"GOAL SPECIFIC": ["ANA", "https://pubmed.ncbi.nlm.nih.gov/12562399/"]}
            )
            test_link.append(
                {"GOAL SPECIFIC": ["TFT", "https://pubmed.ncbi.nlm.nih.gov/30698146/"]}
            )

            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.tests = list
            patient.save()
    # RESPIRATORY PROBLEM
    if patient.question1 == "Do you have any of the following respiratory symptoms?":
        list.append((test[47]))
        list.append((test[131]))

        if patient.age <= 13:
            list.append((test[49]))

        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()

    # SKIN ALLERGY
    if patient.question1 == "Do you have any of the following skin related symptoms?":
        list.append(str(test[47]))
        list.append(str(test[48]))
        if patient.age <= 13:
            list.append(str(test[49]))
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()
    # FOODALLERGY
    if patient.specificanswer2 == "within 30 min of exposure":
        list.append(str(test[48]))
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()
    elif patient.specificanswer2 == "30 min to 2hours of exposure":
        list.append(str(test[48]))
        list.append(str(test[46]))
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()

    elif patient.specificanswer2 == ">2hours of exposure":
        list.append(str(test[46]))
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()

    # SEXUAL MALE
    if patient.question1 == "Do you have any of these symptoms?":
        if patient.answer1 != "None":
            subg.append("SEXUAL")
            list.append(str(test[27]))
            list.append(str(test[103]))
            list.append(str(test[4]))
            list.append(str(test[7]))
            test_link.append(
                {"GOAL SPECIFIC": ["CBC", "https://pubmed.ncbi.nlm.nih.gov/19377227/"]}
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "UTI1",
                        "https://www.ncbi.nlm.nih.gov/books/NBK470195/",
                    ]
                }
            )
            test_link.append(
                {"GOAL SPECIFIC": ["UTI2", "https://pubmed.ncbi.nlm.nih.gov/29305250/"]}
            )
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.tests = list
            patient.save()

    if patient.specificanswer1 == "Often" or patient.specificanswer1 == "Everyday":
        list.append(str(test[23]))
        test_link.append(
            {
                "GOAL SPECIFIC": [
                    "hbA1c",
                    "https://www.diabetes.co.uk/symptoms/polyuria.html",
                ]
            }
        )
        test_link.append(
            {
                "GOAL SPECIFIC": [
                    "Urine test",
                    "https://pubmed.ncbi.nlm.nih.gov/34509418/",
                ]
            }
        )
        test_link.append(
            {"GOAL SPECIFIC": ["CBC", "https://pubmed.ncbi.nlm.nih.gov/2134078/"]}
        )
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()

    if (
        patient.specificquestion2 == "Do you have any of these symptoms"
        and patient.gender == "Male"
    ):
        if patient.specificanswer2 != "None":
            list.append(str(test[27]))
            list.append(str(test[103]))
            list.append(str(test[4]))
            list.append(str(test[7]))
            if patient.age >= 50:
                list.append(str(test[60]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Urine Retention",
                        "https://www.ncbi.nlm.nih.gov/books/NBK538499/",
                    ]
                }
            )
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.tests = list
            patient.save()

    if patient.specificanswer3 == "Low":
        subg.append("SEXUAL")
        list.append(str(test[35]))
        list.append(str(test[102]))
        list.append(str(test[33]))
        list.append(str(test[55]))
        list.append(str(test[59]))
        list.append(str(test[52]))
        list.append(str(test[30]))
        if patient.gender == "Male":
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Testo&Cortisol",
                        "https://pubmed.ncbi.nlm.nih.gov/21993767/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "DHEAS",
                        "https://pubmed.ncbi.nlm.nih.gov/28118059/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Sex Hormone",
                        "https://pubmed.ncbi.nlm.nih.gov/11942957/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Thyroid Tests",
                        "https://pubmed.ncbi.nlm.nih.gov/30057137/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Cholesterol",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6060264/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Iron",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6283628/",
                    ]
                }
            )
        elif patien.gender == "Female":
            list.append(str(test[41]))
            list.append(str(test[40]))
            list.append(str(test[42]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Hormones 1",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5776161/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Hormones 2",
                        "https://pubmed.ncbi.nlm.nih.gov/36018001/",
                    ]
                }
            )

        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()

    elif patient.specificanswer3 == "High":
        list.append(str(test[35]))
        list.append(str(test[102]))
        list.append(str(test[55]))
        list.append(str(test[52]))
        test_link.append(
            {
                "GOAL SPECIFIC": [
                    "Intolerance",
                    "https://pubmed.ncbi.nlm.nih.gov/21993767/",
                ]
            }
        )
        test_link.append(
            {"GOAL SPECIFIC": ["DHEAS", "https://pubmed.ncbi.nlm.nih.gov/28118059/"]}
        )
        if patient.gender == "Male":
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Testo&Cortisol",
                        "https://pubmed.ncbi.nlm.nih.gov/21993767/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "DHEAS",
                        "https://pubmed.ncbi.nlm.nih.gov/28118059/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Sex Hormone",
                        "https://pubmed.ncbi.nlm.nih.gov/11942957/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Thyroid Tests",
                        "https://pubmed.ncbi.nlm.nih.gov/30057137/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Cholesterol",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6060264/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Iron",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6283628/",
                    ]
                }
            )
        elif patient.gender == "Female":
            list.append(str(test[41]))
            list.append(str(test[40]))
            list.append(str(test[42]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Hormones 1",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5776161/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Hormones 2",
                        "https://pubmed.ncbi.nlm.nih.gov/36018001/",
                    ]
                }
            )
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()
    if patient.specificanswer5 == "Can't achieve full erection":
        list.append(str(test[35]))
        list.append(str(test[102]))
        list.append(str(test[55]))
        list.append(str(test[59]))
        list.append(str(test[52]))
        list.append(str(test[25]))
        list.append(str(test[24]))
        list.append(str(test[23]))
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()
    elif patient.specificanswer5 == "Can you achieve orgasm":
        list.append(str(test[35]))
        list.append(str(test[102]))
        list.append(str(test[55]))
        list.append(str(test[59]))
        list.append(str(test[23]))
        list.append(str(test[29]))
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()
    elif patient.specificanswer5 == "Do you have premature ejaculation":
        list.append(str(test[35]))
        list.append(str(test[102]))
        list.append(str(test[55]))
        list.append(str(test[59]))
        list.append(str(test[23]))
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()

    if patient.specificanswer7 != "None" and patient.healthgoal == "Sexual Well Being":
        list.append(str(test[66]))
        test_link.append(
            {"GOAL SPECIFIC": ["STI1", "https://www.ncbi.nlm.nih.gov/books/NBK560808/"]}
        )
        test_link.append(
            {
                "GOAL SPECIFIC": [
                    "STI Screening",
                    "https://pubmed.ncbi.nlm.nih.gov/30704656/",
                ]
            }
        )
        test_link.append(
            {
                "GOAL SPECIFIC": [
                    "Bact Infections",
                    "https://pubmed.ncbi.nlm.nih.gov/14974283/",
                ]
            }
        )
        test_link.append(
            {"GOAL SPECIFIC": ["STI2", "https://pubmed.ncbi.nlm.nih.gov/35015033/"]}
        )
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()

    if patient.specificanswer8 == "Yes" and patient.specificanswer7 != "None":
        list.append(str(test[66]))
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()

    if patient.specificanswer9 == "Yes":
        list.append(str(test[4]))
        list.append(str(test[73]))
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()

    if patient.specificanswer10 == "6months to 1 year":
        list.append(str(test[104]))
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()
    if patient.specificanswer10 == "1 year":
        list.append(str(test[67]))
        list.append(str(test[35]))
        list.append(str(test[67]))
        list.append(str(test[104]))
        list.append(str(test[40]))
        list.append(str(test[41]))
        list.append(str(test[42]))
        list.append(str(test[33]))
        if patient.gender == "Male":
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Male Infertility 1",
                        "https://www.ncbi.nlm.nih.gov/books/NBK562258/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Prolactin",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7196164/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Male Infertility 2",
                        "https://pubmed.ncbi.nlm.nih.gov/387166/",
                    ]
                }
            )
        if patient.gender == "Female":
            list.append(str(test[21]))
            list.append(str(test[4]))
            list.append(str(test[13]))
            list.append(str(test[45]))
            list.append(str(test[71]))
            list.append(str(test[42]))
            list.append(str(test[105]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Female Infertility",
                        "hhttps://www.ncbi.nlm.nih.gov/books/NBK556033/#article-23502.s7",
                    ]
                }
            )

        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()

    # SEXUAL FEMALE
    if (patient.specificquestion2 == "When was the last time you got your PAP smear done"):
        if (patient.specificanswer2 == "Never" or patient.specificanswer2 == "More than 3 years back"):
            if patient.age >= 21 and patient.age <= 65:
                list.append(str(test[69]))
                pk_id = request.session.get("pk_id")
                patient = Patient.objects.get(patient_id=pk_id)
                patient.tests = list
                patient.save()

    if patient.historyfemale_answer == "I experience heavy bleeding":
        list.append(str(test[69]))
        list.append(str(test[31]))
        list.append(str(test[21]))
        list.append(str(test[30]))
        list.append(str(test[103]))
        list.append(str(test[55]))
        list.append(str(test[41]))
        list.append(str(test[40]))
        list.append(str(test[70]))
        list.append(str(test[45]))
        list.append(str(test[72]))
        test_link.append(
            {
                "GOAL SPECIFIC": [
                    "Thyroid tests",
                    "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9107865/",
                ]
            }
        )
        test_link.append(
            {"GOAL SPECIFIC": ["Iron", "https://pubmed.ncbi.nlm.nih.gov/36706856/"]}
        )
        test_link.append(
            {
                "GOAL SPECIFIC": [
                    "Menorrhagia 1",
                    "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6142441/",
                ]
            }
        )
        test_link.append(
            {
                "GOAL SPECIFIC": [
                    "Menorrhagia 2",
                    "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1952557/",
                ]
            }
        )
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()

    if patient.historyfemale_answer == "My periods are irregular":
        list.append(str(test[69]))
        list.append(str(test[31]))
        list.append(str(test[21]))
        list.append(str(test[30]))
        list.append(str(test[103]))
        list.append(str(test[55]))
        list.append(str(test[41]))
        list.append(str(test[40]))
        list.append(str(test[70]))
        list.append(str(test[45]))
        list.append(str(test[72]))
        list.append(str(test[33]))
        list.append(str(test[71]))

        test_link.append(
            {
                "GOAL SPECIFIC": [
                    "Thyroid tests",
                    "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5980701/",
                ]
            }
        )
        test_link.append(
            {"GOAL SPECIFIC": ["Iron", "https://pubmed.ncbi.nlm.nih.gov/1820649/"]}
        )
        test_link.append(
            {
                "GOAL SPECIFIC": [
                    "Irregular periods",
                    "https://www.ncbi.nlm.nih.gov/books/NBK560575/",
                ]
            }
        )

        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()

    if patient.historyfemale_answer == "I have menstrual cramps during periods":
        list.append(str(test[69]))
        list.append(str(test[31]))
        list.append(str(test[21]))
        list.append(str(test[30]))
        list.append(str(test[103]))
        list.append(str(test[55]))
        list.append(str(test[41]))
        list.append(str(test[40]))
        list.append(str(test[70]))
        list.append(str(test[45]))
        list.append(str(test[71]))
        list.append(str(test[33]))

        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()

    if patient.historyfemale_answer == "I am pregnant":
        list.append(str(test[74]))
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()
    if (
        patient.historyfemale_answer
        == "My last pregnency ended in past 2 months or I am nursing"
    ):
        list.append(str(test[4]))
        list.append(str(test[52]))
        list.append(str(test[4]))
        list.append(str(test[29]))
        list.append(str(test[42]))
        test_link.append(
            {
                "GOAL SPECIFIC": [
                    "Thyroid tests",
                    "https://pubmed.ncbi.nlm.nih.gov/32562185/",
                ]
            }
        )
        test_link.append(
            {
                "GOAL SPECIFIC": [
                    "Anemia",
                    "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4401847/",
                ]
            }
        )
        test_link.append(
            {"GOAL SPECIFIC": ["Prolactin", "https://pubmed.ncbi.nlm.nih.gov/665730/"]}
        )

        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()
    if (
        patient.historyfemale_answer
        == "My periods stopped on their own  (I had menopause)"
    ):
        list.append(str(test[74]))
        list.append(str(test[21]))
        list.append(str(test[69]))
        list.append(str(test[83]))
        list.append(str(test[102]))
        list.append(str(test[55]))
        list.append(str(test[20]))
        list.append(str(test[40]))
        test_link.append(
            {
                "GOAL SPECIFIC": [
                    "Postmenopause 1",
                    "https://www.ncbi.nlm.nih.gov/books/NBK279131/",
                ]
            }
        )
        test_link.append(
            {
                "GOAL SPECIFIC": [
                    "Postmenopause 2",
                    "https://www.ncbi.nlm.nih.gov/books/NBK560840/",
                ]
            }
        )

        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()

    if patient.specificanswer9 == "Are you planning a family soon":
        list.append(str(test[4]))
        list.append(str(test[73]))
        if patient.gender == "Female":
            list.append(str(test[21]))
            list.append(str(test[43]))
            list.append(str(test[56]))
            list.append(str(test[11]))
            list.append(str(test[30]))
            list.append(str(test[29]))
            list.append(str(test[27]))
            list.append(str(test[13]))
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()

    # ANEMIA
    if patient.question1 == "Have you ever tested your hemoglobin in the past?":
        if patient.answer1 == "No":
            list.append(str(test[2]))
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.tests = list
            patient.save()
    if patient.specificanswer1 == "11-12.9" or patient.specificanswer1 == "11-11.9":
        list.append(str(test[2]))
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()
    elif patient.specificanswer1 == "8-10.9":
        list.append(str(test[3]))
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()
    elif patient.specificanswer1 == "less than 8":
        list.append(str(test[3]))
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()
    if (
        patient.specificquestion3
        == "Do you have anyone in your family who has thallesemia minor"
    ):
        if patient.specificanswer3 == "Yes":
            list.append(str(test[73]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Hb HPLC 1",
                        "https://pubmed.ncbi.nlm.nih.gov/25548455/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Hb HPLC 2",
                        "https://www.ncbi.nlm.nih.gov/books/NBK585044/#article-145922.s6",
                    ]
                }
            )

            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.tests = list
            patient.save()

    # BONE PAIN
    if patient.question1 == "Where is your pain located?":
        if patient.answer1 == "Hip" or patient.answer1 == "Knee":
            list.append(str(test[4]))
            list.append(str(test[7]))
            list.append(str(test[8]))
            list.append(str(test[85]))
            list.append(str(test[114]))
            list.append(str(test[11]))
            list.append(str(test[12]))
            list.append(str(test[13]))
            if patient.age >= 60:
                list.append(str(test[106]))
        elif patient.answer1 == "Joints of fingers and toes":
            list.append(str(test[5]))
            list.append(str(test[12]))
            if patient.age >= 60:
                list.append(str(test[106]))
        elif (
            patient.answer1
            == "Pain and stiffness in lower back and hips, especially in morning"
        ):
            list.append(str(test[4]))
            list.append(str(test[7]))
            list.append(str(test[8]))
            list.append(str(test[85]))
            list.append(str(test[114]))
            list.append(str(test[11]))
            list.append(str(test[12]))
            list.append(str(test[6]))
            if patient.age >= 60:
                list.append(str(test[106]))
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.tests = list
            patient.save()
    # HYPERTENSION
    if patient.question1 == "Do you have?":
        if patient.answer1 == "Diabetes":
            list.append(str(test[22]))
            list.append(str(test[13]))
            list.append(str(test[13]))
            list.append(str(test[24]))
            list.append(str(test[25]))
            list.append(str(test[26]))
            list.append(str(test[27]))
            list.append(str(test[28]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Lipid Profile",
                        "https://pubmed.ncbi.nlm.nih.gov/30200612/",
                    ]
                }
            )
            test_link.append(
                {"GOAL SPECIFIC": ["BUN", "https://pubmed.ncbi.nlm.nih.gov/29241622/ "]}
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Creatinine",
                        "https://pubmed.ncbi.nlm.nih.gov/22195378/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Microalbuminuria",
                        "https://pubmed.ncbi.nlm.nih.gov/31110390/ ",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Urine Routine",
                        "https://pubmed.ncbi.nlm.nih.gov/20222150/",
                    ]
                }
            )
            test_link.append(
                {"GOAL SPECIFIC": ["BSF,PP,more..", "https://rb.gy/susxds"]}
            )

        if patient.answer1 == "Hypertension":
            list.append(str(test[24]))
            list.append(str(test[25]))
            list.append(str(test[26]))
            list.append(str(test[27]))
            list.append(str(test[28]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Microalbuminuria",
                        "https://pubmed.ncbi.nlm.nih.gov/9839284/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Urine Routine",
                        "https://pubmed.ncbi.nlm.nih.gov/34728882/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Creatinine",
                        "https://pubmed.ncbi.nlm.nih.gov/11343443/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Microalbuminuria",
                        "https://pubmed.ncbi.nlm.nih.gov/31110390/ ",
                    ]
                }
            )

        if patient.answer1 == "Both":
            list.append(str(test[15]))

        if patient.answer2 == "10-15 years" or patient.answer2 == " > 15 years":
            list.append(str(test[14]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Cystatin C",
                        "https://pubmed.ncbi.nlm.nih.gov/20885369/",
                    ]
                }
            )

            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.tests = list
            patient.save()

    # SLEEP AND MOOD
    if patient.question1 == "How often do you have trouble falling or staying asleep?":
        subg.append("SLEEP")
        if patient.answer1 == "Often" or patient.answer1 == "Everyday":
            list.append(str(test[11]))
            list.append(str(test[53]))
            list.append(str(test[54]))
            list.append(str(test[43]))
            list.append(str(test[38]))
            list.append(str(test[39]))
            list.append(str(test[94]))
            list.append(str(test[29]))
            list.append(str(test[55]))
            test_link.append(
                {"GOAL SPECIFIC": ["CRP", "https://pubmed.ncbi.nlm.nih.gov/14975482/"]}
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Micronutrients",
                        "https://pubmed.ncbi.nlm.nih.gov/31581561/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Hormones",
                        "https://pubmed.ncbi.nlm.nih.gov/23092405/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Omega",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8262633/",
                    ]
                }
            )

            if patient.gender == "Female":
                list.append(str(test[45]))
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.tests = list
            patient.save()
    if patient.question2 == "Do you take anything to help you sleep":
        if patient.answer2 == "Medication" or patient.answer2 == "Any other":
            list.append(str(test[11]))
            list.append(str(test[53]))
            list.append(str(test[54]))
            list.append(str(test[43]))
            list.append(str(test[38]))
            list.append(str(test[39]))
            list.append(str(test[94]))
            list.append(str(test[29]))
            list.append(str(test[55]))
            test_link.append(
                {"GOAL SPECIFIC": ["CRP", "https://pubmed.ncbi.nlm.nih.gov/14975482/"]}
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Micronutrients",
                        "https://pubmed.ncbi.nlm.nih.gov/31581561/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Hormones",
                        "https://pubmed.ncbi.nlm.nih.gov/23092405/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Omega",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8262633/",
                    ]
                }
            )
            if patient.gender == "Female":
                list.append(str(test[45]))
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.tests = list
            patient.save()
    if (
        patient.specificquestion2
        == "Do you have any unusual behavior/ movements during sleep?"
    ):
        if patient.specificanswer2 == "Often" or patient.specificanswer2 == "Everyday":
            list.append(str(test[23]))
            list.append(str(test[29]))
            list.append(str(test[30]))
            list.append(str(test[59]))
            list.append(str(test[4]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "HbA1c",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5628550/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Iron/Ferritin",
                        "https://pubmed.ncbi.nlm.nih.gov/32713229/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "CBC",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8474608/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Omega",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8262633/",
                    ]
                }
            )

            if patient.gender == "Female":
                list.append(str(test[45]))
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.tests = list
            patient.save()
    if patient.specificquestion3 == "Do you snore during sleep?":
        if patient.specificanswer3 == "Often" or patient.specificanswer2 == "Everyday":
            list.append(str(test[85]))
            list.append(str(test[4]))
            test_link.append(
                {"GOAL SPECIFIC": ["CBC", "https://pubmed.ncbi.nlm.nih.gov/25126033/"]}
            )

            if patient.gender == "Female":
                list.append(str(test[45]))
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.tests = list
            patient.save()

    if (
        patient.specificquestion5
        == "Do you have difficulty in staying awake during the day?"
    ):
        if patient.specificanswer5 == "Often" or patient.specificanswer5 == "Everyday":
            list.append(str(test[11]))
            list.append(str(test[53]))
            list.append(str(test[54]))
            list.append(str(test[43]))
            list.append(str(test[38]))
            list.append(str(test[39]))
            list.append(str(test[94]))
            list.append(str(test[29]))
            list.append(str(test[55]))
            test_link.append(
                {"GOAL SPECIFIC": ["CRP", "https://pubmed.ncbi.nlm.nih.gov/14975482/"]}
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Micronutrients",
                        "https://pubmed.ncbi.nlm.nih.gov/31581561/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Hormones",
                        "https://pubmed.ncbi.nlm.nih.gov/23092405/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Omega",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8262633/",
                    ]
                }
            )

            if patient.gender == "Female":
                list.append(str(test[45]))
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.tests = list
            patient.save()
    if (
        patient.specificquestion6
        == "Are your legs restless or uncomfortable before bed?"
    ):
        if patient.specificanswer6 == "Often" or patient.specificanswer6 == "Everyday":
            list.append(str(test[23]))
            list.append(str(test[29]))
            list.append(str(test[30]))
            list.append(str(test[59]))
            list.append(str(test[4]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "HbA1c",
                        "https://pubmed.ncbi.nlm.nih.gov/25216659/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "CBC, Creatinine and Micronutrients",
                        "https://www.ncbi.nlm.nih.gov/books/NBK430878/",
                    ]
                }
            )

            if patient.gender == "Female":
                list.append(str(test[45]))
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.tests = list
            patient.save()

    if (
        patient.specificquestion7
        == "How often do you wake to urinate 2 or more times at night"
    ):
        if patient.specificanswer7 == "Often" or patient.specificanswer7 == "Everyday":
            list.append(str(test[23]))
            list.append(str(test[83]))
            list.append(str(test[85]))
            list.append(str(test[4]))
            list.append(str(test[27]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "HbA1c",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4478581/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "PCA",
                        "https://www.ncbi.nlm.nih.gov/books/NBK557495/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Urine Tests",
                        "https://www.ncbi.nlm.nih.gov/books/NBK518987/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Calcium",
                        "https://pubmed.ncbi.nlm.nih.gov/35323672/",
                    ]
                }
            )

            if patient.age >= 50:
                list.append(str(test[60]))
            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.tests = list
            patient.save()

    if (
        patient.specificquestion8
        == "How likely are you to doze off or fall asleep in following situations:"
    ):
        list.append(str(test[11]))
        list.append(str(test[53]))
        list.append(str(test[54]))
        list.append(str(test[43]))
        list.append(str(test[38]))
        list.append(str(test[39]))
        list.append(str(test[94]))
        list.append(str(test[29]))
        list.append(str(test[55]))
        if patient.gender == "Female":
            list.append(str(test[45]))
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()
    if patient.subgoal == "Mood":
        subg.append("MOOD")
        list.append(str(test[4]))
        list.append(str(test[52]))
        list.append(str(test[50]))
        list.append(str(test[85]))
        list.append(str(test[43]))
        list.append(str(test[55]))
        list.append(str(test[25]))
        list.append(str(test[24]))
        list.append(str(test[62]))
        list.append(str(test[64]))
        list.append(str(test[23]))
        list.append(str(test[59]))
        list.append(str(test[38]))
        list.append(str(test[58]))
        test_link.append(
            {"GOAL SPECIFIC": ["CBC", "https://pubmed.ncbi.nlm.nih.gov/28697416/"]}
        )
        test_link.append(
            {
                "GOAL SPECIFIC": [
                    "Thyroid tests",
                    "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3246784/",
                ]
            }
        )
        test_link.append(
            {"GOAL SPECIFIC": ["Anti TPO", "https://pubmed.ncbi.nlm.nih.gov/15317653/"]}
        )
        test_link.append(
            {
                "GOAL SPECIFIC": [
                    "Macronutrients",
                    "https://pubmed.ncbi.nlm.nih.gov/17723028/",
                ]
            }
        )
        test_link.append(
            {"GOAL SPECIFIC": ["Lactate", "https://pubmed.ncbi.nlm.nih.gov/29726068/"]}
        )
        test_link.append(
            {"GOAL SPECIFIC": ["LFT", "https://pubmed.ncbi.nlm.nih.gov/27171561/"]}
        )
        test_link.append(
            {"GOAL SPECIFIC": ["HbA1c", "https://pubmed.ncbi.nlm.nih.gov/31352032/"]}
        )
        test_link.append(
            {
                "GOAL SPECIFIC": [
                    "Cholesterol",
                    "https://pubmed.ncbi.nlm.nih.gov/15013029/",
                ]
            }
        )
        test_link.append(
            {
                "GOAL SPECIFIC": [
                    "Homocysteine",
                    "https://pubmed.ncbi.nlm.nih.gov/32304285/",
                ]
            }
        )
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()

    # PCOS
    if patient.question1 == "Are you facing any of the following issues:":
        q = patient.answer1
        tr = q.split(",")
        count = len(tr)

        if count > 2:
            if "Irregular Periods" in patient.answer1:
                list.append(str(test[1]))
            else:
                list.append(str(test[3]))
        elif count <= 2:
            list.append(str(test[0]))

        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()
    # POST COVID
    if patient.question2 == "Do you have any of the following?":
        q = patient.answer2
        tr = q.split(",")
        count1 = len(tr)
        if count1 < 2:
            list.append(str(test[16]))
            print(list)
        elif count1 >= 2 and count1 <= 3:
            list.append(str(test[17]))
        elif count1 >= 3:
            list.append(str(test[17]))
            list.append(str(test[83]))
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()

    # DEFAULT
    if (
        patient.healthgoal == "Specific Conditions"
        or patient.healthgoal == "Weight"
        or patient.healthgoal == "Fitness"
        or patient.healthgoal == "Ensure Well Being"
    ):
        # AGE AND GENDER
        if patient.age < 18 and patient.gender == "Female":
            subg.append("AGE & GENDER")
            list.append(str(test[112]))
            list.append(str(test[29]))
            list.append(str(test[30]))
            test_link.append(
                {
                    "AGE & GENDER": [
                        "Iron Level",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5620749/",
                    ]
                }
            )
        if patient.age > 18 and patient.age < 50 and patient.gender == "Female":
            subg.append("AGE & GENDER")
            list.append(str(test[112]))
            list.append(str(test[29]))
            list.append(str(test[30]))
            test_link.append(
                {
                    "AGE & GENDER": [
                        "Iron Deficiency",
                        "https://pubmed.ncbi.nlm.nih.gov/29582845/",
                    ]
                }
            )
        if patient.age > 50 and patient.gender == "Female":
            subg.append("AGE & GENDER")
            list.append(str(test[85]))
            list.append(str(test[86]))
            list.append(str(test[23]))
            test_link.append(
                {
                    "AGE & GENDER": [
                        "Calcium and Vitamin D",
                        "https://pubmed.ncbi.nlm.nih.gov/23077993/",
                    ]
                }
            )
        if patient.age > 50 and patient.gender == "Male":
            subg.append("AGE & GENDER")
            list.append(str(test[23]))
            list.append(str(test[60]))
            test_link.append(
                {
                    "AGE & GENDER": [
                        "HbA1c",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4525769/ ",
                    ]
                }
            )
            test_link.append(
                {"AGE & GENDER": ["PSA", "https://pubmed.ncbi.nlm.nih.gov/7693980/"]}
            )

        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()
        # BMI
        if patient.bmi < 18.5:
            list.append(str(test[113]))
            list.append(str(test[23]))
            list.append(str(test[112]))
            list.append(str(test[43]))
            list.append(str(test[29]))
            list.append(str(test[30]))
            list.append(str(test[85]))
            list.append(str(test[114]))
        elif patient.bmi > 25:
            list.append(str(test[113]))
            list.append(str(test[23]))
            list.append(str(test[34]))
            list.append(str(test[77]))
            list.append(str(test[82]))
            list.append(str(test[55]))
            list.append(str(test[85]))
            if patient.gender == "Male":
                list.append(str(test[35]))
                list.append(str(test[104]))
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()

        # FOOD
        if patient.diet_answer == "veg":
            subg.append("DIET")
            list.append(str(test[43]))
            list.append(str(test[11]))
            list.append(str(test[85]))
            list.append(str(test[29]))
            list.append(str(test[39]))
            test_link.append(
                {"DIET": ["Vitamin B12", "https://pubmed.ncbi.nlm.nih.gov/24667752/"]}
            )
            test_link.append(
                {"DIET": ["Vitamin D", "https://pubmed.ncbi.nlm.nih.gov/25098082/"]}
            )
            test_link.append(
                {
                    "DIET": [
                        "Calcium",
                        "https://www.frontiersin.org/articles/10.3389/fendo.2022.899375/full",
                    ]
                }
            )
            test_link.append(
                {
                    "DIET": [
                        "Iron",
                        "https://onlinelibrary.wiley.com/doi/10.1002/jsfa.6179",
                    ]
                }
            )

        elif patient.diet_answer == "nonveg":
            subg.append("DIET")
            list.append(str(test[26]))
            list.append(str(test[92]))
            list.append(str(test[23]))
            list.append(str(test[43]))
            list.append(str(test[87]))
            test_link.append(
                {
                    "DIET": [
                        "Lipid",
                        "https://go.gale.com/ps/i.do?id=GALE%7CA471274916&sid=googleScholar&v=2.1&it=r&linkaccess=abs&issn=22784748&p=AONE&sw=w&userGroupName=anon%7E382fe327",
                    ]
                }
            )
            test_link.append(
                {
                    "DIET": [
                        "Hba1c",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6153574/",
                    ]
                }
            )

        elif patient.diet_answer == "Gluten Free":
            subg.append("DIET")
            list.append(str(test[26]))
            list.append(str(test[92]))
            list.append(str(test[23]))
            list.append(str(test[43]))
            list.append(str(test[87]))
            test_link.append(
                {"DIET": ["Vitamin D", "https://www.mdpi.com/2218-1989/13/1/74"]}
            )
            test_link.append(
                {
                    "DIET": [
                        "Micronutrients",
                        "https://linkinghub.elsevier.com/retrieve/pii/S0261561416300887",
                    ]
                }
            )

        elif patient.diet_answer == "Keto":
            subg.append("DIET")
            list.append(str(test[11]))
            list.append(str(test[53]))
            list.append(str(test[93]))
            list.append(str(test[94]))
            list.append(str(test[29]))
            list.append(str(test[85]))
            list.append(str(test[38]))
            test_link.append(
                {"DIET": ["Vitamin D", "https://pubmed.ncbi.nlm.nih.gov/36557329/"]}
            )

        elif patient.diet_answer == "High Protien":
            subg.append("DIET")
            list.append(str(test[83]))
            list.append(str(test[93]))
            list.append(str(test[94]))
            list.append(str(test[114]))
            list.append(str(test[55]))
            list.append(str(test[23]))
            test_link.append(
                {
                    "DIET": [
                        "High Protien",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4045293/",
                    ]
                }
            )

        # DRINKING ANSWER
        if patient.drinking_answer == "I drink everyday":
            subg.append("DRINKING")
            list.append(str(test[26]))
            list.append(str(test[83]))
            list.append(str(test[23]))
            list.append(str(test[13]))
            list.append(str(test[108]))
            list.append(str(test[109]))
            list.append(str(test[110]))
            list.append(str(test[111]))
            test_link.append(
                {
                    "DRINKING": [
                        "LFT",
                        "https://academic.oup.com/alcalc/article/44/2/199/184610",
                    ]
                }
            )
            test_link.append(
                {"DRINKING": ["Amy,Lip..", "https://pubmed.ncbi.nlm.nih.gov/28431198/"]}
            )
            test_link.append(
                {
                    "DRINKING": [
                        "Vitamin A",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3367262/",
                    ]
                }
            )
            test_link.append(
                {"DRINKING": ["Folate", "https://pubmed.ncbi.nlm.nih.gov/35565159/"]}
            )

        elif patient.drinking_answer == "3-6 days a week.":
            subg.append("DRINKING")
            list.append(str(test[26]))
            list.append(str(test[23]))
            list.append(str(test[13]))
            list.append(str(test[108]))
            list.append(str(test[109]))
            list.append(str(test[20]))
            test_link.append(
                {
                    "DRINKING": [
                        "LFT",
                        "https://academic.oup.com/alcalc/article/44/2/199/184610",
                    ]
                }
            )
            test_link.append(
                {"DRINKING": ["Amy,Lip..", "https://pubmed.ncbi.nlm.nih.gov/28431198/"]}
            )
        elif patient.drinking_answer == "1-3 days a week":
            subg.append("DRINKING")
            list.append(str(test[23]))
            list.append(str(test[20]))
            test_link.append(
                {
                    "DRINKING": [
                        "LFT",
                        "https://academic.oup.com/alcalc/article/44/2/199/184610",
                    ]
                }
            )

        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.testlink = test_link
        patient.save()

        # WORKOUT
        if patient.workout_answer == "Don't remember last time I worked out":
            subg.append("WORKOUT")
            list.append(str(test[23]))
            list.append(str(test[26]))
            list.append(str(test[92]))
            list.append(str(test[87]))
            test_link.append(
                {"WORKOUT": ["HS CRP", "https://pubmed.ncbi.nlm.nih.gov/21602429/"]}
            )
            test_link.append(
                {"WORKOUT": ["Lipid", "https://pubmed.ncbi.nlm.nih.gov/35355910/"]}
            )
            test_link.append(
                {
                    "WORKOUT": [
                        "Lipid profile",
                        "https://pubmed.ncbi.nlm.nih.gov/26256803/",
                    ]
                }
            )
            test_link.append(
                {"WORKOUT": ["HbA1c", "https://pubmed.ncbi.nlm.nih.gov/31756287/"]}
            )

        elif patient.workout_answer == "1 hour of more, less than 2 days a week":
            subg.append("WORKOUT")
            list.append(str(test[23]))
            list.append(str(test[26]))
            list.append(str(test[92]))
            list.append(str(test[87]))
            test_link.append(
                {"WORKOUT": ["HS CRP", "https://pubmed.ncbi.nlm.nih.gov/21602429/"]}
            )
            test_link.append(
                {"WORKOUT": ["Lipid", "https://pubmed.ncbi.nlm.nih.gov/35355910/"]}
            )
            test_link.append(
                {
                    "WORKOUT": [
                        "Lipid profile",
                        "https://pubmed.ncbi.nlm.nih.gov/26256803/",
                    ]
                }
            )
            test_link.append(
                {"WORKOUT": ["HbA1c", "https://pubmed.ncbi.nlm.nih.gov/31756287/"]}
            )

        elif (
            patient.workout_answer == "1 hour of more daily"
            or patient.workout_answer == "1 hour of more, 3 days a week"
        ):
            subg.append("WORKOUT")
            list.append(str(test[83]))
            list.append(str(test[11]))
            list.append(str(test[85]))
            test_link.append(
                {
                    "WORKOUT": [
                        "Vitamin D",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7071499/",
                    ]
                }
            )
            test_link.append(
                {"WORKOUT": ["KFT", "https://pubmed.ncbi.nlm.nih.gov/6567229/"]}
            )
            test_link.append(
                {
                    "WORKOUT": [
                        "Calcium",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4535115/",
                    ]
                }
            )

        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()
    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    patient.tests = list
    patient.save()

    # GUT IMPROVEMENT
    if (
        patient.question1
        == "Which of the following symptoms best describe your problem?"
    ):
        if patient.answer1 == "Gastritis/ Acidity/ GERD":
            list.append(str(test[80]))
            list.append(str(test[115]))
            list.append(str(test[128]))
            test_link.append(
                {"GOAL SPECIFIC": ["FIT", "https://pub med.ncbi.nlm.nih.gov/28884564/"]}
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Dyspepsia",
                        "https://pubmed.ncbi.nlm.nih.gov/22327302/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Fecal Fat",
                        "https://pubmed.ncbi.nlm.nih.gov/35368458/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Multiple",
                        "https://pubmed.ncbi.nlm.nih.gov/28095460/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Stool Analysis",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2780157/",
                    ]
                }
            )

        elif patient.answer1 == "Constipation":
            list.append(str(test[80]))
            list.append(str(test[115]))
            list.append(str(test[38]))
            list.append(str(test[11]))
            list.append(str(test[39]))
            list.append(str(test[115]))
            list.append(str(test[128]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Magnesium",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8645769/",
                    ]
                }
            )

        elif patient.answer1 == "Diarrhoea less than 1week":
            list.append(str(test[4]))
            list.append(str(test[8]))
            list.append(str(test[116]))
            list.append(str(test[117]))
            list.append(str(test[116]))
            list.append(str(test[93]))
            list.append(str(test[94]))
            list.append(str(test[118]))
            list.append(str(test[119]))
            list.append(str(test[120]))
            list.append(str(test[128]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Diarrhea",
                        "https://www.ncbi.nlm.nih.gov/books/NBK448082/",
                    ]
                }
            )

        elif patient.answer1 == "Diarrhoea more than 1 week":
            list.append(str(test[4]))
            list.append(str(test[8]))
            list.append(str(test[116]))
            list.append(str(test[117]))
            list.append(str(test[116]))
            list.append(str(test[93]))
            list.append(str(test[94]))
            list.append(str(test[118]))
            list.append(str(test[85]))
            list.append(str(test[11]))
            list.append(str(test[43]))
            list.append(str(test[56]))
            list.append(str(test[29]))
            list.append(str(test[30]))
            list.append(str(test[128]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Diarrhea",
                        "https://www.ncbi.nlm.nih.gov/books/NBK448082/",
                    ]
                }
            )

            if patient.age > 50:
                list.append(str(test[121]))
                list.append(str(test[122]))

        elif patient.answer1 == "Alternating diarrhoea and constipation":
            list.append(str(test[78]))
            list.append(str(test[128]))
            list.append(str(test[130]))
            list.append(str(test[4]))
            list.append(str(test[8]))
            list.append(str(test[7]))
            list.append(str(test[115]))
            test_link.append(
                {"GOAL SPECIFIC": ["IBD", "https://pubmed.ncbi.nlm.nih.gov/11474909/"]}
            )
            test_link.append(
                {
                    "ANTI TTG": [
                        "IBD",
                        "https://www.sciencedirect.com/science/article/pii/S2237936319301017#:~:text=The%20prevalence%20of%20anti%20tTG%20antibodies%20among%20patients%20with%20IBS,CD%20in%20IBS%20patients%20histologically.",
                    ]
                }
            )
            test_link.append(
                {"GOAL SPECIFIC": ["EMGL", "https://pubmed.ncbi.nlm.nih.gov/23885406/"]}
            )

        elif patient.answer1 == "Nausea/ vomiting":
            list.append(str(test[115]))
            list.append(str(test[109]))
            list.append(str(test[20]))
            list.append(str(test[108]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "FIT",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8152468/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "LFT",
                        "https://www.ncbi.nlm.nih.gov/books/NBK482489/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Amylase",
                        "https://www.ncbi.nlm.nih.gov/books/NBK557738/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Lipase",
                        "https://www.ncbi.nlm.nih.gov/books/NBK537346/",
                    ]
                }
            )

        elif patient.answer1 == "Bloating/ Flatulance / Gas":
            list.append(str(test[115]))
            list.append(str(test[78]))
            list.append(str(test[128]))
            list.append(str(test[130]))

        elif (
            patient.answer1
            == "Trouble digesting fatty food/ uneasy feeling after fatty meal"
        ):
            list.append(str(test[109]))
            list.append(str(test[123]))
            list.append(str(test[124]))
            list.append(str(test[20]))
            list.append(str(test[128]))
            list.append(str(test[110]))
        elif (
            patient.answer1
            == "Irritable bowel syndrome/ Irritable bowel disease/ know more"
        ):
            list.append(str(test[115]))
            list.append(str(test[125]))
            list.append(str(test[126]))
            list.append(str(test[8]))
            list.append(str(test[128]))

        pk_id = request.session.get("pk_id")
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()

    if patient.question2 == "Please choose any of the following FIT profiles":
        if patient.answer2 == "Profile 1":
            list.append(str(test[132]))
        elif patient.answer2 == "Profile 2":
            list.append(str(test[133]))
        elif patient.answer2 == "Profile 3":
            list.append(str(test[134]))
        elif patient.answer2 == "Profile 4":
            list.append(str(test[135]))
        elif patient.answer2 == "Profile 5":
            list.append(str(test[136]))
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list
        patient.save()

    # WEIGHT & FTINESS
    if patient.question2 == "How would you describe your energy levels?":
        if patient.answer2 != "I feel energrtic all day":
            subg.append("ENERGY LEVELS")
            list.append(str(test[4]))
            list.append(str(test[101]))
            list.append(str(test[21]))
            list.append(str(test[23]))
            test_link.append(
                {"FITNESS": ["Fatigue", "https://www.cmaj.ca/content/174/6/765 "]}
            )

            pk_id = request.session.get("pk_id")
            patient = Patient.objects.get(patient_id=pk_id)
            patient.tests = list
            patient.save()

    if patient.question1 == "What is your main concern?":
        if patient.answer1 == "I want to reduce my weight":
            subg.append("WEIGHT")
            list.append(str(test[77]))
            list.append(str(test[53]))
            list.append(str(test[21]))
            test_link.append(
                {"WEIGHT": ["Leptin", "https://pubmed.ncbi.nlm.nih.gov/21460597/"]}
            )
            test_link.append(
                {
                    "WEIGHT": [
                        "Cortisol",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4570173/",
                    ]
                }
            )
            test_link.append(
                {
                    "WEIGHT": [
                        "Thyroid",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3821486/",
                    ]
                }
            )

        elif patient.answer1 == "I want to increase my weight":
            subg.append("WEIGHT")
            list.append(str(test[127]))
            list.append(str(test[77]))
            test_link.append(
                {"WEIGHT": ["Leptin", "https://pubmed.ncbi.nlm.nih.gov/21460597/"]}
            )
            test_link.append(
                {
                    "WEIGHT": [
                        "CBC",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3237273/",
                    ]
                }
            )

        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list

    if (
        patient.question2
        == "Do you or a blood relation suffer from any of the following?"
    ):
        subg.append("BLOOD RELATION")

        if "Diabetes" in patient.answer2:
            list.append(str(test[23]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Diabetes",
                        "https://pubmed.ncbi.nlm.nih.gov/27398023/",
                    ]
                }
            )

        if "Hypertension" in patient.answer2:
            list.append(str(test[26]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Hyperten..",
                        "https://pubmed.ncbi.nlm.nih.gov/17344784/",
                    ]
                }
            )

        if "Heart Disease" in patient.answer2:
            list.append(str(test[82]))
            list.append(str(test[87]))
            list.append(str(test[92]))
            list.append(str(test[97]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Lipid profile",
                        "https://pubmed.ncbi.nlm.nih.gov/29045483/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Pro BNP",
                        "https://pubmed.ncbi.nlm.nih.gov/23470072//",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "LipoA",
                        "https://pubmed.ncbi.nlm.nih.gov/33236085/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "HS CRP",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4669860/",
                    ]
                }
            )

        if "High Cholesterol" in patient.answer2:
            list.append(str(test[82]))
            list.append(str(test[92]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Cholesterol",
                        "https://www.ncbi.nlm.nih.gov/books/NBK542294/",
                    ]
                }
            )
            test_link.append(
                {"GOAL SPECIFIC": ["Lipo", "https://pubmed.ncbi.nlm.nih.gov/34196811/"]}
            )

        if "Kidney Disease" in patient.answer2:
            list.append(str(test[83]))
            list.append(str(test[28]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "KFT",
                        "https://www.ncbi.nlm.nih.gov/books/NBK507821/",
                    ]
                }
            )

        if "Asthma" in patient.answer2:
            list.append(str(test[99]))

        if "Bleeding Disorders" in patient.answer2:
            list.append(str(test[72]))
            list.append(str(test[100]))

        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list

    # HISTORY
    if (
        patient.history_question
        == "Do you or a blood relation have any of the following conditions/complaints?"
    ):
        subg.append("BLOOD RELATION")

        if "Diabetes" in patient.history_answer:
            list.append(str(test[23]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Diabetes",
                        "https://pubmed.ncbi.nlm.nih.gov/27398023/",
                    ]
                }
            )

        if "Hypertension" in patient.history_answer:
            list.append(str(test[26]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Hypertension",
                        "https://pubmed.ncbi.nlm.nih.gov/17344784/",
                    ]
                }
            )

        if (
            "Hypertension" in patient.history_answer
            and "Diabetes" in patient.history_answer
        ):
            list.append(str(test[15]))

        if "Heart Disease" in patient.history_answer:
            list.append(str(test[82]))
            list.append(str(test[87]))
            list.append(str(test[92]))
            list.append(str(test[97]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Lipid profile",
                        "https://pubmed.ncbi.nlm.nih.gov/29045483/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Pro BNP",
                        "https://pubmed.ncbi.nlm.nih.gov/23470072//",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "LipoA",
                        "https://pubmed.ncbi.nlm.nih.gov/33236085/",
                    ]
                }
            )
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "HS CRP",
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4669860/",
                    ]
                }
            )

        if "High Cholesterol" in patient.history_answer:
            list.append(str(test[82]))
            list.append(str(test[92]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "Cholesterol",
                        "https://www.ncbi.nlm.nih.gov/books/NBK542294/",
                    ]
                }
            )
            test_link.append(
                {"GOAL SPECIFIC": ["Lipo", "https://pubmed.ncbi.nlm.nih.gov/34196811/"]}
            )

        if "Kidney Disease" in patient.history_answer:
            list.append(str(test[83]))
            list.append(str(test[28]))
            test_link.append(
                {
                    "GOAL SPECIFIC": [
                        "KFT",
                        "https://www.ncbi.nlm.nih.gov/books/NBK507821/",
                    ]
                }
            )

        if "Asthma" in patient.answer2:
            list.append(str(test[99]))

        if "Bleeding Disorders" in patient.history_answer:
            list.append(str(test[72]))
            list.append(str(test[100]))

        if "Bone Pain" in patient.history_answer:
            list.append(str(test[5]))

        if "PCOS" in patient.history_answer:
            list.append(str(test[0]))

        if "Anemia" in patient.history_answer:
            list.append(str(test[2]))

        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list

    # ENSURE WELL BEING

    if (
        patient.specificquestion1
        == "Do you have any of the following sleep related issues?"
    ):
        if patient.specificanswer1 == "Snoring":
            list.append(str(test[26]))

        elif patient.specificanswer1 == "Day time sleepines":
            list.append(str(test[11]))
            list.append(str(test[53]))
            list.append(str(test[54]))
            list.append(str(test[43]))
            list.append(str(test[38]))
            list.append(str(test[39]))
            list.append(str(test[94]))
            list.append(str(test[29]))
            list.append(str(test[55]))

            if patient.gender == "Female":
                list.append(str(test[45]))

        elif (
            patient.specificanswer1 == "Restlessness or discomfort in legs before sleep"
        ):
            list.append(str(test[23]))
            list.append(str(test[29]))
            list.append(str(test[30]))
            list.append(str(test[59]))
            list.append(str(test[4]))

            if patient.gender == "Female":
                list.append(str(test[45]))

        elif patient.specificanswer1 == "Need to urinate 2 or more times at night":
            list.append(str(test[23]))
            list.append(str(test[83]))
            list.append(str(test[85]))
            list.append(str(test[4]))
            list.append(str(test[27]))
            list.append(str(test[0]))
            print(test[0].test_price)
            if patient.age >= 50:
                list.append(str(test[60]))
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests = list

    # TESTS ENDING

    pk_id = request.session.get("pk_id")
    patient = Patient.objects.get(patient_id=pk_id)
    list2 = set(list)
    list3 = []
    # CALCULATING PRICE LIST
    final_price = []
    for i in set(list2):
        price = Test.objects.get(test=i)
        final_price.append(price.test_price)

    x = len(list2)
    sumf = sum(final_price)
    if sumf <= 5000:
        dprice = 0.05 * sumf
        dfinal = sumf - dprice
    elif sumf > 5000 and sumf < 10000:
        dprice = 0.07 * sumf
        dfinal = sumf - dprice
    elif sumf > 10000 and sumf < 15000:
        dprice = 0.09 * sumf
        dfinal = sumf - dprice
    elif sumf > 15000 and sumf < 20000:
        dprice = 0.11 * sumf
        dfinal = sumf - dprice
    else:
        dprice = 0.12 * sumf
        dfinal = sumf - dprice

    if "Vitamin and Mineral Profile" in list2:
        list2.discard("Iron")
        list2.discard("Vitamin B12")
        list2.discard("Vitamin A")
        list2.discard("Ca (Ionized)")
        list2.discard("Ca (Total)")
        list2.discard("Phosphorus")
        list2.discard("Folic Acid ")
        list2.discard("Magnesium")
        list2.discard("Ferritin")
        list2.discard("Zinc")
        list2.discard("Vitamin D")
    if "Basic PCOS Profile" in list2:
        list2.discard("FSH")
        list2.discard("LH")
        list2.discard("Prolactin")
        list2.discard("Estrogen")
        list2.discard("Progesterone")
        list2.discard("AMH")
        list2.discard("Thyroid Profile")
        list2.discard("DHEAS")

    if "Advanced PCOS Profile" in list2:
        list2.discard("HbA1C")
        list2.discard("LH")
        list2.discard("Prolactin")
        list2.discard("Estrogen")
        list2.discard("Progesterone")
        list2.discard("AMH")
        list2.discard("Thyroid Profile")
        list2.discard("Total Testosterone")
        list2.discard("Free Testosterone")
        list2.discard("Thyroid Profile")
        list2.discard("DHEAS")

    if "Arthritis Profile" in list2:
        list2.discard("CBC")
        list2.discard("ESR")
        list2.discard("CRP")
        list2.discard("Ca (Total)")
        list2.discard("Ca (Ionized)")
        list2.discard("Phosphorus")
        list2.discard("Vitamin D")
    if "Diabetes and Hypertension Profile" in list2:
        list2.discard("Blood Glucose Fasting")
        list2.discard("Blood Glucose PP")
        list2.discard("HbA1C")
        list2.discard("Urea")
        list2.discard("BUN")
        list2.discard("Lipid Profile")
        list2.discard("Urine Routine")
        list2.discard("Creatinine")
        list2.discard("Cystatin C")

    if "Kidney Function Test" in list2:
        list2.discard("Urea")
        list2.discard("BUN")
        list2.discard("Creatinine")
        list2.discard("Uric Acid")
        list2.discard("Phosphorus")
        list2.discard("Potassium")
        list2.discard("Chloride")
        list2.discard("Ca (Total)")
        list2.discard("Ca (Ionized)")

    if "Extended KFT" in list2:
        list2.discard("Urea")
        list2.discard("BUN")
        list2.discard("Creatinine")
        list2.discard("Uric Acid")
        list2.discard("Potassium")
        list2.discard("Phosphorus")
        list2.discard("Chloride")
        list2.discard("Ca (Total)")
        list2.discard("Ca (Ionized)")
        list2.discard("Phosphorus")
        list2.discard("Amylase")
        list2.discard("Kidney Function Test")

    if "Lipid Profile" in list2:
        list2.discard("Cholesterol")

    if "Extended Lipid Profile" in list2:
        list2.discard("Cholesterol")
        list2.discard("Lipid Profile")
        list2.discard("Homocystine")
        list2.discard("Lipoprotien (a)")

    if patient.question2 == "Please choose any of the following FIT profiles":
        if "FIT" in list2:
            list2.discard("FIT")

    if "Urea" in list2:
        if "BUN" in list2:
            list2.discard("Urea")
        else:
            pass

    if "Thyroid Profile" in list2:
        list2.discard("TSH")

    if "Irregular Periods" in patient.answer1:
        test_link.append(
            {
                "GOAL SPECIFIC": [
                    "PROFILE",
                    "https://www.ncbi.nlm.nih.gov/books/NBK560575/",
                ]
            }
        )

    if "Acne" in patient.answer1:
        test_link.append(
            {
                "GOAL SPECIFIC": [
                    "PROFILE",
                    "https://www.ncbi.nlm.nih.gov/books/NBK459173/",
                ]
            }
        )

    if "Extra hair growth on your face or body (hirsuitism)" in patient.answer1:
        test_link.append(
            {
                "GOAL SPECIFIC": [
                    "PROFILE",
                    "https://www.ncbi.nlm.nih.gov/books/NBK470417/",
                ]
            }
        )

    if "skin darkening (neck, groin, under the breasts)" in patient.answer1:
        test_link.append(
            {
                "GOAL SPECIFIC": [
                    "PROFILE",
                    "https://www.ncbi.nlm.nih.gov/books/NBK431057/",
                ]
            }
        )

    if patient.subgoal == "Anemia":
        test_link.append(
            {
                "GOAL SPECIFIC": [
                    "Anemia screening",
                    "https://www.ncbi.nlm.nih.gov/books/NBK499905/",
                ]
            }
        )
        test_link.append(
            {
                "GOAL SPECIFIC": [
                    "Diag workups",
                    "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7429725/",
                ]
            }
        )

    for i in set(list2):
        test_obj_name = Test.objects.get(test=i)
        list3.append(test_obj_name)

    keys_list = []
    values_list = []
    for j in test_link:
        for k in j:
            keys_list.append(k)
            values_list.append(j.get(k))


    encoder_of_url(patient.number,list3,"Next Date")        
    print("keys_list",keys_list)
    print("values_list",values_list)

    if "answer1" in request.POST:
        answer1 = request.POST["answer1"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.buttons_clear = answer1
        patient.save()

    if "answer2" in request.POST:
        answer2 = request.POST["answer2"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.healthgoal_clear = answer2
        patient.save()

    if "answer3" in request.POST:
        answer3 = request.POST["answer3"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.tests_clear = answer3
        patient.save()

    if "answer4" in request.POST:
        answer4 = request.POST["answer4"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.questions_clear = answer4
        patient.save()

    if "answer5" in request.POST:
        answer5 = request.POST["answer5"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.rating = answer5
        patient.save()

    if "comments" in request.POST:
        comments = request.POST["comments"]
        pk_id = request.session.get("pk_id")
        patient = Patient.objects.get(patient_id=pk_id)
        patient.comments = comments
        patient.save()

    if "submit" in request.POST:
        return redirect("home")

    return render(
        request,
        "result.html",
        {
            "patient_answer1": patient.answer1,
            # "list": list2,
            "list": list3,
            "patient_gender": patient.gender,
            "patient_name": patient.name,
            "patient_age": patient.age,
            "x": x,
            "price": final_price,
            "dprice": int(dprice),
            "sumf": sumf,
            "key": keys_list,
            "value": values_list,
            "subg": subg,
        },
    )


# NAVBAR
def navbar(request):
    return render(request, "navbar.html")


def problem1(request):
    if "value1" in request.POST:
        ans = request.POST["value1"]
        g(request)

    elif "value2" in request.POST:
        ans = request.POST["value2"]

    elif "value3" in request.POST:
        ans = request.POST["value3"]

    elif "value4" in request.POST:
        ans = request.POST["value4"]

    elif "value5" in request.POST:
        ans = request.POST["value5"]

    elif "value6" in request.POST:
        ans = request.POST["value6"]

    print(count)

    return render(request, "problem1.html")


def sample(request):
    return render(request, "sample.html")


def underweight(request):
    general2(request)
    b = x
    print("hello")
    print(x)
    return render(request, "underweight.html", {"b": b})


def contactus(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        number = request.POST["number"]
        contactus = Contactus(name=name, email=email, number=number)
        contactus.save()

    return render(request, "home.html")