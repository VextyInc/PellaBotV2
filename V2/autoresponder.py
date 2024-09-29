import time

class AutoResponder:
    def __init__(self, filepath, cooldown_period=10):
        self.responses = self.load_words(filepath)
        self.last_response_time = 0
        self.cooldown_period = cooldown_period

    def load_words(self, filepath):
        responses = {}
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    if '=' in line:
                        trigger, response = line.strip().split('=', 1)
                        responses[trigger.lower()] = response
        except FileNotFoundError:
            print(f"File {filepath} not found!")
        return responses

    def get_response(self, message_content):
        current_time = time.time()
        # Check if the bot is on cooldown to avoid spam
        if current_time - self.last_response_time < self.cooldown_period:
            return None  # No response during cooldown

        for trigger in self.responses:
            if trigger in message_content.lower():
                self.last_response_time = current_time
                return self.responses[trigger]
        return None  # No match found
