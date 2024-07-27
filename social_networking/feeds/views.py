from django.shortcuts import render,redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from feeds.models import UserPost, Group, GroupPost, FriendRequest, ChatRoom, Message, LikedPost
from accounts.models import Interest
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseBadRequest, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from django.contrib.auth.models import User
from django.db.models import Q
import json
from django.db import models
from django.db.models import Count, Case, When, BooleanField

def is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'

@login_required
def user_home(request):
    context = {}
    current_user = request.user

    if request.method == 'POST':
        # Handle form submission
        if 'post' in request.POST:
            content = request.POST.get('post')
            image = request.FILES.get('image_file')
            video = request.FILES.get('video_file')

            if not content and not image and not video:
                return HttpResponseBadRequest("No content, image, or video provided")

            created_by = request.user.profile
            
            new_post = UserPost.objects.create(content=content, created_by=created_by)

            if image:
                new_post.image = image
            elif video:
                new_post.video = video

            new_post.save()

            return redirect(reverse('user_home'))
        elif 'friend_request' in request.POST:
            user_id = request.POST.get('user_id')
            if user_id:
                friend = User.objects.get(pk=user_id)
                # Logic to send friend request goes here
                # For example:
                # request.user.profile.send_friend_request(friend.profile)
                return redirect(reverse('user_home'))  # Redirect to user home after sending request

    # Fetch user created groups and suggested groups
    context['user_created_groups'] = Group.objects.filter(created_by=request.user.profile)
    context['suggested_groups'] = Group.objects.exclude(created_by=request.user.profile)
    
    # Fetch all users except the current user and admin users
    context['suggested_friends'] = User.objects.exclude(id=request.user.id).exclude(is_superuser=True).exclude(is_staff=True)
    
    # Fetch posts, groups, and clicked group (if any)
    context['posts'] = UserPost.objects.annotate(liked_count=Count('likes', filter=models.Q(likes__is_liked=True)),is_liked_by_user=Case(
            When(likes__liked_by=current_user.profile, likes__is_liked=True, then=True),
            default=False,
            output_field=BooleanField()
        )).all()
    context['groups'] = Group.objects.all()
    context['clicked_group'] = None
    
    if 'group_id' in request.POST:
        group_id = request.POST['group_id']
        context['clicked_group'] = Group.objects.get(pk=group_id)

    return render(request, 'user/userHome.html', context)


def like_post(request, post_id):
   
    current_user = request.user
   
    is_liked = False
    like_count = 0
    message = ''

    if UserPost.objects.filter(id=post_id).exists():
     
        user_post = UserPost.objects.get(id=post_id)

        print(user_post)

        if LikedPost.objects.filter(userPost=user_post, liked_by__user=current_user).exists():

            liked_post = LikedPost.objects.get(userPost=user_post, liked_by__user=current_user)
            is_liked = not liked_post.is_liked
            liked_post.is_liked = not liked_post.is_liked
            liked_post.save()
        else:

            LikedPost.objects.create(userPost=user_post, liked_by=current_user.profile, is_liked=True)
            is_liked = True

        like_count = LikedPost.objects.filter(userPost=user_post, is_liked=True).count()
        message = 'Success'
    else:
        message = 'Post does not exist'

    return JsonResponse({'is_liked': is_liked, 'likes_count': like_count, 'message': message})



def create_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('groupName')
        group_topic = request.POST.get('groupTopic')
        location = request.POST.get('location')
        bio = request.POST.get('bio')
        image = request.FILES.get('groupImage')
        interest_ids = request.POST.getlist('interest')  
        created_by = request.user.profile

        new_group = Group.objects.create(
            name=group_name,  
            topic=group_topic, 
            location=location, 
            bio=bio,  
            image=image,  
            created_by=created_by  
        )

        interests = Interest.objects.filter(id__in=interest_ids)
        new_group.interest.set(interests)

        return redirect(reverse('user_home'))
    else:
        interests = Interest.objects.all()
        context = {'interests': interests,
              'title': "Helloworld"}
            
        return render(request, 'user/userHome.html', context)


def user_profile(request):
    current_user = request.user
    current_user_profile = current_user.profile
    current_user_posts = UserPost.objects.filter(created_by=current_user_profile)
    user_profile_info = Profile.objects.get(user=current_user)
    post_count = current_user_posts.count()  # Count posts of the current user only
    return render(request, 'user/userProfilePage.html', {'posts': current_user_posts, 'user_profile_info': user_profile_info, 'post_count': post_count})



def save_personal_details(request):
    if request.method == 'POST':
        user_profile = request.user.profile
        user_profile.designation = request.POST.get('designation')
        user_profile.location = request.POST.get('location')
        user_profile.education1 = request.POST.get('education1')
        user_profile.education2 = request.POST.get('education2')
        user_profile.bio = request.POST.get('bio')
        
        # Save the updated profile
        user_profile.save()
        
        messages.success(request, 'Personal details updated successfully.')
        return redirect('user_profile')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('user_profile')


