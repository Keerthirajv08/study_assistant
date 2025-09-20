from django.contrib import admin
from .models import ChatSession, ChatMessage, StudyTopic, UserProfile



# Register your models here.

@admin.register(StudyTopic)
class StudyTopicAdmin(admin.ModelAdmin):
    """Admin interface for managing study topics"""
    list_display = ['name', 'icon', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    ordering = ['name']

class ChatMessageInline(admin.TabularInline):
    """Inline admin for chat messages within chat sessions"""
    model = ChatMessage
    extra = 0
    readonly_fields = ['timestamp']
    fields = ['message_type', 'content', 'timestamp']

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    """Admin interface for managing chat sessions"""
    list_display = ['user', 'title', 'created_at', 'updated_at', 'message_count']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ChatMessageInline]

    def message_count(self, obj):
        """Display the number of messages in each session"""
        return obj.messages.count()
    
    message_count.short_description = 'Messages'

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """Admin interface for managing chat messages"""
    list_display = ['session', 'message_type', 'content_preview', 'timestamp']
    list_filter = [ 'message_type', 'timestamp']
    search_fields = ['session__title', 'content']
    readonly_fields = ['timestamp']

    def content_preview(self, obj):
        """Shows a preview of the message content"""
        return obj.content[:100] + "..." if len(obj.content) > 100 else obj.content

    content_preview.short_description = 'Content Preview'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for managing user profiles"""
    list_display = ['user', 'grade_level', 'favourite_subjects_count', 'created_at', 'theme_preference']
    list_filter = ['grade_level', 'created_at', 'theme_preference']
    search_fields = ['user__username', 'user__email']
    filter_horizontal = ['favourite_subjects']
    readonly_fields = ['created_at']

    def favourite_subjects_count(self, obj):
        """Display the number of favourite subjects for each user"""
        return obj.favourite_subjects.count()
    
    favourite_subjects_count.short_description = 'Favourite Subjects'

#Customize admin site header and title

admin.site.site_header = 'StudyAI Assistant Admin'
admin.site.site_title = 'StudyAI Admin'
admin.site.index_title = 'Welcome to StudyAI Administration'
