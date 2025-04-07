import subprocess
import logging

# Konfiguriere das Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def run_git_command(command_list):
    """
    Führt einen Git-Befehl aus und gibt die Standardausgabe zurück.
    Bei einem Fehler wird eine aussagekräftige Fehlermeldung geloggt und die Exception weitergereicht.
    """
    try:
        result = subprocess.run(
            command_list,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        logging.debug(f"Git command {' '.join(command_list)} output: {result.stdout.strip()}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Git command {' '.join(command_list)} failed: {e.stderr.strip()}")
        raise

def get_current_branch():
    """Gibt den aktuellen Git-Branch zurück."""
    return run_git_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])

def list_branches():
    """Gibt eine Liste aller lokalen Branches zurück."""
    return run_git_command(["git", "branch"])

def checkout_branch(branch_name, create_new=False):
    """
    Wechselt zu einem bestehenden Branch oder erstellt einen neuen.
    
    Parameter:
        branch_name (str): Name des Branches
        create_new (bool): Falls True, wird ein neuer Branch erstellt.
    """
    try:
        if create_new:
            logging.info(f"Erstelle und wechsle zu neuem Branch: {branch_name}")
            return run_git_command(["git", "checkout", "-b", branch_name])
        else:
            logging.info(f"Wechsle zu Branch: {branch_name}")
            return run_git_command(["git", "checkout", branch_name])
    except Exception as e:
        logging.error(f"Fehler beim Wechseln zu Branch {branch_name}: {e}")
        raise

def auto_commit(file_path, message):
    """
    Fügt eine Datei dem Commit hinzu und führt einen Commit mit der angegebenen Nachricht durch.
    Falls keine Änderungen vorhanden sind, wird der Commit übersprungen.
    
    Parameter:
        file_path (str): Pfad zur Datei
        message (str): Commit-Nachricht
    """
    try:
        logging.info(f"Füge Datei {file_path} dem Commit hinzu")
        run_git_command(["git", "add", file_path])
        
        # Prüfe, ob es gestagte Änderungen gibt
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            check=False
        )
        if result.returncode == 0:
            logging.warning("Keine Änderungen zum Commit vorhanden. Commit wird übersprungen.")
            return
        
        logging.info(f"Commit mit Nachricht: {message}")
        run_git_command(["git", "commit", "-m", message])
    except Exception as e:
        logging.error(f"Fehler beim Commit von {file_path}: {e}")
        raise

# Remote-Operationen

def git_pull(remote="origin", branch=None):
    """
    Führt ein git pull aus. Falls branch angegeben ist, wird dieser gezogen.
    """
    try:
        command = ["git", "pull", remote]
        if branch:
            command.append(branch)
        logging.info(f"Pulle Änderungen: {' '.join(command)}")
        return run_git_command(command)
    except Exception as e:
        logging.error(f"Fehler beim Pull von {remote}: {e}")
        raise

def git_push(remote="origin", branch=None):
    """
    Führt ein git push aus. Falls branch angegeben ist, wird dieser gepusht.
    """
    try:
        command = ["git", "push", remote]
        if branch:
            command.append(branch)
        logging.info(f"Pushe Änderungen: {' '.join(command)}")
        return run_git_command(command)
    except Exception as e:
        logging.error(f"Fehler beim Push zu {remote}: {e}")
        raise

def git_fetch(remote="origin"):
    """
    Führt ein git fetch vom angegebenen Remote aus.
    """
    try:
        logging.info(f"Fetche Änderungen vom Remote: {remote}")
        return run_git_command(["git", "fetch", remote])
    except Exception as e:
        logging.error(f"Fehler beim Fetch von {remote}: {e}")
        raise

def list_remote_branches(remote="origin"):
    """
    Listet alle Remote-Branches auf.
    """
    try:
        output = run_git_command(["git", "ls-remote", "--heads", remote])
        branches = []
        for line in output.splitlines():
            parts = line.split()
            if len(parts) == 2:
                ref = parts[1]
                if ref.startswith("refs/heads/"):
                    branch_name = ref.replace("refs/heads/", "")
                    branches.append(branch_name)
        logging.info(f"Remote-Branches von {remote}: {branches}")
        return branches
    except Exception as e:
        logging.error(f"Fehler beim Abrufen der Remote-Branches von {remote}: {e}")
        raise

# Branch-Vorschläge

def suggest_feature_branch(prefix="feature"):
    """
    Gibt eine Liste von existierenden Branches zurück, die mit dem angegebenen Präfix beginnen.
    Falls keine vorhanden sind, wird eine leere Liste zurückgegeben.
    """
    try:
        branches_output = run_git_command(["git", "branch", "--list"])
        # Entferne führende '*' (aktueller Branch) und Leerzeichen
        branches = [b.strip("* ").strip() for b in branches_output.splitlines()]
        suggestions = [b for b in branches if b.startswith(prefix)]
        if suggestions:
            logging.info(f"Vorschläge für existierende Feature-Branches: {suggestions}")
        else:
            logging.info("Keine existierenden Feature-Branches gefunden. Neuer Branch wird empfohlen.")
        return suggestions
    except Exception as e:
        logging.error(f"Fehler bei der Branch-Vorschlagsfunktion: {e}")
        raise