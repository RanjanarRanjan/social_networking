from django.urls import path
from .views import user_home, create_group, user_profile, other_profile, community, community_create, other_community, community_chat, user_chat, chief_user, chief_group, chief_report, save_personal_details, edit_group, friend_request, handle_messages, save_message,like_post

urlpatterns = [
    path('user-home/', user_home, name='user_home'), 
    path('like-post/<int:post_id>/',like_post, name='like_post'),
    path('create-group/', create_group, name='create_group'),
    path('user-profile/', user_profile, name='user_profile'), 
    path('other-profile/', other_profile, name='other_profile'),
    path('other-profile/<int:user_id>/', other_profile, name='other_profile'),
    path('friend_request/<int:user_id>/', friend_request, name='friend_request'),
    path('community/<int:group_id>/', community, name='community'),
    path('other-community/', other_community, name='other_community'),
    path('other-community/<int:group_id>/', other_community, name='other_community'),
    path('community/<int:group_id>/community-create/', community_create, name='community_create'), 
    path('other-community/community-chat/', community_chat, name='community_chat'), 
    path('user-chat/', user_chat, name='user_chat'), 
    path('user-chat/<int:user_id>/', handle_messages, name='handle_messages'), 
    path('save-message/', save_message, name='save_message'),
    path('chief-user/', chief_user, name='chief_user'), 
    path('chief-group/', chief_group, name='chief_group'), 
    path('chief-report/', chief_report, name='chief_report'), 
    path('save-personal-details/', save_personal_details, name='save_personal_details'),
    path('community/', edit_group, name='edit_group'),
]
