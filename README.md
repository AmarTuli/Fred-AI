# 🤖 Fred AI - Your Friendly AI Assistant

Fred AI is a modern, beautiful AI chatbot built with Python Flask and a responsive web interface. It features a warm, helpful personality and can assist with various tasks including answering questions, helping with coding, creative writing, and general conversation.

## ✨ Features

- **Beautiful Modern UI**: Clean, responsive design with smooth animations
- **Real-time Chat**: Instant messaging with typing indicators
- **Mobile Responsive**: Works perfectly on desktop and mobile devices
- **Friendly Personality**: Fred AI has a warm, helpful personality
- **Error Handling**: Graceful error handling and user feedback
- **Auto-resize Input**: Textarea automatically resizes as you type

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- OpenAI API key

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd ai-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**
   
   Create a `.env` file in the project root:
   ```bash
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```
   
   Replace `your_openai_api_key_here` with your actual OpenAI API key.

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   
   Navigate to `http://localhost:5000` to start chatting with Fred AI!

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```
OPENAI_API_KEY=your_openai_api_key_here
```

Replace `your_openai_api_key_here` with your actual OpenAI API key.

### Customizing Fred AI's Personality

You can modify Fred AI's personality by editing the `FRED_SYSTEM_PROMPT` in `app.py`. This allows you to customize how Fred AI responds and behaves.

## 📁 Project Structure

```
ai-chatbot/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── .env               # Environment variables (create this)
└── templates/
    └── index.html     # Web interface
```

## 🛠️ API Endpoints

- `GET /` - Main chat interface
- `POST /api/chat` - Send message to Fred AI
- `GET /api/health` - Health check endpoint

## 🎨 Customization

### Styling

The interface uses modern CSS with:
- Gradient backgrounds
- Smooth animations
- Responsive design
- Beautiful typography

### Fred AI's Personality

Fred AI is designed to be:
- Friendly and approachable
- Helpful and knowledgeable
- Honest about limitations
- Conversational in tone

## 🔒 Security Notes

- Never commit your `.env` file to version control
- Keep your OpenAI API key secure
- Consider rate limiting for production use

## 🚀 Deployment

For production deployment, consider:
- Using a production WSGI server like Gunicorn
- Setting up proper environment variables
- Adding rate limiting
- Implementing user authentication if needed

## 🤝 Contributing

Feel free to contribute to Fred AI by:
- Improving the UI/UX
- Adding new features
- Enhancing Fred AI's personality
- Fixing bugs

## 📄 License

This project is open source and available under the MIT License.

---

**Enjoy chatting with Fred AI! 🤖✨**

