import csv


def load_csv(csv_file_path: str) -> list:
    data = []
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data


