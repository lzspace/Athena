import os

subprocess.run(["pipreqs", "--force", "--savepath=requirements.txt", "scripts/"])

def list_py_files(start_dir="assistant_core/modules"):
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
    return file_map