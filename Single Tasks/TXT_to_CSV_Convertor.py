import pandas as pd
import os
import configparser

def read_parameter_from_config(config_file, Section, parameter):
    
    config = configparser.ConfigParser()
    config.read(config_file)
    if Section in config and parameter in config[Section]:
        return config[Section][parameter]
    else:
        return None


def convert_txt_to_csv(input_folder, output_folder, new_column_names):

    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_filepath = os.path.join(input_folder, filename)
            output_filepath = os.path.join(output_folder, filename.replace('.txt', '.csv'))

            df = pd.read_csv(input_filepath, sep='\s+')

            df = df.iloc[:, [1, 4]]

            df.columns = new_column_names

            df.to_csv(output_filepath, index=False)



# Setting
folder_path_config = r"C:\Users\keyva\Desktop\Codes" # Codes Folder System Path
config_file = os.path.join(folder_path_config, 'Parameters.config')

input_folder = read_parameter_from_config(config_file, 'TXT_to_CSV_Convertor', 'input_folder')
output_folder = read_parameter_from_config(config_file, 'TXT_to_CSV_Convertor', 'output_folder')
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
new_column_names = ['FREQ(CM**-1)', 'IR INTENS.']

convert_txt_to_csv(input_folder, output_folder, new_column_names)

print("TXT to CSV Converted, Sucsess!")