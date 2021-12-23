from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError

from django.http import HttpResponse
from main.rooms import room

from .models import Todo
from .forms import TodoForm
from django.contrib.auth import login,logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'main/index.html')

def register(request):
    return render(request, 'main/register.html')

def sing_in(request):
    return render(request, 'main/sign_in.html')

def Presidental(request):
    return render(request, 'main/Presidental.html')

def index2(request):
    data = {
        'title': 'About us',
        'values': ['Dias', 'Miras', 'Shah', 'Bek'],
        'obj': {
            'car': 'Nissan',
            'age': '14',
            'hobby': 'volleyball'
        }
    }
    return render(request, 'main/index2.html', data)

def contact_us(request):
    return render(request, 'main/contact_us.html')

def booking(request):
    rooms = [
        room("Junior Suite", "main/Images/0189_2(1)_0.webp"),
        room("Family Suite", "main/Images/IMG_6314.webp"),
        room("Luxury Suite", "main/Images/Suite 518 - BedroomT.webp"),
        room("Presidential Suite", "main/Images/Presidential Suite Main BedroomT.webp"),

        room("King Room", "Images/King%20room.jpg"),
        room("Twin Room", "main/Images/Twin room.jpg"),
        room("Superior", "main/Images/Superior.webp"),
        room("Royal Suite", "main/Images/Royal suite.jpg")
    ]
    return render(request, 'main/booking.html', {"rooms": rooms})

def rooms(request):
    rooms = [
        room("Junior Suite", "main/Images/0189_2(1)_0.webp"),
        room("Family Suite", "main/Images/IMG_6314.webp"),
        room("Luxury Suite", "main/Images/Suite 518 - BedroomT.webp"),
        room("Presidential Suite", "main/Images/Presidential Suite Main BedroomT.webp"),

        room("King Room", "Images/King%20room.jpg"),
        room("Twin Room", "main/Images/Twin room.jpg"),
        room("Superior", "main/Images/Superior.webp"),
        room("Royal Suite", "main/Images/Royal suite.jpg")
    ]
    User = Todo.objects.all()

def signupuser(request):
    if request.method == 'GET':
        return render(request, './main/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'] , password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodo')
            except IntegrityError:
                return render(request, './main/signupuser.html', {'form': UserCreationForm()},'error','this acc - ')
        else:
            return render(request, './main/signupuser.html', {'form': UserCreationForm()}, 'error', 'this acc no ')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'main/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'main/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodo')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'main/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodo')
        except ValueError:
            return render(request, 'main/createtodo.html', {'form':TodoForm(), 'error':'Bad data passed in. Try again.'})

@login_required
def currenttodo(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request,'./main/currenttodo.html',{'todos':todos})

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'main/completedtodos.html', {'todos':todos})

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'main/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodo')
        except ValueError:
            return render(request, 'main/viewtodo.html', {'todo':todo, 'form':form, 'error':'Bad info'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodo')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodo')