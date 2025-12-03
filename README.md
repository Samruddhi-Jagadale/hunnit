# 🛍️ Neusearch AI - Product Discovery Chatbot  
## **AI Engineering Intern - Technical Assignment**  

A mini AI-powered **product discovery assistant** built to recommend products from [Hunnit.com](https://hunnit.com) based on open-ended user queries. The system combines web scraping, vector databases, retrieval-augmented generation (RAG), and a FastAPI backend with a simple React frontend.  

---

## 🚀 **Live Demo**

🎥 **Demo Video:** [https://www.loom.com/share/c909385c45de4211a71d1bbed566de94](#)  

---

## 🏗️ **Project Overview**

This project covers **end-to-end system development**, including:

1. **Data Collection Pipeline**  
   - Scrapes product data from **Hunnit.com** (minimum 25 products).  
   - Each product includes:
     - Title, Price, Description, Features/Attributes, Image URL, Category.  
   - Scraping implemented as a **FastAPI service** using **Selenium**.  
   - Data stored in **PostgreSQL** for clean, consistent, and queryable storage.

2. **Backend (FastAPI + PostgreSQL)**  
   - **Schema design** and **input validation** using Pydantic models.  
   - **Error handling** and clean code structure.  
   - RESTful endpoints for product listing, product details, and chatbot queries.  

3. **Vectorization + RAG Pipeline**  
   - Product data is **chunked** for better embeddings.  
   - Embeddings generated using **OpenAI / HuggingFace embeddings**.  
   - Stored in **PgVector** (PostgreSQL) for semantic search.  
   - Retrieval pipeline:
     - Searches relevant products for user queries.  
     - Uses **LLM** to interpret abstract queries, ask clarifying questions, and recommend products with explanations.  
   - Handles nuanced queries such as:
     - “Looking for something I can wear in the gym and also in meetings.”  
     
4. **Frontend (React)**  
   - **Home Page:** Displays all scraped products in grid/list view fetched from backend.  
   - **Product Detail Page:** Shows title, price, features, images with URL routing.  
   - **Chat Interface:**  
     - Message bubbles for conversation.  
     - Displays product cards when bot recommends items.  
   - Clean and minimal **UI/UX** prioritizing usability over aesthetics.

5. **Deployment**  
   - Backend and frontend deployed using **Render / Railway / Vercel**.  
   - Docker configuration included for reproducibility.  
   - Environment variables for API keys and database credentials.  

---

## ⚙️ **Tech Stack**

- **Backend:** Python, FastAPI, PostgreSQL, PgVector, Pydantic  
- **Vectorization & RAG:** OpenAI embeddings, HuggingFace models, LLMs  
- **Frontend:** React, HTML, CSS, JavaScript  
- **Scraping:** Selenium, BeautifulSoup  
- **Deployment:** Render / Railway / Docker  

---

## 📂 **Project Structure**

📦 Neusearch-AI-Product-Discovery
│
├── 📂 backend
│ ├── main.py # FastAPI entrypoint
│ ├── models.py # Pydantic models & DB schema
│ ├── routes
│ │ ├── products.py
│ │ └── chat.py
│ └── utils.py # Helper functions
│
├── 📂 frontend
│ ├── src
│ │ ├── components # UI components
│ │ ├── pages # Home, ProductDetail, Chat
│ │ └── App.js
│
├── 📂 data # Scraped product data CSV
├── 📂 readme_images # Screenshots
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env # Environment variables (not committed)
└── README.md


---

## 📝 **Installation & Local Setup**

### 1️ Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/Neusearch-AI.git
cd Neusearch-AI
```

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

### 2 Database Setup

Install PostgreSQL

Create database products_db

Update .env with database credentials:

DATABASE_URL=postgresql://user:password@localhost:5432/products_db
OPENAI_API_KEY=your_openai_api_key

### 3 Run Backend

```bash
uvicorn main:app --reload
```

### 4 Frontend Setup

```bash
cd ../frontend
npm install
npm start
```
### 💡 Architecture & Decisions

Scraping: Selenium + BeautifulSoup for reliable DOM navigation.

Storage: PostgreSQL for structured storage + PgVector for vector embeddings.

Vectorization: Chunks product descriptions/features to generate embeddings for semantic retrieval.

RAG Pipeline: Combines vector retrieval + LLM reasoning to interpret abstract queries.

Frontend: Simple React UI for listing products, viewing details, and chatting with AI.

### ⚠️ Challenges & Trade-offs

Handling inconsistent product data from Hunnit.com → performed thorough preprocessing.

Limited data (25+ products) → vector retrieval tested with small dataset; production would need more data.

Chatbot latency → embedding size vs speed trade-off.

Abstract query interpretation → prompts optimized

