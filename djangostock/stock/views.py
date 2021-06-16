from django.shortcuts import render
import requests


def stock(request):
	return render(request, 'stock.html', {})

def home(request):
	return render(request, 'home.html', {})

