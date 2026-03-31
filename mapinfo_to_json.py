import json
import os

def parse_mapinfo(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return [], []
    maps = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if len(lines) < 3:
        print("Error: File is too short or empty.")
        return [], []
    headers = [h.strip() for h in lines[0].split('|')]
    for line in lines[2:]:
        if not line.strip() or line.startswith('='):
            continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) == len(headers):
            maps.append(parts)
    return maps

def save_to_json(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, separators=(',', ':'), ensure_ascii=False)

if __name__ == "__main__":
    input_file = 'mapinfo.txt'
    output_file = 'mapinfo.json'
    maps_data = parse_mapinfo(input_file)
    if maps_data:
        save_to_json(maps_data, output_file)
    else:
        print("No data found to convert.")
