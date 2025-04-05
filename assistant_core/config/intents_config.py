#!/usr/bin/env python3
"""
intents_config.py

Loads YAML-based intents config, returning a structure you can use in your intent_parser.
"""
import os
import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INTENTS_YAML_PATH = os.path.join(BASE_DIR, "modules", "appointments", "intents.yaml")

def load_intents():
    if not os.path.exists(INTENTS_YAML_PATH):
        raise FileNotFoundError(
            f"Intents configuration file not found at {INTENTS_YAML_PATH}. "
            "Please ensure the file exists or provide a valid path."
        )
    with open(INTENTS_YAML_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    # data should look like: {"intents": {...}}
    # Return the "intents" dict for convenience
    return data["intents"]