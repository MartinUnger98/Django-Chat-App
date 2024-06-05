from django.shortcuts import render, redirect
from .models import Chat, Message
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers

@login_required(login_url='/login/')
def index(request):
    """
    this is a view to render the chat html.
    """
    if request.method == 'POST':
        print("Received data: " + request.POST['textmessage'])
        myChat = Chat.objects.get(id=1)
        newMessage = Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user,)
        serialited_obj = serializers.serialize('json', [newMessage,])
        return JsonResponse(serialited_obj[1:-1], safe=False)
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {'messages': chatMessages})

def login_view(request):
    redirect = request.GET.get('next')
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return HttpResponseRedirect(request.POST.get('redirect'))
        else:
            return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
        
    return render(request, 'auth/login.html', {'redirect': redirect})

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('newusername')
        email=request.POST.get('newuseremail')
        password=request.POST.get('newpassword')
        if User.objects.filter(username = username).exists():
            return render(request, 'auth/register.html', {'userAlreadyExists': True})
        elif User.objects.filter(email = email).exists():
            return render(request, 'auth/register.html', {'emailAlreadyExists': True})
        else:
            user = User.objects.create_user(username, email, password)
            if user:
                return redirect('/chat/')
                
        
    return render(request, 'auth/register.html')