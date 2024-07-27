from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
import os


def generate_file_path(instance, filename, image_category, category_type):
    upload_path = f"media/accounts/{image_category}-{category_type}"
    return os.path.join(upload_path, instance.id, filename)

def profile_image_file_path(instance, filename):
    return generate_file_path(instance, filename, 'profile', 'image')


PROFILE_GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
)


class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    gender  = models.CharField(max_length=10, choices=PROFILE_GENDER_CHOICES, blank=True)
    interests = models.ManyToManyField('Interest', related_name='profiles', blank=True)
    user_image = models.ImageField(upload_to=profile_image_file_path, blank=True)
    username = models.CharField(max_length=256)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', blank=True)
    designation = models.CharField(max_length=256, blank=True, null=True, default='Unspecified')
    location = models.CharField(max_length=256, blank=True, null=True)
    education1 = models.CharField(max_length=256, blank=True, null=True)
    education2 = models.CharField(max_length=256, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    password = models.CharField(max_length=256)

    class Meta :
        db_table = 'account_profile'
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        ordering = ('first_name','last_name')
    
    def __str__(self):
        return self.username or f"{self.first_name} {self.last_name}"
    

class Interest(models.Model):
    title = models.CharField(max_length=256, blank=True)

    class Meta:
        db_table = "account_interest"
        verbose_name = _("Interest")
        verbose_name_plural = _("Interests")
        ordering = ('title',)

    def __str__(self):
        return self.title