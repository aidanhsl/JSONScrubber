
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import json

# Existing script functions
def find_string_in_json(folder_path, search_string, output_folder_base):
    found_files = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith('.json'):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    if isinstance(data, dict):
                        data_str = json.dumps(data)
                        if search_string in data_str:
                            found_files.append(filename)
                    elif isinstance(data, list):
                        data_str = json.dumps(data)
                        if search_string in data_str:
                            found_files.append(filename)
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error reading/parsing file {filename}: {e}")
    return found_files


def extract_fields_from_json(filename, fields):
    extracted_data = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for field in fields:
                if field in data:
                    extracted_data[field] = data[field]
                for key, value in data.items():
                    if isinstance(value, dict) and field in value:
                        extracted_data[f"{key}.{field}"] = value[field]
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading/parsing file {filename}: {e}")
    return extracted_data

def create_output_folder(folder_path, output_folder_base):
    output_folder = os.path.join(folder_path, output_folder_base)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder

def aggregate_and_export_data(folder_path, found_files, fields, output_folder_base):
    output_folder = create_output_folder(folder_path, output_folder_base)
    aggregated_data = []
    for filename in found_files:
        file_path = os.path.join(folder_path, filename)
        file_data = extract_fields_from_json(file_path, fields)
        if file_data:
            aggregated_data.append({"Comment": f"Data from {filename}", "Data": file_data})
    
    output_file = generate_output_file_name(output_folder, 'output')
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(aggregated_data, file, indent=4)
    except IOError as e:
        print(f"Error writing to file {output_file}: {e}")

def generate_output_file_name(folder_path, base_name):
    counter = 0
    output_file = os.path.join(folder_path, f"{base_name}.json")
    while os.path.exists(output_file):
        counter += 1
        output_file = os.path.join(folder_path, f"{base_name}{counter}.json")
    return output_file

# GUI event handler to process files
def process_files():
    search_string = search_string_var.get()
    fields = fields_var.get().split(',')
    json_folder = folder_path_var.get()
    output_folder = output_folder_var.get()

    try:
        found_files = find_string_in_json(json_folder, search_string, 'Outputs')
        aggregate_and_export_data(json_folder, found_files, fields, 'Outputs')
        messagebox.showinfo("Success", "Files processed successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def select_json_folder():
    folder_path = filedialog.askdirectory()
    folder_path_var.set(folder_path)

def select_output_folder():
    folder_path = filedialog.askdirectory()
    output_folder_var.set(folder_path)

# Create the main window
root = tk.Tk()
root.title("JSON File Analyzer")

# Search string input
search_string_var = tk.StringVar()
tk.Label(root, text="Search String:").pack()
tk.Entry(root, textvariable=search_string_var).pack()

# Fields input
fields_var = tk.StringVar()
tk.Label(root, text="Fields (comma-separated):").pack()
tk.Entry(root, textvariable=fields_var).pack()

# Folder path input
folder_path_var = tk.StringVar()
tk.Label(root, text="Folder Containing JSON Files:").pack()
tk.Entry(root, textvariable=folder_path_var).pack()
tk.Button(root, text="Browse...", command=select_json_folder).pack()

# Output folder input
output_folder_var = tk.StringVar()
tk.Label(root, text="Output Folder:").pack()
tk.Entry(root, textvariable=output_folder_var).pack()
tk.Button(root, text="Browse...", command=select_output_folder).pack()

# Process button
tk.Button(root, text="Process Files", command=process_files).pack()

# Run the application
root.mainloop()
