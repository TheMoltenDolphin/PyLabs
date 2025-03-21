import json

with open(input(), "r") as f:
    tables = json.load(f)
    f.close()

for table in tables:
    csv = ""
    flag = False
    for data in tables[table]:
        for column in data:
            if not flag:
                csv += f'"{column}",'
            else:
                csv += f'"{data[column]}",'
        flag = True
        csv = csv.rstrip(",")
        csv += "\n"
    with open(f"{table}.csv", "w") as f:
        f.write(csv)
        f.close()
