from django.contrib import admin
from feeds.models import UserPost, Group, Report, Follow, FriendRequest, GroupPost, ChatRoom, Message,LikedPost

class UserPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'image', 'video', 'created_by')
    # Add any other fields you want to display in the list view

admin.site.register(UserPost, UserPostAdmin)


admin.site.register(Group)


admin.site.register(GroupPost)


admin.site.register(Report)


admin.site.register(Follow)


admin.site.register(FriendRequest)


admin.site.register(ChatRoom)


admin.site.register(Message)

@admin.register(LikedPost)
class LikedPostAdmin(admin.ModelAdmin):
    list_display = ('userPost','liked_by','is_liked')
    search_fields = ['userPost']
