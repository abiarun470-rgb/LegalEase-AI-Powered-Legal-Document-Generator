# LegalEase-AI-Powered-Legal-Document-Generator
LegalEase is an AI-powered legal document generation application that helps users create legal document drafts quickly and easily. Users can enter details such as the document type, parties involved, terms and conditions, effective date, and jurisdiction. 
# ⚖️ LegalEase – AI-Powered Legal Document Generator

LegalEase is an AI-powered web application that helps users generate professional legal document drafts using Google's Gemini AI.

The application provides a simple interface where users can enter document details, parties, terms, and an effective date. LegalEase then generates a structured legal document draft that can be edited, previewed, and exported as TXT, DOCX, or PDF.

> **Disclaimer:** LegalEase is an AI-assisted document drafting tool and does not provide legal advice. Generated documents should be reviewed by a qualified legal professional before use.

---

## 🚀 Features

- 🤖 AI-powered legal document generation using Google Gemini
- 📄 Multiple document types
- ✍️ Editable generated documents
- 👁️ Document preview
- 📥 Export documents as:
  - TXT
  - DOCX
  - PDF
- 🔒 Environment-variable based API key configuration
- ⚡ FastAPI backend
- 🎨 Streamlit frontend
- 🔄 Retry handling for temporary Gemini service errors
- 🧹 Text sanitization for generated documents
- 🧪 Automated API and document export tests
- 🐳 Docker support
- 💻 VS Code development configuration

---

## 🏗️ Project Architecture

```text
                    ┌─────────────────────┐
                    │      User           │
                    │   Web Browser       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Streamlit Frontend  │
                    │    frontend/app.py  │
                    └──────────┬──────────┘
                               │ HTTP
                               ▼
                    ┌─────────────────────┐
                    │    FastAPI Backend  │
                    │    backend/main.py  │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
       ┌──────────────────┐        ┌──────────────────┐
       │ Gemini AI Engine │        │ Document Engine  │
       │  Google Gemini   │        │ TXT/DOCX/PDF     │
       └──────────────────┘        └──────────────────┘
