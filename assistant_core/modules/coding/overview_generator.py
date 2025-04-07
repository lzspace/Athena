def generate_script_overview(script_path: str, description: str, used_libs: list, tests: list):
    overview = f"""
# Skriptübersicht: {script_path}

## 🧩 Beschreibung
{description}

## 📁 Ablageort
{script_path}

## 📦 Verwendete Libraries
- {', '.join(used_libs) if used_libs else 'Keine externen Bibliotheken'}

## 🧪 Zugeordnete Tests
- {', '.join(tests) if tests else 'Keine Tests gefunden'}
"""
    with open("SCRIPTS.md", "a") as f:
        f.write(overview)