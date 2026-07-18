import os
import configparser
import subprocess
import numpy
import sys

def update_config(config_file, section, parameter, value):
    """
    Update the value of a specific parameter in the configuration file.

    Args:
        config_file (str): configuration file System Path
        section (str): Parameter section Name
        parameter (str): Parameter Name
        value (str): Parameter New Value
    """
    config = configparser.ConfigParser()
    config.read(config_file)
    if section in config:
        config[section][parameter] = value
        with open(config_file, 'w') as configfile:
            config.write(configfile)
    else:
        print(f"section '{section}' did not found in config file.")

def run_script(script_path):
    """
    Run a Python script.

    Args:
        script_path (str): Python script System path
    """
    try:
        print(f"Running script: {script_path}")
        subprocess.run([sys.executable, script_path], check=True, cwd=folder_path_config)
        print(f"script '{script_path}' execution completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error For Running '{script_path}': {e}")
    except FileNotFoundError:
        print(f"Script '{script_path}' Not Found")

def run_scripts_for_multiple_parameters(config_file, multiple_parameters, scripts_to_run):
    """
    Perform parameter value changes and execute scripts in a loop.

    Args:
        config_file (str): Config File System Path
        multiple_parameters (dict): The dictionary contains the section name, the parameter name, and a list of values ​​to change.
                                 Example : {'section1': {'param_a': [1, 2, 3], 'param_b': [0.1, 0.2]}, ...}
        scripts_to_run (list): A list of Python script paths to run.
    """
    import itertools

    parameter_names = []
    parameter_values_lists = []
    for section, params in multiple_parameters.items():
        for param_name, values in params.items():
            parameter_names.append((section, param_name))
            parameter_values_lists.append(values)

    # Generate all possible combinations of parameter values
    all_combinations = itertools.product(*parameter_values_lists)

    print("Scripts Run For Parameters begins:")

    for combination in all_combinations:
        print("\n---")
        print("Set values For Parameters:")
        for i, (section, param_name) in enumerate(parameter_names):
            value = str(combination[i])
            update_config(config_file, section, param_name, value)
            print(f"  Section: [{section}], Parameter: {param_name} = {value}")

        print("\nScripts Run For Current Parameter Values:")
        for script_path in scripts_to_run:
            run_script(script_path)

        print("---")

    print("changing parameter values and executing scripts were complete.")

def read_parameter_from_config(config_file, Section, parameter):
    
    config = configparser.ConfigParser()
    config.read(config_file)
    if Section in config and parameter in config[Section]:
        return config[Section][parameter]
    else:
        return None

def write_parameter_to_config(config_file, Section, parameter, new_value):
    
    config = configparser.ConfigParser()
    config.read(config_file)

    if Section in config and parameter in config[Section]:
        config[Section][parameter] = new_value
        try:
            with open(config_file, 'w') as configfile:
                config.write(configfile)
            return True  # To indicate Sucsess in writing Process
        except IOError:
            print(f"eror in modify the file {config_file}")
            return False # To indicate an error in writing Process
    else:
        print(f"section '{Section}' with '{parameter}' did not found in config file.")
        return False # To indicate that a section or parameter was not found.

def execute_python_script(script_path):
    """
    Executes a Python script given its file path as the sole argument.

    Args:
        script_path (str): The full or relative path to the Python script file.

    Returns:
        tuple: A tuple containing the return code (int) and the output (str) of the script.
               Returns (None, None) if an error occurs during execution.
    """
    try:
        process = subprocess.run(
            [sys.executable, script_path],
            cwd=folder_path_config,
            capture_output=True,
            text=True,
            check=False,
        )
        return process.returncode, process.stdout
    except FileNotFoundError:
        print(f"Error: Script not found at path: {script_path}")
        return None, None
    except Exception as e:
        print(f"An error occurred during execution: {e}")
        return None, None

# Settings
folder_path_config = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(folder_path_config)
config_file = os.path.join(folder_path_config, 'Parameters.config')