@login_required
def friend_request(request, user_id):
    if request.method == "POST":
        # Get the target user's profile or return a 404 error if not found
        target_user_profile = get_object_or_404(Profile, user_id=user_id)

        # Get the current user's profile
        current_user_profile = request.user.profile

        # Create a new FriendRequest instance
        friend_request = FriendRequest.objects.create(
            profile=target_user_profile,
            requested_by=current_user_profile,
            request_status='pending'
        )

        # Optionally, you can display a success message
        messages.success(request, f"Friend request sent to {target_user_profile.user.username}.")

        # Redirect the user back to the target user's profile page
        return redirect('other_profile', user_id=user_id)

    # Handle invalid requests (GET requests or direct URL access)
    messages.error(request, "Invalid request.")
    return redirect('error_page')


def other_profile(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        profile = user.profile

        user_posts = UserPost.objects.filter(created_by=profile)
        post_count = user_posts.count()

    except Profile.DoesNotExist:
        # If Profile does not exist, fallback to User model
        user = get_object_or_404(User, pk=user_id)
        profile = user.profile
        user_posts = []
        post_count = 0

    context = {
        'user': user,
        'user_posts': user_posts,
        'post_count': post_count
    }

    return render(request, 'user/otherProfile.html', context)


def community(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    group_posts = GroupPost.objects.filter(group_id=group_id)  # Retrieve group posts for the specific group
    group_posts_count = GroupPost.objects.filter(group_id=group_id).count()
    context = {
        'group': group,
        'group_id': group_id,
        'group_posts': group_posts,
        'group_posts_count' : group_posts_count
    }
    return render(request, 'user/communityPage.html', context)


def edit_group(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')

        print(request.POST)

        print("Edit group")

        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            raise Http404("Group does not exist")

        group.name = request.POST.get('groupName')
        group.topic = request.POST.get('groupTopic')
        group.location = request.POST.get('location')
        group.bio = request.POST.get('bio')

        if 'groupImage' in request.FILES:
            group.image = request.FILES.get('groupImage')

        group.save()

        messages.success(request, 'Group details updated successfully.')
        return redirect(reverse('community',kwargs={"group_id":group_id})) 
    
    messages.error(request, 'Failed to update group details.')
    return redirect('community')



def other_community(request, group_id):
    # Retrieve the selected group
    group = get_object_or_404(Group, pk=group_id)

    # Retrieve posts belonging to the selected group and count them
    group_posts = GroupPost.objects.filter(group=group)
    post_count = group_posts.count()

    # Define the context dictionary
    context = {
        'group': group,
        'group_posts': group_posts,
        'post_count': post_count,
    }

    # Pass the context to the template
    return render(request, 'user/otherCommunity.html', context)



def community_create(request, group_id):
    if request.method == 'POST':
        content = request.POST.get('post')
        image = request.FILES.get('image_file')
        video = request.FILES.get('video_file')

        if not content and not image and not video:
            return HttpResponseBadRequest("No content, image, or video provided")

        created_by = request.user.profile
        
        group_post = GroupPost.objects.create(content=content, image=image, video=video, group_id=group_id, created_by=created_by)

        if image:
            group_post.image = image
        elif video:
            group_post.video = video

        group_post.save()

        return redirect(reverse('community', kwargs={'group_id': group_id}))  # Pass group_id to the reverse function
    
    groups = Group.objects.all()
    clicked_group = None
    if 'group_id' in request.POST:
        group_id = request.POST['group_id']
        clicked_group = Group.objects.get(pk=group_id)
    print("Clicked group:", clicked_group) 

    return render(request, 'user/communityCreatePost.html', {'groups': groups, 'clicked_group': clicked_group, 'group_id': group_id})



@login_required
def user_chat(request):
    users = Profile.objects.exclude(user=request.user)  # Exclude the current user

    context = {
        'users': users
    }

    return render(request, 'user/chatPage.html', context)


@login_required
def handle_messages(request, user_id):
    # if request.method == 'POST':
    if request.method == 'POST' and is_ajax(request):
        data = json.loads(request.body)
        receiver = Profile.objects.get(id=user_id).user
        
        current_user_profile =Profile.objects.get(user=request.user).user
        chat_room = ChatRoom.objects.filter(
            Q(user1=current_user_profile, user2=receiver) | 
            Q(user1=receiver, user2=current_user_profile)
        ).first()

        if not chat_room:
            print("*****************$$$$$$$$##########")
            chat_room = ChatRoom.objects.create(user1=current_user_profile, user2=receiver)

        return JsonResponse({'chat_room_id': chat_room.id}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def save_message(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        message_text = request.POST.get('message_text')

        # Assuming you have a Message model with 'receiver_id' and 'message_text' fields
        message = Message.objects.create(receiver_id=receiver_id, message_text=message_text)

        # Return a JSON response indicating success
        return JsonResponse({'success': True})
    else:
        # Return a JSON response indicating failure if the request method is not POST
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

def community_chat(request):
    return render(request, 'user/communityChat.html')


def chief_user(request):
    return render(request, 'chief/adminUser.html')


def chief_group(request):
    return render(request, 'chief/adminGroup.html')


def chief_report(request):
    return render(request, 'chief/adminReport.html')


def notifications(request):
    # Fetch all friend requests associated with the logged-in user
    friend_requests = FriendRequest.objects.filter(profile=request.user.profile)
    
    # Pass friend requests to the template
    context = {
        'friend_requests': friend_requests
    }
    
    return render(request, 'notifications.html', context)