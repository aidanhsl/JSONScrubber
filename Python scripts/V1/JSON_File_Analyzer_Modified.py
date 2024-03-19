
import os
import json

def find_string_in_json(folder_path, search_string):
    found_files = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    data_str = json.dumps(data)
                    if search_string in data_str:
                        found_files.append(filename)
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error reading/parsing file {filename}: {e}")
    return found_files

def extract_relevant_data_from_json(filename, search_string):
    extracted_data = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for key, value in data.items():
                if search_string in str(value) or 'dstip' in str(value):
                    extracted_data[key] = value
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading/parsing file {filename}: {e}")
    return extracted_data

def aggregate_and_export_data(folder_path, found_files, search_string, output_file):
    aggregated_data = []
    for filename in found_files:
        file_path = os.path.join(folder_path, filename)
        file_data = extract_relevant_data_from_json(file_path, search_string)
        if file_data:
            aggregated_data.append(file_data)
    
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(aggregated_data, file, indent=4)
    except IOError as e:
        print(f"Error writing to file {output_file}: {e}")

user_search_string = input("Enter the exact string you want to search for in the folder:")
file_path = input(r"Please input the file path for a folder containing JSON files:")


found_files = find_string_in_json(file_path, user_search_string)
aggregate_and_export_data(file_path, found_files, ['field1', 'field2'], 'output.json')
