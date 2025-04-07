"""
generator.py

Code-Generator für die automatische Erstellung von Skripten.
"""

def generate_script(script_name, context):
    """
    Generiert ein Skript anhand eines Templates und führt optional einen automatischen Commit durch.
    
    Parameter:
        script_name: Name des Skripts (ohne Dateiendung)
        context: Kontextdaten, die zur Codegenerierung genutzt werden
    
    Rückgabe:
        Der Pfad zum generierten Skript.
    """
    # Beispiel: Bestimme den Zielpfad für das Skript
    script_path = f"scripts/{script_name}.py"
    
    # Generiere einfachen Code (dieser Teil kann später durch Template-Logik oder LLM-Generierung ersetzt werden)
    code = f"# Auto-generiertes Skript: {script_name}\n\n"
    code += "# Hier folgt der generierte Code\n"
    
    # Schreibe den Code in die Datei
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(code)
    
    # Führe einen automatischen Commit durch
    from assistant_core.modules.coding import git_utils
    git_utils.auto_commit(script_path, f"auto: add generated script '{script_name}'")
    
    return script_path

# Optional: Du kannst auch einen einfachen Testlauf hier einbauen, der nur ausgeführt wird, wenn dieses Skript direkt gestartet wird.
if __name__ == "__main__":
    # Beispielaufruf: Erstelle ein Skript namens "example"
    generate_script("example", context={})