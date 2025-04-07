import os
import yaml

INTENTS_DIR = os.path.join(os.path.dirname(__file__), "config", "modules")

def load_all_intents():
    intents = []
    for root, dirs, files in os.walk(INTENTS_DIR):
        for file in files:
            if file == "intents.yaml":
                intent_path = os.path.join(root, file)
                with open(intent_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    if isinstance(data, dict) and "intents" in data:
                        intents.extend(data["intents"].values())
                    else:
                        print(f"⚠️ Warning: {intent_path} doesn't contain valid intents")
    return intents

# Example usage
if __name__ == "__main__":
    all_intents = load_all_intents()
    for intent in all_intents:
        print(f"Intent: {intent['description']} => Phrases: {intent['examples']}")
