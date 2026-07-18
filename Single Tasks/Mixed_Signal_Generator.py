import pandas as pd
import os
import matplotlib.pyplot as plt
import re
import configparser
# Inupt file Name should have a float number (not integer) for example 5.0 and 0.8 but not 5

def read_parameter_from_config(config_file, Section, parameter):
    
    config = configparser.ConfigParser()
    config.read(config_file)
    if Section in config and parameter in config[Section]:
        return config[Section][parameter]
    else:
        return None

# Setting
folder_path_config = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(folder_path_config)
config_file = os.path.join(folder_path_config, 'Parameters.config')

input_folder = read_parameter_from_config(config_file, 'Mixed_Signal_Generator', 'input_folder')

output_folder2 = read_parameter_from_config(config_file, 'Mixed_Signal_Generator', 'output_folder')
if not os.path.exists(output_folder2):
    os.makedirs(output_folder2)

output_folder = os.path.join(output_folder2, "Mixed Signal Generator Output")  
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

all_files = [i for i in os.listdir(input_folder) if i.endswith('.csv')]

dfs = []

for file in all_files:

    factor = float(re.search(r'\d+\.\d+', file).group())
    df = pd.read_csv(os.path.join(input_folder, file))

    df['y'] *= factor
    dfs.append(df)

df_sum = pd.concat(dfs).groupby('x')['y'].sum().reset_index()

plt.figure(figsize=(10, 6))

for df in dfs:
    plt.plot(df['x'], df['y'], color='gray', alpha=0.5)

plt.plot(df_sum['x'], df_sum['y'], color='blue', label='Sum')

plt.title('Comparison of Intensity Values')
plt.xlabel('Frequency')
plt.ylabel('Intensity')
plt.legend()

plt.savefig(os.path.join(output_folder, "combined_plot.png"))

df_sum.to_csv(os.path.join(output_folder, "SUM_Results.csv"), index=False)
plt.close() 
print('Mixed Signal Generated, Sucsses!')
