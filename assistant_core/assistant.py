#!/usr/bin/env python3
"""
assistant.py

- Defines the Assistant class, which uses an intent registry to route
  user commands to the correct handler function.
- Also includes a 'build_assistant()' function to register appointment handlers.
- Provides a simple command-line loop at the bottom for testing.
"""

from assistant_core.intent_parser import parse_intent
from assistant_core.handlers.appointments import (
    handle_create_appointment,
    handle_list_appointments,
    handle_update_appointment
)

class Assistant:
    def __init__(self):
        """
        Creates an Assistant with an empty intent registry.
        You can add new domain handlers by calling register_intent().
        """
        self.intent_registry = {}

    def register_intent(self, intent_name, handler_fn):
        """
        Map an intent string to a handler function.

        Example:
          assistant.register_intent("create_appointment", handle_create_appointment)
        """
        self.intent_registry[intent_name] = handler_fn

    def process_message(self, user_text: str) -> str:
        """
        1) parse user_text -> {intent: '...', ...} via parse_intent()
        2) look up the handler in self.intent_registry
        3) call the handler, return its result or an error if not found
        """
        parsed = parse_intent(user_text)
        intent = parsed.get("intent", "unknown")

        handler_fn = self.intent_registry.get(intent)
        if handler_fn:
            return handler_fn(parsed)
        else:
            return f"I didn't understand the intent '{intent}'."


def build_assistant() -> Assistant:
    """
    Creates an Assistant instance, registers known domain handlers,
    and returns it ready for use.
    """
    assistant = Assistant()

    # Register the 3 appointment-related intents:
    assistant.register_intent("create_appointment", handle_create_appointment)
    assistant.register_intent("list_appointments", handle_list_appointments)
    assistant.register_intent("update_appointment", handle_update_appointment)

    # In the future, you can register more:
    # e.g., assistant.register_intent("create_task", handle_create_task)

    return assistant


def main():
    """
    A simple command-line loop to interact with the assistant.
    Run: python3 assistant.py
    """
    assistant = build_assistant()

    print("Assistant is ready! Type your commands or 'quit' to exit.")

    while True:
        user_input = input("You > ")
        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break

        response = assistant.process_message(user_input)
        print("Assistant >", response)


if __name__ == "__main__":
    main()
