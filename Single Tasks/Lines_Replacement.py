import os
import configparser

def read_parameter_from_config(config_file, Section, parameter):
    
    config = configparser.ConfigParser()
    config.read(config_file)
    if Section in config and parameter in config[Section]:
        return config[Section][parameter]
    else:
        return None

def replace_first_lines(file_path, new_lines):

    with open(file_path, 'r') as f:
        lines = f.readlines()

    lines[:len(new_lines)] = new_lines

    with open(file_path, 'w') as f:
        f.writelines(lines)


# Setting
folder_path_config = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(folder_path_config)
config_file = os.path.join(folder_path_config, 'Parameters.config')

folder_path = read_parameter_from_config(config_file, 'Lines_Replacement', 'folder')
files_extention = f".{read_parameter_from_config(config_file, 'Lines_Replacement', 'files_extention')}"

new_lines = ["first line\n", "second line\n", "third line\n"]

for filename in os.listdir(folder_path):
    if filename.endswith(files_extention):
        file_path = os.path.join(folder_path, filename)
        replace_first_lines(file_path, new_lines)

print("Lines Replaced, Sucsess!")
