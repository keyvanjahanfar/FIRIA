import os
import shutil
import configparser

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
            return True
        except IOError:
            print(f"fail to save parameter in : {config_file}")
            return False
    else:
        print(f"section '{Section}' or parameter '{parameter}'didnot find in Config file")
        return False


# Setting
folder_path_config = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(folder_path_config)
config_file = os.path.join(folder_path_config, 'Parameters.config')


source_dir = read_parameter_from_config(config_file, 'File_Extraction', 'source_folder')

output_dir = read_parameter_from_config(config_file, 'File_Extraction', 'output_folder')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
extention_format = read_parameter_from_config(config_file, 'File_Extraction', 'extention')
extensions = [f'.{extention_format}']

for root, _, files in os.walk(source_dir):
    for filename in files:
        if os.path.splitext(filename)[1] in extensions:
            
            dst_file = os.path.join(output_dir, filename)

            shutil.copyfile(os.path.join(root, filename), dst_file)

            print(f'Copied {filename} to {dst_file}')

print("File Extraction Sucsess!")
