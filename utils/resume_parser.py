import PyPDF2
import pdfplumber
import docx
import re
import spacy
from typing import Dict, List, Any
import io

class ResumeParser:
    def __init__(self):
        # Load spaCy model (download with: python -m spacy download en_core_web_sm)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.phone_pattern = re.compile(r'(\+\d{1,3}[-.\s]?)?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}')
        self.url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        
    def extract_text(self, file) -> str:
        """Extract text from uploaded file"""
        text = ""
        file_type = file.name.split('.')[-1].lower()
        
        if file_type == 'pdf':
            text = self._extract_from_pdf(file)
        elif file_type == 'docx':
            text = self._extract_from_docx(file)
        elif file_type == 'txt':
            text = str(file.read(), 'utf-8')
        
        return text
    
    def _extract_from_pdf(self, file) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            # Try with pdfplumber first (better for complex layouts)
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except:
            # Fallback to PyPDF2
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        
        return text
    
    def _extract_from_docx(self, file) -> str:
        """Extract text from DOCX file"""
        doc = docx.Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def parse_resume(self, text: str) -> Dict[str, Any]:
        """Parse resume and extract structured information"""
        doc = self.nlp(text)
        
        resume_data = {
            'text': text,
            'emails': self.extract_emails(text),
            'phones': self.extract_phones(text),
            'urls': self.extract_urls(text),
            'skills': self.extract_skills(text),
            'education': self.extract_education(text),
            'experience': self.extract_experience(text),
            'entities': self.extract_entities(doc),
            'sections': self.identify_sections(text)
        }
        
        return resume_data
    
    def extract_emails(self, text: str) -> List[str]:
        """Extract email addresses"""
        return self.email_pattern.findall(text)
    
    def extract_phones(self, text: str) -> List[str]:
        """Extract phone numbers"""
        phones = self.phone_pattern.findall(text)
        return [p for p in phones if len(p) >= 10]
    
    def extract_urls(self, text: str) -> List[str]:
        """Extract URLs"""
        return self.url_pattern.findall(text)
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume"""
        # Common technical skills (expand this list based on your needs)
        skill_patterns = [
            'python', 'java', 'javascript', 'c\\+\\+', 'sql', 'html', 'css', 'react', 
            'angular', 'vue', 'node', 'django', 'flask', 'spring', 'docker', 'kubernetes',
            'aws', 'azure', 'gcp', 'machine learning', 'deep learning', 'data analysis',
            'project management', 'agile', 'scrum', 'git', 'ci/cd', 'devops', 'api',
            'rest', 'graphql', 'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in skill_patterns:
            if re.search(r'\b' + skill + r'\b', text_lower):
                found_skills.append(skill)
        
        return found_skills
    
    def extract_education(self, text: str) -> List[str]:
        """Extract education information"""
        education_keywords = [
            'bachelor', 'master', 'phd', 'doctorate', 'degree', 'university', 
            'college', 'institute', 'school', 'certification', 'certified'
        ]
        
        lines = text.split('\n')
        education_lines = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in education_keywords):
                education_lines.append(line.strip())
        
        return education_lines
    
    def extract_experience(self, text: str) -> List[str]:
        """Extract work experience"""
        experience_keywords = [
            'experience', 'worked', 'working', 'job', 'position', 'role',
            'company', 'organization', 'intern', 'employee', 'developer',
            'engineer', 'manager', 'analyst', 'consultant', 'specialist'
        ]
        
        lines = text.split('\n')
        experience_lines = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in experience_keywords):
                experience_lines.append(line.strip())
        
        return experience_lines[:10]  # Return top 10 lines
    
    def extract_entities(self, doc) -> Dict[str, List[str]]:
        """Extract named entities"""
        entities = {
            'persons': [],
            'organizations': [],
            'locations': [],
            'dates': []
        }
        
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                entities['persons'].append(ent.text)
            elif ent.label_ == "ORG":
                entities['organizations'].append(ent.text)
            elif ent.label_ in ["GPE", "LOC"]:
                entities['locations'].append(ent.text)
            elif ent.label_ == "DATE":
                entities['dates'].append(ent.text)
        
        return entities
    
    def identify_sections(self, text: str) -> Dict[str, str]:
        """Identify different sections in the resume"""
        sections = {}
        section_headers = [
            'summary', 'objective', 'experience', 'education', 'skills',
            'projects', 'achievements', 'certifications', 'awards', 'publications'
        ]
        
        lines = text.split('\n')
        current_section = None
        section_content = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if line is a section header
            for header in section_headers:
                if header in line_lower and len(line_lower) < 50:
                    if current_section:
                        sections[current_section] = '\n'.join(section_content)
                    current_section = header
                    section_content = []
                    break
            else:
                if current_section:
                    section_content.append(line)
        
        # Add the last section
        if current_section:
            sections[current_section] = '\n'.join(section_content)
        
        return sections