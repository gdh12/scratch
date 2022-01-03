import argparse
import csv
from typing import Dict, List, Sequence


def open_csv(file_name: str, key: str):
    with open(file_name, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        data = {}
        i = 0
        headers = []
        for row in reader:
            if i < 2:
                headers.append(row)
                i += 1
            else:
                data[row[key]] = row
    return data, fieldnames, headers
    

def do_diff(old_data: Dict, new_data: Dict, full_diff: bool) -> Dict:
    new_records = {}
    for key, value in new_data.items():
        if key not in old_data:
            new_records[key] = value
        elif full_diff and value != old_data[key]:
            new_records[key] = value
    return new_records


def write_file(file_name: str, fieldnames: Sequence[str], new_data: List[Dict], header, sort_key):
    new_data.sort(key=lambda x: x[sort_key])
    with open(file_name, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames)
        writer.writeheader()
        writer.writerows(header)
        writer.writerows(new_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--old', type=str, help='old csv file')
    parser.add_argument('--new', type=str, help='new csv file')
    parser.add_argument('--output', type=str, help='output file')
    parser.add_argument('--ids', action='store_true', help='id difference only. Not full row check')
    parser.add_argument('--key', type=str, help='Key to use for the id')

    args = parser.parse_args()

    # Yup the key looks like this
    key = args.key or '\ufeffkey'
    new, csv_fieldnames, extra_headers = open_csv(args.new, key)
    old, _, _ = open_csv(args.old, key)

    new_stuff = do_diff(old, new, not args.ids)

    write_file(args.output, csv_fieldnames, list(new_stuff.values()), extra_headers, key)
