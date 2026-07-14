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

def calculate_average_rmsd(folder_path):
    
    all_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    results = {}

    for file_name in all_files:
        file_path = os.path.join(folder_path, file_name)
        try:
            df = pd.read_csv(file_path, index_col=0)
            df = df.replace('', np.nan).astype(float) # Replace empty values ​​with NaN and convert to float type
            matrix = df.values
            index_names = df.index.tolist()
            column_names = df.columns.tolist()
            n = len(index_names)

            ww_values = []
            wm_values = []
            mm_values = []
            total_values = []

            for i in range(n):
                for j in range(n):
                    if i != j and not np.isnan(matrix[i, j]): # Ignoring the original diameter and NaN values
                        name1 = index_names[i]
                        name2 = column_names[j]
                        value = matrix[i, j]
                        total_values.append(value)

                        if name1.startswith('W') and name2.startswith('W'):
                            ww_values.append(value)
                        elif (name1.startswith('W') and name2.startswith('M')) or \
                             (name1.startswith('M') and name2.startswith('W')):
                            wm_values.append(value)
                        elif name1.startswith('M') and name2.startswith('M'):
                            mm_values.append(value)

            results[file_name] = {
                'W-W_Ave': np.mean(ww_values) if ww_values else np.nan,
                'W-M_Ave': np.mean(wm_values) if wm_values else np.nan,
                'M-M_Ave': np.mean(mm_values) if mm_values else np.nan,
                'Total_Ave': np.mean(total_values) if total_values else np.nan,
                'W-W_Min': np.min(ww_values) if ww_values else np.nan,
                'W-M_Min': np.min(wm_values) if wm_values else np.nan,
                'M-M_Min': np.min(mm_values) if mm_values else np.nan,
                'Total_Min': np.min(total_values) if total_values else np.nan
            }
        except Exception as e:
            print(f"Error reading or processing file {file_name}: {e}")
            results[file_name] = {
                'W-W_Ave': np.nan,
                'W-M_Ave': np.nan,
                'M-M_Ave': np.nan,
                'Total_Ave': np.nan,
                'W-W_Min': np.nan,
                'W-M_Min': np.nan,
                'M-M_Min': np.nan,
                'Total_Min': np.nan
            }



    results_df = pd.DataFrame.from_dict(results, orient='index')
    results_df.index = [os.path.splitext(idx)[0] for idx in results_df.index]
    results_df.index.name = 'File Name'
    
    diff_values_Ave = []
    for index in results_df.index:
        ww = results_df.loc[index, 'W-W_Ave']
        wm = results_df.loc[index, 'W-M_Ave']
        if pd.notna(ww) and pd.notna(wm):
            diff = wm - ww
            diff_values_Ave.append(diff)
        else:
            diff_values_Ave.append(np.nan)

    results_df['W-W and M-W Difference_Ave'] = diff_values_Ave

    results_df = results_df[['W-W_Ave', 'W-M_Ave', 'M-M_Ave', 'W-W and M-W Difference_Ave', 'Total_Ave', 'W-W_Min', 'W-M_Min', 'M-M_Min', 'Total_Min']] # تغییر ترتیب ستون ها


    #results_df = results_df.transpose() # add # to this line for rotate the matrix
    results_df.index.name = ''
    results_df = results_df.rename(index={0: 'W-W_Ave', 1: 'W-M_Ave', 2: 'M-M_Ave', 3: 'Total_Ave', 4: 'W-W_Min', 5: 'W-M_Min', 6: 'M-M_Min', 7: 'Total_Min'})

    return results_df

# Setting
folder_path_config = r"C:\Users\keyva\Desktop\Codes" # Codes Folder System Path
config_file = os.path.join(folder_path_config, 'Parameters.config')

input_path = read_parameter_from_config(config_file, 'RMSD_Matrix_Average_Calculator', 'input_folder')

output_path = read_parameter_from_config(config_file, 'RMSD_Matrix_Average_Calculator', 'output_folder')
if not os.path.exists(output_path):
    os.makedirs(output_path)

output_dir1 = os.path.join(output_path, "Avarage RMSD Matrices Output")  
if not os.path.exists(output_dir1):
    os.makedirs(output_dir1)

average_rmsd_df = calculate_average_rmsd(input_path)

output_file_name = read_parameter_from_config(config_file, 'RMSD_Matrix_Average_Calculator', 'output_file_name')

output_file = os.path.join(output_dir1, f'{output_file_name}.csv')
average_rmsd_df.to_csv(output_file)

print(f"Sucsess! RMSD_Averages_Calculated and saved in'{output_file}'")