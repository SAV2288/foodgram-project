from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAdmin(UserAdmin):
    list_filter = ("username", "email", 'is_staff', 'is_superuser',)
    empty_value_display = "-пусто-"


admin.site.unregister(User) 
admin.site.register(User, UserAdmin)