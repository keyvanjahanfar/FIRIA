import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import random
import subprocess
import configparser
import platform
import sys

class StatisticalSoftwareGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FIRIA Signal Modeling and Statistical Analysis Software (FIRIA-SMSA)")
        # Locate the project root from this file so the project can be moved
        # to any folder without editing a system-specific path.
        self.source_path = os.path.dirname(os.path.abspath(__file__))
        self.selected_category = tk.StringVar(root)
        self.selected_category.set("please choose")
        self.selected_task = tk.StringVar(root)
        self.selected_task.set("please choose Your Task")
        self.parameter_entries = {}
        self.changed_parameters = {}

        self.load_background()
        self.set_initial_size()
        self.create_widgets()

    def load_background(self):
        background_folder = os.path.join(self.source_path, "Background")
        try:
            background_files = [f for f in os.listdir(background_folder) if f.endswith(".png")]
            if background_files:
                random_background = random.choice(background_files)
                self.bg_image_path = os.path.join(background_folder, random_background)
            else:
                self.bg_image_path = None
        except FileNotFoundError:
            self.bg_image_path = None

        if self.bg_image_path:
            self.bg_image = Image.open(self.bg_image_path)
            self.bg_photo = None # Will be updated in resize event
            self.root.bind("<Configure>", self.resize_background)

    def set_initial_size(self):
        if self.bg_image:
            aspect_ratio = self.bg_image.width / self.bg_image.height
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            initial_width = int(screen_height * aspect_ratio * 0.7) # windows width size is 70% of screen height
            initial_height = int(screen_height * 0.7) # windows height size is 70% of screen height
            self.root.geometry(f"{initial_width}x{initial_height}")
        else:
            self.root.geometry("800x600") # Default size if no background

    def resize_background(self, event):
        if self.bg_image:
            width = event.width
            height = event.height
            resized_image = self.bg_image.resize((width, height), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized_image)
            self.background_label.config(image=self.bg_photo)
            self.background_label.place(relwidth=1, relheight=1)

    def create_widgets(self):
        self.background_label = tk.Label(self.root)
        self.background_label.place(relwidth=1, relheight=1)
        self.load_background() # Initial load

        # Category selection
        self.category_selection = ttk.Combobox(self.root, textvariable=self.selected_category, state="readonly", width=20)
        self.category_selection['values'] = ["please choose", "Automatic Processes", "Single Tasks", "Documents", "Settings"]
        self.category_selection.place(x=10, y=10)
        self.category_selection.bind("<<ComboboxSelected>>", self.show_secondary_options)

        # Placeholder for secondary task selection
        self.task_selection = None
        self.task_selection_label = None

        # Placeholder for parameter frame
        self.parameter_frame = None
        self.instruction_label = None

        # Placeholder for document/settings buttons
        self.document_buttons_frame = None
        self.settings_buttons_frame = None

        # Frame for Run, Save Parameters buttons and Terminal output
        self.bottom_frame = tk.Frame(self.root)
        self.terminal_output = tk.Text(self.bottom_frame, height=6, width=60)
        self.save_button = tk.Button(self.bottom_frame, text="Save Parameters", command=self.save_parameters)
        self.run_button = tk.Button(self.bottom_frame, text="Run", command=self.run_script)

    def show_secondary_options(self, event):
        selected_category = self.selected_category.get()

        # Destroy any existing secondary widgets
        if self.task_selection:
            self.task_selection.destroy()
            self.task_selection = None
        if self.parameter_frame:
            self.parameter_frame.destroy()
            self.parameter_frame = None
        if self.instruction_label:
            self.instruction_label.destroy()
            self.instruction_label = None
        if self.document_buttons_frame:
            self.document_buttons_frame.destroy()
            self.document_buttons_frame = None
        if self.settings_buttons_frame:
            self.settings_buttons_frame.destroy()
            self.settings_buttons_frame = None
        self.run_button.pack_forget()
        self.save_button.pack_forget()
        self.terminal_output.pack_forget()
        self.bottom_frame.place_forget()

        if selected_category in ["Automatic Processes", "Single Tasks"]:
            self.task_selection = ttk.Combobox(self.root, textvariable=self.selected_task, state="readonly", width=45)
            self.task_selection.place(x=170, y=10) # Adjusted x position
            self.task_selection['values'] = ["please choose Your Task"] + self.get_scripts_in_folder(os.path.join(self.source_path, selected_category))
            self.selected_task.set("please choose Your Task")
            self.task_selection.bind("<<ComboboxSelected>>", self.load_parameters)
        elif selected_category == "Documents":
            self.create_document_buttons()
        elif selected_category == "Settings":
            self.create_settings_buttons()

    def get_scripts_in_folder(self, folder_path):
        try:
            return [f.replace(".py", "") for f in os.listdir(folder_path) if f.endswith(".py")]
        except FileNotFoundError:
            return []

    def load_parameters(self, event):
        selected_task = self.selected_task.get()
        selected_category = self.selected_category.get()

        if selected_task == "please choose Your Task":
            if self.parameter_frame:
                self.parameter_frame.destroy()
                self.parameter_frame = None
            if self.instruction_label:
                self.instruction_label.destroy()
                self.instruction_label = None
            self.run_button.pack_forget()
            self.save_button.pack_forget()
            self.terminal_output.pack_forget()
            self.bottom_frame.place_forget()
            return

        config_file_path = os.path.join(self.source_path, "Parameters.config")
        config = configparser.ConfigParser()
        config.read(config_file_path)

        # Destroy any existing parameter widgets and instruction label
        if self.parameter_frame:
            self.parameter_frame.destroy()
            self.parameter_frame = None
        if self.instruction_label:
            self.instruction_label.destroy()
            self.instruction_label = None
        self.parameter_entries = {}
        self.changed_parameters = {}

        if selected_task in config:
            self.instruction_label = tk.Label(self.root, text=config[selected_task].get("instruction", ""), wraplength=400, justify='left')
            self.instruction_label.place(x=10, y=self.category_selection.winfo_y() + self.category_selection.winfo_height() + 10, anchor="nw")
            instruction_height = self.instruction_label.winfo_reqheight() + 10

            self.parameter_frame = tk.Frame(self.root)
            self.parameter_frame.place(x=10, y=self.category_selection.winfo_y() + self.category_selection.winfo_height() + instruction_height + 10, anchor="nw")
            row = 0
            for param_name, param_value in config[selected_task].items():
                if param_name == "instruction":
                    continue
                tk.Label(self.parameter_frame, text=param_name).grid(row=row, column=0, padx=5, pady=5, sticky="w")
                entry = tk.Entry(self.parameter_frame, width=30)
                entry.insert(0, param_value)
                entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
                entry.bind("<FocusOut>", lambda event, name=param_name, entry_widget=entry: self.check_parameter_change(name, entry_widget))
                self.parameter_entries[param_name] = entry

                if "\\" in param_value or "/" in param_value:
                    browse_button = tk.Button(self.parameter_frame, text="Browse", command=lambda p_name=param_name, entry_widget=entry: self.browse_folder(p_name, entry_widget))
                    browse_button.grid(row=row, column=2, padx=5, pady=5, sticky="e")

                changed_label = tk.Label(self.parameter_frame, text="", fg="red", name=f"{param_name}_changed")
                changed_label.grid(row=row, column=3, padx=5, pady=5, sticky="w")
                row += 1

            # Place bottom frame
            self.bottom_frame.place(relx=0, rely=1, anchor="sw", relwidth=1, height=150) # Fixed height

            # Layout widgets in the bottom frame
            self.run_button.pack(side="right", padx=10, pady=10, anchor="se")
            self.save_button.pack(side="right", padx=10, pady=10, anchor="se")
            self.terminal_output.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        else:
            # Clear parameter widgets if the selected task has no parameters
            if self.parameter_frame:
                self.parameter_frame.destroy()
                self.parameter_frame = None
            if self.instruction_label:
                self.instruction_label.destroy()
                self.instruction_label = None
            self.run_button.pack_forget()
            self.save_button.pack_forget()
            self.terminal_output.pack_forget()
            self.bottom_frame.place_forget()

    def check_parameter_change(self, param_name, entry_widget):
        config_file_path = os.path.join(self.source_path, "Parameters.config")
        config = configparser.ConfigParser()
        config.read(config_file_path)
        selected_task = self.selected_task.get()

        if selected_task in config and param_name in config[selected_task]:
            original_value = config[selected_task][param_name]
            current_value = entry_widget.get()
            changed_label = self.parameter_frame.nametowidget(f"{param_name}_changed")
            if current_value != original_value:
                changed_label.config(text="Parameter Changed!")
                self.changed_parameters[param_name] = current_value
            else:
                changed_label.config(text="")
                if param_name in self.changed_parameters:
                    del self.changed_parameters[param_name]

    def browse_folder(self, param_name, entry_widget):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, folder_selected)
            self.check_parameter_change(param_name, entry_widget)

    def run_script(self):
        selected_script = self.selected_task.get()
        selected_category = self.selected_category.get()
        if selected_script == "please choose Your Task":
            messagebox.showerror("Error", "Please choose a task first.")
            return

        config_file_path = os.path.join(self.source_path, "Parameters.config")
        config = configparser.ConfigParser()
        config.read(config_file_path)

        if selected_script in config:
            # Update parameters in the config object
            for param_name, entry_widget in self.parameter_entries.items():
                config[selected_script][param_name] = entry_widget.get()

            # Write the updated configuration back to the file
            with open(config_file_path, 'w') as configfile:
                config.write(configfile)

        script_path = os.path.join(self.source_path, selected_category, f"{selected_script}.py")
        if os.path.exists(script_path):
            self.terminal_output.delete(1.0, tk.END)
            self.terminal_output.insert(tk.END, f"Running: {script_path}\n")
            self.root.update_idletasks() # Update to show the running message

            process = subprocess.Popen(
                [sys.executable, script_path],
                cwd=self.source_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.terminal_output.insert(tk.END, output)
                    self.terminal_output.see(tk.END) # Scroll to the bottom
                    self.root.update_idletasks() # Update the GUI to show output in real-time
            self.terminal_output.insert(tk.END, f"Script finished with exit code: {process.returncode}\n")
        else:
            self.terminal_output.insert(tk.END, f"Error: Script '{script_path}' not found.\n")

    def save_parameters(self):
        selected_script = self.selected_task.get()
        if selected_script == "please choose Your Task":
            messagebox.showerror("Error", "Please choose a task first.")
            return

        config_file_path = os.path.join(self.source_path, "Parameters.config")
        config = configparser.ConfigParser()
        config.read(config_file_path)

        if selected_script in config:
            # Update parameters in the config object
            for param_name, entry_widget in self.parameter_entries.items():
                config[selected_script][param_name] = entry_widget.get()

            # Write the updated configuration back to the file
            with open(config_file_path, 'w') as configfile:
                try:
                    config.write(configfile)
                    messagebox.showinfo("Success", "Parameters saved successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"Error saving parameters: {e}")
        else:
            messagebox.showerror("Error", f"Section '{selected_script}' not found in Parameters.config.")

    def create_document_buttons(self):
        documents_path = os.path.join(self.source_path, "Documents")
        if not os.path.exists(documents_path):
            return

        self.document_buttons_frame = tk.Frame(self.root)
        self.document_buttons_frame.place(x=10, y=self.category_selection.winfo_y() + self.category_selection.winfo_height() + 10, anchor="nw")

        items = os.listdir(documents_path)
        for item in items:
            button = tk.Button(self.document_buttons_frame, text=item, command=lambda path=os.path.join(documents_path, item): self.open_file_explorer(path))
            button.pack(pady=2, anchor="w")

    def create_settings_buttons(self):
        self.settings_buttons_frame = tk.Frame(self.root)
        self.settings_buttons_frame.place(x=10, y=self.category_selection.winfo_y() + self.category_selection.winfo_height() + 10, anchor="nw")

        source_button = tk.Button(self.settings_buttons_frame, text="Source Code", command=lambda: self.open_file_explorer(self.source_path))
        source_button.pack(pady=2, anchor="w")

    def open_file_explorer(self, path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

if __name__ == "__main__":
    root = tk.Tk()
    gui = StatisticalSoftwareGUI(root)
    root.mainloop()
