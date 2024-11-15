from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.middleware.csrf import get_token, constant_time_compare
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.utils import timezone

from userauth.forms import UserForm, MyUserCreationForm, UserProfileForm
from userauth.models import (
    User, UserProfile, TermsAndConditions, SocialMediaAccount, Post, Connection
)
import requests
from SLID.secrets import (
    INSTAGRAM_CLIENT_ID, INSTAGRAM_CLIENT_SECRET,
    FACEBOOK_CLIENT_ID, FACEBOOK_CLIENT_SECRET
)
from langchain_community.agent_toolkits.sql import create_sql_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()

# Social Media API Functions
def fetch_social_media_data(account):
    """Generic function to fetch data from social media platforms"""
    platform_handlers = {
        'instagram': fetch_instagram_data,
        'facebook': fetch_facebook_data
    }
    
    handler = platform_handlers.get(account.platform)
    if handler:
        return handler(account.token)
    return None

def fetch_instagram_data(token):
    """Fetch Instagram data using the platform's API"""
    api_url = 'https://graph.instagram.com/me/media'
    params = {
        'fields': 'id,caption,media_type,media_url,thumbnail_url,username,timestamp',
        'access_token': token
    }
    response = requests.get(api_url, params=params)
    return response.json() if response.status_code == 200 else None

def fetch_facebook_data(token):
    """Fetch Facebook data using the platform's API"""
    api_url = 'https://graph.facebook.com/v12.0/me'
    params = {
        'fields': 'name,email,birthday,photos,posts,likes,events,hometown,friends',
        'access_token': token
    }
    response = requests.get(api_url, params=params)
    return response.json() if response.status_code == 200 else None

# Profile Views
@login_required
def profile(request, username):
    """Display user profile with social media integrations"""
    profile = get_object_or_404(User, username=username)
    logged_user_profile = UserProfile.objects.get(user=request.user)
    is_own_profile = request.user.is_authenticated and request.user.username == profile.username

    is_connected = Connection.objects.filter(
        user=request.user,
        connected_user=profile,
        is_deleted=False
    ).exists()

    try:
        user_profile = UserProfile.objects.get(user=profile)
        social_accounts = SocialMediaAccount.objects.filter(
            user=profile,
            is_linked=True
        )
        
        # Update social media data
        for account in social_accounts:
            platform_data = fetch_social_media_data(account)
            if platform_data:
                account.data = platform_data
                account.last_sync = timezone.now()
                account.save()

    except ObjectDoesNotExist:
        user_profile = None
        social_accounts = []

    posts = Post.objects.filter(user=profile).order_by('-created_at')
    connected_users = Connection.objects.filter(user=profile)
    recent_posts_from_connected_users = Post.objects.filter(
        user__in=connected_users.values_list('connected_user', flat=True)
    ).order_by('-created_at')[:4]

    context = {
        "user_profile": user_profile,
        "logged_user_profile": logged_user_profile,
        "is_own_profile": is_own_profile,
        "is_connected": is_connected,
        "posts": posts,
        "social_accounts": social_accounts,
        "recent_posts_from_connected_users": recent_posts_from_connected_users,
        "connected_users": connected_users,
    }
    return render(request, "userauth/members-page.html", context)

# AI Integration Functions
def get_user_profile(user):
    """Fetch comprehensive user profile data"""
    try:
        user_account = User.objects.get(username=user)
        user_profile = UserProfile.objects.get(user=user)
        social_accounts = SocialMediaAccount.objects.filter(user=user, is_linked=True)
        
        return {
            'profile': {
                'username': user_account.username,
                'email': user_account.email,
                'date_joined': user_account.date_joined,
                'last_login': user_account.last_login,
                'full_name': user_profile.fullName,
                'bio': user_profile.bio,
                'profile_picture': user_profile.profilePicture.url if user_profile.profilePicture else None,
                'qr_code': user_profile.qr_code.url if user_profile.qr_code else None,
                'user_code': user_profile.user_code,
                'verified': user_profile.verified,
                'created_at': user_profile.created_at,
            },
            'social_media': {
                account.platform: account.data
                for account in social_accounts
            }
        }
    except (UserProfile.DoesNotExist, User.DoesNotExist):
        return None

# AI and Database Integration
def construct_schema_prompt():
    """Generate database schema description for AI queries"""
    return """
    Database Schema:
    - UserProfile: User details (fullName, bio, profilePicture, verified status)
    - SocialMediaAccount: Unified social platform data
        * Platform types: instagram, facebook, youtube, linkedin, google, x, tiktok
        * Stores: authentication, platform data, connection status
    - Connection: User relationships and networking
    - Post: Content shared across platforms
    """


@login_required
def ai(request):
    """Handle AI-powered user data analysis and queries"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    user_query = request.POST.get('data')
    if not user_query:
        return JsonResponse({'error': 'No query provided'}, status=400)

    try:
        # Get user context including social media data
        user_data = get_user_profile(request.user)
        if not user_data:
            return JsonResponse({'error': 'User profile not found'}, status=404)

        # Initialize AI components
        db = SQLDatabase.from_uri(os.getenv('DATABASE_URL'))
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=os.getenv('OPENAI_API_KEY')
        )

        # Create and execute AI agent
        agent = create_sql_agent(llm, db=db, verbose=True)

        # Include social media context in the query
        enhanced_query = f"""
        Context: User {user_data['profile']['username']} with {len(user_data['social_media'])} connected platforms.
        Query: {user_query}
        Schema: {construct_schema_prompt()}
        """

        answer = agent.run(enhanced_query)
        return JsonResponse({'message': answer})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def members(request):
    """Display and search member profiles"""
    search_query = request.POST.get('search_query', '')

    # Base queryset excluding the current user
    users_profile = UserProfile.objects.exclude(user=request.user)

    if search_query:
        users_profile = users_profile.filter(
            Q(user__username__icontains=search_query) |
            Q(fullName__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(user_code__icontains=search_query)
        )

    # Get current user's profile and connections
    logged_user_profile = UserProfile.objects.get(user=request.user)
    connected_users = Connection.objects.filter(
        user=request.user,
        is_deleted=False
    ).values_list('connected_user', flat=True)

    context = {
        "users_profile": users_profile,
        "logged_user_profile": logged_user_profile,
        "connected_users": connected_users,
    }
    return render(request, "userauth/members2.html", context)

@login_required
def update_profile(request):
    """Handle user profile updates"""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile_management:profile', username=request.user.username)
    
    return redirect('profile_management:profile', username=request.user.username)

@login_required
def connect(request, username):
    """Create a connection between users"""
    try:
        connected_user = User.objects.get(username=username)

        # Check if connection already exists
        connection, created = Connection.objects.get_or_create(
            user=request.user,
            connected_user=connected_user,
            defaults={'is_deleted': False}
        )

        if not created and connection.is_deleted:
            # Reactivate soft-deleted connection
            connection.is_deleted = False
            connection.save()
        elif not created:
            messages.info(request, "Connection already exists")

    except User.DoesNotExist:
        messages.error(request, "User not found")

    return redirect('profile_management:profile', username=username)


@login_required
def disconnect(request, username):
    """Soft delete a connection between users"""
    try:
        connected_user = User.objects.get(username=username)
        connection = Connection.objects.get(
            user=request.user,
            connected_user=connected_user
        )
        connection.is_deleted = True
        connection.save()
        messages.success(request, "Connection removed")
    except (User.DoesNotExist, Connection.DoesNotExist):
        messages.error(request, "Connection not found")

    return redirect('profile_management:profile', username=username)