import csv


def location_dict_list():
    file = open('distances.csv')
    type(file)
    csvreader = csv.reader(file)

    header = []
    header = next(csvreader)

    rows = [row for row in csvreader]

    for row in rows:
        row.pop(0)
    location_dict = {"place": {"name": "", "end": []}}
    location_dict_list = []

    for row in rows:
        temp = location_dict["place"]["name"]
        if row[0] in temp:
            location_dict["place"]["end"].append({row[1]: row[2]})
        else:
            location_dict["place"] = {"name": row[0], "end": [{row[1]: row[2]}]}
            location_dict_list.append(location_dict.copy())

    return location_dict_list


def locations():
    file = open('victor.csv')
    type(file)
    csvreader = csv.reader(file)

    header = []
    header = next(csvreader)

    rows = [row for row in csvreader]
    temp = []
    list_temp = []
    name = rows[0][1]
    for row in rows:
        temp.append(row[3])
        if name == row[1]:
            list_temp.append(temp)
            name = row[1]
            temp = []
    return rows
