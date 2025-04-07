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
    all_intents = {}
    modules_dir = os.path.join(BASE_DIR, "modules")

    for module_name in os.listdir(modules_dir):
        module_path = os.path.join(modules_dir, module_name)
        if os.path.isdir(module_path):
            intents_path = os.path.join(module_path, "intents.yaml")
            if os.path.exists(intents_path):
                with open(intents_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    for intent, config in data.get("intents", {}).items():
                        all_intents[intent] = config

    return all_intents