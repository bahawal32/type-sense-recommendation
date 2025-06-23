import json
import argparse
import unicodedata
from tqdm import tqdm


def clean_text(text):
    if isinstance(text, str):
        return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return text
# Load data.json


def clean_text_fields(item):
    # Recursively clean all string fields in a dict
    if isinstance(item, dict):
        return {k: clean_text_fields(v) for k, v in item.items()}
    elif isinstance(item, list):
        return [clean_text_fields(elem) for elem in item]
    else:
        return clean_text(item)


def main(json_file_path, jsonl_file_path):
    # Load data from data.json
    with open(json_file_path, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    # Convert to JSONL format and write to data.jsonl
    with open(jsonl_file_path, 'w', encoding='utf-8') as outfile:
        for item in tqdm(data, desc="Converting to JSONL", unit="item"):
            cleaned_item = clean_text_fields(item)
            json_line = json.dumps(cleaned_item, ensure_ascii=False)
            outfile.write(json_line + '\n')
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert JSON to JSONL format.')
    parser.add_argument('--json_file_path', type=str, default='data.json',
                        help='Path to the input JSON file.')
    parser.add_argument('--jsonl_file_path', type=str, default='data.jsonl',
                        help='Path to the output JSONL file.')
    args = parser.parse_args()
    main(args.json_file_path, args.jsonl_file_path)