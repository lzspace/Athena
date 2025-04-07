import os
import subprocess
import logging
import subprocess
from datetime import datetime

def get_diff_files(commit_range="HEAD~1..HEAD"):
    """
    Gibt eine Liste von Dateien zurück, die sich zwischen den angegebenen Commits geändert haben.
    commit_range kann z.B. 'HEAD~1..HEAD' oder 'main..feature-branch' sein.
    """
    try:
        diff_output = subprocess.check_output(
            ["git", "diff", "--name-status", commit_range],
            stderr=subprocess.STDOUT
        ).decode().strip()
        
        changed_files = []
        for line in diff_output.splitlines():
            # Format: M\tpath/to/file.py  oder A, D etc.
            status, path = line.split(maxsplit=1)
            changed_files.append({"status": status, "file": path})
        
        return changed_files
    except subprocess.CalledProcessError as e:
        print("Fehler beim Ausführen von git diff:", e)
        return []

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def run_flake8_check(file_path=None):
    """
    Führt flake8 auf einer Datei oder dem gesamten Projekt aus.
    Gibt eine Liste von Fehlern/Warnings zurück.
    """
    command = ["flake8"]
    if file_path:
        command.append(file_path)
    else:
        command.append(".")
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            # Keine Fehler
            return []
        else:
            # flake8 gibt Fehler über stdout oder stderr aus
            issues = result.stdout.strip().splitlines() if result.stdout else result.stderr.strip().splitlines()
            return issues
    except FileNotFoundError:
        logging.warning("flake8 ist nicht installiert. Bitte installiere es, um Code-Checks durchzuführen.")
        return []


def collect_file_stats(start_dir="assistant_core/modules"):
    """
    Durchsucht das angegebene Verzeichnis rekursiv nach Python-Dateien
    und erfasst detaillierte Statistiken wie Dateigröße, letzte Änderungszeit und Zeilenzahl.
    Gibt eine Liste von Dictionaries zurück.
    """
    stats_list = []
    for root, _, files in os.walk(start_dir):
        for f in files:
            if f.endswith(".py"):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path)
                
                # Hole Dateigröße und Änderungszeit
                file_stat = os.stat(full_path)
                size_bytes = file_stat.st_size
                modified_time = datetime.fromtimestamp(file_stat.st_mtime)
                
                # Zeilenzahl ermitteln
                with open(full_path, "r", encoding="utf-8") as fd:
                    lines = fd.readlines()
                line_count = len(lines)

                stats_list.append({
                    "file": rel_path,
                    "size_bytes": size_bytes,
                    "modified": modified_time.isoformat(),
                    "line_count": line_count
                })
    return stats_list

def list_py_files(start_dir="assistant_core/modules"):
    """
    Durchsucht das angegebene Verzeichnis rekursiv nach Python-Dateien
    und gibt ein Dictionary mit relativen Pfaden, Dateinamen und Verzeichnisnamen zurück.
    """
    file_map = {}
    for root, _, files in os.walk(start_dir):
        for f in files:
            if f.endswith(".py"):
                rel_path = os.path.relpath(os.path.join(root, f))
                file_map[rel_path] = {
                    "name": f,
                    "path": rel_path,
                    "dir": os.path.basename(root)
                }
    
    # Versuche pipreqs auszuführen, um requirements.txt zu aktualisieren
    try:
        subprocess.run(
            ["pipreqs", "--force", "--savepath=requirements.txt", "scripts/"],
            check=True
        )
    except FileNotFoundError:
        logging.warning("pipreqs wurde nicht gefunden. Bitte installiere pipreqs, falls du automatische Abhängigkeitsaktualisierungen benötigst.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Fehler bei der Ausführung von pipreqs: {e}")
    
    return file_map