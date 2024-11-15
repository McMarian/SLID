from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
    
#UserProfile model with profile score and deletion fields   
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profilePicture = models.ImageField(null=True, default="default_pp.png", blank=True)
    qr_code = models.ImageField(null=True, default="qr_code.png", blank=True)
    user_code = models.CharField(max_length=16, null=True, blank=True, unique=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_score = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['user']), #Index for fast profile lookup
            models.Index(fields=['profile_score']), #Index for quick engagment queries
        ]
    
    def update_profile_score(self):
        score=0
        if self.fullName: score += 20
        if self.bio: score += 20
        if self.profilePicture: score += 20
        if self.qr_code: score += 20
        if self.verified: score += 20
        self.profile_score = score
        self.save()

    def __str__(self):
        return self.user.username    
    

#Unified connection model for all social media platforms
class SocialMediaAccount(models.Model):
    PLATFORMS = {
        ('facebook', 'Facebook'), 
        ('instagram', 'Instagram'),
        ('youtube', 'Youtube'),
        ('linkedin', 'Linkedin'),
        ('google', 'Google'),
        ('x', 'X'),
        ('tiktok', 'Tiktok'),
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20, choices=PLATFORMS)
    token = models.CharField(max_length=500, null=True)
    token_type = models.CharField(max_length=20, null=True)
    expires = models.DateTimeField(null=True)
    data = models.JSONField(null=True, blank=True) #Store Json data for each platform
    last_sync = models.DateTimeField(auto_now=True)
    is_linked = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'platform')
        indexes = [
            models.Index(fields=['user', 'platform']), #Index for user-platform lookups
            models.Index(fields=['platform']),

        ]

    def __str__(self):
        return f"{self.user.username} - {self.platform}"


#Connection with soft deletion    
class Connection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connections')
    connected_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connected_to')
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'connected_user')  # Ensure only one connection between two users
        indexes = [
            models.Index(fields=['user', 'connected_user']),
        ]

    def __str__(self):
        return f"{self.user.username} connected with {self.connected_user.username}"
    
    
class TermsAndConditions(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    date_accepted = models.DateTimeField(auto_now_add=True)

      
#Post model with added metadata for engagement data soft deletion
class Post(models.Model):
    CONTENT_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
        ('text', 'Text'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    content = models.TextField(null=True)  # Stores text content, descriptions, or HTML for embedded media
    media_file = models.FileField(upload_to='posts/media/', blank=True, null=True)  # Optional media
    metadata = models.JSONField(null=True, blank=True) #Analytics or engagement data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'content_type']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at}"


#AuditLog to track user's actions
class AuditLog(models.Model):
    ACTIONS = [
        ('login', 'User Login'),
        ('update_profile', 'Update Profile'),
        ('post', 'Create Post'),
        ('connect', 'Connect with user'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=ACTIONS)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'action']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"
