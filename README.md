<div align="center">

# 🚀 AI-Powered ATS Resume Checker

<img src="https://img.shields.io/badge/ATS-Resume%20Checker-667eea?style=for-the-badge&logo=rocket&logoColor=white" alt="ATS Resume Checker"/>

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge)](https://github.com/yourusername/ats-resume-checker/pulls)
[![Stars](https://img.shields.io/github/stars/yourusername/ats-resume-checker?style=for-the-badge&color=yellow)](https://github.com/yourusername/ats-resume-checker/stargazers)

---

### 🎯 An intelligent AI-powered tool that analyzes resumes against job descriptions and provides ATS compatibility scores with actionable improvement suggestions.

 [📖 Documentation](#-how-to-use) • [🐛 Report Bug](https://github.com/yourusername/ats-resume-checker/issues) • [✨ Request Feature](https://github.com/yourusername/ats-resume-checker/issues)

---

<img src="assets/screenshot1.png" alt="App Screenshot" width="90%"/>

</div>

---

## 📋 Table of Contents

- [About The Project](#-about-the-project)
- [Features](#-features)
- [Demo](#-demo)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [How to Use](#-how-to-use)
- [Tech Stack](#-tech-stack)
- [Scoring System](#-scoring-system)
- [Contact](#-contact)
- [Acknowledgments](#-acknowledgments)

---

## 🎯 About The Project

**ATS Resume Checker** is a powerful AI-driven web application designed to help job seekers optimize their resumes for **Applicant Tracking Systems (ATS)**. 

### 🤔 The Problem

> **75% of resumes are rejected by ATS** before they ever reach a human recruiter.

Most job seekers don't realize that their carefully crafted resumes are being filtered out by automated systems because they lack the right keywords, formatting, or structure.

### 💡 The Solution

Our AI-powered tool analyzes your resume against specific job descriptions and provides:
- ✅ **Instant ATS compatibility score**
- ✅ **Keyword gap analysis**
- ✅ **Skills matching report**
- ✅ **Actionable improvement suggestions**
- ✅ **Downloadable PDF reports**

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 📊 Analysis Features

- **Multi-Format Support** - PDF, DOCX, TXT
- **Real-time ATS Scoring** - Instant results
- **Keyword Analysis** - Match & missing keywords
- **Skills Matching** - Technical & soft skills
- **Experience Evaluation** - Relevance scoring
- **Education Matching** - Qualification check
- **Format Analysis** - ATS compatibility check

</td>
<td width="50%">

### 🎨 User Experience

- **Beautiful UI** - Modern glassmorphism design
- **Dark Theme** - Easy on the eyes
- **Interactive Charts** - Plotly visualizations
- **Radar Charts** - Visual score breakdown
- **Gauge Meters** - Score representation
- **PDF Reports** - Download detailed analysis
- **Mobile Responsive** - Works on all devices

</td>
</tr>
</table>

### 🔥 Key Highlights

| Feature | Description |
|---------|-------------|
| 🤖 **AI-Powered Analysis** | Advanced NLP using spaCy for intelligent parsing |
| 📈 **Detailed Scoring** | 5 categories with weighted scoring algorithm |
| 💡 **Smart Suggestions** | Actionable tips to improve your resume |
| 🎯 **Keyword Optimization** | Identify missing keywords from job descriptions |
| 📥 **PDF Reports** | Professional downloadable analysis reports |
| ⚡ **Instant Results** | Get feedback in seconds, not hours |
| 🔒 **Privacy First** | No data stored - all processing in memory |
| 🆓 **100% Free** | Open source and free to use |

---

### 📸 Screenshots

<details>
<summary>Click to view screenshots</summary>

<br>

**📤 Upload Section**
> Upload your resume and paste the job description

<img src="assets/screenshot2.png" alt="Upload Section" width="80%"/>

---

**📊 Results Dashboard**
> View your ATS score with detailed breakdown

<img src="assets/screenshot3.png" alt="Results" width="80%"/>

---

**🛠️ Skills Analysis**
> See matched and missing skills

<img src="assets/screenshot4.png" alt="Skills Analysis" width="80%"/>

---

**📥 PDF Report**
> Download comprehensive analysis report

<img src="assets/screenshot5.png" alt="PDF Report" width="80%"/>

</details>

---

## 🚀 Getting Started

Follow these steps to run the project locally.

### Prerequisites

- **Python 3.8+** - [Download Python](https://python.org)
- **pip** - Python package manager (comes with Python)
- **Git** - [Download Git](https://git-scm.com)

### Installation

**1️⃣ Clone the repository**

```bash
git clone https://github.com/isha9803/ai-resume-screening-system
cd ai-resume-screening-system
```
**2️⃣ Create a virtual environment**
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
```
**3️⃣ Install dependencies**

``` bash
pip install -r requirements.txt
```
**4️⃣ Download NLP model**
```bash
python -m spacy download en_core_web_sm
```
**5️⃣ Run the application**
```bash
streamlit run app.py
```
**6️⃣ Open in browser**
```text
http://localhost:8501
```
- 🎉 That's it! The app should now be running locally.

---

## 📖 How to Use

### Step-by-Step Guide

<table>
<tr>
<td align="center" width="20%">

### Step 1
📄

**Upload Resume**

Upload your resume in PDF, DOCX, or TXT format

</td>
<td align="center" width="20%">

### Step 2
📋

**Paste Job Description**

Copy and paste the target job posting

</td>
<td align="center" width="20%">

### Step 3
🔍

**Analyze**

Click the "Analyze Resume" button

</td>
<td align="center" width="20%">

### Step 4
📊

**Review Results**

Check scores, issues, and suggestions

</td>
<td align="center" width="20%">

### Step 5
📥

**Download Report**

Get a detailed PDF report

</td>
</tr>
</table>

---

**💻 Code Usage**
```python
from utils.resume_parser import ResumeParser
from utils.ats_scorer import ATSScorer
from utils.text_processor import TextProcessor

# Initialize components
parser = ResumeParser()
scorer = ATSScorer()
processor = TextProcessor()

# Parse resume
resume_text = parser.extract_text(resume_file)
resume_data = parser.parse_resume(resume_text)

# Clean and analyze
cleaned_resume = processor.clean_text(resume_text)
cleaned_jd = processor.clean_text(job_description)

# Get ATS score
results = scorer.calculate_ats_score(cleaned_resume, cleaned_jd, resume_data)

# Access results
print(f"Overall Score: {results['overall_score']}%")
print(f"Matched Skills: {results['matched_skills']}")
print(f"Missing Skills: {results['missing_skills']}")
print(f"Suggestions: {results['suggestions']}")
```
---

## 🛠️ Tech Stack

| Technology | Purpose | Link |
|------------|---------|------|
| [![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org) | Backend & Logic | [python.org](https://python.org) |
| [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io) | Web Framework | [streamlit.io](https://streamlit.io) |
| [![spaCy](https://img.shields.io/badge/spaCy-09A3D5?style=for-the-badge&logo=spacy&logoColor=white)](https://spacy.io) | NLP Processing | [spacy.io](https://spacy.io) |
| [![NLTK](https://img.shields.io/badge/NLTK-154F3C?style=for-the-badge&logo=python&logoColor=white)](https://nltk.org) | Text Processing | [nltk.org](https://nltk.org) |
| [![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com) | Visualizations | [plotly.com](https://plotly.com) |
| [![ReportLab](https://img.shields.io/badge/ReportLab-F7A80D?style=for-the-badge&logo=adobe-acrobat-reader&logoColor=white)](https://reportlab.com) | PDF Generation | [reportlab.com](https://reportlab.com) |

---

**📦 Dependencies**
```text
streamlit==1.28.0       # Web application framework
plotly==5.17.0          # Interactive visualizations
spacy==3.7.0            # NLP processing
pdfplumber==0.10.2      # PDF text extraction
PyPDF2==3.0.1           # PDF handling
python-docx==1.0.1      # DOCX parsing
pandas==2.1.2           # Data manipulation
numpy==1.24.3           # Numerical computing
nltk==3.8.1             # Natural language toolkit
scikit-learn==1.3.1     # Machine learning utilities
reportlab==4.0.5        # PDF report generation
```

---

## 📊 Scoring System

Our AI analyzes resumes across **5 key categories**:

| Category | Weight | What We Check |
|----------|--------|---------------|
| 🔑 **Keywords** | 30% | Matching keywords from job description |
| 🛠️ **Skills** | 30% | Technical and soft skills alignment |
| 💼 **Experience** | 15% | Relevant experience and achievements |
| 🎓 **Education** | 10% | Educational qualifications match |
| 📄 **Format** | 15% | Resume structure and ATS compatibility |

### Score Interpretation

| Score Range | Rating | Meaning |
|-------------|--------|---------|
| 80-100% | 🟢 Excellent | Your resume is well-optimized for ATS |
| 60-79% | 🟡 Good | Minor improvements recommended |
| 40-59% | 🟠 Fair | Significant improvements needed |
| 0-39% | 🔴 Poor | Major overhaul required |

---

## 📞 Contact

<div align="center">

**Isha Pradhan** - ML Engineer

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/isha9803)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/isha-pradhan-122199339/)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:ishapradha098@gmail.com)

---

**Project Link:** [https://github.com/isha9803/ai-resume-screening-system](https://github.com/isha9803/ai-resume-screening-system)

</div>

---

## 🙏 Acknowledgments

Special thanks to these amazing projects and resources:

- [Streamlit](https://streamlit.io) - For the incredible web framework
- [spaCy](https://spacy.io) - For powerful NLP capabilities
- [Plotly](https://plotly.com) - For beautiful interactive charts
- [ReportLab](https://reportlab.com) - For PDF generation
- [NLTK](https://nltk.org) - For text processing
- [Shields.io](https://shields.io) - For beautiful badges

---

<div align="center">

### 🌟 If you found this project helpful, please give it a star!

[![Stars](https://img.shields.io/github/stars/isha9803/ai-resume-screening-system?style=for-the-badge&color=yellow)](https://github.com/isha9803/ai-resume-screening-system/stargazers)

---

Made with ❤️ and ☕ by [Isha Pradhan](https://github.com/isha9803)

</div>
