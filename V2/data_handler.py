import json

def load_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def find_best_answer(question, datasets):
    # Simplified matching algorithm
    best_answer = None
    highest_score = 0

    for dataset in datasets:
        for entry in dataset:
            score = calculate_similarity(question.lower(), entry['question'].lower())
            if score > highest_score:
                highest_score = score
                best_answer = entry['answer']

    return best_answer

def calculate_similarity(question, target):
    # Basic keyword matching, can be improved with NLP techniques
    question_words = set(question.split())
    target_words = set(target.split())
    common_words = question_words.intersection(target_words)
    return len(common_words)  # Return the number of matching words
