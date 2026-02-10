import re
import string
from typing import List, Dict
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
for resource in ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger']:
    try:
        nltk.data.find(f'tokenizers/{resource}')
    except LookupError:
        nltk.download(resource)

class TextProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www.\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters but keep spaces and basic punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\;\:\!\?\-]', ' ', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def advanced_clean(self, text: str) -> str:
        """Advanced text cleaning with lemmatization"""
        # Basic cleaning
        text = self.clean_text(text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        cleaned_tokens = []
        for token in tokens:
            if token not in self.stop_words and len(token) > 2:
                lemmatized = self.lemmatizer.lemmatize(token)
                cleaned_tokens.append(lemmatized)
        
        return ' '.join(cleaned_tokens)
    
    def extract_sentences(self, text: str) -> List[str]:
        """Extract sentences from text"""
        return sent_tokenize(text)
    
    def extract_key_phrases(self, text: str, num_phrases: int = 10) -> List[str]:
        """Extract key phrases from text"""
        # Simple n-gram based approach
        words = word_tokenize(text.lower())
        
        # Remove stopwords
        words = [w for w in words if w not in self.stop_words and w.isalnum()]
        
        # Create bigrams and trigrams
        bigrams = [' '.join(words[i:i+2]) for i in range(len(words)-1)]
        trigrams = [' '.join(words[i:i+3]) for i in range(len(words)-2)]
        
        # Count frequency
        from collections import Counter
        phrase_freq = Counter(bigrams + trigrams)
        
        # Return top phrases
        return [phrase for phrase, _ in phrase_freq.most_common(num_phrases)]
    
    def calculate_readability_score(self, text: str) -> float:
        """Calculate readability score (Flesch Reading Ease)"""
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        
        if not sentences or not words:
            return 0.0
        
        # Count syllables (simplified)
        syllable_count = 0
        for word in words:
            syllable_count += max(1, len(re.findall(r'[aeiouAEIOU]', word)))
        
        # Calculate Flesch Reading Ease
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables_per_word = syllable_count / len(words)
        
        flesch_score = 206.835 - 1.015 * avg_sentence_length - 84.6 * avg_syllables_per_word
        
        # Normalize to 0-100
        return max(0, min(100, flesch_score))