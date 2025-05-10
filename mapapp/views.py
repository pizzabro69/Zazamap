from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import MapPin
import json

def home(request):
    return render(request, 'mapapp/home.html')

def get_pins(request):
    pins = MapPin.objects.all()
    data = [{
        'id': pin.id,
        'title': pin.title,
        'description': pin.description,
        'latitude': pin.latitude,
        'longitude': pin.longitude,
        'created_at': pin.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'username': pin.user.username if pin.user else 'Anonymous',
        'image': pin.image.url if pin.image else None
    } for pin in pins]
    return JsonResponse(data, safe=False)

@csrf_exempt
@login_required
def create_pin(request):
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            description = request.POST.get('description')
            latitude = float(request.POST.get('latitude'))
            longitude = float(request.POST.get('longitude'))
            
            pin = MapPin(
                title=title,
                description=description,
                latitude=latitude,
                longitude=longitude,
                user=request.user
            )
            
            # Handle image if present
            if 'image' in request.FILES:
                pin.image = request.FILES['image']
                
            pin.save()
            
            return JsonResponse({
                'id': pin.id,
                'title': pin.title,
                'description': pin.description,
                'latitude': pin.latitude,
                'longitude': pin.longitude,
                'created_at': pin.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'username': pin.user.username,
                'image': pin.image.url if pin.image else None
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def about(request):
    return render(request, 'mapapp/about.html')

def contact(request):
    return render(request, 'mapapp/contact.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('mapapp:home')
        else:
            return render(request, 'mapapp/login.html', {'error_message': 'Invalid credentials'})
    return render(request, 'mapapp/login.html')

def logout_view(request):
    logout(request)
    return redirect('mapapp:home')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 != password2:
            return render(request, 'mapapp/register.html', {'error_message': 'Passwords do not match'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'mapapp/register.html', {'error_message': 'Username already exists'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'mapapp/register.html', {'error_message': 'Email already exists'})
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect('mapapp:home')
    
    return render(request, 'mapapp/register.html')
