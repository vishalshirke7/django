from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.template import loader
from django.urls import reverse
from django.template.loader import render_to_string
from signup.random_string_generator import random_string_generator_c
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from .forms import SignupForm, LoginForm
from .models import User


def index(request):
    if 'user_email' in request.session:
        useremail = request.session['user_email']
        user = User.objects.get(email=useremail)
        return render(request, 'signup/welcome.html', {'user': user})
    else:
        return render(request, 'signup/index.html')


def register(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User()
            user.fname = form.cleaned_data['fname'].strip()
            user.lname = form.cleaned_data['lname'].strip()
            user.email = form.cleaned_data['email'].strip()
            ranstr = random_string_generator_c()
            user_verf_link =  ranstr.id_generator(size=17, chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz")
            user.active = False
            user.verf_link = user_verf_link
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('signup/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid' : user.id,
                'link':user_verf_link,
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'signup/verify.html')
    else:
        form = SignupForm()

    return render(request, 'signup/register.html', {'form': form})


def activate(request, link):
    try:
        user = User.objects.get(verf_link=link)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    link1 = user.verf_link
    if user.password is None:
        if user is not None and link == link1:
            user.active = True
            ranstr = random_string_generator_c()
            uspw =  ranstr.id_generator(size=7, chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz")
            user.password = uspw
            #request.session['uspw']=uspw
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('signup/acc_password_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uspw': uspw,
            })
            to_email = user.email
            user.save()
            email = EmailMessage(
                      mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'signup/successfulreg.html')
    elif link != link1:
        return HttpResponse('<html><h3 style="color:red;text-align:center;font-size:60px">Activation link is invalid!<h3></html>')
    else:
        return render(request, 'signup/already_signedin.html')


def login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=request.POST['username'])
            request.session['user_email'] = user.email
            #return render(request, 'signup/welcome.html', {'user': user})
            return HttpResponseRedirect(reverse('signup:index'))
    elif 'user_email' in request.session:
        return HttpResponseRedirect(reverse('signup:index'))
    else:
        form = LoginForm()
    return render(request, 'signup/login.html', {'form': form})


def logout(request):

        try:
            del request.session['user_email']
        except KeyError:
            pass  # return HttpResponse('<h2 style="text-align:center;color:red;;font-size:70px">We caught you! <h2>')
        return render(request, 'signup/logout.html')
