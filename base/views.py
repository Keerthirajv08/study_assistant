from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.paginator import Paginator
import json

from .models import ChatSession, ChatMessage, StudyTopic
from .ai_service import AIService


# Create your views here.

def home(request):
    """Home page view - shows welcome page and study topics """
    study_topics = StudyTopic.objects.filter(is_active=True)
    context = {
        'current_theme': request.session.get('theme', 'light'),
        'study_topics': study_topics,
        'user': request.user if request.user.is_authenticated else None
    }
    return render(request, 'base/home.html', context)


@login_required
def chat_view(request, session_id=None):
    """Main chat interface view"""
    #Get or create chat session
    if session_id:
        chat_session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    else:
        #Create new chat session 
        chat_session = ChatSession.objects.create(
            user=request.user,
            title="New Study Session"
        )
        return redirect('chat_view', session_id=chat_session.id)
    
    #Get all messages for this session
    messages = chat_session.messages.all()

    #Get user's recent sessions for sidebar
    recent_sessions = ChatSession.objects.filter(user=request.user)[:10]

    context = {
        'current_theme': request.session.get('theme', 'light'),
        'chat_session': chat_session,
        'messages': messages,
        'recent_sessions': recent_sessions,
    }

    return render(request, 'base/chat.html', context)


@csrf_exempt
@login_required
def send_message(request):
    """Handle AJAX request to send message to chatbot"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_id = data.get('session_id')
            user_message = data.get('message', '').strip()

            if not user_message:
                return JsonResponse({'error': 'Message cannot be empty'}, status=400)
            
            #Get chat session
            chat_session = get_object_or_404(ChatSession, id=session_id, user=request.user)

            #Save user message
            user_msg = ChatMessage.objects.create(
                session=chat_session,
                message_type='user',
                content=user_message,
            )

            #Update session title if it's the first message
            if chat_session.messages.count() == 1:
                #Use first few words as title
                title = user_message[:50] + "..." if len(user_message) > 50 else user_message
                chat_session.title = title
                chat_session.save()

            #Get AI response
            ai_service = AIService()

            #Get conversation context (last few messages)
            recent_messages = chat_session.messages.filter(message_type='user').order_by('-timestamp')[:3]
            context = " ".join([msg.content for msg in reversed(recent_messages)])

            ai_response = ai_service.get_study_response(context, user_message)

            #Save AI response
            ai_msg = ChatMessage.objects.create(
                session=chat_session,
                message_type='ai',
                content=ai_response
            ) 
            
            #Update session 
            chat_session.save()     #This updates the updated_at timestamp

            return JsonResponse({
                'success': True,
                'user_message': user_msg.id,
                    'id': user_msg.id,
                    'content': user_msg.content,
                    'timestamp': user_msg.timestamp.strftime('%H:%M')
            },
            {'ai_message'
                'id' : ai_msg.id,
                'content': user_msg.content,
                'timestamp': user_msg.timestamp.strftime('%H:%M')                
            },
            {'session_title': chat_session.title
        })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)        #405 Method Not Allowed url exists but http method used is not allowed for that url
            

@login_required
def new_chat(request):
    """Create a new chat session"""
    new_session = ChatSession.objects.create(
        user=request.user,
        title="New Study Session",
    )
    return redirect('chat_view', session_id=new_session.id)

@login_required
def delete_session(request, session_id):
    """Delete a chat session"""
    if request.method == 'POST':
        session = get_object_or_404(ChatSession, id=session_id, user=request.user)
        session.delete()
        messages.success(request, 'Chat session deleted successfully!')
    
        #Redirect to most recent session or create a new one
        latest_session = ChatSession.objects.filter(user=request.user).first()
        if latest_session:
            return redirect('chat_view', session_id=latest_session.id)
        else:
            return redirect('new_chat')
    
    return redirect('home')


def signup_view(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!")

            #Log the user in automatically
            authenticated_user = authenticate(username=username, password=form.cleaned_data.get('password1'))
            if authenticated_user:
                login(request, authenticated_user)
                return redirect('home')
            else:
                messages.error(request, "Invalid signup details. Please try again.")
                return redirect('signup')
    else:
            form = UserCreationForm()
    

    return render(request, 'registration/signup.html', {'form': form})   
           
@login_required
def study_topics_view(request):
    """View for show all available study topics"""
    topics = StudyTopic.objects.filter(is_active=True)

    #Get study suggestions for each topic
    ai_service = AIService()
    topics_with_suggestions = []

    for topic in topics:
        suggestions = ai_service.get_study_suggestions(topic.name)
        topics_with_suggestions.append({
            'topic': topic,
            'suggestions': suggestions[:3]      #Show only first 3 suggestions
        })

    context = {
        'topics_with_suggestions': topics_with_suggestions,
        'current_theme': request.session.get('theme', 'light'),
    }

    return render(request, 'base/study_topics.html', context)

@login_required
def chat_history(request):
    """View to show user's chat history"""
    sessions = ChatSession.objects.filter(user=request.user)

    #Add pagination
    paginator = Paginator(sessions, 10)     #10 sessions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'current_theme': request.session.get('theme', 'light'),
        'sessions': page_obj,
    }

    return render(request, 'base/chat_history.html', context)   


def about_view(request):
    """About page view"""
    context = get_theme_context(request)
    context.update({
        "app_name" : "AI Study Assistant for Students & Professionals",
        "description": "Your personal AI-powered Study companion that helps you learn faster, stay organized, and answer your academic questions effectively & instantly.",
        "features": [
            "AI-powered Q&A on study topics",
            "Summarizes textbooks & notes",
            "Creates quizzes for practice",
            "Tracks your study progress",
            "Study tips & strategies",
            "Chat history"
        ],
        "creator": "Keiky",
    })
    return render(request, 'base/about.html', context)

@login_required
def get_study_tips(request):
    """API endpoint to get quick study tips for a given topic"""
    if request.method == 'GET':
        subject = request.GET.get('subject', 'general')

        ai_service = AIService()
        tips = ai_service.get_study_suggestions(subject)

        return JsonResponse({
            'tips': tips,
            'subject': subject,
            'success': True
        })
    
    return JsonResponse({ 'error':'Invalid request method'}, status=405)



#Making dark theme 
def toggle_theme(request):
    """Toggle between light and dark theme"""
    if request.method == 'POST':
        data = json.loads(request.body)
        theme = data.get('theme', 'light')
        
        # Store theme preference in session
        request.session['theme'] = theme
        
        return JsonResponse({'status': 'success', 'theme': theme})
    
    return JsonResponse({'status': 'error'})


def get_theme_context(request):
    """Get current theme from session"""
    return {
        'current_theme': request.session.get('theme', 'light'),
        'is_dark': request.session.get('theme', 'light') == 'dark',
    }




