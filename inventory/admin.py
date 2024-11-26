from django.contrib import admin
from .models import Pharmacy, Equipment, Medicine

# Register your models here.

admin.site.register(Pharmacy)
admin.site.register(Medicine)
admin.site.register(Equipment)