import os
import pandas as pd
import re
import configparser

def read_parameter_from_config(config_file, Section, parameter):
    
    config = configparser.ConfigParser()
    config.read(config_file)
    if Section in config and parameter in config[Section]:
        return config[Section][parameter]
    else:
        return None

def get_numeric_part(s):
    """Extract the first decimal number from a string."""
    match = re.search(r'(\d+\.\d+|\d+)', s)
    if match:
        return float(match.group(1))
    else:
        return float('inf') # For cases that do not have decimal numbers, we consider Integer value.

def combine_x_column(folder_path, output_filename, column_name='x'):
    """
    Combine column 'x' from multiple CSV files into a new CSV file and sort by title.
    """
    all_data = {}
    row_names = None
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    if not files:
        print(f"No CSV files were found in folder '{folder_path}'.")
        return

    for file in files:
        file_path = os.path.join(folder_path, file)
        try:
            df = pd.read_csv(file_path, index_col=0)
            if row_names is None:
                row_names = df.index.tolist()
            elif df.index.tolist() != row_names:
                print(f"The file '{file}' has different row names and will not be included in the combination.")
                continue

            if column_name in df.columns:
                file_name_without_ext = os.path.splitext(file)[0]
                all_data[file_name_without_ext] = df[column_name]
            else:
                print(f"Column '{column_name}' not found in file '{file}'.")
        except FileNotFoundError:
            print(f"File '{file}' not found.")
        except Exception as e:
            print(f"Error reading file '{file}': {e}")

    if all_data:
        final_df = pd.DataFrame(all_data)

        # Sort columns by decimal number in title
        sorted_columns = sorted(final_df.columns, key=get_numeric_part)
        final_df = final_df[sorted_columns]

        # Sort rows by decimal number in title
        sorted_index = sorted(final_df.index, key=get_numeric_part)
        final_df = final_df.reindex(sorted_index)

        #final_df = final_df.transpose() # add # to rotate Matrix

        output_path = os.path.join(output_folder, 'Thresholds comparison')
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        final_df.to_csv(os.path.join(output_path, output_filename))
        print(f"'{output_filename}' With Sucsses saved in '{folder_path}'")
    else:
        print("No data for combination found!")

# Setting
folder_path_config = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(folder_path_config)
config_file = os.path.join(folder_path_config, 'Parameters.config')

input_folder = read_parameter_from_config(config_file, 'Threshold_Finder', 'input_folder')
output_folder = read_parameter_from_config(config_file, 'Threshold_Finder', 'output_folder')


column_to_extract = read_parameter_from_config(config_file, 'Threshold_Finder', 'column_to_extract')

output_filename = f'Final Result - {column_to_extract}.csv'

combine_x_column(input_folder, output_filename, column_to_extract)

print("Threshold Finder Run Sucsess!")
