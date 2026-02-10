# ⚡ ResumeIQ — AI-Powered Resume Screener

> Semantic NLP matching that understands meaning, not just keywords.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=flat&logo=huggingface&logoColor=black)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)

---

## 🧠 What It Does

ResumeIQ is an AI-powered resume screening tool that compares resumes against job descriptions using **semantic similarity** — not keyword matching.

Traditional screening tools fail when a resume says *"ML Engineer"* but the job says *"Machine Learning Developer"*. ResumeIQ understands they mean the same thing.

**Upload a resume → Paste a job description → Get an instant match score with skill analysis.**

---

## ✨ Features

- 📄 **PDF Resume Parsing** — Extracts and cleans text from any PDF resume
- 🤖 **Semantic Matching** — Uses transformer embeddings to understand meaning beyond keywords
- 📊 **Match Score** — Percentage score with Strong / Moderate / Weak classification
- 🔍 **Skill Gap Analysis** — Shows exactly which skills match and which are missing
- 🏆 **Multi-Resume Ranking** — Upload multiple resumes and rank candidates instantly
- 🎨 **Modern Dark UI** — Clean, professional interface built with Streamlit

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| NLP Model | `sentence-transformers/all-MiniLM-L6-v2` |
| Similarity | Cosine Similarity (scikit-learn) |
| PDF Parsing | PyPDF2 |
| Frontend | Streamlit |
| Embeddings | Hugging Face Transformers |

---

## 🚀 How to Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/BrundaVenkatesh01/resume-screening-ai.git
cd resume-screening-ai
```

**2. Create a virtual environment**
```bash
python -m venv venv

# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` 🎉

---

## 📁 Project Structure

```
resume-screening-ai/
│
├── app.py              # Streamlit web app & UI
├── matcher.py          # NLP matching logic (embeddings + cosine similarity)
├── resume_parser.py    # PDF text extraction & cleaning
├── requirements.txt    # Project dependencies
└── README.md
```

---

## 🔬 How It Works

```
PDF Resume ──► Text Extraction ──► Clean Text ──► Sentence Embeddings
                                                          │
Job Description ──────────────────► Clean Text ──► Sentence Embeddings
                                                          │
                                              Cosine Similarity Score
                                                          │
                                         Match % + Skill Gap Analysis
```

1. **Text Extraction** — PyPDF2 reads each page of the PDF and extracts raw text
2. **Text Cleaning** — Removes special characters, normalizes whitespace
3. **Embedding Generation** — `all-MiniLM-L6-v2` converts text to 384-dimensional vectors
4. **Cosine Similarity** — Measures the angle between vectors (1.0 = identical meaning)
5. **Skill Analysis** — Keyword extraction identifies matched and missing skills

---

## 💡 Why Semantic Matching?

Traditional keyword matching misses context:

| Resume Says | Job Requires | Keyword Match | Semantic Match |
|------------|-------------|---------------|----------------|
| ML Engineer | Machine Learning Developer | ❌ | ✅ |
| Built neural networks | Deep learning experience | ❌ | ✅ |
| Python, pandas | Data manipulation skills | ❌ | ✅ |

Semantic matching using transformer embeddings captures **meaning**, not just exact words.

---

## 🎯 Future Improvements

- [ ] Deploy to Streamlit Cloud for public access
- [ ] Add support for DOCX resumes
- [ ] LLM-generated improvement suggestions per resume
- [ ] Batch processing via CSV upload
- [ ] API endpoint with FastAPI

---

## 👩‍💻 Author

**Brunda Venkatesh**  
M.S. Computer Science — AI/ML  
[LinkedIn](https://www.linkedin.com/in/brunda-venkatesh/) · [GitHub](https://github.com/BrundaVenkatesh01)
