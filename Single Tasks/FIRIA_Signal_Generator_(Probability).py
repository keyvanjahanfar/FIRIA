import numpy as np
import matplotlib.pyplot as plt
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


# Setting
folder_path_config = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(folder_path_config)
config_file = os.path.join(folder_path_config, 'Parameters.config')

input_path = read_parameter_from_config(config_file, 'FIRIA_Signal_Generator_(Probability)', 'input_folder')

output_path = read_parameter_from_config(config_file, 'FIRIA_Signal_Generator_(Probability)', 'output_folder')
if not os.path.exists(output_path):
    os.makedirs(output_path)


gaussian_width = read_parameter_from_config(config_file, 'FIRIA_Signal_Generator_(Probability)', 'gaussian_width')
stddev = float(gaussian_width)

Lower_limit_of_frequency_range_in_per_cm = float(read_parameter_from_config(config_file, 'FIRIA_Signal_Generator_(Probability)', 'Lower_limit_of_frequency_range_in_per_cm'))
Upper_limit_of_frequency_range_in_per_cm = float(read_parameter_from_config(config_file, 'FIRIA_Signal_Generator_(Probability)', 'Upper_limit_of_frequency_range_in_per_cm'))

x_range = (Lower_limit_of_frequency_range_in_per_cm, Upper_limit_of_frequency_range_in_per_cm)
x_min = x_range[0]
x_max = x_range[1]

num_points = (x_range[1] - x_range[0])*5 / stddev + 1
#num_points = 1000
num_points = int(num_points)
filenames = [f for f in os.listdir(input_path) if f.endswith('.csv')]


for filename in filenames:

    data = pd.read_csv(os.path.join(input_path, filename))

    means = data['FREQ(CM**-1)'].to_numpy()

    heights = data['IR INTENS.'].to_numpy()

    #heights = data['RAMAN ACT.'].to_numpy()

    colors = ['gray'] * len(means) + ['blue']
    
    fig, ax = plt.subplots(figsize=(100, 30))

    total_y = np.zeros_like(np.linspace(*x_range, num_points))

    for i in range(len(means)):
        
        mean = means[i]
        height = heights[i]
        color = colors[i]
        
        x = np.linspace(*x_range, num_points)

      
        def gaussian_pdf(x, mean, height):
            return (1 / (height * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / height)**2)

        y = height * gaussian_pdf(x, mean, stddev)
        
        plt.plot(x, y, label=f'Gaussian {i+1}', color=color)
        total_y += y

    
    x_total = ax.get_lines()[len(ax.get_lines()) - 1].get_xdata()
    y_1total = total_y

    data = pd.DataFrame({'x': x_total, 'y': y_1total})

    output_dir2 = os.path.join(output_path, "FIRIA Signal Generator Output")  
    if not os.path.exists(output_dir2):
        os.makedirs(output_dir2)

    output_dir1 = os.path.join(output_dir2, f"{stddev} SD")  
    if not os.path.exists(output_dir1):
        os.makedirs(output_dir1)
    
    output_dir = os.path.join(output_dir1, os.path.splitext(filename)[0])  
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    name, ext = os.path.splitext(filename)
    
    data.to_csv(os.path.join(output_dir, f"{name}.csv"), index=False)

    plt.plot(x, total_y, label='Total', color='blue', linewidth=0.5)
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Sum of Gaussian Distributions')
    
    #plt.legend()
    #plt.show()
    
    plt.savefig(os.path.join(output_dir, f"{name}.png"))
    plt.close()  

print("FIRIA Signal Generated, Sucsess!")
