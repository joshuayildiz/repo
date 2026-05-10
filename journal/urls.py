from django.urls import path
from . import views

urlpatterns = [
	path('history/', views.history, name='history'),
	path('new/', views.new, name='new'),
	path('', views.stock, name='stock'),
]