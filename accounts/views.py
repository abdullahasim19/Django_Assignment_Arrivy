from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
import re
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse


# Create your views here.

def account_index(request):
    return HttpResponse('Accounts App')


def is_valid_email(email):
    # Regular expression for basic email validation
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


def register_user(request):
    if request.method == 'POST':
        # print('mm')
        # print(request.body)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)


        field_values = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']
        missing_fields = []
        for val in field_values:
            if val not in data.keys():
                missing_fields.append(val)

        if len(missing_fields) > 0:
            miss = ', '.join(missing_fields)
            return HttpResponse(f'Following are missing in request body: {miss}', status=400)
        # return HttpResponse('Testing')

        for key,value in data.items():
            if type(value)!=str:
                return HttpResponse('Datatype of all fields should be string')
        #return HttpResponse('Debug')


        username = data.get('username')
        password1 = data.get('password1')
        password2 = data.get('password2')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')

        if not username or not password1 or not password2:
            return JsonResponse({'error': 'Username or Password is missing'}, status=400)
        try:
            checkuser = User.objects.get(username=username)
        except:
            checkuser = None
        if checkuser is not None:
            return JsonResponse({'error': 'A user with that username already exists'}, status=400)

        if password1 != password2:
            return JsonResponse({"error": "The two password fields didn't match"}, status=400)

        if len(password1) < 1:
            return JsonResponse({"error": "This password is too short. It must contain at least 8 characters"}
                                , status=400)

        if email:
            if not is_valid_email(email):
                return JsonResponse({'error': 'Enter a valid email address'}, status=400)

        # user = User.objects.create(username=username, password=password1, email=email, first_name=first_name
        #  , last_name=last_name
        #  )
        user = User(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password1)
        user.save()

        return JsonResponse({'message': 'User created successfully', }, status=201)
    else:
        return HttpResponse("Invalid Request Type", status=400)


def login_user(request):
    # print('dataa', request)
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('profile'))
        else:
            return HttpResponse('No user is logged in!')
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        field_values = ['username', 'password']
        missing_fields = []
        for val in field_values:
            if val not in data.keys():
                missing_fields.append(val)

        if len(missing_fields) > 0:
            miss = ', '.join(missing_fields)
            return HttpResponse(f'Following are missing in request body: {miss}', status=400)

        for key, value in data.items():
            if type(value) != str:
                return HttpResponse('Datatype of all fields should be string')

        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return JsonResponse({'error': 'Username or Password is missing'}, status=400)

        if request.user.is_authenticated:
            # request.session['message']='Already logged in!'
            return HttpResponseRedirect(reverse('profile'))
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            # return HttpResponse('Login Done')
            # request.session['message'] = 'Login Successful!!'
            return HttpResponseRedirect(reverse('profile'))
        else:
            return HttpResponse('Username or password is invalid', status=401)
    else:
        return HttpResponse("Invalid Request Type", status=400)


def logout_user(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            logout(request)
            return HttpResponse('Logged Out Successfully')
        return HttpResponse('Already logged out')

    return HttpResponse("Invalid Request Type", status=400)


def view_login_user(request):
    if request.user.is_authenticated:
        return HttpResponse(f'Currently user: {request.user} is logged in!')
    return HttpResponse('No user is logged in!')
