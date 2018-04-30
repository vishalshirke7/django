from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.template import loader
from .models import User
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .forms import SignupForm, LoginForm, PasswordForm, PasswordReset, UpdateForm, ChangePassword
from signup.random_string_generator import random_string_generator_c
from django import forms


def index(request):
    if 'user_id' in request.session:
        userid = request.session['user_id']
        user = User.objects.get(pk=userid)
        return render(request, 'signup/welcome.html', {'user': user})
    else:
        return render(request,'signup/index.html')

        	
def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)  
        if form.is_valid():
            user = User()
            user.user_fname = form.cleaned_data['fname'].strip()
            user.user_lname = form.cleaned_data['lname'].strip()
            user.user_email = form.cleaned_data['email'].strip()
            ranstr = random_string_generator_c()
            user_verf_link =  ranstr.id_generator(size=17, chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz")
            user.user_isactive = False
            user.user_verf_link = user_verf_link
            user.save() 
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('signup/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'link':user_verf_link,
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request,'signup/verify.html')
    elif 'user_id' in request.session:
        return HttpResponseRedirect(reverse('signup:index'))
    else:
        form = SignupForm()

    return render(request, 'signup/register.html', {'form': form})


def login(request): 
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid(): 
            user = User.objects.get(user_email=request.POST['username'])
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('signup:index'))
    elif 'user_id' in request.session:
        return HttpResponseRedirect(reverse('signup:index'))
    else:
        form = LoginForm()
    return render(request, 'signup/login.html', {'form': form})

#def setpassword(request):
    #if request.method == 'POST':
       # form = PasswordForm(request.POST)
      #  if form.is_valid():
     #       user = User.objects.get(user_password=request.POST['password'])
    #        user.user_password = form.cleaned_data['fname'].strip()
   #         user.save()

  #  else:
 #       form = PasswordForm()
#    return render(request, 'signup/setpassword.html', {'form': form})


def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return render(request,'signup/logout.html')


def forgotpassword(request):
    if request.method == 'POST':
        form = PasswordReset(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email'].strip()
            user = User.objects.get(user_email=user_email)
            ranstr = random_string_generator_c()
            user_verf_link = ranstr.id_generator(size=17,chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz")
            user.user_verf_link = user_verf_link
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Forgot your password'
            message = render_to_string('signup/acc_forgot_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'link': user_verf_link,
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponseRedirect(reverse('signup:index'))
    elif 'user_id' in request.session:
        return HttpResponseRedirect(reverse('signup:index'))
    else:
        form = PasswordReset()
    return render(request, 'signup/password_reset.html', {'form': form})

  
def activate(request, link):
    try:
        link2 = link
        user = User.objects.get(user_verf_link=link2)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    link1 = user.user_verf_link
    if user is not None and link == link1:
        user.user_isactive = True
        if request.method == 'POST':
            form = PasswordForm(request.POST)
            if form.is_valid():
                uspw = form.cleaned_data['password']
                ranstr = random_string_generator_c()
                userpasw = ranstr.hash_password(uspw)
                user.user_password = userpasw
                user.save()
                return render(request, 'signup/account_setup.html')
            else:
                return render(request, 'signup/setpassword.html', {'form': form})

        #elif user.user_password != '':
         #   return HttpResponseRedirect(reverse('signup:index'))
        else:
            form = PasswordForm()
            return render(request, 'signup/setpassword.html', {'form': form, 'user': user})
            #request.session['uspw']=uspw  
    else:
        pass


def updateinfo(request):
    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            fname = form.cleaned_data['fname']
            lname = form.cleaned_data['lname']
            userid = request.session['user_id']
            user = User.objects.get(id=userid)
            user.user_fname = fname
            user.user_lname = lname
            user.save()
            return HttpResponseRedirect(reverse('signup:index'))
    elif 'user_id' not in request.session:
        return HttpResponseRedirect(reverse('signup:index'))
    else:
        form = UpdateForm()
    return render(request, 'signup/update_information.html', {'form': form})


def changepassword(request):
    if request.method == 'POST':
        form = ChangePassword(request.POST)
        if form.is_valid():
            psw = form.cleaned_data.get('password')
            userid = request.session['user_id']
            user = User.objects.get(id=userid)
            ranstr = random_string_generator_c()
            userpasw = ranstr.hash_password(psw)
            user.user_password = userpasw
            user.save()
            return HttpResponseRedirect(reverse('signup:login'))
    elif 'user_id' not in request.session:
        return HttpResponseRedirect(reverse('signup:index'))
    else:
        form = ChangePassword()
    return render(request, 'signup/change_password.html', {'form': form})


def handler404(request):
    return render(request, 'signup/error_404.html', status=404)


def handler500(request):
    return render(request, 'signup/error_500.html', status=500)
        
