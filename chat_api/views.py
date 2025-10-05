from django.shortcuts import render
import google.generativeai as genai
import os

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Configure Gemini AI
genai.configure(api_key=os.getenv('GEMINI_API_KEY', 'AIzaSyCOP-54RgQRAXXpX2-2UluyqHeXBnfA8iA'))

@api_view(['POST'])
def chat(request):
    user_message = request.data.get('message', '')
    
    try:
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-pro')
        
        # Generate response
        response = model.generate_content(user_message)
        
        return Response({"reply": response.text})
    
    except Exception as e:
        # Fallback to simple response if Gemini fails
        return Response({"reply": f"Sorry, I'm having trouble connecting to AI right now. You said: {user_message}"})
