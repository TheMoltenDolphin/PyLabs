import csv
import random
import os


class CSVHandler:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _read_csv(self):
        with open(self.file_path, encoding='utf-8', newline='') as f:
            return [row for row in csv.reader(f) if any(row)]

    def _write_csv(self, data):
        with open(self.file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)

    def show(self, mode="top", count=5, sep=","):
        data = self._read_csv()
        if not data:
            print("No data in file")
            return

        header, rows = data[0], data[1:]
        if mode not in {"top", "bottom", "random"}:
            print("Invalid mode")
            return

        col_widths = [max(len(row[i]) for row in data) for i in range(len(header))]

        def format_row(row):
            return sep.join(f"{val:<{col_widths[i]}}" for i, val in enumerate(row))

        print(format_row(header))
        print("-" * (sum(col_widths) + (len(col_widths) - 1) * len(sep)))

        selected_rows = []
        if mode == "top":
            selected_rows = rows[:count]
        elif mode == "bottom":
            selected_rows = rows[-count:]
        elif mode == "random":
            selected_rows = random.sample(rows, min(count, len(rows)))

        for row in selected_rows:
            print(format_row(row))

        if len(rows) < count:
            print("Not enough rows")

    def info(self):
        with open(self.file_path, encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        if not rows:
            print("0x0")
            return

        fields = reader.fieldnames
        print(f"{len(rows)}x{len(fields)}")

        print(f"{'Field Name':<16}{'Count':>6}  {'Type':<10}")
        print("-" * 34)

        for field in fields:
            values = [row[field].strip() for row in rows if row[field].strip()]
            count = len(values)

            inferred = "string"
            if values:
                if all(v.isdigit() for v in values):
                    inferred = "int"
                else:
                    try:
                        list(map(float, values))
                        inferred = "float"
                    except ValueError:
                        pass

            print(f"{field:<16}{count:>6}  {inferred:<10}")

    def DelNaN(self):
        data = self._read_csv()
        if not data:
            print("No data in file")
            return

        cleaned = [row for row in data if all(cell.strip() for cell in row)]
        self._write_csv(cleaned)

    def MakeDS(self):
        data = self._read_csv()
        if not data:
            print("No data in file")
            return

        header, rows = data[0], data[1:]
        random.shuffle(rows)

        split_idx = int(len(rows) * 0.7)
        train, test = rows[:split_idx], rows[split_idx:]

        os.makedirs("workdata/Learning", exist_ok=True)
        os.makedirs("workdata/Testing", exist_ok=True)

        def write_to_file(path, dataset):
            with open(path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(dataset)

        write_to_file("workdata/Learning/train.csv", train)
        write_to_file("workdata/Testing/test.csv", test)
        print("Data split into training and testing sets successfully.")


# Пример использования:
reader = CSVHandler("Employees.csv")
# reader.show("top", 5, "|")
# reader.DelNaN()
# reader.info()
reader.MakeDS()
reader.show("top", 5, "|")