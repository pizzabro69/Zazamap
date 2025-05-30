import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib import messages
from .models import MapPin, Review, Favorite, Profile, Conversation, Message
from django.utils import timezone
import json

def home(request):
    return render(request, 'mapapp/home.html')

def get_pins(request):
    pins = MapPin.objects.all()
    pins_data = []
    
    for pin in pins:
        pins_data.append({
            'id': pin.id,
            'title': pin.title,
            'description': pin.description,
            'latitude': pin.latitude,
            'longitude': pin.longitude,
            'category': pin.category,
            'username': pin.user.username if pin.user else 'Anonymous',
            'created_at': pin.created_at.isoformat(),
            'image': pin.image.url if pin.image else None,  # Make sure this returns the full URL
            'average_rating': pin.rating_set.aggregate(Avg('rating'))['rating__avg'] or 0 if hasattr(pin, 'rating_set') else 0,
            'rating_count': pin.rating_set.count() if hasattr(pin, 'rating_set') else 0,
            'is_favorite': request.user.is_authenticated and pin.favorite_set.filter(user=request.user).exists() if hasattr(pin, 'favorite_set') else False,
            
            # Add all amenity fields
            'has_seating': pin.has_seating,
            'is_scenic': pin.is_scenic,
            'is_sheltered': pin.is_sheltered,
            'is_private': pin.is_private,
            'is_accessible': pin.is_accessible,
            'security_level': pin.security_level
        })
    
    return JsonResponse(pins_data, safe=False)

@csrf_exempt
def create_pin(request):
    if request.method == 'POST':
        # Add logging to debug form data
        print("Form data:", request.POST)
        
        pin = MapPin(
            title=request.POST.get('title'),
            description=request.POST.get('description', ''),
            latitude=float(request.POST.get('latitude')),
            longitude=float(request.POST.get('longitude')),
            category=request.POST.get('category'),
            user=request.user if request.user.is_authenticated else None,
            
            # Process amenity fields properly
            has_seating=request.POST.get('has_seating') == 'on',
            is_scenic=request.POST.get('is_scenic') == 'on',
            is_sheltered=request.POST.get('is_sheltered') == 'on',
            is_private=request.POST.get('is_private') == 'on',
            is_accessible=request.POST.get('is_accessible') == 'on',
            security_level=int(request.POST.get('security_level', 1))
        )
        
        # Handle image upload
        if 'image' in request.FILES:
            pin.image = request.FILES['image']
            
        pin.save()
        
        # Return all pin data including amenities
        return JsonResponse({
            'id': pin.id,
            'title': pin.title,
            'description': pin.description,
            'latitude': pin.latitude,
            'longitude': pin.longitude,
            'category': pin.category,
            'username': pin.user.username if pin.user else 'Anonymous',
            'created_at': pin.created_at.isoformat(),
            'image': pin.image.url if pin.image else None,
            'has_seating': pin.has_seating,
            'is_scenic': pin.is_scenic,
            'is_sheltered': pin.is_sheltered,
            'is_private': pin.is_private,
            'is_accessible': pin.is_accessible,
            'security_level': pin.security_level
        })
    
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

@login_required
def my_profile(request):
    """Redirect to the user's own profile page"""
    return redirect('mapapp:profile', username=request.user.username)

