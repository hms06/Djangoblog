from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name="home"),
    path('stock', views.stock, name="stock"),
]