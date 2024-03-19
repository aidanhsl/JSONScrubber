
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import json

# Function definitions (find_string_in_json, extract_fields_from_json, etc.)
# ...

# Create the main window with a light gray theme and organized layout
root = tk.Tk()
root.title("JSON File Analyzer")
root.configure(bg='#f0f0f0')  # Light gray background

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

# Process button
process_button = tk.Button(root, text="Process Files", command=process_files, bg='#0078D7', fg='white')
process_button.pack(padx=10, pady=10)

# Run the application
root.mainloop()
