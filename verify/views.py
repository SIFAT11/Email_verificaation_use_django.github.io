from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Profile
from django.conf import settings
from django.contrib.auth.hashers import make_password
from decouple import config
import secrets
import logging

# Any duplicate value delet
logger = logging.getLogger(__name__)

# Function to generate OTP
def generate_otp():
    return str(secrets.randbelow(900000) + 100000)

# Function to send verification email

def send_verification_email(request, profile):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account'
    message = render_to_string('activation_email.html', {
        'user': profile,
        'domain': current_site.domain,
        'otp': profile.otp,
        'protocol': 'http', 
    })
    to_email = profile.email
    send_mail(
        mail_subject,
        message,
        config('EMAIL_HOST_USER'),
        [to_email],
        fail_silently=False
    )

# Function to verify email
def verify_email(request, user_id, otp):
    try:
        profile = Profile.objects.get(id=user_id)
        profile.user.is_active = True
        profile.user.save()
        login(request, profile.user)
        profile.email_verified = True
        profile.save()
        messages.success(request, 'Your email has been verified. You are now logged in.')
    except Profile.DoesNotExist:
        messages.error(request, 'Invalid verification link. Please try again.')
        return redirect('login')
    return redirect('login')
 

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        retype_password = request.POST['retype_password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        age = request.POST['age']
        gender = request.POST['gender']
        city = request.POST['city']
        phone = request.POST['phone']
        email = request.POST['email']
        image = request.FILES['image']
        address = request.POST['address']

        if password != retype_password:
            messages.error(request, 'Passwords do not match. Please re-enter your password.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different one.')
            return redirect('register')
        otp = generate_otp() 
        user = User(
            username=username,
            password=make_password(password), 
            is_active=False
        )
        user.save()

        profile = Profile(
            user=user,
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            city=city,
            phone=phone,
            email=email,
            image=image,
            address=address,
            otp=otp
        )
        profile.save()

        # Send verification email
        send_verification_email(request, profile)

        messages.success(request, 'Registration successful! Check your email for verification.')
        return redirect('login')
    else:
        return render(request, 'registration.html')



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                profile = Profile.objects.get(user=user)
                if profile.email_verified:
                    login(request, user)
                    messages.success(request, 'Login successful!')
                    return redirect('login')
                else:
                    messages.error(request, 'Please verify your email before logging in.')
            except ObjectDoesNotExist:
                messages.error(request, 'Profile does not exist for this user. Please register first.')
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')
    
    return render(request, 'login.html')
