from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.members, name='members'),
    path('login', views.login, name='login'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('services', views.services, name='services'),
     path('book', views.book, name='book'),
      path('plan', views.plan, name='plan'),
path('details/<int:id>/', views.details, name='details'),
        path('process_payment', views.process_payment, name='process_payment'),


]

 