import json


class JSONUtils:
    def save_in_json(self, data, output_file):
        with open(output_file, 'w', encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Data saved to {output_file}")