from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ChatSession(models.Model):
    """model to store chat sessions for each user 
    Each session represents a conversation between a user and a chatbot."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, default="New Chat")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']      #Latest first

    def __str__(self):
        return f"{self.title} - {self.created_at.strftime('%Y-%m-%d')}"
    
class ChatMessage(models.Model):
    """model to store chat messages for each chat session"""
    MESSAGE_TYPES = (
        ('user', 'User'),
        ('ai', 'AI Assistant'),
    )
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']        #oldest first for conversation flow

    def __str__(self):
        return f"{self.message_type}: {self.content[:50]}..."
    
class StudyTopic(models.Model):
    """Model to story topics/subjects for each user"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, default="📚")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    """Extended user profile for additional student information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme_preference = models.CharField(
        max_length=10, 
        choices=[('light', 'Light'), ('dark', 'Dark')],
        default='light'
    )
    grade_level = models.CharField(max_length=50, blank=True)
    favourite_subjects = models.ManyToManyField(StudyTopic, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    




    
