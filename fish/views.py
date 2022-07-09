from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .forms import User_form, Room_form
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Message, Topic
# Create your views here.

def user_register(request):
    status = 'register'
    form_register = UserCreationForm()

    if request.method == 'POST':
        form_register = UserCreationForm(request.POST)
        if form_register.is_valid():
            user = form_register.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
    context = {'status':status, 'form_register':form_register}
    return render(request, 'fish/login_register.html', context)

def user_login(request):
    status = 'login'
    login_form = User_form()

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_status = True
        try:
            user = User.objects.get(username=username)
        except:
            user_status = False

        user = authenticate(request, username=username, password=password)
        if (user_status is False) or (user is None):
            messages.error(request, 'Błędna nazwa użytkowinka lub hasło')
        else:
            login(request, user)
            return redirect('home')

    context = {'login_form':login_form, 'status':status}
    return render(request, 'fish/login_register.html', context)

def user_logout(request):
    logout(request)
    return redirect('/')


def home(request):
    rooms = Room.objects.all()
    topics = Topic.objects.all()
    messages_comp = Message.objects.all()
    context = {'rooms':rooms, 'messages_comp':messages_comp, 'topics':topics}
    return render(request, 'fish/home.html', context)

def room_page(request, pk):
    rooms = Room.objects.get(id=pk)
    messages_room = Message.objects.all()
    context = {'rooms':rooms,"messages_room":messages_room}
    return render(request, 'fish/room_page.html', context)

def room_form(request):
    room_form = Room_form()
    topics = Topic.objects.all()
    context = {"room_form":room_form, 'topics':topics}
    if request.method == "POST":
        topic_n = request.POST.get("room_topic")
        room_topic, created = Topic.objects.get_or_create(topic_name=topic_n)
        Room.objects.create(
            host=request.user,
            room_topic = room_topic,
            room_name=request.POST.get('room_name'),
            room_desription=request.POST.get('room_desription'),
        )

        return redirect("home")
    return render(request, 'fish/room_form.html', context)

def message_component(request):
    messages_comp = Message.objects.all()
    context = {"messages_comp":messages_comp}
    return render(request, 'fish/messages_component.html', context)

def rooms_component(request):
    rooms_comp = Room.objects.all()
    context  = {'rooms_comp':rooms_comp}
    return render(request, 'fish/rooms_component.html', context)

def topics_component(request):
    topics_comp = Topic.objects.all()
    context = {'topics_comp':topics_comp}
    return render(request, 'fish/topics_component.html', context)