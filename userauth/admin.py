from django.contrib import admin
from .models import UserProfile, TermsAndConditions, SocialMediaAccount, Connection, Post, AuditLog


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'fullName', 'bio', 'profilePicture', 'qr_code', "user_code", "verified", "created_at"]
    search_fields = ['user__username', 'fullName', 'bio', 'profilePicture', 'qr_code', "user_code", "verified", "created_at"]
    list_filter = ["verified", "created_at"]
    list_per_page = 25

class TermsAndConditionsAdmin(admin.ModelAdmin):
    list_display = ['user', 'accepted', 'date_accepted']
    search_fields = ['user__username', 'accepted', 'date_accepted']
    list_filter = ['accepted', 'date_accepted']
    list_per_page = 25
    
class SocialMediaAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'platform', 'token', 'token_type', 'expires', 'last_sync', 'is_linked']
    search_fields = ['user__username', 'platform', 'token', 'token_type', 'expires', 'last_sync']
    list_filter = ['platform', 'is_linked', 'last_sync']
    list_per_page = 25


class ConnectionAdmin(admin.ModelAdmin):
    list_display = ['user', "connected_user", "created_at", "is_deleted"]
    search_fields = ['user__username', "connected_user__username", "created_at"]
    list_filter = ["created_at", "is_deleted"]
    list_per_page = 25
    
    
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', "content_type", "created_at", "is_deleted"]
    search_fields = ['user__username', "content_type", "created_at"]
    list_filter = ["content_type", "created_at", "is_deleted"]
    list_per_page = 25

class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'timestamp']
    search_fields = ['user__username', 'action', 'timestamp']
    list_filter = ['action', 'timestamp']
    list_per_page = 25

    
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(TermsAndConditions, TermsAndConditionsAdmin)
admin.site.register(SocialMediaAccount , SocialMediaAccountAdmin)
admin.site.register(Connection, ConnectionAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(AuditLog, AuditLogAdmin)