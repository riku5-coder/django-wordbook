from django.contrib import admin
from .models import UserWord

# Register your models here.

@admin.register(UserWord)
class UserWordAdmin(admin.ModelAdmin):
    list_display = ("word", "user", "source", "created_at")
    list_filter = ("user", "source")
    search_fields = ("word", "meaning")