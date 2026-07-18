import os
import subprocess
import sys


def run_script(script_path):
    """
    Run a Python Script

    Args:
        script_path (str): Python Script System Path
    """
    try:
        print(f"Running script: {script_path}")
        subprocess.run([sys.executable, script_path], check=True, cwd=project_root)
        print(f"script '{script_path}' execution completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error For Running '{script_path}': {e}")
    except FileNotFoundError:
        print(f"Script '{script_path}' Not Found")

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

scripts_to_execute = [
    os.path.join(project_root, "Automatic_Run_1.py"),
    os.path.join(project_root, "Treshold Finder.py"),

    # More Scripts Can Add to this List
]

for script_path in scripts_to_execute:
    run_script(script_path)

print("Sucsess!")
