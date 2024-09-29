import re

# Comprehensive list of keywords and phrases for NSFW content
NSFW_KEYWORDS = [
    r'\bsex\b', r'\bporn\b', r'\bnaked\b', r'\bfuck\b', r'\bboobs\b', r'\bass\b', r'\bpenis\b', r'\bvagina\b',
    r'\bcock\b', r'\bbutts\b', r'\bdick\b', r'\btits\b', r'\bscrotum\b', r'\bcum\b', r'\bmilf\b', r'\bbra\b',
    # Deliberately obfuscated words
    r'\bp0rn\b', r'\bpr0n\b', r'\bsex0\b', r'\bf*ck\b', r'\bs*x\b', r'\bp*rn\b', r'\bbutt\b',
    # Detect common NSFW phrases (can expand more)
    r'hot pictures', r'sexy video', r'nude photos', r'free porn', r'onlyfans', r'explicit content'
]

# Advanced Regex patterns to detect character obfuscation
OBFUSCATION_PATTERNS = [
    r'p[o0]+rn', r'f[a@]+ck', r'b[i1]+tch', r's[e3]+x', r'd[i1]+ck', r'c[o0]+ck', r'a[s$]+s',
    # Catch common bypasses with numbers or special characters
    r'n[a4]+ked', r'm[i1]+lf', r'b[o0]+ob[s$]', r'v[a@]+gina', r't[i1]+ts', r'c[u*]+m'
]

def contains_nsfw(content):
    """
    Check if the given content contains any NSFW keywords or obfuscated patterns.
    """
    # Check for keyword-based NSFW detection
    for keyword in NSFW_KEYWORDS:
        if re.search(keyword, content, re.IGNORECASE):
            return True

    # Check for obfuscated pattern detection
    for pattern in OBFUSCATION_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            return True

    return False
