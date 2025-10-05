from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai
import os

# Configure Gemini AI - get from environment variable
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyCOP-54RgQRAXXpX2-2UluyqHeXBnfA8iA')
genai.configure(api_key=GEMINI_API_KEY,client_options={"api_endpoint": "https://generativelanguage.googleapis.com/v1"})


@api_view(['POST'])
def chat(request):
    user_message = request.data.get('message', '')
    
    if not user_message:
        return Response(
            {"error": "Message is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        model = genai.GenerativeModel('models/gemini-1.5-pro')
        response = model.generate_content(user_message)
        
        return Response({"reply": response.text})
    
    except Exception as e:
        print(f"Gemini API Error: {str(e)}")
        return Response(
            {"reply": f"Sorry, I encountered an error: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )