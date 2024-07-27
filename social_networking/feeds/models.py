from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from accounts.models import Profile, Interest
import os



def generate_file_path(instance, filename, image_category, category_type):
    upload_path = f"feeds/{image_category}-{category_type}"
    instance_id_str = str(instance.id)
    return os.path.join(upload_path, instance_id_str, filename)


def post_image_file_path(instance, filename):
    return generate_file_path(instance, filename, 'post', 'images')


def post_video_file_path(instance, filename):
    return generate_file_path(instance, filename, 'post', 'videos')


def group_image_file_path(instance, filename):
    return generate_file_path(instance, filename, 'group', 'image')


def group_post_image_file_path(instance, filename):
    return generate_file_path(instance, filename, 'group_post', 'image')


def group_post_video_file_path(instance, filename):
    return generate_file_path(instance, filename, 'group_post', 'video')



REPORT_TYPE_CHOICES = [
        ('profile', 'Profile'),
        ('post', 'Post'),
        ('group', 'Group'),
    ]


REPORT_REASON_CHOICES = [
        ('hate_speech', 'Hate Speech'),
        ('inappropriate_language', 'Inappropriate Language'),
        ('disrespectful_behavior', 'Disrespectful Behavior'),
        ('violent_or_threatening_language', 'Violent or Threatening Language'),
        ('other', 'Other'),
    ]


FRIENDREQUEST_CATEGORY_CHOICES = (
    ('friend_request', 'Friend Request'),
)


FRIENDREQUEST_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('approved', 'approved'),
    ('denied', 'denied'),
)

    
class UserPost(models.Model):
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to=post_image_file_path, blank=True)
    video = models.FileField(upload_to=post_video_file_path, blank=True)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "feeds_userpost"
        verbose_name = _("User Post")
        verbose_name_plural = _("User Posts")
        ordering = ("created_by", )

    def __str__(self):
        return f"{self.created_by}'s Post"
        

class LikedPost(models.Model):

    userPost = models.ForeignKey(UserPost, on_delete=models.CASCADE, blank=True, null=True,related_name='likes')
    liked_by = models.ForeignKey(Profile, on_delete=models.CASCADE,blank=True,null=True)
    is_liked = models.BooleanField(default=True)

    class Meta:
        db_table = "feeds_liked_post"
        verbose_name = _("Liked post")
        verbose_name_plural = _("Liked posts")
        ordering = ("userPost", )

    def __str__(self):
        return f"{self.userPost}'s Post"

class Group(models.Model):
    name = models.CharField(max_length=256, blank=True)
    topic = models.CharField(max_length=256, blank=True)
    location = models.CharField(max_length=256, blank=True)
    bio = models.TextField(blank=True)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name= 'groups', blank= True)
    image = models.ImageField(upload_to=group_image_file_path, blank=True)
    interest = models.ManyToManyField(Interest, related_name='group_interest', blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "feeds_group"
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")
        ordering = ("name", )

    def __str__(self):
            return self.name
    

class GroupPost(models.Model):
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to=group_post_image_file_path,  blank=True)
    video = models.FileField(upload_to=group_post_video_file_path, blank=True)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="group_posts", blank=True)
    is_delete =  models.BooleanField(default=False)
    group = models.ForeignKey(Group,on_delete=models.CASCADE ,related_name ="group_post")
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "feeds_grouppost"
        verbose_name = _("Group Post")
        verbose_name_plural = _("Group Posts")
        ordering = ('-created_time','id')

    def __str__(self):
        return self.content
        
        
class Report(models.Model):
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES, blank=True)
    reported_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reports_sent', blank=True)
    to_whom = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reports_received', blank=True)
    reason = models.CharField(max_length=100, choices=REPORT_REASON_CHOICES, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "feeds_report"
        verbose_name = _('Report')
        verbose_name_plural = _('Reports')
        ordering = ("report_type", )

    def __str__(self):
        return self.report_type


class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follower_relationships', blank=True)
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following_relationships', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "feeds_follow"
        verbose_name = _('Follow')
        verbose_name_plural = _('Follows')
        ordering = ("created_at", )

    def __str__(self):
        return str(self.created_at)


class FriendRequest(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name= 'friendrequest', blank=True)
    category = models.CharField(max_length=256, choices=FRIENDREQUEST_CATEGORY_CHOICES, blank=True)
    requested_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name= 'requested_by', blank=True)
    request_status = models.CharField(max_length=8, choices=FRIENDREQUEST_STATUS_CHOICES, default="pending")

    class Meta:
        db_table = "feeds_friendrequest"
        verbose_name = _("Friend Request")
        verbose_name_plural = _("Friend Requests")
        ordering = ('-request_status','profile__user__username')

    def __str__(self):
        return f"Friend request from {self.requested_by.user.username} to {self.profile.user.username}"


class ChatRoom(models.Model):
    user1 = models.ForeignKey(User, related_name='chatroom_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='chatroom_user2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user1.username} and {self.user2.username}"

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Message from {self.sender.username} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"