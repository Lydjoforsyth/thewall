from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, Message, Comment

def index(request):
    return render(request, 'login.html')

def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hash_pw)
        
        request.session['uid'] = user.id

        return redirect('/success')

def login(request):
    user = User.objects.filter(email=request.POST['email']) # why are we using filter here instead of get?
    if len(user) > 0:
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['uid'] = logged_user.id
            return redirect('/success')
        else: 
            messages.error(request, 'Email and password did not match.')
    else:
        messages.error(request, 'Email address is not registered yet.')
        return redirect("/")

def success(request):
    context = {
        "logged_user": User.objects.get(id=request.session['uid']),
        "all_messages": Message.objects.order_by("-created_at")
    }
    return render(request, 'success.html', context)

def create_message(request):
    Message.objects.create(message=request.POST['message'], creator=User.objects.get(id=request.session['uid']))

    return redirect('/success')

def create_comment(request):
    Comment.objects.create(
        comment=request.POST['comment_content'], 
        creator=User.objects.get(id=request.session['uid']), 
        message=Message.objects.get(id=request.POST['message_id'])
        )

    return redirect('/success')

def logout(request):
    request.session.flush()
    
    return redirect('/')
    
