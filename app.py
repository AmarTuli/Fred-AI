from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import random

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Mock responses for when OpenAI API is unavailable
MOCK_RESPONSES = {
    'greetings': [
        "Hello there! 👋 I'm Fred AI, your friendly assistant. How can I help you today?",
        "Hi! Great to see you! I'm Fred AI and I'm here to help with whatever you need.",
        "Hey! 👋 Fred AI here! What can I assist you with today?",
        "Greetings! I'm Fred AI, your helpful AI companion. How may I be of service?"
    ],
    'general': [
        "That's an interesting question! I'd love to help you with that.",
        "I'm here to assist you with that! What specific information are you looking for?",
        "Great question! Let me help you explore that topic.",
        "I'm happy to help! Could you tell me a bit more about what you need?"
    ],
    'coding': [
        "I'd be happy to help you with coding! What programming language are you working with?",
        "Coding questions are my specialty! What specific problem are you trying to solve?",
        "I love helping with programming! What can I assist you with today?",
        "Great! I'm here to help with your coding needs. What are you working on?"
    ],
    'thanks': [
        "You're very welcome! 😊 I'm always happy to help!",
        "Anytime! That's what I'm here for!",
        "My pleasure! Let me know if you need anything else!",
        "Glad I could help! Feel free to ask more questions anytime!"
    ],
    'default': [
        "I'm Fred AI, your friendly assistant! I'm here to help with questions, coding, writing, or just chatting.",
        "That's interesting! I'd love to help you with that. What would you like to know more about?",
        "I'm here to assist you! Whether it's questions, coding help, or just conversation, I'm ready!",
        "Hi! I'm Fred AI! I can help with various tasks - just let me know what you need!"
    ]
}

def get_mock_response(user_message):
    """Generate a contextual mock response based on user input"""
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return random.choice(MOCK_RESPONSES['greetings'])
    elif any(word in message_lower for word in ['code', 'programming', 'python', 'javascript', 'html', 'css']):
        return random.choice(MOCK_RESPONSES['coding'])
    elif any(word in message_lower for word in ['thank', 'thanks', 'appreciate']):
        return random.choice(MOCK_RESPONSES['thanks'])
    elif any(word in message_lower for word in ['help', 'assist', 'support']):
        return random.choice(MOCK_RESPONSES['general'])
    else:
        return random.choice(MOCK_RESPONSES['default'])

# Fred AI's personality and system prompt
FRED_SYSTEM_PROMPT = """You are Fred AI, a friendly, helpful, and knowledgeable AI assistant. You have a warm personality and always try to be helpful while maintaining a conversational tone. You can help with various tasks including:

- Answering questions and providing information
- Helping with coding and technical problems
- Creative writing and brainstorming
- General conversation and companionship
- Problem-solving and analysis

Always respond in a friendly, helpful manner while being accurate and informative. If you're not sure about something, be honest about it."""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Try to use OpenAI API first
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": FRED_SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            fred_response = response.choices[0].message.content
            
            return jsonify({
                'response': fred_response,
                'status': 'success'
            })
            
        except Exception as api_error:
            # If OpenAI API fails, use mock response
            print(f"OpenAI API error: {api_error}")
            mock_response = get_mock_response(user_message)
            
            return jsonify({
                'response': mock_response,
                'status': 'success (mock)'
            })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'bot': 'Fred AI'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

