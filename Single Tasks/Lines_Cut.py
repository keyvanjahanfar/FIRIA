import os
import configparser

def read_parameter_from_config(config_file, Section, parameter):
    
    config = configparser.ConfigParser()
    config.read(config_file)
    if Section in config and parameter in config[Section]:
        return config[Section][parameter]
    else:
        return None


def extract_lines_between_markers(file_path, marker1, marker2):

    with open(file_path, 'r') as f:
        lines = f.readlines()

    start_index = -1
    end_index = -1
    for i, line in enumerate(lines):
        if marker1 in line:
            start_index = i
        if marker2 in line:
            end_index = i
            break

    if start_index != -1 and end_index != -1:
        extracted_lines = lines[start_index:end_index-2]
        return extracted_lines
    else:
        return []


# Setting
folder_path_config = r"C:\Users\keyva\Desktop\Codes" # Codes Folder System Path
config_file = os.path.join(folder_path_config, 'Parameters.config')

input_folder = read_parameter_from_config(config_file, 'Lines_Cut', 'input_folder')

output_folder = read_parameter_from_config(config_file, 'Lines_Cut', 'output_folder')
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

start_marker = read_parameter_from_config(config_file, 'Lines_Cut', 'start_marker')
end_marker = read_parameter_from_config(config_file, 'Lines_Cut', 'end_marker')
input_files_extention = f".{read_parameter_from_config(config_file, 'Lines_Cut', 'input_files_extention')}"
output_files_extention = f".{read_parameter_from_config(config_file, 'Lines_Cut', 'output_files_extention')}"

for filename in os.listdir(input_folder):
    if filename.endswith(input_files_extention):
        file_path = os.path.join(input_folder, filename)
        extracted_lines = extract_lines_between_markers(file_path, start_marker, end_marker)
        if extracted_lines:
            output_file = os.path.join(output_folder, filename.replace(input_files_extention, output_files_extention))
            with open(output_file, 'w') as f:
                f.writelines(extracted_lines)

print("Lines Cutted, Sucsess!")