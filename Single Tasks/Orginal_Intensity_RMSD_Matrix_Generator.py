import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import configparser

def read_parameter_from_config(config_file, Section, parameter):
    
    config = configparser.ConfigParser()
    config.read(config_file)
    if Section in config and parameter in config[Section]:
        return config[Section][parameter]
    else:
        return None

def modify_csv_and_empty_diagonal(file_path):
    """
    Opens a CSV file, removes the last four characters from the first row (header)
    and the first column (index), empties the diagonal elements (sets them to NaN),
    and saves the modified DataFrame back to the same file.

    Args:
        file_path (str): The path to the CSV file.
    """
    try:
        # Read the CSV file, assuming the first row is the header and the first column is the index
        df = pd.read_csv(file_path, index_col=0)

        # Modify column names (header)
        new_columns = []
        for col in df.columns:
            if isinstance(col, str) and len(col) >= 4:
                new_columns.append(col[:-4])
            else:
                new_columns.append(col)
        df.columns = new_columns

        # Modify index names (first column)
        new_index = []
        for idx in df.index:
            if isinstance(idx, str) and len(idx) >= 4:
                new_index.append(idx[:-4])
            else:
                new_index.append(idx)
        df.index = new_index

        # Empty the diagonal elements
        min_len = min(df.shape[0], df.shape[1])
        for i in range(min_len):
            if df.index[i] in df.columns:
                df.loc[df.index[i], df.columns[i]] = np.nan

        # Save the modified DataFrame back to the same CSV file
        df.to_csv(file_path)

    except FileNotFoundError:
        print(f"Error: CSV file not found at {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Setting
folder_path_config = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(folder_path_config)
config_file = os.path.join(folder_path_config, 'Parameters.config')

input_path = read_parameter_from_config(config_file, 'Orginal_Intensity_RMSD_Matrix_Generator', 'input_folder')

filenames = [f for f in os.listdir(input_path) if f.endswith('.csv')]

rmsd_matrix = np.zeros((len(filenames), len(filenames)))

filename_to_index = {f: i for i, f in enumerate(filenames)}

for i in range(len(filenames)):
    for j in range(i + 1, len(filenames)):
        file1 = os.path.join(input_path, filenames[i])
        file2 = os.path.join(input_path, filenames[j])

        data1 = pd.read_csv(file1)
        data2 = pd.read_csv(file2)

        x1 = data1['x']
        y1 = data1['y']

        x2 = data2['x']
        y2 = data2['y']

        diff_y = y2 - y1

        rmsd = np.sqrt(np.mean(diff_y**2))

        rmsd_matrix[filename_to_index[filenames[i]], filename_to_index[filenames[j]]] = rmsd
        rmsd_matrix[filename_to_index[filenames[j]], filename_to_index[filenames[i]]] = rmsd  

rmsd_df = pd.DataFrame(rmsd_matrix, index=filenames, columns=filenames)

rmsd_df.index.name = 'Row'
rmsd_df.columns.name = 'Column'

output_Path = read_parameter_from_config(config_file, 'Orginal_Intensity_RMSD_Matrix_Generator', 'output_folder')
if not os.path.exists(output_Path):
    os.makedirs(output_Path)

output_dir1 = os.path.join(output_Path, "Orginal Intensity RMSD Matrix Output")  
if not os.path.exists(output_dir1):
    os.makedirs(output_dir1)

rmsd_df.to_csv(os.path.join(output_dir1, 'Orginal_Intensity_RMSD_Matrix.csv'), index=True)

modify_csv_and_empty_diagonal(os.path.join(output_dir1, 'Orginal_Intensity_RMSD_Matrix.csv'))

print("Orginal Intensity RMSD Matrix Generated, Sucsess!")
