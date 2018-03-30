from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.template import loader
from .models import User
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage



def index(request):
    return render(request,'signup/index.html')
	
def register(request):
    return render(request,'signup/register.html')
	
def verify(request):
    if request.method == 'POST':
        user=User()
        user.user_fname=request.POST.get('fnm')
        user.user_lname=request.POST.get('lnm')
        user.user_email=request.POST.get('email')
        user.user_isactive=False
        user.save()
        current_site = get_current_site(request)
        mail_subject = 'Activate your blog account.'
        message = render_to_string('signup/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
        print(message)
        to_email = request.POST.get('email')
        email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
        email.send()
                
    return render(request,'signup/verify.html')	

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.user_isactive = True
        my_password=User.objects.make_random_password(8)
        user.set_password(my_password)
        user.save()
        current_site = get_current_site(request)
        mail_subject = 'Password for your account.'
        message = render_to_string('{Hi {{ user.user_fname }}, This is the password for your account {{user.get_password()}}', {
                'user': user,
                'domain': current_site.domain,
                'password': my_password})
        print(message)
        to_email = request.POST.get('email')
        email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
        email.send()
        #login(request, user)        
        return render(request,'signup/index.html')
    else:
        return HttpResponse('Activation link is invalid!')
#def login(request)
  #  return render(request, 'signup/login.html')
