from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .forms import User_form, Room_form
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Message, Topic, User_activity
from django.db.models import Q
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

def search(request):
    if request.method == 'POST':
        search = request.POST.get('search_bar')
        room_filter = Room.objects.filter(
            Q(room_topic__topic_name__icontains=search) |
            Q(room_name__icontains=search) |
            Q(room_desription__icontains=search)
        )
        return render(request, 'fish/search_page.html', {'room_filter':room_filter})

def home(request):
    rooms = Room.objects.all()[0:6]
    topics = Topic.objects.all()[0:15]
    messages_comp = Message.objects.all()[0:13]
    context = {'rooms':rooms, 'messages_comp':messages_comp, 'topics':topics}
    return render(request, 'fish/home.html', context)

def room_form(request):
    room_form = Room_form()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name_request = request.POST.get("room_topic")
        topic_room, created = Topic.objects.get_or_create(topic_name=topic_name_request)
        Room.objects.create(
            host=request.user,
            room_topic = topic_room,
            room_name=request.POST.get('room_name'),
            room_desription=request.POST.get('room_desription'),
        )
        if not User_activity.objects.filter(activity_topic=topic_room, activity_user=request.user):
            User_activity.objects.create(
                activity_user = request.user,
                activity_topic = topic_room
            )
        return redirect("home")
    context = {"room_form":room_form, 'topics':topics}
    return render(request, 'fish/room_form.html', context)

def room_page(request, pk):
    rooms = Room.objects.get(id=pk)
    messages_room = rooms.message_set.all()
    parties = rooms.participants.all()
    context = {'rooms':rooms,"messages_room":messages_room, 'parties':parties}
    if request.method == 'POST':
        Message.objects.create(
            room_messages = rooms,
            owner = request.user,
            body = request.POST.get('body')
        )
        if not User_activity.objects.filter(activity_topic=rooms.room_topic.id, activity_user=request.user):
            User_activity.objects.create(
                activity_user = request.user,
                activity_topic = rooms.room_topic
            )
        rooms.participants.add(request.user)
        return redirect('room_page', rooms.id)
    return render(request, 'fish/room_page.html', context)



def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'fish/delete.html', {'instance':message})

def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'fish/delete.html', {'instance':room})

def update(request, pk):
    room = Room.objects.get(id=pk)
    room_form = Room_form(instance=room)
    topics = Topic.objects.all()
    context = {'room':room, 'room_form':room_form, 'topics':topics}
    if request.method == 'POST':
        topic_name_request = request.POST.get('room_topic')
        topic_room, created = Topic.objects.get_or_create(topic_name=topic_name_request)
        room.room_topic = topic_room
        room_desription_request = request.POST.get('room_desription')
        room.room_desription = room_desription_request
        room_name_request = request.POST.get('room_name')
        room.room_name = room_name_request
        room.save()
        return redirect('home')
    return render(request, 'fish/update.html', context)

def profile_page(request, pk):
    profile_link = User.objects.get(id=pk)
    activity_data = User_activity.objects.filter(activity_user=profile_link)
    rooms = profile_link.room_set.all()
    message = profile_link.message_set.all()
    context = {'profile_link':profile_link, 'message':message, 'rooms':rooms, 'activity_data':activity_data}
    return render(request, 'fish/profile_page.html', context)

def topics_page(request, pk):
    topics = Topic.objects.get(id=pk)
    rooms = topics.room_set.all()
    context = {'topics':topics, 'rooms':rooms}
    return render(request, 'fish/topics.html', context)

def message_component(request):
    messages_comp = Message.objects.all()[0:5]
    context = {"messages_comp":messages_comp}
    return render(request, 'fish/messages_component.html', context)

def rooms_component(request):
    rooms_comp = Room.objects.all()
    context  = {'rooms_comp':rooms_comp}
    return render(request, 'fish/rooms_component.html', context)

def topics_component(request):
    topics_comp = Topic.objects.all()[0:2]
    context = {'topics_comp':topics_comp}
    return render(request, 'fish/topics_component.html', context)