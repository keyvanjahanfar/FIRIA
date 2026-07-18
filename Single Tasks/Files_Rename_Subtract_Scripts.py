import os
import configparser

def read_parameter_from_config(config_file, Section, parameter):
    
    config = configparser.ConfigParser()
    config.read(config_file)
    if Section in config and parameter in config[Section]:
        return config[Section][parameter]
    else:
        return None


def remove_scripts(folder_path):


    for filename in os.listdir(folder_path):
        if os.path.splitext(filename)[1] in extension:
            file_path = os.path.join(folder_path, filename)
            
            # Separate the file name from the extension
            name, ext = os.path.splitext(filename)
            
            # Remove the last n characters from the file name.
            new_name = name[:-scripts_number_to_remove]
            new_filename = new_name + ext
            new_file_path = os.path.join(folder_path, new_filename)
            
            os.rename(file_path, new_file_path)


# Setting
folder_path_config = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(folder_path_config)
config_file = os.path.join(folder_path_config, 'Parameters.config')

folder_path = read_parameter_from_config(config_file, 'Files_Rename_Subtract_Scripts', 'folder')

extension_format = read_parameter_from_config(config_file, 'Files_Rename_Subtract_Scripts', 'extention')
extension = [f'.{extension_format}']
scripts_number_to_remove = int (read_parameter_from_config(config_file, 'Files_Rename_Subtract_Scripts', 'scripts_number_to_remove'))

remove_scripts(folder_path)

print("subtract Rename , Sucsess!")
