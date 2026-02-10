from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Dict, List, Any
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK data if not already present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class ATSScorer:
    def __init__(self):
        # Load sentence transformer model for semantic similarity
        self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.tfidf_vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        self.stop_words = set(stopwords.words('english'))
        
    def calculate_ats_score(self, resume_text: str, job_description: str, resume_data: Dict) -> Dict[str, Any]:
        """Calculate comprehensive ATS score"""
        
        # Calculate different score components
        keyword_score = self.calculate_keyword_match(resume_text, job_description)
        semantic_score = self.calculate_semantic_similarity(resume_text, job_description)
        skills_score = self.calculate_skills_match(resume_data.get('skills', []), job_description)
        experience_score = self.evaluate_experience(resume_data.get('experience', []))
        education_score = self.evaluate_education(resume_data.get('education', []))
        format_score = self.evaluate_format(resume_data)
        
        # Calculate overall score (weighted average)
        overall_score = (
            keyword_score * 0.25 +
            semantic_score * 0.20 +
            skills_score * 0.25 +
            experience_score * 0.15 +
            education_score * 0.10 +
            format_score * 0.05
        )
        
        # Identify issues and suggestions
        issues = self.identify_issues(
            keyword_score, skills_score, experience_score, 
            education_score, format_score, resume_data
        )
        
        suggestions = self.generate_suggestions(
            keyword_score, skills_score, experience_score,
            education_score, format_score, resume_data, job_description
        )
        
        # Find missing keywords
        missing_keywords = self.find_missing_keywords(resume_text, job_description)
        
        return {
            'overall_score': round(overall_score, 2),
            'keyword_match_score': round(keyword_score, 2),
            'semantic_similarity': round(semantic_score, 2),
            'skills_score': round(skills_score, 2),
            'experience_score': round(experience_score, 2),
            'education_score': round(education_score, 2),
            'format_score': round(format_score, 2),
            'issues': issues,
            'suggestions': suggestions,
            'missing_keywords': missing_keywords,
            'matched_skills': resume_data.get('skills', []),
            'sections_found': list(resume_data.get('sections', {}).keys())
        }
    
    def calculate_keyword_match(self, resume: str, job_desc: str) -> float:
        """Calculate keyword matching score using TF-IDF"""
        try:
            # Tokenize and process texts
            resume_tokens = word_tokenize(resume.lower())
            jd_tokens = word_tokenize(job_desc.lower())
            
            # Remove stopwords
            resume_words = [w for w in resume_tokens if w.isalnum() and w not in self.stop_words]
            jd_words = [w for w in jd_tokens if w.isalnum() and w not in self.stop_words]
            
            # Calculate word frequency
            resume_freq = Counter(resume_words)
            jd_freq = Counter(jd_words)
            
            # Find common words
            common_words = set(resume_freq.keys()) & set(jd_freq.keys())
            
            if len(jd_freq) == 0:
                return 0.0
            
            # Calculate match percentage
            match_score = (len(common_words) / len(set(jd_freq.keys()))) * 100
            
            return min(match_score, 100)
        except:
            return 50.0
    
    def calculate_semantic_similarity(self, resume: str, job_desc: str) -> float:
        """Calculate semantic similarity using sentence transformers"""
        try:
            # Generate embeddings
            resume_embedding = self.semantic_model.encode([resume])
            jd_embedding = self.semantic_model.encode([job_desc])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(resume_embedding, jd_embedding)[0][0]
            
            # Convert to percentage
            return similarity * 100
        except:
            return 50.0
    
    def calculate_skills_match(self, resume_skills: List[str], job_desc: str) -> float:
        """Calculate skills matching score"""
        if not resume_skills:
            return 30.0
        
        job_desc_lower = job_desc.lower()
        matched_skills = 0
        
        # Extract skills from job description
        jd_skills = self.extract_skills_from_jd(job_desc)
        
        if not jd_skills:
            # If no skills found in JD, check basic presence
            for skill in resume_skills:
                if skill.lower() in job_desc_lower:
                    matched_skills += 1
            return min((matched_skills / max(len(resume_skills), 1)) * 100, 100)
        
        # Calculate match with extracted JD skills
        for skill in resume_skills:
            if skill.lower() in [s.lower() for s in jd_skills]:
                matched_skills += 1
        
        return (matched_skills / len(jd_skills)) * 100
    
    def extract_skills_from_jd(self, job_desc: str) -> List[str]:
        """Extract required skills from job description"""
        # Common skill indicators
        skill_patterns = [
            r'required skills?:?(.*?)(?:preferred|desired|responsibilities|qualifications|\n\n)',
            r'must have:?(.*?)(?:nice to have|preferred|\n\n)',
            r'technical skills?:?(.*?)(?:soft skills|experience|\n\n)',
            r'qualifications?:?(.*?)(?:responsibilities|duties|\n\n)'
        ]
        
        skills = []
        job_desc_lower = job_desc.lower()
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, job_desc_lower, re.DOTALL | re.IGNORECASE)
            for match in matches:
                # Extract individual skills
                skill_lines = match.split('\n')
                for line in skill_lines:
                    # Clean and extract skills
                    line = re.sub(r'[•\-\*]', '', line).strip()
                    if line and len(line) > 3:
                        skills.append(line)
        
        return skills[:20]  # Return top 20 skills
    
    def evaluate_experience(self, experience_lines: List[str]) -> float:
        """Evaluate experience section"""
        if not experience_lines:
            return 30.0
        
        score = 50.0  # Base score for having experience section
        
        # Check for quantifiable achievements
        achievement_patterns = [
            r'\d+%', r'\$[\d,]+', r'increased', r'decreased', r'improved',
            r'reduced', r'achieved', r'exceeded', r'delivered', r'managed'
        ]
        
        achievements_found = 0
        for line in experience_lines:
            for pattern in achievement_patterns:
                if re.search(pattern, line.lower()):
                    achievements_found += 1
                    break
        
        if achievements_found > 0:
            score += min(achievements_found * 5, 30)  # Up to 30 points for achievements
        
        # Check for date ranges (shows clear timeline)
        date_pattern = r'\d{4}'
        dates_found = sum(1 for line in experience_lines if re.search(date_pattern, line))
        if dates_found >= 2:
            score += 20
        
        return min(score, 100)
    
    def evaluate_education(self, education_lines: List[str]) -> float:
        """Evaluate education section"""
        if not education_lines:
            return 40.0
        
        score = 60.0  # Base score for having education
        
        # Check for degree levels
        degree_keywords = ['bachelor', 'master', 'phd', 'doctorate', 'mba', 'associate']
        for line in education_lines:
            if any(deg in line.lower() for deg in degree_keywords):
                score = 80.0
                break
        
        # Check for GPA mention (shows transparency)
        if any('gpa' in line.lower() or 'grade' in line.lower() for line in education_lines):
            score += 10
        
        # Check for year of graduation
        if any(re.search(r'\d{4}', line) for line in education_lines):
            score += 10
        
        return min(score, 100)
    
    def evaluate_format(self, resume_data: Dict) -> float:
        """Evaluate resume format and structure"""
        score = 0.0
        
        # Check for contact information
        if resume_data.get('emails'):
            score += 20
        if resume_data.get('phones'):
            score += 20
        
        # Check for clear sections
        sections = resume_data.get('sections', {})
        important_sections = ['experience', 'education', 'skills']
        for section in important_sections:
            if section in sections:
                score += 20
        
        # Check for reasonable length (not too short or too long)
        text_length = len(resume_data.get('text', ''))
        if 500 <= text_length <= 5000:
            score += 20
        elif 300 <= text_length < 500 or 5000 < text_length <= 7000:
            score += 10
        
        return min(score, 100)
    
    def identify_issues(self, keyword_score, skills_score, experience_score, 
                       education_score, format_score, resume_data):
        """Identify specific issues with the resume"""
        issues = []
        
        if keyword_score < 40:
            issues.append("❌ Very low keyword match with job description")
        elif keyword_score < 60:
            issues.append("⚠️ Moderate keyword match - consider adding more relevant keywords")
        
        if skills_score < 40:
            issues.append("❌ Skills section needs significant improvement")
        elif skills_score < 60:
            issues.append("⚠️ Some key skills might be missing")
        
        if experience_score < 50:
            issues.append("❌ Experience section lacks quantifiable achievements")
        
        if education_score < 50:
            issues.append("⚠️ Education section could be more detailed")
        
        if format_score < 60:
            issues.append("❌ Resume format needs improvement for ATS parsing")
        
        if not resume_data.get('emails'):
            issues.append("❌ Email address not found")
        
        if not resume_data.get('phones'):
            issues.append("❌ Phone number not found")
        
        if len(resume_data.get('text', '')) < 300:
            issues.append("❌ Resume is too short - add more relevant content")
        elif len(resume_data.get('text', '')) > 7000:
            issues.append("⚠️ Resume might be too long - consider being more concise")
        
        return issues
    
    def generate_suggestions(self, keyword_score, skills_score, experience_score,
                           education_score, format_score, resume_data, job_desc):
        """Generate improvement suggestions"""
        suggestions = []
        
        if keyword_score < 70:
            suggestions.append("💡 Incorporate more keywords from the job description naturally throughout your resume")
        
        if skills_score < 70:
            suggestions.append("💡 Add a dedicated skills section with relevant technical and soft skills")
            suggestions.append("💡 Match your skills with those mentioned in the job requirements")
        
        if experience_score < 70:
            suggestions.append("💡 Add quantifiable achievements (percentages, dollar amounts, team sizes)")
            suggestions.append("💡 Use action verbs to start your experience bullet points")
            suggestions.append("💡 Include specific dates for each position")
        
        if education_score < 70:
            suggestions.append("💡 Include graduation year and GPA (if above 3.5)")
            suggestions.append("💡 Add relevant coursework, projects, or academic achievements")
        
        if format_score < 70:
            suggestions.append("💡 Ensure clear section headers (Experience, Education, Skills)")
            suggestions.append("💡 Include all contact information at the top")
            suggestions.append("💡 Use consistent formatting throughout")
        
        if not resume_data.get('urls'):
            suggestions.append("💡 Consider adding your LinkedIn profile or portfolio URL")
        
        # Add specific skill suggestions based on JD
        jd_skills = self.extract_skills_from_jd(job_desc)
        resume_skills = set([s.lower() for s in resume_data.get('skills', [])])
        missing_skills = [s for s in jd_skills[:5] if s.lower() not in resume_skills]
        
        if missing_skills:
            suggestions.append(f"💡 Consider adding these skills if you have them: {', '.join(missing_skills[:3])}")
        
        return suggestions
    
    def find_missing_keywords(self, resume: str, job_desc: str) -> List[str]:
        """Find important keywords missing from resume"""
        # Extract important words from job description
        jd_tokens = word_tokenize(job_desc.lower())
        resume_tokens = set(word_tokenize(resume.lower()))
        
        # Filter important words (exclude stopwords and short words)
        important_words = []
        word_freq = Counter(jd_tokens)
        
        for word, freq in word_freq.most_common(50):
            if (word not in self.stop_words and 
                len(word) > 3 and 
                word.isalnum() and 
                word not in resume_tokens and
                freq > 1):  # Word appears more than once in JD
                important_words.append(word)
        
        return important_words[:15]  # Return top 15 missing keywords