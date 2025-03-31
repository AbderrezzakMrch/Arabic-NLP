# modules/utils.py
import json

def save_in_json(data, output_file):
    """
    Save data to a JSON file.
    
    :param data: Data to save.
    :param output_file: Path to the output JSON file.
    """
    with open(output_file, 'w', encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Data saved to {output_file}")