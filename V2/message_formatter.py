import json
import os
from data_handler import find_best_answer, load_data

def format_logged_messages(log_file='data/ai_gen_data.txt', output_file='data/formatted_data.json'):
    formatted_data = []

    # Load datasets
    dataset1 = load_data('data/PellaData1.json')
    dataset2 = load_data('data/PellaData2.json')
    datasets = [dataset1, dataset2]

    if not os.path.exists(log_file):
        print("Log file not found!")
        return

    with open(log_file, 'r') as file:
        for line in file:
            question = line.strip()
            if question:  # Only process non-empty questions
                answer = find_best_answer(question, datasets)  # Find the best answer from datasets
                context = "User Input"
                tags = ["user input", "logged message"]

                formatted_data.append({
                    "question": question,
                    "answer": answer if answer else "I couldn't find a suitable answer.",
                    "context": context,
                    "tags": tags
                })

    # Save the formatted data
    with open(output_file, 'w') as json_file:
        json.dump(formatted_data, json_file, indent=4)

    print(f"Formatted data saved to {output_file}.")
