import os
import json

def find_string_in_json(folder_path, search_string):
    """
    Search for a given string in all JSON files within a specified folder.

    Args:
    folder_path (str): Path to the folder containing JSON files.
    search_string (str): String to search for in the JSON files.

    Returns:
    list: Filenames of the JSON files where the search string was found.
    """
    found_files = []

    # Iterate through all files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    # Load JSON data from file
                    data = json.load(file)

                    # Convert JSON object to string for searching
                    data_str = json.dumps(data)

                    # Check if the search string is in the JSON string
                    if search_string in data_str:
                        found_files.append(filename)

            except (IOError, json.JSONDecodeError) as e:
                # Handle file read errors or JSON parsing errors
                print(f"Error reading/parsing file {filename}: {e}")

    return found_files

user_search_string = input("Enter the exact string you want to search for in the folder:")
file_path = input(r"Please input the file path for a folder containing JSON files:")

# C:\Users\Aidan\Documents\Stellar Cyber Scraper\Json Files
result = find_string_in_json(file_path, user_search_string)
print(result)
