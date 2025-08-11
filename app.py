from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

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
        
        # Create chat completion with Fred AI's personality
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
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'bot': 'Fred AI'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

