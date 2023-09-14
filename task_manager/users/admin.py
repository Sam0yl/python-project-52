from django.contrib import admin
from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['username']
    list_display = ('id', 'username', 'first_name', 'last_name')
