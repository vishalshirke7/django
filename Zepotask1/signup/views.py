from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.template import loader
from .models import User
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .forms import SignupForm, LoginForm
from signup.random_string_generator import random_string_generator_c


def index(request):
    if 'user_id' in request.session:
        userid = request.session['user_id']
        user = User.objects.get(pk=userid)
        return HttpResponseRedirect(reverse('signup:loginview', args=(user.user_fname,)))
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
            user_verf_link =  ranstr.id_generator(size=17,chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz")      
            user.user_isactive = False
            user.user_verf_link = user_verf_link
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
            return render(request,'signup/verify.html')	
    else:
        form = SignupForm()

    return render(request, 'signup/register.html', {'form': form})

def login(request): 
    if request.method == 'POST':  
        form = LoginForm(request.POST)
        if form.is_valid(): 
            user = User.objects.get(user_email=request.POST['username'])
            if user.user_password == request.POST['password']:
                request.session['user_id'] = user.id
                #context = {'username': user.user_fname,'user': user}        
                return HttpResponseRedirect(reverse('signup:loginview', args=(user.user_fname,)))	
    elif 'user_id' in request.session:
        userid = request.session['user_id']
        user = User.objects.get(pk=userid)
        return HttpResponseRedirect(reverse('signup:loginview', args=(user.user_fname,)))
        #return render(request,'signup/welcome.html',{'user': user})
    else:
        form = LoginForm()
    return render(request, 'signup/login.html', {'form': form})

def setpassword(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid(): 
            user = User.objects.get(user_password=request.POST['password'])
            user.user_password = form.cleaned_data['fname'].strip()
            user.save()
            
    else:
        form = PasswordForm()
    return render(request, 'signup/setpassword.html', {'form': form})

        

def loginview(request, username):
    if 'user_id' in request.session:
        userid = request.session['user_id']
        user = User.objects.get(pk=userid)
        username1 = user.user_fname
        if(username == username1):
            return render(request,'signup/welcome.html', {'user': user})
    else:
        return HttpResponse('<h2 style="text-align:center;color:red;font-size:70px">We caught you! <h2>')
    

def logout(request):
        try:
            del request.session['user_id']
        except KeyError:
            pass    #return HttpResponse('<h2 style="text-align:center;color:red;;font-size:70px">We caught you! <h2>')
        return render(request,'signup/logout.html')        
  
def activate(request, uid, link):
    try:
        uid = uid
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    link1= user.user_verf_link
    #if user.user_password == "":
    if user is not None and link == link1:
        user.user_isactive = True
        if request.method == 'POST':
            form = PasswordForm(request.POST)
            if form.is_valid():
                user = User.objects.get(user_password=request.POST['password'])
                user.user_password = form.cleaned_data['fname'].strip()
                user.save()
                return render(request, 'signup/accountsetup.html')
        else:
            form = PasswordForm()
        return render(request, 'signup/setpassword.html', {'form': form})
            #request.session['uspw']=uspw  
    elif link != link1:
        return HttpResponse('<html><h3 style="color:red;text-align:center;font-size:60px">Activation link is invalid!<h3></html>')
    else:
        pass
        
def handler404(request):
    return render(request, 'signup/error_404.html',status=404)

def handler500(request):
    return render(request, 'signup/error_500.html',status=500)
        
