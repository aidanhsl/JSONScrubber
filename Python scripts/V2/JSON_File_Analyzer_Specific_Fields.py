
import os
import json

def find_string_in_json(folder_path, search_string, output_file_base):
    found_files = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith('.json') and not filename.startswith(output_file_base):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    data_str = json.dumps(data)
                    if search_string in data_str:
                        found_files.append(filename)
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error reading/parsing file {filename}: {e}")
    return found_files

def extract_specific_fields_from_json(filename, fields):
    extracted_data = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for field in fields:
                if field in data:
                    extracted_data[field] = data[field]
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading/parsing file {filename}: {e}")
    return extracted_data

def aggregate_and_export_data(folder_path, found_files, fields, output_file_base):
    aggregated_data = []
    for filename in found_files:
        file_path = os.path.join(folder_path, filename)
        file_data = extract_specific_fields_from_json(file_path, fields)
        if file_data:
            aggregated_data.append(file_data)
    
    output_file = generate_output_file_name(folder_path, output_file_base)
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

# Fields to extract
fields_to_extract = ['tenant_name', 'appid_name', 'srcport', 'totalbytes', 'totalpackets', 'dstip']

# Getting user inputs
search_string = input("Enter the exact string you want to search for in the folder: ")
folder_path = input("Please input the file path for a folder containing JSON files: ")

# Function calls
found_files = find_string_in_json(folder_path, search_string, 'output')
aggregate_and_export_data(folder_path, found_files, fields_to_extract, 'output')
