import os
import argparse
import json
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

class SentimentAnalyzer:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.nlp = spacy.load('en_core_web_md')
        self.nlp.add_pipe('spacytextblob')
        self.derogatory_word_weights = {
                                        "hate": 0.8,
                                        "stupid": 0.6,
                                        "idiot": 0.7,
                                        "dumb": 0.1,
                                        # Add more words and weights
                                        }

    def open_json(self, filepath): 
        with open(filepath, 'r') as file:
            data = json.load(file)
        text = data['text']['text']
        return text
        
    def calculate_derogatory_score(self, sentence):
        normalized_score = 0
        total_weight = sum(self.derogatory_word_weights.values())
        words = word_tokenize(sentence)
        words = [word for word in words if word.lower() not in self.stop_words]

        for word in words:
            if word.lower() in self.derogatory_word_weights:
                normalized_score += self.derogatory_word_weights[word.lower()]

        if total_weight > 0:
            normalized_score /= total_weight

        return normalized_score

    def nltk_analyzer(self, sentence):
        words = word_tokenize(sentence)
        words = [word for word in words if word.lower() not in self.stop_words]

        sia = SentimentIntensityAnalyzer()
        sentiment_score = sia.polarity_scores(sentence)['compound']

        emotion_words = ['happy', 'sad', 'angry', 'excited', 'fearful', 'hate']
        emotion_found = any(word in words for word in emotion_words)

        derogatory_phrases = self.derogatory_word_weights.keys()
        derogatory_found = any(phrase in sentence.lower() for phrase in derogatory_phrases)
        derogatory_score = self.calculate_derogatory_score(sentence)

        return sentiment_score, emotion_found, derogatory_found, derogatory_score

    def spacy_analyzer(self, sentence):
        doc = self.nlp(sentence)
        return {
            "Polarity": doc._.blob.polarity,
            "Subjectivity": doc._.blob.subjectivity,
            "Emotion_words": doc._.blob.sentiment_assessments.assessments
        }

    def analyze_comments(self, filepath):
        base_filename = os.path.splitext(filepath)[0]
        output_file = f'{base_filename}.sentiment_analysis.txt'
        if filepath.endswith('.json'):
            text = self.open_json(filepath)
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
        with open(output_file, 'w') as output:
            output.write(f'Filename: {filepath}\n')
            output.write(f'\nText: {text}\n')
            for sentence in sentences:
                sentiment, has_emotion, is_derogatory, derogatory_score = self.nltk_analyzer(sentence)
                spacy_analysis = self.spacy_analyzer(sentence)
                output.write(f"\nSentence: {sentence}\n")
                output.write(f"Sentiment Score: {sentiment}\n")
                output.write(f"Has Emotion: {has_emotion}\n")
                output.write(f"Is Derogatory: {is_derogatory}\n")
                output.write(f"Derogatory Score: {derogatory_score:.2f}\n")
                for key, value in spacy_analysis.items():
                    output.write(f"{key}: {value}\n")
                output.write("-" * 30 + "\n")

def main(): 
    
    parser = argparse.ArgumentParser(description="Analyze comments for sentiment, emotion, and derogatory content.")
    parser.add_argument("-f", "--filepath", help="List of sentences to analyze")
    args = parser.parse_args()
    
    analyzer = SentimentAnalyzer()
    analyzer.analyze_comments(args.filepath)
    
if __name__ == "__main__":
    main()