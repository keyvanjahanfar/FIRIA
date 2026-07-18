import os
import pandas as pd
import numpy as np
import configparser

def read_parameter_from_config(config_file, Section, parameter):
    
    config = configparser.ConfigParser()
    config.read(config_file)
    if Section in config and parameter in config[Section]:
        return config[Section][parameter]
    else:
        return None

def calculate_rmsd(file1, file2, a, b, c):
    """
    calculate RMSD between 2 files
    """
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Add 0 to Y values ​​if there where no 0 in Y Values
    if 0 not in df1['y'].values:
        df1 = df1._append({'y': 0}, ignore_index=True)
    if 0 not in df2['y'].values:
        df2 = df2._append({'y': 0}, ignore_index=True)

    # Column Y normalization
    min_y1 = df1['y'].min()
    max_y1 = df1['y'].max()
    min_y2 = df2['y'].min()
    max_y2 = df2['y'].max()

    df1['Y_normalized'] = (df1['y'] - min_y1) / (max_y1 - min_y1) * (b - a) + a
    df2['Y_normalized'] = (df2['y'] - min_y2) / (max_y2 - min_y2) * (b - a) + a

    # Filter rows based on C value
    merged_df = pd.merge(df1, df2, on='x', suffixes=('_1', '_2'), how='outer')
    merged_df.fillna(0, inplace=True)
    filtered_df = merged_df[(merged_df['Y_normalized_1'] > c) | (merged_df['Y_normalized_2'] > c)]

    # RMSD Calculation
    if len(filtered_df) > 0:
        rmsd = np.sqrt(np.mean((filtered_df['Y_normalized_1'] - filtered_df['Y_normalized_2'])**2))
    else:
        rmsd = float('nan')

    return rmsd

def calculate_rmsd_matrix(folder_path, a, b, c):
    """
    make RMSD Matrix
    """
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    n = len(files)
    file_names_without_ext = [os.path.splitext(f)[0] for f in files]
    rmsd_matrix = pd.DataFrame(index=file_names_without_ext, columns=file_names_without_ext)

    for i in range(n):
        for j in range(n):
            file1 = os.path.join(folder_path, files[i])
            file2 = os.path.join(folder_path, files[j])
            rmsd_value = calculate_rmsd(file1, file2, a, b, c)
            if i == j:
                rmsd_matrix.loc[file_names_without_ext[i], file_names_without_ext[j]] = ''
            else:
                rmsd_matrix.loc[file_names_without_ext[i], file_names_without_ext[j]] = rmsd_value

    return rmsd_matrix

# Setting
folder_path_config = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(folder_path_config)
config_file = os.path.join(folder_path_config, 'Parameters.config')


input_folder = read_parameter_from_config(config_file, 'Normalized_Intensity_RMSD_Matrix_Generator', 'input_folder')  # Path to the folder containing the CSV files

Lower_Normal_Range = float(read_parameter_from_config(config_file, 'Normalized_Intensity_RMSD_Matrix_Generator', 'lower_normal_range')) # Minimum value for normalization

Upper_Normal_Range = float(read_parameter_from_config(config_file, 'Normalized_Intensity_RMSD_Matrix_Generator', 'upper_normal_range')) # Maximum value for normalization

Threshold = float(read_parameter_from_config(config_file, 'Normalized_Intensity_RMSD_Matrix_Generator', 'threshold'))

if Threshold is not None:
    
    rmsd_matrix = calculate_rmsd_matrix(input_folder, Lower_Normal_Range, Upper_Normal_Range, Threshold)
    
    output_Path = (read_parameter_from_config(config_file, 'Normalized_Intensity_RMSD_Matrix_Generator', 'output_folder'))
    if not os.path.exists(output_Path):
        os.makedirs(output_Path)

    output_dir1 = os.path.join(output_Path, "Normalized_Intensity_RMSD_Matrix_Output")  
    if not os.path.exists(output_dir1):
        os.makedirs(output_dir1)

    rmsd_matrix.to_csv(os.path.join(output_dir1, f'{Threshold} T.csv'), index=True)

    print("Sucsess! Normalized Intensity RMSD Matrix generated")
else:
    print("Error")
