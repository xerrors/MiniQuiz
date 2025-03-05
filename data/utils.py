import csv
import json

def convert_csv_to_json(csv_file, save_as=None):
    with open(csv_file, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if save_as:
        with open(save_as, 'w', encoding="utf-8") as f:
            json.dump(rows, f, indent=4, ensure_ascii=False)
    return rows

def convert_excel_to_json(excel_file, save_as=None):
    import pandas as pd
    df = pd.read_excel(excel_file)
    if save_as:
        df.to_json(save_as, orient='records', force_ascii=False)
    return df.to_dict(orient='records')

def convert_json_to_csv(json_file, save_as=None):
    with open(json_file, 'r', encoding="utf-8") as f:
        data = json.load(f)
    if save_as:
        with open(save_as, 'w', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

def convert_json_to_csv(json_file, save_as=None):
    with open(json_file, 'r', encoding="utf-8") as f:
        data = json.load(f)
    if save_as:
        with open(save_as, 'w', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

def convert_excel_to_csv(excel_file, save_as=None):
    import pandas as pd
    df = pd.read_excel(excel_file)
    if save_as:
        df.to_csv(save_as, index=False)
    return df.to_dict(orient='records')

if __name__ == '__main__':
    convert_excel_to_csv('data/aigc_simple_100.xlsx', 'data/aigc_simple_100.csv')
