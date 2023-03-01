from django.contrib import admin

from .models import Bmi, Contactus, Patient, Test, HealthGoal, Option

admin.site.register(Bmi)
admin.site.register(Contactus)
admin.site.register(Patient)
admin.site.register(Test)
admin.site.register(HealthGoal)
admin.site.register(Option)