import nltk
from collections import Counter
from nltk.corpus import wordnet
from nltk import word_tokenize, pos_tag
from textstat import flesch_reading_ease, flesch_kincaid_grade

nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')

def calculate_readability(lyrics):
    return {
        "flesch_reading_ease": flesch_reading_ease(lyrics), # higher is easier, 100-0
        "flesch_kincaid_grade": flesch_kincaid_grade(lyrics), # higher is harder
    }

def type_token_ratio(lyrics): # higher is more diverse and complex
    words = lyrics.split()
    return len(set(words)) / len(words) if len(words) > 0 else 0

def lexical_density(lyrics): # higher is more informative and complex
    words = word_tokenize(lyrics)
    pos_tags = pos_tag(words)
    content_words = [word for word, tag in pos_tags if tag.startswith(('NN', 'VB', 'JJ', 'RB'))]
    return len(content_words) / len(words) if len(words) > 0 else 0

def average_sentence_length(lyrics): # higher is longer and more complex
    sentences = nltk.sent_tokenize(lyrics)
    words = nltk.word_tokenize(lyrics)
    return len(words) / len(sentences) if len(sentences) > 0 else 0

def word_difficulty(word): # higher is harder
    synsets = wordnet.synsets(word)
    return len(synsets)

def lyrics_difficulty_score(lyrics):
    readability = flesch_kincaid_grade(lyrics)
    lexical = lexical_density(lyrics)
    sentence_complexity = average_sentence_length(lyrics)
    return 0.4 * readability + 0.3 * lexical + 0.2 * sentence_complexity