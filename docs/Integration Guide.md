# Social Media Integration Guide

## Introduction

This guide explains how to integrate SLID with various social media platforms. SLID currently supports integration with Facebook, Instagram, YouTube, LinkedIn, Google, X (formerly Twitter), and TikTok. This document provides detailed instructions for developers who want to set up these integrations or extend support to additional platforms.

## Prerequisites

Before integrating with any social media platform, ensure you have:

1. A SLID developer account
2. Developer accounts on the platforms you want to integrate with
3. Familiarity with OAuth 2.0 authentication flows
4. Understanding of REST APIs and JSON data structures
5. Knowledge of Django web framework

## General Integration Process

While each platform has its specific requirements, the general integration process follows these steps:

1. **Register Application**: Create a developer application on the social media platform
2. **Configure OAuth**: Set up OAuth credentials and permissions
3. **Implement Authorization Flow**: Create endpoints to handle authorization
4. **Access Token Management**: Securely store and refresh access tokens
5. **Data Retrieval and Posting**: Connect to the platform's API for content

## Facebook Integration

### Setting Up Facebook Developer App

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app (choose "Consumer" as the app type)
3. Navigate to Settings > Basic and note your App ID and App Secret
4. Add the Facebook Login product to your app
5. Under Facebook Login > Settings, add the following Redirect URIs:
   - `https://your-slid-domain.com/oauth/facebook/callback/`
   - `http://localhost:8000/oauth/facebook/callback/` (for development)

### Required Permissions

Request these permissions in your OAuth scope:
- `email` - Access to user's email
- `public_profile` - Access to user's public profile
- `user_posts` - Access to user's posts

### Authorization Flow

Implement these views for Facebook OAuth:

```python
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
```

### Data Retrieval

Fetch Facebook data using:

```python
def fetch_facebook_data(token):
    """Fetch Facebook data using the platform's API"""
    api_url = 'https://graph.facebook.com/v12.0/me'
    params = {
        'fields': 'name,email,birthday,photos,posts,likes,events,hometown,friends',
        'access_token': token
    }
    response = requests.get(api_url, params=params)
    return response.json() if response.status_code == 200 else None
```

## Instagram Integration

### Setting Up Instagram Developer App

