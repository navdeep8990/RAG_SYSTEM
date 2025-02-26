# MultiRAG Source Retrieval

## Introduction

**MultiRAG Source Retrieval** is an AI-powered system that allows users to upload multiple sources, including **PDF files** or **web links**, and retrieve information from them using a chatbot interface. The system leverages **Retrieval-Augmented Generation (RAG)** to enhance responses with factual accuracy by retrieving data from the uploaded sources before generating an answer.

---

## Setup Guide

### 1. Create a Virtual Environment

To ensure smooth installation and avoid conflicts, create a virtual environment before installing dependencies.

#### **Windows**

```sh
python -m venv multiRAG_env
multiRAG_env\Scripts\activate
```

#### **macOS/Linux**

```sh
python3 -m venv multiRAG_env
source multiRAG_env/bin/activate
```

---

### 2. Install Dependencies

Once the virtual environment is activated, install the required dependencies:

```sh
pip install -r requirements.txt
```

---

## Features

✅ **Multi-Source Retrieval** - Upload PDFs or provide web links as knowledge sources.\
✅ **AI-Powered Q&A** - Ask questions based on uploaded documents and receive precise answers.\
✅ **Interactive Web Interface** - Built with **Streamlit** for an intuitive UI.\
✅ **Efficient Vector Search** - Uses **FAISS** for fast and scalable document retrieval.\
✅ **SQLAlchemy Backend** - Manages metadata storage for document processing.

---

## Tech Stack

### 1. **LangChain & LangChain Community**

Used for **retrieval-augmented generation (RAG)** and managing different document loaders.\
🔗 [LangChain Documentation](https://python.langchain.com/docs/)\
🔗 [LangChain Community Documentation](https://github.com/langchain-ai/langchain)

### 2. **Streamlit** (Frontend)

Used for creating an interactive user interface for uploading documents and interacting with the chatbot.\
🔗 [Streamlit Documentation](https://docs.streamlit.io/)

### 3. **SQLAlchemy** (Backend)

Manages structured storage of document metadata and embeddings.\
🔗 [SQLAlchemy Documentation](https://www.sqlalchemy.org/)

### 4. **FAISS** (Vector Database)

Efficient and scalable nearest-neighbor search for document retrieval.\
🔗 [FAISS Documentation](https://faiss.ai/)

---

## Usage Guide

1. **Run the Application**
   ```sh
   streamlit run app.py
   ```
2. **Upload a PDF or provide a URL**
3. **Ask questions based on the uploaded sources**
4. **Get precise and AI-enhanced responses**

---

## Contribution

Feel free to contribute by improving retrieval techniques, enhancing the UI, or adding support for more data sources!

📧 Contact: **Navdeep Singh**

---

## License

This project is licensed under the **MIT License**.

