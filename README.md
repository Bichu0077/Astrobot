# 🌌 AstroBot

A quirky, space-themed chatbot that makes astrophysics accessible through AI-powered conversations. Built with RAG (Retrieval-Augmented Generation) to provide accurate, engaging answers about space and astronomy.

## 📸 Demo

![AstroBot Demo](./assets/demo.gif)

![Chat Interface](./assets/chat-interface.png)

[![Demo Video](./assets/video-thumbnail.png)](https://youtu.be/your-demo-video)

## ✨ Features

- 🧠 **RAG-based QA**: Retrieves relevant astrophysics data before generating responses
- 🗃️ **Wikipedia Integration**: Fetches, cleans, and indexes astrophysics content automatically
- 🤖 **Grok AI Powered**: Uses Grok AI's API for natural, conversational responses
- 🧬 **Semantic Chunking**: Smart document processing for better retrieval accuracy
- 🧠 **Memory Support**: Maintains context across conversation turns
- 🪐 **Quirky Personality**: Space-themed responses with character and humor
- 🛠️ **FastAPI Backend**: Production-ready REST API
- 🎨 **Gradio Frontend**: Clean, interactive chat interface

## 🛠️ Tech Stack

- **Backend**: FastAPI
- **Frontend**: Gradio
- **LLM**: Grok AI
- **Embeddings**: `all-MiniLM-L6-v2` (sentence-transformers)
- **Vector Database**: FAISS
- **Data Source**: Wikipedia API
- **Deployment**: Docker

## 📋 Requirements

- Python 3.10+
- Grok AI API key
- 4GB+ RAM recommended

## ⚡ Installation

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/astrobot.git
   cd astrobot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set API key**
   ```bash
   export GROK_API_KEY="your_api_key_here"
   ```

5. **Run the application**
   ```bash
   # FastAPI backend
   uvicorn app.main:app --reload
   

6. **Access the app**
   - FastAPI: http://localhost:8000


### Docker Setup

1. **Build and run**
   ```bash
   docker build -t astrobot .
   docker run -e GROK_API_KEY=your_api_key_here -p 8000:8000 astrobot
   ```

2. **Using Docker Compose**
   ```bash
   # Create .env file with GROK_API_KEY=your_key
   docker-compose up -d
   ```

## 🚀 Usage

Send questions about astrophysics and space to AstroBot:

- "What is a black hole?"
- "How do stars form?"
- "Explain the Big Bang theory"
- "What are exoplanets?"

AstroBot will retrieve relevant information and respond with its quirky, space-themed personality!


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