def profile_view(request, username):
    """Display a user's profile"""
    user = get_object_or_404(User, username=username)
    
    # Get user statistics
    pins_created = MapPin.objects.filter(user=user).count()
    favorite_count = Favorite.objects.filter(user=user).count()
    review_count = Review.objects.filter(user=user).count()
    
    # Get pins created by user
    pins = MapPin.objects.filter(user=user).order_by('-created_at')
    
    context = {
        'profile_user': user,
        'pins_created': pins_created,
        'favorite_count': favorite_count,
        'review_count': review_count,
        'pins': pins,
        'is_own_profile': request.user == user if request.user.is_authenticated else False
    }
    
    return render(request, 'mapapp/profile.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        try:
            # Update email if provided
            email = request.POST.get('email')
            if email:
                request.user.email = email
                request.user.save()
            
            # Update profile picture if provided
            if request.FILES.get('avatar'):
                profile, created = Profile.objects.get_or_create(user=request.user)
                if profile.avatar:
                    profile.avatar.delete(save=False)  # Delete old avatar
                profile.avatar = request.FILES.get('avatar')
                profile.save()
            
            # Check if AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Profile updated successfully'})
            else:
                # Redirect back to profile page for non-AJAX requests
                messages.success(request, "Profile updated successfully.")
                return redirect('mapapp:my_profile')
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            else:
                messages.error(request, f"Error updating profile: {str(e)}")
                return redirect('mapapp:my_profile')
    
    # GET request redirects to profile
    return redirect('mapapp:my_profile')

def media(request, file_path=None):
    from django.conf import settings as cfg
    media_root = getattr(cfg, 'MEDIA_ROOT', None)

    if not media_root:
        return HttpResponseBadRequest('Invalid Media Root Configuration')
    if not file_path:
        return HttpResponseBadRequest('Invalid File Path')

    with open(os.path.join(media_root, file_path), 'rb') as doc:
        response = HttpResponse(doc.read(), content_type='application/doc')
        response['Content-Disposition'] = 'filename=%s' % (file_path.split('/')[-1])
        return response

@login_required
def inbox_view(request):
    """Display user's message inbox"""
    conversations = Conversation.objects.filter(participants=request.user)
    
    for conversation in conversations:
        conversation.other_user = conversation.get_other_participant(request.user)
        conversation.last_message = conversation.messages.last()
        # Count unread messages
        conversation.unread_count = conversation.messages.filter(
            is_read=False
        ).exclude(sender=request.user).count()
    
    context = {
        'conversations': conversations
    }
    return render(request, 'mapapp/inbox.html', context)

@login_required
def conversation_view(request, conversation_id=None, username=None):
    """Display a conversation with another user"""
    conversation = None
    other_user = None
    
    # Get conversation by ID or create new one with user by username
    if conversation_id:
        conversation = get_object_or_404(
            Conversation.objects.filter(participants=request.user), 
            id=conversation_id
        )
        other_user = conversation.get_other_participant(request.user)
    elif username:
        other_user = get_object_or_404(User, username=username)
        
        # Check if conversation already exists
        conversations = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants=other_user
        )
        
        if conversations.exists():
            conversation = conversations.first()
        else:
            # Create new conversation
            conversation = Conversation.objects.create()
            conversation.participants.add(request.user, other_user)
    
    if conversation:
        # Mark messages as read
        conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
        messages = conversation.messages.all()
    else:
        messages = []
    
    context = {
        'conversation': conversation,
        'messages': messages,
        'other_user': other_user
    }
    
    return render(request, 'mapapp/conversation.html', context)

@login_required
def send_message(request, conversation_id):
    """Send a message in a conversation"""
    conversation = get_object_or_404(
        Conversation.objects.filter(participants=request.user),
        id=conversation_id
    )
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        
        if content:
            message = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            
            # Update conversation timestamp
            conversation.updated_at = timezone.now()
            conversation.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message_id': message.id,
                    'created_at': message.created_at.strftime("%b %d, %Y, %I:%M %p")
                })
    
    return redirect('mapapp:conversation', conversation_id=conversation_id)

@login_required
def get_unread_count(request):
    """Get count of unread messages for the current user"""
    count = Message.objects.filter(
        conversation__participants=request.user,
        is_read=False
    ).exclude(sender=request.user).count()
    
    return JsonResponse({'unread_count': count})

@login_required
def get_new_messages(request, conversation_id):
    """Get new messages in a conversation since the given ID"""
    conversation = get_object_or_404(
        Conversation.objects.filter(participants=request.user),
        id=conversation_id
    )
    
    # Mark messages as read
    conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    
    # Get the ID to fetch messages since
    since_id = request.GET.get('since', 0)
    try:
        since_id = int(since_id)
    except ValueError:
        since_id = 0
    
    # Get new messages
    new_messages = conversation.messages.filter(id__gt=since_id)
    
    # Format messages for JSON response
    messages_data = []
    for message in new_messages:
        messages_data.append({
            'id': message.id,
            'content': message.content,
            'is_own': message.sender == request.user,
            'created_at': message.created_at.strftime("%b %d, %I:%M %p")  # Fixed format
        })
    
    return JsonResponse({'messages': messages_data})
