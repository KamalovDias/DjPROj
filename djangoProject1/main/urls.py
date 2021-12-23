from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('booking/', views.booking, name='booking'),
    path('about us', views.index2, name='index2'),
    path('contact us', views.contact_us, name='contact_us'),
    path('Presidental', views.Presidental, name='Presidental'),

    path('register/', views.register, name='register'),
    path('sign_in/', views.sing_in, name='sign_in'),
    path('login/', views.loginuser, name='loginuser'),
    path('signup/',views.signupuser,name = 'signupuser'),

    path('current/',views.currenttodo,name = 'currenttodo'),
    path('completed/', views.completedtodos, name='completedtodos'),
    path('create/', views.createtodo, name='createtodo'),
    path('todo/<int:todo_pk>', views.viewtodo, name='viewtodo'),
    path('todo/<int:todo_pk>/complete', views.completetodo, name='completetodo'),
    path('todo/<int:todo_pk>/delete', views.deletetodo, name='deletetodo')
]