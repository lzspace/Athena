import subprocess

def get_current_branch():
    return subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()

def list_branches():
    return subprocess.check_output(["git", "branch"]).decode()

def checkout_branch(branch_name, create_new=False):
    if create_new:
        subprocess.run(["git", "checkout", "-b", branch_name])
    else:
        subprocess.run(["git", "checkout", branch_name])

def auto_commit(file_path, message):
    subprocess.run(["git", "add", file_path])
    subprocess.run(["git", "commit", "-m", message])