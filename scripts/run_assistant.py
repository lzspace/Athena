from pathlib import Path

# Define run_assistant.py content
assistant_cli_code = '''"""
Script: run_assistant.py
Category: CLI Tool

Description:
A simple terminal-based loop to interact with the Athena assistant.
"""

from assistant_core.modules.nlu.nlu_pipeline import process_user_input

print("🧠 Athena is listening. Type 'exit' to quit.")
while True:
    try:
        user_input = input("You: ")
        if user_input.strip().lower() in {"exit", "quit"}:
            print("👋 Goodbye!")
            break
        response = process_user_input(user_input)
        print(f"Athena: {response}")
    except Exception as e:
        print(f"⚠️ Error: {e}")
'''

# Write to file
cli_file_path = Path("run_assistant.py")
cli_file_path.write_text(assistant_cli_code)
cli_file_path