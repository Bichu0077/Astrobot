# 🌌 AstroBot ![CI](https://github.com/Bichu0077/Astrobot/actions/workflows/ci.yml/badge.svg)

A quirky, space-themed chatbot that makes astrophysics accessible through AI-powered conversations. Built with RAG (Retrieval-Augmented Generation) to provide accurate, engaging answers about space and astronomy.

---

## 📸 Demo

![AstroBot Demo](./assets/demo.gif)

![Chat Interface](./assets/chat-interface.png)

[![Demo Video](./assets/video-thumbnail.png)](https://youtu.be/your-demo-video)

---

## ✨ Features

- 🧠 **RAG-based QA**: Retrieves relevant astrophysics data before generating responses  
- 🗃️ **Wikipedia Integration**: Fetches, cleans, and indexes astrophysics content automatically  
- 🤖 **Grok AI Powered**: Uses Grok AI's API for natural, conversational responses  
- 🧬 **Semantic Chunking**: Smart document processing for better retrieval accuracy  
- 🧠 **Memory Support**: Maintains context across conversation turns  
- 🪐 **Quirky Personality**: Space-themed responses with character and humor  
- 🛠️ **FastAPI Backend**: Production-ready REST API  
- 🎨 **Jinja2 Frontend**: Custom HTML/CSS/JS interface for full UI control  
- 🐳 **Dockerized**: Production-ready Dockerfile & Compose support  
- 🔁 **Automated Data Pipeline**: `pipeline.py` supports full ingestion → embedding → vectorization  
- ✅ **CI Integration**: GitHub Actions test every commit to keep the code reliable  
- 🧪 **Pytest Test Suite**: Includes pipeline test with NLTK, FAISS, LangChain integration  
- 📄 **Logs + Configurable .env**: Monitored logs and environment-based configuration  

---

## 🛠️ Tech Stack

| Layer        | Technology                                 |
|--------------|---------------------------------------------|
| **Backend**  | FastAPI                                     |
| **Frontend** | HTML, CSS, JS via Jinja2                    |
| **LLM**      | Grok AI API                                 |
| **Embedder** | `all-MiniLM-L6-v2` via SentenceTransformers |
| **Vector DB**| FAISS                                       |
| **Pipeline** | Custom `pipeline.py` w/ chunking, embedding |
| **CI/CD**    | GitHub Actions                              |
| **Testing**  | Pytest with structured output               |
| **Infra**    | Docker & Docker Compose                     |

---

## 📋 Requirements

- Python 3.10+  
- Grok AI API key  
- NLTK `punkt` tokenizer (auto-managed)  
- At least 4GB RAM recommended  

---

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

   
### 🛠️ Pipeline Usage (Data Processing)
 ```bash
   # Run entire pipeline: fetch → clean → chunk → embed
   python scripts/pipeline.py --query "What is the theory of relativity?"
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
