import requests     #making HTTP requests to AI service(talking to websites, APIs, servers)
import json
from django.conf import settings


class AIService:
    """Service class to handle AI interactions
    we'll use a free API  servie for educational responses"""

    def __init__(self):
        #Using a free API service (Hugging Face Inference API as example)
        #You can replace this with your own AI service
        self.base_url = "https://api-inference.huggingface.co/models/"
        self.model = "microsoft/DialoGPT-large"     #Free conversational model

    def get_study_response(self, question, context=""):
        """Get AI response for study-related questions
        
        Args:
            question (str): The student's question
            context (str): Previous conversation context
        
        Returns: 
            str: AI response"""
        
        study_prompt = self._create_study_prompt(question, context)

        try:
            #Try to get response from AI service
            response = self._call_ai_api(study_prompt)

            if response:
                return self._call_ai_api(study_prompt)
            else:
                #Fallback to rule-based response
                return self._get_fallback_response(question)
            
        except Exception as e:
            print(f"AI Service Error: {e}")
            return self._get_fallback_response(question)
    
    
    def _create_study_prompt(self, question, context=""):
        """Create a study-focused prompt for better educational responses"""
        prompt = f"""You are a helpful study assistant for students. Please provide a clear, educational response to this question:

Question: {question}

Please:
1. Give a clear, easy-to-understand answer
2. Include examples if helpful
3. Break down complex concepts
4. Encourage further learning

Response: """
        return prompt

    def _call_ai_gpi(self, prompt):
        """Make API call to AI service
        Note: This is a simplified version. In production, you'd handle authentication, rate limiting, etc.
        """

        try:
            #Simplified AI response - you can integrate with any AI API
            #For now, we'll use a mock response that varies based on keywords
            return self._generate_educational_response(prompt)
        except Exception as e:
            print(f"API call failed: {e}")
            return None
        

    def _generate_educational_response(self, prompt):
        """Generate educational responses based on keywords in the question/prompt
        This is a simplified approach for demo purposes"""
        prompt_lower = prompt.lower()

        #Math-related response
        if any(word in prompt_lower for word in ['math', 'mathematics', 'solve', 'calculate']):
            return {
                'response': """I'd be happy to help with math! Here are some tips:

1. **Break down the problems** into smaller steps
2. **Identify what you know** and what you need to find 
3. **Choose the right method** or formula
4. **Show your work** step by step
5. **Check your answer** by substituting back

What specific math topic are you working on? I can provide more targeted help!"""
            }
        
        #Science-related responses
        elif any(word in prompt_lower for word in ['science', 'biology', 'physics', 'experiment']):
            return {
                'response': """Science is fascinating! Here's how to study science:
1. **Understand the concept** before memorizing facts
2. **Connect theory to real-world examples**
3. **Practice with diagrams** and visual aids
4. **Do experiments** when possible
5. **Ask "why" and "how"** questions 

What specific topic interests you most? I can help you explaining specific concepts!
                """
            }
        
        #History-related responses
        elif any(word in prompt_lower for word in ['history', 'ancient', 'medieval', 'renaissance', 'past', 'civilization']):
            return {
                'response': """History helps us understand the world! Study tips:

1. **Create timelines** to see connections between events
2. **Understand cause and effect** relationships
3. **Connect past events** to current situations
4. **Learn about key figures** and their contributions
5. **Use maps** to understand geographical context

Which historical period or event are you studying?"""
            }
        
        #Language/English-related responses
        elif any(word in prompt_lower for word in ['english', 'grammar', 'spelling', 'writing', 'essay', 'sentence', 'literature']):
            return {
                'response': """Great question about language arts! Here are some study strategies:

1. **Read actively** - take notes and ask questions
2. **Practice writing** regularly
3. **Learn grammar rules** through examples
4. **Build vocabulary** by reading diverse texts
5. **Analyze literary devices** in stories and poems

What specific language art topic are you interested in?"""
            }
        
        #Default response - general study tips
        else:
            return {
                'response': """I'm here to help with your studies! Here are some general study tips:
1.**Create a study schedule** and stick with it
2.**Find a quiet study space** free from distractions
3.**Focus on one topic at a time**
4.**Take regular breaks** (try the pomodoro technique)
5.**Use active learning** - summarize , teach others , make flashcards
6.**Get enough sleep** and stay healthy

What specific study topic are you interested in? I can provide more specific guidance!"""
            }

    def _format_response(self, api_response):
        """Format the AI API response for display"""

        if isinstance(api_response, dict) and 'response' in api_response:
            return api_response['response']
        elif isinstance(api_response, str):
            return api_response
        else:
            return "I'm here to help with your studies! What would you like to learn abour?"

    def _get_fallback_response(self, question):
        """Provide fallback responses when AI service is unavailable"""

        fallback_responses = [
            "That's a great question! Let me help you think through this step by step. Can you tell me more about what specifically you're trying to learn?",

            "I'd love to help you with that! Breaking down complex topics into smaller parts often makes them easier to understand. What part would you like to start with?",

            "Excellent question! Learning is all about curiosity. Have you tried looking at this from a different angle or finding real-world examples?",

            "That's an interesting topic to explore! Sometimes it helps to connect new information to things you already know. What related concepts are you familiar with?"
        ]

        #Simple hash to pick a consistent response for similar questions
        response_index = len(question) % len(fallback_responses)
        return fallback_responses[response_index]
    

    def get_study_suggestions(self, subject):
        """Get study suggestions based on subject"""
        suggestions = {
            'math': [
                "Practice problems daily for 15-30 minutes",
                "Use visual aids like graphs and diagrams",
                "Explain solutions out loud to yourself",
                "Check your work by substituting answers back"
            ],
            'science': [
                "Create concept maps to connect ideas",
                "Do hands-on experiments when possible",
                "Watch educational videos for visual learning",
                "Form study groups to discuss concepts"
            ],
            'history': [
                "Create timeline charts for important events",
                "Use mnemonic devices for dates and facts",
                "Read primary sources when available",
                "Connect historical events to current events"
            ],
            'english': [
                "Read diverse genres and authors",
                "Keep a vocabulary journal",
                "Practice writing different types of essays",
                "Join book clubs or discussion groups"
            ]
        }
        
        return suggestions.get(subject.lower(), [
            "Set specific, achievable study goals",
            "Use active recall techniques",
            "Teach the material to someone else",
            "Take regular breaks to avoid burnout"
        ])


