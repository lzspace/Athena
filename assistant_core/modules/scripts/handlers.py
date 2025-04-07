def handle_run_script(script_name: str) -> str:
    import subprocess
    try:
        result = subprocess.run(["python", f"scripts/{script_name}"], capture_output=True, text=True)
        return result.stdout or result.stderr
    except Exception as e:
        return f"⚠️ Fehler beim Ausführen von {script_name}: {e}"
    
def handle_run_script(script_name: str) -> str:
    if not script_name:
        return "⚠️ Kein Skriptname erkannt. Bitte gib z.B. 'führe das Skript pre_commit.sh aus' ein."