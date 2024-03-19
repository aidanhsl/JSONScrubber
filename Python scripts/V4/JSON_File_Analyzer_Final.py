
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import json
import threading

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
            except Exception as e:
                continue
    return found_files

def extract_fields_from_json(filename, fields):
    extracted_data = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for field in fields:
                if field in data:
                    extracted_data[field] = data[field]
    except Exception as e:
        pass
    return extracted_data

def create_output_folder(folder_path, output_folder_base):
    output_folder = os.path.join(folder_path, output_folder_base)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder

def aggregate_and_export_data(folder_path, found_files, fields, output_folder_base, progress_callback):
    output_folder = create_output_folder(folder_path, output_folder_base)
    aggregated_data = []
    total_files = len(found_files)
    for i, filename in enumerate(found_files):
        file_path = os.path.join(folder_path, filename)
        file_data = extract_fields_from_json(file_path, fields)
        if file_data:
            aggregated_data.append({"Comment": f"Data from {filename}", "Data": file_data})
        progress_callback(i + 1, total_files)
    
    output_file = generate_output_file_name(output_folder, 'output')
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(aggregated_data, file, indent=4)

def generate_output_file_name(folder_path, base_name):
    counter = 0
    output_file = os.path.join(folder_path, f"{base_name}.json")
    while os.path.exists(output_file):
        counter += 1
        output_file = os.path.join(folder_path, f"{base_name}{counter}.json")
    return output_file

# Function to select JSON folder
def select_json_folder():
    folder_path = filedialog.askdirectory()
    folder_path_var.set(folder_path)

# Function to select output folder
def select_output_folder():
    folder_path = filedialog.askdirectory()
    output_folder_var.set(folder_path)

def process_files_threaded():
    search_string = search_string_var.get()
    selected_fields = [field for field, var in checkboxes.items() if var.get()]
    json_folder = folder_path_var.get()
    output_folder = output_folder_var.get()

    def update_progress(file_count, total_files):
        progress_var.set(file_count / total_files * 100)
        progress_bar['value'] = progress_var.get()
        root.update_idletasks()

    try:
        found_files = find_string_in_json(json_folder, search_string, 'Outputs')
        aggregate_and_export_data(json_folder, found_files, selected_fields, 'Outputs', update_progress)
        messagebox.showinfo("Success", "Files processed successfully!")
        root.destroy()
    except Exception as e:
        messagebox.showerror("Error", str(e))
        root.destroy()

def process_files():
    threading.Thread(target=process_files_threaded, daemon=True).start()

# GUI setup
root = tk.Tk()
root.title("JSON File Analyzer")
root.configure(bg='#f0f0f0')

# Search string input
search_string_var = tk.StringVar()
search_frame = tk.Frame(root, bg='#f0f0f0')
search_frame.pack(padx=10, pady=5)
tk.Label(search_frame, text="Search String:", bg='#f0f0f0').pack(side=tk.LEFT)
tk.Entry(search_frame, textvariable=search_string_var).pack(side=tk.LEFT, padx=5)

# Checkboxes for field selection
fields_frame = tk.Frame(root, bg='#f0f0f0')
fields_frame.pack(padx=10, pady=5)
checkboxes = {}
fields = ['tenant_name', 'appid_name', 'srcport', 'totalbytes', 'totalpackets', 'dstip', 'dstport', 'login_result', 'srcip_host', 'srcip_username',
          'dstip_geo', 'dstmac', 'dstip_host', 'duration', 'engid_name', 'event_name', 'fidelity', 'flow_score', 'srcip_geo', 'srcip_reputation',
          'dstip_reputation', 'xrd_event']
columns = [tk.Frame(fields_frame, bg='#f0f0f0') for _ in range((len(fields) + 9) // 10)]
for col in columns:
    col.pack(side=tk.LEFT, fill=tk.Y, expand=True)

for i, field in enumerate(fields):
    var = tk.BooleanVar()
    cb = tk.Checkbutton(columns[i // 10], text=field, variable=var, bg='#f0f0f0')
    cb.pack(anchor='w')
    checkboxes[field] = var

# Folder path input
folder_path_var = tk.StringVar()
folder_frame = tk.Frame(root, bg='#f0f0f0')
folder_frame.pack(padx=10, pady=5)
tk.Label(folder_frame, text="Folder Containing JSON Files:", bg='#f0f0f0').pack(side=tk.LEFT)
folder_entry = tk.Entry(folder_frame, textvariable=folder_path_var)
folder_entry.pack(side=tk.LEFT, padx=5)
tk.Button(folder_frame, text="Browse...", command=select_json_folder, bg='#0078D7', fg='white').pack(side=tk.LEFT, padx=5)

# Output folder input
output_folder_var = tk.StringVar()
output_frame = tk.Frame(root, bg='#f0f0f0')
output_frame.pack(padx=10, pady=5)
tk.Label(output_frame, text="Output Folder:", bg='#f0f0f0').pack(side=tk.LEFT)
output_entry = tk.Entry(output_frame, textvariable=output_folder_var)
output_entry.pack(side=tk.LEFT, padx=5)
tk.Button(output_frame, text="Browse...", command=select_output_folder, bg='#0078D7', fg='white').pack(side=tk.LEFT, padx=5)

# Progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", variable=progress_var)
progress_bar.pack(padx=10, pady=5)

# Process button
process_button = tk.Button(root, text="Process Files", command=process_files, bg='#0078D7', fg='white')
process_button.pack(padx=10, pady=10)

root.mainloop()
