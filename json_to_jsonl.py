import json
import argparse


# Load data.json

def main(json_file_path, jsonl_file_path):
    # Load data from data.json
    with open(json_file_path, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    # Convert to JSONL format and write to data.jsonl
    with open(jsonl_file_path, 'w', encoding='utf-8') as outfile:
        for item in data:
            json_line = json.dumps(item, ensure_ascii=False)
            outfile.write(json_line + '\n')
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert JSON to JSONL format.')
    parser.add_argument('--json_file_path', type=str, default='data.json',
                        help='Path to the input JSON file.')
    parser.add_argument('--jsonl_file_path', type=str, default='data.jsonl',
                        help='Path to the output JSONL file.')
    args = parser.parse_args()
    main(args.json_file_path, args.jsonl_file_path)