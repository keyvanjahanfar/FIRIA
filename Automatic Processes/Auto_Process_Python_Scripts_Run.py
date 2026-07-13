import os
import subprocess


def run_script(script_path):
    """
    Run a Python Script

    Args:
        script_path (str): Python Script System Path
    """
    try:
        print(f"Running script: {script_path}")
        subprocess.run(['python', script_path], check=True)
        print(f"script '{script_path}' execution completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error For Running '{script_path}': {e}")
    except FileNotFoundError:
        print(f"Script '{script_path}' Not Found")

scripts_to_execute = [
    r"C:\Users\keyva\Desktop\Codes\Automatic_Run_1.py",
    r"C:\Users\keyva\Desktop\Codes\Treshold Finder.py",

    # More Scripts Can Add to this List
]

for script_path in scripts_to_execute:
    run_script(script_path)

print("Sucsess!")