1. Create a Facebook Developer account if you don't have one
2. Create a new app (Instagram APIs are part of Facebook's platform)
3. Add the "Instagram Basic Display" product
4. Configure your app settings:
   - Go to Instagram Basic Display > Basic Display
   - Add your OAuth Redirect URIs:
     - `https://your-slid-domain.com/oauth/instagram/callback/`
     - `http://localhost:8000/oauth/instagram/callback/` (for development)
   - Add your Deauthorize Callback URL
   - Add your Data Deletion Request URL
5. Note your Instagram App ID and App Secret

### Required Permissions

Request these permissions in your OAuth scope:
- `user_profile` - Basic profile information
- `user_media` - Photos and videos in the user's Instagram account

### Authorization Flow

Implement these views for Instagram OAuth:

```python
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
```

### Data Retrieval

Fetch Instagram data using:

```python
def fetch_instagram_data(token):
    """Fetch Instagram data using the platform's API"""
    api_url = 'https://graph.instagram.com/me/media'
    params = {
        'fields': 'id,caption,media_type,media_url,thumbnail_url,username,timestamp',
        'access_token': token
    }
    response = requests.get(api_url, params=params)
    return response.json() if response.status_code == 200 else None
```

## YouTube/Google Integration

### Setting Up Google Developer Project

1. Go to the [Google Developer Console](https://console.developers.google.com/)
2. Create a new project
3. Navigate to "APIs & Services" > "Library"
4. Enable the YouTube Data API v3
5. Go to "APIs & Services" > "Credentials"
6. Create an OAuth 2.0 Client ID
7. Configure the OAuth consent screen
8. Add authorized redirect URIs:
   - `https://your-slid-domain.com/oauth/google/callback/`
   - `http://localhost:8000/oauth/google/callback/` (for development)
9. Note your Client ID and Client Secret

### Required Permissions

Request these permission scopes:
- `https://www.googleapis.com/auth/youtube.readonly` - Read-only access to YouTube data
- `https://www.googleapis.com/auth/userinfo.profile` - User profile info
- `https://www.googleapis.com/auth/userinfo.email` - User email

### Authorization Flow

Implement these views for Google/YouTube OAuth:

```python
@login_required
def googleAuthorize(request):
    """Initiate Google OAuth flow"""
    csrf_token = get_token(request)
    request.session['google_csrf_token'] = csrf_token

    authorization_url = (
        f"https://accounts.google.com/o/oauth2/auth?"
        f"client_id={GOOGLE_CLIENT_ID}&"
        f"redirect_uri={settings.GOOGLE_REDIRECT_URI}&"
        f"scope=https://www.googleapis.com/auth/youtube.readonly "
        f"https://www.googleapis.com/auth/userinfo.profile "
        f"https://www.googleapis.com/auth/userinfo.email&"
        f"response_type=code&"
        f"access_type=offline&"
        f"state={csrf_token}"
    )
    return redirect(authorization_url)

@login_required
def googleCallback(request):
    """Handle Google OAuth callback"""
    code = request.GET.get('code')
    state = request.GET.get('state')
    stored_state = request.session.get('google_csrf_token')

    if not code or not constant_time_compare(state, stored_state):
        messages.error(request, "Invalid authorization request")
        return redirect('profile_management:profile', username=request.user.username)

    try:
        # Exchange code for access token
        token_response = requests.post('https://oauth2.googleapis.com/token', data={
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': settings.GOOGLE_REDIRECT_URI
        })

        if token_response.status_code != 200:
            raise Exception("Failed to obtain access token")

        token_data = token_response.json()

        # Create or update Google account
        account = create_social_media_account(request.user, 'google', token_data)
        
        # If specifically connecting for YouTube
        if request.session.get('connect_youtube'):
            # Mark this Google connection as for YouTube
            account.platform = 'youtube'
            account.save()
            messages.success(request, "YouTube account connected successfully")
        else:
            messages.success(request, "Google account connected successfully")

    except Exception as e:
        messages.error(request, f"Failed to connect Google account: {str(e)}")

    return redirect('profile_management:profile', username=request.user.username)
```

### Data Retrieval

Fetch YouTube data using:

```python
def fetch_youtube_data(token):
    """Fetch YouTube data using the platform's API"""
    api_url = 'https://www.googleapis.com/youtube/v3/channels'
    params = {
        'part': 'snippet,contentDetails,statistics',
        'mine': 'true',
        'access_token': token
    }
    
    # Get the channel info first
    response = requests.get(api_url, params=params)
    if response.status_code != 200:
        return None
        
    channel_data = response.json()
    channel_id = channel_data['items'][0]['id']
    
    # Now get videos for this channel
    videos_url = 'https://www.googleapis.com/youtube/v3/search'
    videos_params = {
        'part': 'snippet',
        'channelId': channel_id,
        'maxResults': 50,
        'order': 'date',
        'access_token': token
    }
    
    videos_response = requests.get(videos_url, params=videos_params)
    if videos_response.status_code != 200:
        return channel_data
        
    # Combine the data
    return {
        'channel': channel_data,
        'videos': videos_response.json()
    }
```

## LinkedIn Integration

### Setting Up LinkedIn Developer App

1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Create a new app
3. Request the necessary products (Sign In with LinkedIn, Share on LinkedIn)
4. Configure OAuth 2.0 settings and add authorized redirect URLs:
   - `https://your-slid-domain.com/oauth/linkedin/callback/`
   - `http://localhost:8000/oauth/linkedin/callback/` (for development)
5. Note your Client ID and Client Secret

### Required Permissions

Request these permission scopes:
- `r_liteprofile` - Basic profile information
- `r_emailaddress` - Email address
- `w_member_social` - Post to LinkedIn (optional)

### Authorization Flow

Implement these views for LinkedIn OAuth:

```python
@login_required
def linkedinAuthorize(request):
    """Initiate LinkedIn OAuth flow"""
    csrf_token = get_token(request)
    request.session['linkedin_csrf_token'] = csrf_token

    authorization_url = (
        f"https://www.linkedin.com/oauth/v2/authorization?"
        f"client_id={LINKEDIN_CLIENT_ID}&"
        f"redirect_uri={settings.LINKEDIN_REDIRECT_URI}&"
        f"scope=r_liteprofile%20r_emailaddress%20w_member_social&"
        f"response_type=code&"
        f"state={csrf_token}"
    )
    return redirect(authorization_url)

@login_required
def linkedinCallback(request):
    """Handle LinkedIn OAuth callback"""
    code = request.GET.get('code')
    state = request.GET.get('state')
    stored_state = request.session.get('linkedin_csrf_token')

    if not code or not constant_time_compare(state, stored_state):
        messages.error(request, "Invalid authorization request")
        return redirect('profile_management:profile', username=request.user.username)

    try:
        # Exchange code for access token
        token_response = requests.post('https://www.linkedin.com/oauth/v2/accessToken', data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.LINKEDIN_REDIRECT_URI,
            'client_id': LINKEDIN_CLIENT_ID,
            'client_secret': LINKEDIN_CLIENT_SECRET
        })

        if token_response.status_code != 200:
            raise Exception("Failed to obtain access token")

        token_data = token_response.json()

        # Create or update LinkedIn account
        account = create_social_media_account(request.user, 'linkedin', token_data)
        messages.success(request, "LinkedIn account connected successfully")

    except Exception as e:
        messages.error(request, f"Failed to connect LinkedIn account: {str(e)}")

    return redirect('profile_management:profile', username=request.user.username)
```

### Data Retrieval

Fetch LinkedIn data using:

```python
def fetch_linkedin_data(token):
    """Fetch LinkedIn data using the platform's API"""
    headers = {
        'Authorization': f"Bearer {token}",
        'cache-control': 'no-cache',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    
    # Get basic profile information
    profile_response = requests.get('https://api.linkedin.com/v2/me', headers=headers)
    if profile_response.status_code != 200:
        return None
    
    profile_data = profile_response.json()
    
    # Get email address
    email_response = requests.get('https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))', headers=headers)
    if email_response.status_code == 200:
        email_data = email_response.json()
        profile_data['email'] = email_data
    
    return profile_data
```

## X (Twitter) Integration

### Setting Up X Developer App

1. Go to [X Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a new Project and App
3. Apply for Elevated access if needed for additional endpoints
4. Set up the OAuth 2.0 settings:
   - Enable OAuth 2.0
   - Add the callback URLs:
     - `https://your-slid-domain.com/oauth/twitter/callback/`
     - `http://localhost:8000/oauth/twitter/callback/` (for development)
   - Select the required scopes
5. Note your Client ID and Client Secret

### Required Permissions

Request these permission scopes:
- `tweet.read` - Read Tweets from X
- `users.read` - Read user profile information
- `offline.access` - Get a refresh token

### Authorization Flow

Implement these views for X OAuth:

```python
@login_required
def twitterAuthorize(request):
    """Initiate X (Twitter) OAuth flow"""
    csrf_token = get_token(request)
    request.session['twitter_csrf_token'] = csrf_token

    authorization_url = (
        f"https://twitter.com/i/oauth2/authorize?"
        f"client_id={TWITTER_CLIENT_ID}&"
        f"redirect_uri={settings.TWITTER_REDIRECT_URI}&"
        f"scope=tweet.read%20users.read%20offline.access&"
        f"response_type=code&"
        f"state={csrf_token}"
    )
    return redirect(authorization_url)

@login_required
def twitterCallback(request):
    """Handle X (Twitter) OAuth callback"""
    code = request.GET.get('code')
    state = request.GET.get('state')
    stored_state = request.session.get('twitter_csrf_token')

    if not code or not constant_time_compare(state, stored_state):
        messages.error(request, "Invalid authorization request")
        return redirect('profile_management:profile', username=request.user.username)

    try:
        # Convert client ID and secret to Base64 for Basic Auth
        auth_str = f"{TWITTER_CLIENT_ID}:{TWITTER_CLIENT_SECRET}"
        auth_bytes = auth_str.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')

        # Exchange code for access token
        token_response = requests.post(
            'https://api.twitter.com/2/oauth2/token',
            headers={
                'Authorization': f'Basic {auth_b64}',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={
                'code': code,
                'grant_type': 'authorization_code',
                'client_id': TWITTER_CLIENT_ID,
                'redirect_uri': settings.TWITTER_REDIRECT_URI,
                'code_verifier': 'challenge'  # Should be generated and stored properly
            }
        )

        if token_response.status_code != 200:
            raise Exception("Failed to obtain access token")

        token_data = token_response.json()

        # Create or update X (Twitter) account
        account = create_social_media_account(request.user, 'x', token_data)
        messages.success(request, "X (Twitter) account connected successfully")

    except Exception as e:
        messages.error(request, f"Failed to connect X (Twitter) account: {str(e)}")

    return redirect('profile_management:profile', username=request.user.username)
```

### Data Retrieval

Fetch X (Twitter) data using:

```python
def fetch_twitter_data(token):
    """Fetch X (Twitter) data using the platform's API"""
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json'
    }
    
    # Get user information
    me_response = requests.get('https://api.twitter.com/2/users/me?user.fields=description,profile_image_url,public_metrics', headers=headers)
    if me_response.status_code != 200:
        return None
    
    user_data = me_response.json()
    user_id = user_data['data']['id']
    
    # Get recent tweets
    tweets_response = requests.get(
        f'https://api.twitter.com/2/users/{user_id}/tweets?max_results=100&tweet.fields=created_at,public_metrics',
        headers=headers
    )
    
    if tweets_response.status_code == 200:
        user_data['tweets'] = tweets_response.json()
    
    return user_data
```

## TikTok Integration

### Setting Up TikTok Developer App

1. Go to [TikTok for Developers](https://developers.tiktok.com/)
2. Create a new app under TikTok Login Kit
3. Configure your app settings:
   - Add redirect domains
   - Set up callback URLs:
     - `https://your-slid-domain.com/oauth/tiktok/callback/`
     - `http://localhost:8000/oauth/tiktok/callback/` (for development)
4. Note your Client Key and Client Secret

### Required Permissions

Request these permission scopes:
- `user.info.basic` - Basic user info
- `video.list` - List of user's videos

### Authorization Flow

Implement these views for TikTok OAuth:

```python
@login_required
def tiktokAuthorize(request):
    """Initiate TikTok OAuth flow"""
    csrf_token = get_token(request)
    request.session['tiktok_csrf_token'] = csrf_token

    authorization_url = (
        f"https://www.tiktok.com/auth/authorize?"
        f"client_key={TIKTOK_CLIENT_KEY}&"
        f"redirect_uri={settings.TIKTOK_REDIRECT_URI}&"
        f"scope=user.info.basic,video.list&"
        f"response_type=code&"
        f"state={csrf_token}"
    )
    return redirect(authorization_url)

@login_required
def tiktokCallback(request):
    """Handle TikTok OAuth callback"""
    code = request.GET.get('code')
    state = request.GET.get('state')
    stored_state = request.session.get('tiktok_csrf_token')

    if not code or not constant_time_compare(state, stored_state):
        messages.error(request, "Invalid authorization request")
        return redirect('profile_management:profile', username=request.user.username)

    try:
        # Exchange code for access token
        token_response = requests.post(
            'https://open-api.tiktok.com/oauth/access_token/',
            data={
                'client_key': TIKTOK_CLIENT_KEY,
                'client_secret': TIKTOK_CLIENT_SECRET,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': settings.TIKTOK_REDIRECT_URI
            }
        )

        if token_response.status_code != 200:
            raise Exception("Failed to obtain access token")

        token_data = token_response.json()
        if token_data.get('message') != 'success':
            raise Exception(f"TikTok error: {token_data.get('data', {})}")

        # Create or update TikTok account
        account = create_social_media_account(request.user, 'tiktok', token_data.get('data', {}))
        messages.success(request, "TikTok account connected successfully")

    except Exception as e:
        messages.error(request, f"Failed to connect TikTok account: {str(e)}")

    return redirect('profile_management:profile', username=request.user.username)
```

### Data Retrieval

Fetch TikTok data using:

```python
def fetch_tiktok_data(token):
    """Fetch TikTok data using the platform's API"""
    # Get user info
    user_info_response = requests.get(
        'https://open-api.tiktok.com/user/info/',
        params={
            'access_token': token,
            'fields': 'open_id,union_id,avatar_url,display_name,bio_description,profile_deep_link'
        }
    )
    
    if user_info_response.status_code != 200:
        return None
        
    user_data = user_info_response.json()
    if user_data.get('message') != 'success':
        return None
        
    # Get videos
    videos_response = requests.get(
        'https://open-api.tiktok.com/video/list/',
        params={
            'access_token': token,
            'fields': 'id,create_time,cover_image_url,share_url,video_description,duration,height,width,title,embed_html,like_count,comment_count,share_count,view_count'
        }
    )
    
    if videos_response.status_code == 200:
        videos_data = videos_response.json()
        if videos_data.get('message') == 'success':
            user_data['videos'] = videos_data.get('data', {})
    
    return user_data.get('data', {})
```

## General Helper Functions

These helper functions can be used for all platforms:

### Creating/Updating Social Media Accounts

```python
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
```

### Disconnecting Platforms

```python
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
```

## Security Best Practices

When implementing social media integrations, follow these security best practices:

1. **Secure Storage of Credentials**:
   - Never hardcode client IDs and secrets in your code
   - Use environment variables or a secure secrets management system
   - If using Django, store secrets in `secrets.py` and exclude it from version control

2. **OAuth State Parameter**:
   - Always use the state parameter to prevent CSRF attacks
   - Verify the state parameter in callback functions

3. **Token Storage**:
   - Encrypt access tokens before storing them in the database
   - Set appropriate expiration times for sessions and tokens
   - Implement token refresh mechanisms for long-lived access

4. **Error Handling**:
   - Implement comprehensive error handling
   - Provide clear error messages to users
   - Log errors for debugging, but do not expose sensitive information

5. **Scope Limitations**:
   - Request only the permissions your application needs
   - Be transparent with users about what permissions you're requesting
   - Provide a clear privacy policy explaining how you use their data

## Extending to New Platforms

To add support for a new social media platform:

1. Research the platform's OAuth implementation and API documentation
2. Register a developer application on the platform
3. Add the platform to the `PLATFORMS` choices in the `SocialMediaAccount` model:
   ```python
   PLATFORMS = {
       # Existing platforms
       ('new_platform', 'New Platform'),
   }
   ```
4. Create authorization and callback views for the platform
5. Implement a data retrieval function
6. Update templates to support the new platform
7. Test the integration thoroughly

## Troubleshooting

Common integration issues and their solutions:

### OAuth Redirects Not Working
- Check that the redirect URI exactly matches what's registered on the platform
- Ensure HTTPS is used in production
- Verify that the client ID and secret are correct

### Access Token Expiration
- Implement token refresh mechanisms
- Store token expiration time and check before making API calls
- Handle re-authorization gracefully if tokens expire

### API Rate Limiting
- Implement rate limiting detection and backoff strategies
- Cache API responses where appropriate
- Monitor usage to stay within platform limits

### Data Retrieval Issues
- Platform API changes: Keep up with platform API version changes
- Handle changes to response formats gracefully
- Implement robust error handling for API requests


Remember to regularly review platform documentation, as APIs and authentication methods may change over time. Stay informed about security best practices and platform policy changes to maintain compliant and secure integrations. 