#for Gaussian_Width in [0.1, 0.3, 1, 3, 10, 30, 100] :
for Gaussian_Width in [30, 100] :

    # Part 1 : File_Extraction

    confing_input_Path = read_parameter_from_config(config_file, 'Auto_Process_Treshold_Finder', 'input_folder')
    input_Path2 = os.path.join(confing_input_Path, f"{Gaussian_Width} SD") 
    write_parameter_to_config(config_file, 'File_Extraction', 'source_folder', input_Path2)

    config_output_path = read_parameter_from_config(config_file, 'Auto_Process_Treshold_Finder', 'output_folder')
    output_path2 = os.path.join(config_output_path, "tmp", "Normal_RMSD_Matrix_Generator_Input")
    write_parameter_to_config(config_file, 'File_Extraction', 'output_folder', output_path2)

    write_parameter_to_config(config_file, 'File_Extraction', 'extention', 'csv')

    execute_python_script(os.path.join(folder_path_config, "Single Tasks", "File_Extraction.py"))

    # Part 2 : Build Normal RMSD Matrix for Tresholds

    write_parameter_to_config(config_file, 'Normalized_Intensity_RMSD_Matrix_Generator', 'input_folder', output_path2)

    output_path3 = os.path.join(config_output_path, r"tmp") 
    write_parameter_to_config(config_file, 'Normalized_Intensity_RMSD_Matrix_Generator', 'output_folder', output_path3)

    threshold_steps_interwall = float (read_parameter_from_config(config_file, 'Auto_Process_Treshold_Finder', 'threshold_steps_interwall'))

    upper_treshold_range = threshold_steps_interwall + float (read_parameter_from_config(config_file, 'Auto_Process_Treshold_Finder', 'upper_treshold_range'))

    lower_treshold_range = float (read_parameter_from_config(config_file, 'Auto_Process_Treshold_Finder', 'lower_treshold_range'))

    

    Threshold_Values = numpy.arange(lower_treshold_range, upper_treshold_range, threshold_steps_interwall).tolist()
    Threshold_Values = [round(x, 8) for x in Threshold_Values]

    multiple_parameters_1 = {
        'Normalized_Intensity_RMSD_Matrix_Generator': {
            #'threshold': [0.2, 0.4, 0.6],
            'Threshold': Threshold_Values

        },
    
    }

    scripts_to_execute_1 = [
        os.path.join(folder_path_config, "Single Tasks", "Normalized_Intensity_RMSD_Matrix_Generator.py"),
        # More scripts can be added to this list.
    ]

    run_scripts_for_multiple_parameters(config_file, multiple_parameters_1, scripts_to_execute_1)

    # Part 3 : Average_Calculator

    input_Path4 = os.path.join(output_path3, r"Normalized_Intensity_RMSD_Matrix_Output")
    write_parameter_to_config(config_file, 'RMSD_Matrix_Average_Calculator', 'input_folder', input_Path4)

    output_path4 = os.path.join(config_output_path) 
    write_parameter_to_config(config_file, 'RMSD_Matrix_Average_Calculator', 'output_folder', output_path4)

    file_name = f"{Gaussian_Width} SD"

    write_parameter_to_config(config_file, 'RMSD_Matrix_Average_Calculator', 'output_file_name', file_name)

    execute_python_script(os.path.join(folder_path_config, "Single Tasks", "RMSD_Matrix_Average_Calculator.py"))

    # Part 4 : cut RMSD Files from tmp to Main Result directory

    input_Path5 = os.path.join(config_output_path, "tmp", "Normalized_Intensity_RMSD_Matrix_Output")
    write_parameter_to_config(config_file, 'File_Extraction', 'source_folder', input_Path5)


    output_path5 = os.path.join(config_output_path, "Normal_RMSD_Matrices", f"{Gaussian_Width} SD")
    write_parameter_to_config(config_file, 'File_Extraction', 'output_folder', output_path5)

    write_parameter_to_config(config_file, 'File_Extraction', 'extention', 'csv')

    execute_python_script(os.path.join(folder_path_config, "Single Tasks", "File_Extraction.py"))

# Part 5 : Delet tmp contents
tmp_path = os.path.join(config_output_path, "tmp")
write_parameter_to_config(config_file, 'Delete_Contents', 'folder', tmp_path)

execute_python_script(os.path.join(folder_path_config, "Single Tasks", "Delete_Contents.py"))

# Part 6 : Run Threshold Finder
input_Path6 = os.path.join(config_output_path, "Avarage RMSD Matrices Output") 
write_parameter_to_config(config_file, 'Threshold_Finder', 'input_folder', input_Path6)

output_path6 = os.path.join(config_output_path)
write_parameter_to_config(config_file, 'Threshold_Finder', 'output_folder', output_path6)

for column in ["W-W_Ave", "W-M_Ave", "M-M_Ave", "Total_Ave", "W-W and M-W Difference_Ave", "W-W_Min", "W-M_Min", "M-M_Min", "Total_Min"] :

    write_parameter_to_config(config_file, 'Threshold_Finder', 'column_to_extract', column)
    execute_python_script(os.path.join(folder_path_config, "Single Tasks", "Threshold_Finder.py"))

print("Auto_Process for Threshold Finder Sucsess!")
