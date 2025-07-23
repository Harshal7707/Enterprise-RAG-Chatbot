# 🏢 Enterprise RAG-Chatbot (Gemini-Powered)

A smart chatbot that uses **Retrieval-Augmented Generation (RAG)** with **Google Gemini** to answer enterprise-specific questions from internal documents. It combines the power of search with large language models to deliver accurate, contextual answers.

---

## 🎥 Demo
Input
<img width="1818" height="649" alt="Screenshot 2025-07-23 202155" src="https://github.com/user-attachments/assets/5514b1ee-b904-4f45-9c92-0eef388871cc" />


Output
<img width="1810" height="623" alt="image" src="https://github.com/user-attachments/assets/2749bc17-dbee-49d4-ad81-eb09f6791f65" />


---

## 🚀 Features

- 🔍 **Context-Aware Chat** over internal enterprise documents
- 🤖 **Google Gemini Pro Integration** for advanced language understanding
- ⚡ **Fast Retrieval** using FAISS / ChromaDB
- 🧠 **RAG Architecture**: Retrieve + Generate for powerful QA
- 📄 **Supports Multiple Formats**: PDF, DOCX, TXT, Markdown, and more

---

## 🧑‍💻 Tech Stack

| Component       | Technology         |
|----------------|--------------------|
| LLM             | Google Gemini Pro |
| Embeddings      | Gemini / SentenceTransformers |
| Vector DB       | FAISS / ChromaDB  |
| File Parsing    | LangChain / unstructured / PyMuPDF |
| Frontend        | Gradio / Streamlit |
| Backend         | Python             |

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/enterprise-rag-chatbot.git
cd enterprise-rag-chatbot
