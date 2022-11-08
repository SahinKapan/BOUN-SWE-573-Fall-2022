from django.shortcuts import render
from login.forms import UserForm, UserProfileInfoForm

from django.views.generic import CreateView
from . import forms
#
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from django.contrib import messages

# Create your views here.

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('index')
    template_name = 'login/registration.html'




def index(request):
    return render(request,'login/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in , Nice!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))


def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)


        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'login/registration.html',
                           {'user_form':user_form,
                             'profile_form':profile_form,
                              'registered':registered})




def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse_lazy('index'))

            else:
                messages.error(request,'ACCOUNT NOT ACTIVE')
                return render(request,'login/login.html')

        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password {}".format(username,password))
            messages.error(request,'Invalid login details supplied')
            return render(request,'login/login.html')
    else:
        return render(request,'login/login.html',{})
