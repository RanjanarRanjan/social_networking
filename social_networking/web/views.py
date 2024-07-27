from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from accounts.models import Profile, Interest
from django.urls import reverse
from django.contrib import messages


def login_view(request):
    message =''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            auth_user = User.objects.filter(username=username).first()

            if auth_user.check_password(password):
                user =  authenticate(username=username, password=password)

                if user is not None:
                    login(request=request, user=user)

                    if Profile.objects.filter(user=user).exists():
                        role = 'user'
                        return redirect('/user-home/')
                    elif  Profile.objects.filter(user=user,).exists():
                        role = 'admin'
                        return redirect('/chief-user/')
                    else:
                        message = "User role doesn't exist"
                else:
                    message = "User does't exist"
            else:
                message = "Password doesn't match"
        else:
            message = "User not exists"
    context = {
        'message' : message,
    }
    return render(request, 'auth/login.html')


def registration(request):
    if request.method == "POST":
        # Retrieve form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        interest_ids = request.POST.getlist('interest[]')
        user_image = request.POST.get('user_image')
        username = request.POST.get('username')
        designation = request.POST.get('designation')
        location = request.POST.get('location')
        education1 = request.POST.get('education1')
        education2 = request.POST.get('education2')
        bio = request.POST.get('bio')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        print(interest_ids, '==============================================')
        if password == confirm_password:
            if not User.objects.filter(username=username).exists():
                # Create the user
                user = User.objects.create_user(username=username, password=password)
                # Create profile
                profile = Profile.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    gender=gender,
                    user_image=user_image,
                    designation=designation,
                    location=location,
                    education1=education1,
                    education2=education2,
                    bio=bio,
                    password=password,
                )
                # Add interests
                interests = Interest.objects.filter(id__in=interest_ids)
                print(interests, '------------------------------')
                for interests in interests:
                    profile.interests.add(interests)

                # Redirect to login page after successful registration
                login_url = reverse('login')
                return redirect(login_url)
            else:
                return render(request, 'auth/registrationPage.html', {'error_message': 'Username already exists'})
        else:
            return render(request, 'auth/registrationPage.html', {'error_message': 'Passwords do not match'})
    else:
        interests = Interest.objects.all()
        context = {'interests': interests}
        return render(request, 'auth/registrationPage.html', context)
    

def logout_user(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        message = f'Successfully logged out {username}.'
    else:
        message = 'No user was logged in.'
    return redirect('login') 