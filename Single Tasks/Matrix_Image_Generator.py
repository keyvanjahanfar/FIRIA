import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.colors
import configparser

def read_parameter_from_config(config_file, section, parameter):
    config = configparser.ConfigParser()
    config.read(config_file)
    if section in config and parameter in config[section]:
        return config[section][parameter]
    return None

def get_color(val, min_val, max_val, cmap):
    """
    Takes a numeric value and returns a color from the color map based on that value.
    """
    if pd.isna(val):
        return 'lightgray'  # Color for empty values
    if max_val == min_val:
        norm = 0.5  # Prevent division by zero if all values ​​are the same
    else:
        norm = (val - min_val) / (max_val - min_val)
    return matplotlib.colors.to_hex(cmap(norm))

def process_csv_and_save_image(folder_path):
    """
    It processes all CSV files in a folder, colors each one independently based on their own values ​​and saves the result as a PNG file, adding the desired spacing.
    """
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            try:
                df = pd.read_csv(file_path, index_col=0)
                df_filtered = df.loc[[idx for idx in df.index if isinstance(idx, str) and (idx.startswith('W') or idx.startswith('M'))],
                                     [col for col in df.columns if isinstance(col, str) and (col.startswith('W') or col.startswith('M'))]].copy()
                numeric_df = df_filtered.apply(pd.to_numeric, errors='coerce')

                # Finding boundary indices to create spacing
                w_row_indices = [i for i, idx in enumerate(numeric_df.index) if idx.startswith('W')]
                m_row_indices = [i for i, idx in enumerate(numeric_df.index) if idx.startswith('M')]
                w_col_indices = [i for i, col in enumerate(numeric_df.columns) if col.startswith('W')]
                m_col_indices = [i for i, col in enumerate(numeric_df.columns) if col.startswith('M')]

                row_split_index = -1
                if w_row_indices and m_row_indices and max(w_row_indices) < min(m_row_indices):
                    row_split_index = max(w_row_indices)
                elif w_row_indices and m_row_indices and max(m_row_indices) < min(w_row_indices):
                    row_split_index = max(m_row_indices)

                col_split_index = -1
                if w_col_indices and m_col_indices and max(w_col_indices) < min(m_col_indices):
                    col_split_index = max(w_col_indices)
                elif w_col_indices and m_col_indices and max(m_col_indices) < min(w_col_indices):
                    col_split_index = max(m_col_indices)

                # Create a new data frame with empty rows and columns for spacing
                if row_split_index != -1:
                    top_part = numeric_df.iloc[:row_split_index + 1]
                    bottom_part = numeric_df.iloc[row_split_index + 1:]
                    empty_row = pd.Series([np.nan] * len(numeric_df.columns), index=numeric_df.columns)
                    numeric_df_with_space = pd.concat([top_part, pd.DataFrame(empty_row).T, bottom_part])
                else:
                    numeric_df_with_space = numeric_df

                if col_split_index != -1:
                    left_part = numeric_df_with_space.iloc[:, :col_split_index + 1]
                    right_part = numeric_df_with_space.iloc[:, col_split_index + 1:]
                    empty_col = pd.Series([np.nan] * len(numeric_df_with_space.index))
                    numeric_df_with_space = pd.concat([left_part, pd.DataFrame(empty_col, columns=['']).T, right_part], axis=1)

                min_val = numeric_df_with_space.min().min()
                max_val = numeric_df_with_space.max().max()

                if pd.isna(min_val) or pd.isna(max_val):
                    print(f"No valid numeric data was found in the file {filename}.")
                    continue

                cmap = matplotlib.colors.LinearSegmentedColormap.from_list("rg", ["red", "yellow", "green"], N=256)

                fig, ax = plt.subplots(figsize=(12, 10))
                ax.axis('off')

                cell_colors = []
                cell_text = []
                row_labels = list(numeric_df_with_space.index)
                col_labels = list(numeric_df_with_space.columns)

                for i, row_label in enumerate(row_labels):
                    row_colors = []
                    row_values = []
                    for j, col_label in enumerate(col_labels):
                        value = numeric_df_with_space.at[row_label, col_label] if row_label in numeric_df_with_space.index and col_label in numeric_df_with_space.columns else np.nan
                        row_values.append(f"{value:.2f}" if pd.notna(value) else "")
                        row_colors.append(get_color(value, min_val, max_val, cmap))
                    cell_colors.append(row_colors)
                    cell_text.append(row_values)

                table = ax.table(cellText=cell_text,
                                 rowLabels=row_labels,
                                 colLabels=col_labels,
                                 cellColours=cell_colors,
                                 loc='center')
                table.auto_set_font_size(False)
                table.set_fontsize(8)
                table.scale(1, 1.2)

                plt.title(f"Colored matrix from {filename}")
                plt.tight_layout()
                output_path = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}_colored_spaced.png")
                plt.savefig(output_path)
                plt.close()
                print(f"The colored image for {filename} was saved with space in {output_path}.")

            except Exception as e:
                print(f"Error processing file {filename}: {e}")

if __name__ == "__main__":
    folder_path_config = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(folder_path_config)
    config_file = os.path.join(folder_path_config, "Parameters.config")
    folder_path = read_parameter_from_config(config_file, "Matrix_Image_Generator", "input_folder")
    process_csv_and_save_image(folder_path)
    print("Processing of all files has finished.")
