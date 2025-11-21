# 🐥 WiseChicken – AI-Powered Course Recommendation Chatbot

A cross-platform AI chatbot that helps confused students become slightly less confused.

### 🧠 Overview

WiseChicken is an intelligent, RAG-powered course recommendation chatbot designed to help students discover the best learning paths based on their background, interests, and career goals.
It uses:

FastAPI for a blazing-fast backend

Pinecone for semantic vector search

Mixtral 8x7B (via Together API) as the LLM

Sentence-Transformers for embedding generation

A lightweight modern web UI for chatting

Your persistence and questionable sanity to put it all together 💫

WiseChicken answers questions such as:

“I want to learn cybersecurity. Where do I start?”
“Suggest me cloud certifications for placements.”
“I like AI but I’m not from CS — help!”

And then magically returns tailored, context-grounded course suggestions.


### 🚀 Features

🧠 RAG-powered pipeline using Pinecone vector search

🤖 Mixtral-8x7B-Instruct for intelligent recommendations

⚡ FastAPI backend (Fast, async, clean. Basically the Beyoncé of Python frameworks.)

💬 Modern ChatGPT-style UI with chat bubbles and typing animation

📚 Custom knowledge base loaded from a text dataset

🌐 Fully browser-based (no installations required)

🔐 Environment-variable based API key management

🎓 Designed specifically for student course guidance

### 🏗️ Architecture
                ┌─────────────────┐
                │    Frontend     │
                │   (HTML + JS)   │
                └───────┬─────────┘
                        │  POST /chat
                        ▼
              ┌──────────────────────┐
              │       FastAPI        │
              │      (main.py)       │
              └────────┬─────────────┘
                       │
                       ▼
           ┌───────────────────────────┐
           │     RAG Engine            │
           │   (rag_engine.py)         │
           ├──────────┬────────────────┤
           │ Pinecone │  Together API  │
           └──────────┴────────────────┘

### 🗂️ Project Structure
```
WISECHICKEN/
│
├── backend/
│   ├── gnerate.py      # Embeddings, Pinecone, Mixtral logic
│   ├── main.py            # FastAPI app
│   └── .env               # API keys (keep this secret!)
│
└── frontend/
    ├── index.html         # Chat UI
    ├── script.js          # Chat logic
    └── styles.css         # Modern UI styling
```

### ⚙️ Installation & Setup
- 1️⃣ Clone this repository
```
git clone https://github.com/yourusername/WiseChicken.git
cd WiseChicken
```
- 2️⃣ Install Backend Dependencies
```
pip install -r requirements.txt
```
- 3️⃣ Create .env File
```
PINECONE_API_KEY=your_key_here
PINECONE_IDX_NAME=your_index_name
TOGETHER_API_KEY=your_together_api_key
```
- 4️⃣ Start the FastAPI Server
```
cd backend
uvicorn main:app --reload --port 5000
```
You should see: Uvicorn running on http://127.0.0.1:5000
- 5️⃣ Open the Website
```
website/index.html
```
### 🧪 How It Works
1. User inputs a question
2. Sentence-Transformers encodes the query
3. Pinecone retrieves relevant course chunks
4. A grounded prompt is created
5. Mixtral-8x7B generates an answer
6. The UI displays it with chat bubbles
7. The user goes:

“Wow, this chicken is smarter than me.”

### 👨‍💻 Author

Gnana Sai Siddartha (WiseChicken Tamer)
If this project confused you, trust me — building it confused me more.

### 🐥 Final Note

WiseChicken may not lay eggs,
but it does lay some solid course recommendations.

Enjoy! 🎓✨