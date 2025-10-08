from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import traceback

# Try to import and configure Gemini
try:
    import google.generativeai as genai
    import os
    
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyCOP-54RgQRAXXpX2-2UluyqHeXBnfA8iA')
    
    # Configure with v1 API (not v1beta)
    genai.configure(
        api_key=GEMINI_API_KEY,
        transport='rest'  # Use REST instead of gRPC
    )
    GEMINI_AVAILABLE = True
    print("✓ Gemini AI configured successfully")
except Exception as e:
    GEMINI_AVAILABLE = False
    print(f"✗ Failed to configure Gemini: {e}")


@api_view(['POST'])
def chat(request):
    """Handle chat requests with Gemini AI"""
    
    # Check if Gemini is available
    if not GEMINI_AVAILABLE:
        return Response(
            {"error": "Gemini AI is not properly configured", "reply": "AI service is currently unavailable"}, 
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    
    # Get message from request
    user_message = request.data.get('message', '')
    
    if not user_message:
        return Response(
            {"error": "Message is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        print(f"\n{'='*50}")
        print(f"📩 Received message: {user_message}")
        
        # Try gemini-1.5-flash first (more stable)
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            print("✓ Model initialized (gemini-2.5-flash)")
        except:
            # Fallback to pro
            model = genai.GenerativeModel('gemini-pro')
            print("✓ Model initialized (gemini-pro)")
        
        # Generate response
        response = model.generate_content(user_message)
        print(f"✓ Response generated: {response.text[:100]}...")
        print(f"{'='*50}\n")
        
        return Response({
            "reply": response.text,
            "status": "success"
        })
    
    except AttributeError as e:
        # This happens if response.text doesn't exist
        error_msg = f"Response format error: {str(e)}"
        print(f"✗ {error_msg}")
        traceback.print_exc()
        return Response(
            {"error": error_msg, "reply": "Sorry, I received an invalid response format."}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    except Exception as e:
        # Catch all other errors
        error_msg = str(e)
        print(f"✗ Gemini API Error: {error_msg}")
        traceback.print_exc()
        
        return Response(
            {
                "error": error_msg, 
                "reply": f"Sorry, I encountered an error: {error_msg}"
            }, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
