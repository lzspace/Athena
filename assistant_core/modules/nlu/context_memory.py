"""
Script: context_memory.py
Category: Memory

Description:
A scalable, modular memory manager for tracking contextual state across different assistant modules.
"""

from collections import defaultdict

# _context[module][user_id] = data
_context = defaultdict(dict)

def set_context(module: str, user_id: str, data: dict):
    """Store context for a specific module and user."""
    _context[module][user_id] = data

def get_context(module: str, user_id: str) -> dict:
    """Retrieve context for a specific module and user."""
    return _context[module].get(user_id, {})

def clear_context(module: str, user_id: str):
    """Clear context for a specific module and user."""
    if user_id in _context[module]:
        del _context[module][user_id]

def has_context(module: str, user_id: str) -> bool:
    return user_id in _context[module]