import os
import configparser

def read_parameter_from_config(config_file, Section, parameter):
    
    config = configparser.ConfigParser()
    config.read(config_file)
    if Section in config and parameter in config[Section]:
        return config[Section][parameter]
    else:
        return None

def rename_files(folder_path, new_prefix):

    for filename in os.listdir(folder_path):
        if filename.endswith(f".{extention}"):
            file_path = os.path.join(folder_path, filename)
            name, ext = os.path.splitext(filename)
            new_filename = name + new_prefix + ext
            new_file_path = os.path.join(folder_path, new_filename)
            
            os.rename(file_path, new_file_path)

# Setting
folder_path_config = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(folder_path_config)
config_file = os.path.join(folder_path_config, 'Parameters.config')

folder_path = read_parameter_from_config(config_file, 'Files_Rename_add_Scripts', 'folder')
extention = read_parameter_from_config(config_file, 'Files_Rename_add_Scripts', 'extention')
new_prefix = read_parameter_from_config(config_file, 'Files_Rename_add_Scripts', 'scripts')
rename_files(folder_path, new_prefix)
print("Files Rename Sucsess!")
