import re
from collections import defaultdict
from transformers import pipeline

# Pre-trained ML-based NSFW classifier
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Comprehensive list of keywords and phrases for NSFW content
NSFW_KEYWORDS = [
    # Regular words and phrases
    r'\bsex\b', r'\bporn\b', r'\bnaked\b', r'\bfuck\b', r'\bboobs\b', r'\bass\b', r'\bpenis\b',
    r'\bcock\b', r'\btits\b', r'\bscrotum\b', r'\bmilf\b', r'onlyfans', r'explicit content'
]

# Advanced Regex patterns to detect character obfuscation
OBFUSCATION_PATTERNS = [
    r'p[o0]+rn', r'f[a@]+ck', r'b[i1]+tch', r's[e3]+x', r'd[i1]+ck', r'c[o0]+ck', r'a[s$]+s'
]

user_offense_count = defaultdict(int)
OFFENSE_LIMIT = 3

def contains_nsfw(content):
    """
    Check if the given content contains any NSFW keywords or obfuscated patterns.
    """
    for keyword in NSFW_KEYWORDS:
        if re.search(keyword, content, re.IGNORECASE):
            return True

    for pattern in OBFUSCATION_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            return True

    return ml_nsfw_filter(content)

def ml_nsfw_filter(content):
    """
    Use a machine learning model to classify whether the content is NSFW.
    Returns True if the content is inappropriate.
    """
    labels = ["NSFW", "SFW"]
    result = classifier(content, candidate_labels=labels)
    return result["labels"][0] == "NSFW"

def check_for_offenses(message, user_id):
    """
    Increment offense count if a user violates the NSFW filter.
    If the user exceeds the OFFENSE_LIMIT, trigger an action (e.g., ban or mute).
    """
    if contains_nsfw(message.content):
        user_offense_count[user_id] += 1
        if user_offense_count[user_id] >= OFFENSE_LIMIT:
            return "You have been warned multiple times for inappropriate content. You are now banned or muted."
        return "This message contains inappropriate content and cannot be processed."
    return None
