from django.contrib import admin
from accounts.models import Profile, Interest
# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'gender', 'user_image', 'designation', 'location', 'education1', 'education2', 'bio', 'password']

admin.site.register(Interest)