from .models import *
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.shortcuts import render_to_response
from django.contrib.auth import login as django_login
from django.contrib.auth.models import User
from django.contrib.auth import logout
import json
# Create your views here.

def registration_page(request):
    return render_to_response("html_templates/registration.html")

def login_view(request):
    return render_to_response("html_templates/login.html")

def home_page(request):
    return render_to_response('html_templates/home.html')


def registration(request):
    # jsonobj=json.loads(request.body)
    jsonobj = request.POST

    user=jsonobj.get('user')
    username = jsonobj.get('username')
    mob_no = jsonobj.get('mob_no')
    email = jsonobj.get('email')
    password = jsonobj.get('password')

    print username,mob_no,email,password


    user = User.objects.create(username=user)
    user.set_password(password)
    user.save()
    # user_detail =UserDetail.objects.all()
    # print user_detail.email



    user_reg = UserLoginForm.objects.create(username=username,mob_no=mob_no,email=email,user=user)
    user_reg.save()

    # return HttpResponse(json.dumps({"validation":"employee added succesfully","status":True}), content_type="application/json")
    return render_to_response('html_templates/home.html')



def loginme(request):
    # jsonobj=json.loads(request.body)
    jsonobj =request.POST
    username = jsonobj.get('username')
    password = jsonobj.get('password')

    if username == None:
        return HttpResponse(json.dumps({'validation':'enter user name',"status":False}), content_type="application/json")
    elif password ==None:
        return HttpResponse(json.dumps({'validation':'Enter password',"status":False}), content_type="application/json")


    user_detail = UserLoginForm.objects.all()
    for user__ in user_detail:
        if str(user__.mob_no) == username or user__.email == username:
            user_st = user__.username
            user = authenticate(username=user_st, password=password)
            
            if not user:
                return HttpResponse(json.dumps({'validation':'Invalid user',"status":False}),content_type="application/json")

            if not user.is_active:
                return HttpResponse(json.dumps({'validation':'The password is valid but account is disabled',"status":False}), content_type="application/json")
                django_login(request,user)
    queryset= show_user(user)
    return render_to_response('html_templates/show_user.html',queryset)
    
    

def show_user(user):

    user_info = UserLoginForm.objects.get(username=user)

    username = user_info.username
    email = user_info.email
    mob_no =user_info.mob_no

    queryset = { "user":username,
                    "email":email,
                        "mob_no":mob_no
            }

    return queryset

def logout(request):
    return render_to_response('html_templates/home.html')
