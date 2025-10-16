from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import random
from datetime import datetime
import sqlite3
import hashlib
import secrets

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

# Configure OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Database initialization
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            birthday TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            display_name TEXT NOT NULL,
            wifi_network TEXT,
            wifi_password TEXT,
            email TEXT,
            phone TEXT,
            avatar TEXT DEFAULT '🤖',
            theme TEXT DEFAULT 'default',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database
init_db()

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

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Verify a password against its hash"""
    return hash_password(password) == password_hash

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and verify_password(password, user[5]):  # user[5] is password_hash
            session['user_id'] = user[0]
            session['username'] = user[4]
            session['display_name'] = user[6]
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birthday = request.form['birthday']
        username = request.form['username']
        password = request.form['password']
        display_name = request.form['display_name']
        
        # Hash the password
        password_hash = hash_password(password)
        
        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (first_name, last_name, birthday, username, password_hash, display_name)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (first_name, last_name, birthday, username, password_hash, display_name))
            conn.commit()
            conn.close()
            
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists. Please choose another.')
        except Exception as e:
            flash(f'Registration failed: {str(e)}')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/settings')
def settings():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT first_name, last_name, birthday, display_name, email, phone, 
               avatar, theme, wifi_network, wifi_password 
        FROM users WHERE id = ?
    ''', (session['user_id'],))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        user_data = {
            'first_name': user[0],
            'last_name': user[1],
            'birthday': user[2],
            'display_name': user[3],
            'email': user[4] or '',
            'phone': user[5] or '',
            'avatar': user[6] or '🤖',
            'theme': user[7] or 'default',
            'wifi_network': user[8] or '',
            'wifi_password': user[9] or ''
        }
    else:
        user_data = {
            'first_name': '', 'last_name': '', 'birthday': '', 'display_name': '',
            'email': '', 'phone': '', 'avatar': '🤖', 'theme': 'default',
            'wifi_network': '', 'wifi_password': ''
        }
    
    return render_template('settings.html', user=user_data)

@app.route('/update_wifi', methods=['POST'])
def update_wifi():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    wifi_network = request.form['wifi_network']
    wifi_password = request.form['wifi_password']
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET wifi_network = ?, wifi_password = ? WHERE id = ?', 
                  (wifi_network, wifi_password, session['user_id']))
    conn.commit()
    conn.close()
    
    flash('WiFi settings updated successfully!')
    return redirect(url_for('settings'))

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    birthday = request.form['birthday']
    display_name = request.form['display_name']
    email = request.form['email']
    phone = request.form['phone']
    avatar = request.form['avatar']
    theme = request.form['theme']
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET 
        first_name = ?, last_name = ?, birthday = ?, display_name = ?, 
        email = ?, phone = ?, avatar = ?, theme = ?
        WHERE id = ?
    ''', (first_name, last_name, birthday, display_name, email, phone, avatar, theme, session['user_id']))
    conn.commit()
    conn.close()
    
    # Update session
    session['display_name'] = display_name
    
    flash('Profile updated successfully!')
    return redirect(url_for('settings'))

@app.route('/api/chat', methods=['POST'])
def chat():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
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

# Security: Block any attempts to access environment variables
@app.route('/env')
@app.route('/.env')
@app.route('/api/env')
def block_env_access():
    return jsonify({'error': 'Access denied'}), 403

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080, threaded=True)

