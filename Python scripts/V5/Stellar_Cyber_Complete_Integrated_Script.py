
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests
import json
import threading

# Placeholder values for API credentials and endpoint
API_URL = "https://PLACEHOLDER/connect/api/v1/cases"
TENANT_ID = "PLACEHOLDER_TENANT_ID"
API_TOKEN = "PLACEHOLDER_API_TOKEN"  # Replace with your actual token

def get_api_data(api_url, tenant_id, api_token, limit=10):
    headers = {"Authorization": f"Bearer {api_token}"}
    params = {
        "tenant_id": tenant_id,
        "limit": limit,
        "sort": "case_score",
        "order": "desc"
    }
    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Commented out old file fetching functions
# def find_string_in_json(folder_path, search_string, output_folder_base):
#     ...
# def extract_fields_from_json(filename, fields):
#     ...

def process_files_threaded():
    selected_fields = [field for field, var in checkboxes.items() if var.get()]

    try:
        # Fetching top 10 case JSON files from API
        cases_data = get_api_data(API_URL, TENANT_ID, API_TOKEN, 10)
        # Logic to process each case data and update progress
        total_cases = len(cases_data.get('cases', []))
        for i, case in enumerate(cases_data.get('cases', []), 1):
            # Extract and process fields from each case JSON
            # Placeholder logic to process fields
            # ...
            progress_var.set(i / total_cases * 100)
            progress_bar['value'] = progress_var.get()
            root.update_idletasks()

        messagebox.showinfo("Success", "Top 10 cases processed successfully!")
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

# Checkboxes for field selection
fields_frame = tk.Frame(root, bg='#f0f0f0')
fields_frame.pack(padx=10, pady=5)
checkboxes = {}
fields = ['tenant_name', 'appid_name', 'srcport', 'totalbytes', 'totalpackets', 'dstip', 'dstport', 'login_result', 'srcip_host', 'srcip_username']
for field in fields:
    var = tk.BooleanVar()
    cb = tk.Checkbutton(fields_frame, text=field, variable=var, bg='#f0f0f0')
    cb.pack(anchor='w')
    checkboxes[field] = var

# Progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", variable=progress_var)
progress_bar.pack(padx=10, pady=5)

# Process button
process_button = tk.Button(root, text="Process Files", command=process_files, bg='#0078D7', fg='white')
process_button.pack(padx=10, pady=10)

root.mainloop()
