
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import json

# Function to find files containing the search string
def find_string_in_json(folder_path, search_string, output_folder_base):
    found_files = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith('.json'):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    if isinstance(data, dict) and search_string in json.dumps(data):
                        found_files.append(filename)
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error reading/parsing file {filename}: {e}")
    return found_files

# Function to extract selected fields from JSON file
def extract_fields_from_json(filename, fields):
    extracted_data = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for field in fields:
                if field in data:
                    extracted_data[field] = data[field]
                elif '.' in field:
                    top_field, nested_field = field.split('.', 1)
                    if top_field in data and nested_field in data[top_field]:
                        extracted_data[field] = data[top_field][nested_field]
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading/parsing file {filename}: {e}")
    return extracted_data

# Function to create output folder
def create_output_folder(folder_path, output_folder_base):
    output_folder = os.path.join(folder_path, output_folder_base)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder

# Function to aggregate data and export to a JSON file
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

# Function to generate a unique output file name
def generate_output_file_name(folder_path, base_name):
    counter = 0
    output_file = os.path.join(folder_path, f"{base_name}.json")
    while os.path.exists(output_file):
        counter += 1
        output_file = os.path.join(folder_path, f"{base_name}{counter}.json")
    return output_file

# Function to process files based on user inputs
def process_files():
    search_string = search_string_var.get()
    selected_fields = [field for field, var in checkboxes.items() if var.get()]
    json_folder = folder_path_var.get()
    output_folder = output_folder_var.get()

    try:
        found_files = find_string_in_json(json_folder, search_string, 'Outputs')
        aggregate_and_export_data(json_folder, found_files, selected_fields, 'Outputs')
        messagebox.showinfo("Success", "Files processed successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to select JSON folder
def select_json_folder():
    folder_path = filedialog.askdirectory()
    folder_path_var.set(folder_path)

# Function to select output folder
def select_output_folder():
    folder_path = filedialog.askdirectory()
    output_folder_var.set(folder_path)

# Create the main window
root = tk.Tk()
root.title("XVPN JSON File Nuker")

# Search string input
search_string_var = tk.StringVar()
tk.Label(root, text="Search String:").pack()
tk.Entry(root, textvariable=search_string_var).pack()

# Checkboxes for field selection
checkboxes = {}
fields = ['tenant_name', 'appid_name', 'srcport', 'totalbytes', 'totalpackets', 'dstip', 'dstport', 'login_result', 'srcip_host', 'srcip_username',
          'dstip_geo', 'dstmac', 'dstip_host', 'duration', 'engid_name', 'event_name', 'fidelity', 'flow_score', 'srcip_geo', 'srcip_reputation',
          'dstip_reputation', 'xrd_event']
for field in fields:
    var = tk.BooleanVar()
    tk.Checkbutton(root, text=field, variable=var).pack()
    checkboxes[field] = var

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
