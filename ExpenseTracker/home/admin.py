# Register your models here.
from .models import Addmoney_info
from django.contrib import admin


class Addmoney_infoAdmin(admin.ModelAdmin):
    list_display=("user","quantity","Date","Category","add_money")

admin.site.register(Addmoney_info,Addmoney_infoAdmin)

from django.contrib.sessions.models import Session

admin.site.register(Session)

from .models import UserProfile

admin.site.register(UserProfile)