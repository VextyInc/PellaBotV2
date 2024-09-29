import re
from collections import defaultdict

# Comprehensive NSFW list
NSFW_KEYWORDS = [
    r'\bsex\b', r'\bporn\b', r'\bnaked\b', r'\bfuck\b', r'\bboobs\b', r'\bvagina\b', 
    r'\bcock\b', r'\btits\b', r'\bscrotum\b', r'\bmilf\b', r'onlyfans'
]

OBFUSCATION_PATTERNS = [
    r'p[o0]+rn', r'f[a@]+ck', r'b[i1]+tch', r's[e3]+x', r'd[i1]+ck', r'c[o0]+ck', r'a[s$]+s',
    r'n[a4]+ked', r'm[i1]+lf', r'b[o0]+ob[s$]', r'v[a@]+gina'
]

# User offense tracker
user_offense_count = defaultdict(int)
OFFENSE_LIMIT = 3

def contains_nsfw(content):
    """
    Check if content contains NSFW keywords or obfuscation patterns.
    """
    # Check for explicit NSFW keywords
    for keyword in NSFW_KEYWORDS:
        if re.search(keyword, content, re.IGNORECASE):
            return True

    # Check for common obfuscation patterns
    for pattern in OBFUSCATION_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            return True

    return False

def check_for_offenses(message, author_id):
    """
    Analyze a message and warn the user if NSFW content is found.
    """
    if contains_nsfw(message.content):
        user_offense_count[author_id] += 1
        
        if user_offense_count[author_id] >= OFFENSE_LIMIT:
            # Too many offenses, take action
            return f"⚠️ {message.author.mention}, you have been warned for inappropriate language."
        else:
            return f"⚠️ {message.author.mention}, please refrain from using NSFW language."
    return None
