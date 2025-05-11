from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import MapPin, Review, Favorite
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
        'image': pin.image.url if pin.image else None,
        'average_rating': pin.average_rating(),
        'rating_count': Review.objects.filter(pin=pin).count(),
        'category': pin.category
    } for pin in pins]
    return JsonResponse(data, safe=False)

@csrf_exempt
@login_required
def create_pin(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        image = request.FILES.get('image')
        category = request.POST.get('category', 'smoke')
        
        # Get amenities
        has_seating = request.POST.get('has_seating') == 'on'
        is_scenic = request.POST.get('is_scenic') == 'on'
        is_sheltered = request.POST.get('is_sheltered') == 'on'
        is_private = request.POST.get('is_private') == 'on'
        is_accessible = request.POST.get('is_accessible') == 'on'
        security_level = int(request.POST.get('security_level', 1))
        
        try:
            pin = MapPin.objects.create(
                title=title,
                description=description,
                latitude=latitude,
                longitude=longitude,
                user=request.user,
                image=image,
                category=category,
                has_seating=has_seating,
                is_scenic=is_scenic,
                is_sheltered=is_sheltered,
                is_private=is_private,
                is_accessible=is_accessible,
                security_level=security_level
            )
            
            return JsonResponse({
                'id': pin.id,
                'title': pin.title,
                'description': pin.description,
                'latitude': pin.latitude,
                'longitude': pin.longitude,
                'created_at': pin.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'username': request.user.username,
                'image': pin.image.url if pin.image else None,
                'category': pin.category,
                'has_seating': pin.has_seating,
                'is_scenic': pin.is_scenic,
                'is_sheltered': pin.is_sheltered,
                'is_private': pin.is_private,
                'is_accessible': pin.is_accessible,
                'security_level': pin.security_level
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
@login_required
def create_review(request, pin_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pin = get_object_or_404(MapPin, id=pin_id)
            rating = int(data.get('rating'))
            comment = data.get('comment', '')
            
            # Check rating is between 1-5
            if not (1 <= rating <= 5):
                return JsonResponse({'error': 'Rating must be between 1 and 5'}, status=400)
            
            # Create or update the review
            review, created = Review.objects.update_or_create(
                pin=pin,
                user=request.user,
                defaults={'rating': rating, 'comment': comment}
            )
            
            return JsonResponse({
                'id': review.id,
                'rating': review.rating,
                'comment': review.comment,
                'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'username': review.user.username,
                'pin_id': pin.id,
                'average_rating': pin.average_rating(),
                'rating_count': pin.reviews.count()
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
@login_required
def delete_pin(request, pin_id):
    if request.method == 'DELETE':
        try:
            pin = get_object_or_404(MapPin, id=pin_id)
            
            # Check if the requesting user is the pin owner
            if pin.user != request.user:
                return JsonResponse({'error': 'You do not have permission to delete this pin'}, status=403)
            
            # Delete the pin
            pin.delete()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_reviews(request, pin_id):
    pin = get_object_or_404(MapPin, id=pin_id)
    reviews = Review.objects.filter(pin=pin).order_by('-created_at')
    
    data = [{
        'id': review.id,
        'rating': review.rating,
        'comment': review.comment,
        'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'username': review.user.username,
    } for review in reviews]
    
    return JsonResponse({
        'reviews': data,
        'average_rating': pin.average_rating(),
        'rating_count': reviews.count()
    })

@csrf_exempt
@login_required
def toggle_favorite(request, pin_id):
    if request.method == 'POST':
        try:
            pin = MapPin.objects.get(id=pin_id)
            favorite, created = Favorite.objects.get_or_create(user=request.user, pin=pin)
            
            if not created:  # If favorite already existed, remove it
                favorite.delete()
                return JsonResponse({'status': 'removed', 'message': 'Pin removed from favorites'})
            
            return JsonResponse({'status': 'added', 'message': 'Pin added to favorites'})
            
        except MapPin.DoesNotExist:
            return JsonResponse({'error': 'Pin not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def get_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('pin')
    data = [{
        'id': fav.pin.id,
        'title': fav.pin.title,
        'description': fav.pin.description,
        'latitude': fav.pin.latitude,
        'longitude': fav.pin.longitude,
        'created_at': fav.pin.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'username': fav.pin.user.username if fav.pin.user else 'Anonymous',
        'image': fav.pin.image.url if fav.pin.image else None,
        'average_rating': fav.pin.average_rating(),
        'rating_count': Review.objects.filter(pin=fav.pin).count(),
        'category': fav.pin.category
    } for fav in favorites]
    
    return JsonResponse(data, safe=False)

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
