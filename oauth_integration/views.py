from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.middleware.csrf import get_token, constant_time_compare
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.utils import timezone

from userauth.models import User, UserProfile, SocialMediaAccount
from SLID.secrets import (
    INSTAGRAM_CLIENT_ID, INSTAGRAM_CLIENT_SECRET,
    FACEBOOK_CLIENT_ID, FACEBOOK_CLIENT_SECRET
)

import requests
from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv

load_dotenv()


def create_social_media_account(user, platform, token_data):
    """Helper function to create or update social media account"""
    account, created = SocialMediaAccount.objects.get_or_create(
        user=user,
        platform=platform,
        defaults={
            'token': token_data.get('access_token'),
            'token_type': token_data.get('token_type', 'bearer'),
            'expires': timezone.now() + timedelta(seconds=token_data.get('expires_in', 3600)),
            'is_linked': True
        }
    )

    if not created:
        account.token = token_data.get('access_token')
        account.token_type = token_data.get('token_type', 'bearer')
        account.expires = timezone.now() + timedelta(seconds=token_data.get('expires_in', 3600))
        account.is_linked = True
        account.save()

    return account


@login_required
def instagramAuthorize(request):
    """Initiate Instagram OAuth flow"""
    csrf_token = get_token(request)
    request.session['instagram_csrf_token'] = csrf_token

    authorization_url = (
        f"https://api.instagram.com/oauth/authorize?"
        f"client_id={INSTAGRAM_CLIENT_ID}&"
        f"redirect_uri={settings.INSTAGRAM_REDIRECT_URI}&"
        f"scope=user_profile,user_media&"
        f"response_type=code&"
        f"state={csrf_token}"
    )
    return redirect(authorization_url)


@login_required
def instagramCallback(request):
    """Handle Instagram OAuth callback"""
    code = request.GET.get('code')
    state = request.GET.get('state')
    stored_state = request.session.get('instagram_csrf_token')

    if not code or not constant_time_compare(state, stored_state):
        messages.error(request, "Invalid authorization request")
        return redirect('profile_management:profile', username=request.user.username)

    try:
        # Exchange code for access token
        token_response = requests.post('https://api.instagram.com/oauth/access_token', data={
            'client_id': INSTAGRAM_CLIENT_ID,
            'client_secret': INSTAGRAM_CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'redirect_uri': settings.INSTAGRAM_REDIRECT_URI,
            'code': code
        })

        if token_response.status_code != 200:
            raise Exception("Failed to obtain access token")

        token_data = token_response.json()

        # Create or update Instagram account
        account = create_social_media_account(request.user, 'instagram', token_data)
        messages.success(request, "Instagram account connected successfully")

    except Exception as e:
        messages.error(request, f"Failed to connect Instagram account: {str(e)}")

    return redirect('profile_management:profile', username=request.user.username)


@login_required
def facebookAuthorize(request):
    """Initiate Facebook OAuth flow"""
    csrf_token = get_token(request)
    request.session['facebook_csrf_token'] = csrf_token

    authorization_url = (
        f"https://www.facebook.com/v12.0/dialog/oauth?"
        f"client_id={FACEBOOK_CLIENT_ID}&"
        f"redirect_uri={settings.FACEBOOK_REDIRECT_URI}&"
        f"scope=email,public_profile,user_posts&"
        f"state={csrf_token}"
    )
    return redirect(authorization_url)


@login_required
def facebookCallback(request):
    """Handle Facebook OAuth callback"""
    code = request.GET.get('code')
    state = request.GET.get('state')
    stored_state = request.session.get('facebook_csrf_token')

    if not code or not constant_time_compare(state, stored_state):
        messages.error(request, "Invalid authorization request")
        return redirect('profile_management:profile', username=request.user.username)

    try:
        # Exchange code for access token
        token_response = requests.get('https://graph.facebook.com/v12.0/oauth/access_token', params={
            'client_id': FACEBOOK_CLIENT_ID,
            'client_secret': FACEBOOK_CLIENT_SECRET,
            'redirect_uri': settings.FACEBOOK_REDIRECT_URI,
            'code': code
        })

        if token_response.status_code != 200:
            raise Exception("Failed to obtain access token")

        token_data = token_response.json()

        # Create or update Facebook account
        account = create_social_media_account(request.user, 'facebook', token_data)
        messages.success(request, "Facebook account connected successfully")

    except Exception as e:
        messages.error(request, f"Failed to connect Facebook account: {str(e)}")

    return redirect('profile_management:profile', username=request.user.username)


@login_required
def disconnectPlatform(request, platform):
    """Disconnect a social media platform"""
    try:
        account = SocialMediaAccount.objects.get(user=request.user, platform=platform)
        account.is_linked = False
        account.save()
        messages.success(request, f"{platform.title()} account disconnected successfully")
    except SocialMediaAccount.DoesNotExist:
        messages.error(request, f"No {platform.title()} account found")

    return redirect('profile_management:profile', username=request.user.username)