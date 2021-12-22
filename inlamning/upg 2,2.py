import import_csv
import random
from matplotlib import pyplot as plt
import csv

def location_dict_list():
    """loads a CSV file and remove header and index value"""
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

# Initialize dict
location_dict_list = location_dict_list()
travel_distant_tot = []


# Change to 10000 for assignment. Start att 100 for a fast test
for i in range(100):
    # Initialize values for every run
    ldl = import_csv.location_dict_list()
    start_val = random.randint(0, len(location_dict_list) - 1)
    distant = 0
    for _ in range(len(location_dict_list)):
        # Generate a random value
        random_val = random.randint(0, len(ldl[start_val]["place"]["end"]) - 1)
        if random_val == start_val and len(ldl[start_val]["place"]["end"]) - 1 != 0:
            while random_val == start_val:
                random_val = random.randint(0, len(ldl[start_val]["place"]["end"]) - 1)

        # Looks from start detention to end detention
        start = ldl[start_val]["place"]["name"]
        end = ldl[start_val]["place"]["end"][random_val]

        # if len(ldl) == 3:
        #    print()

        # print()
        # Removes visited place from all dicts (very inefficient but works)
        for p in ldl:
            p['place']['end'].pop(random_val)
        ldl.pop(start_val)

        # Adds all distant value together
        end_val = list(end.values())
        distant += int(end_val[0])

        # Sets nex start value to current end
        if start_val > random_val:
            start_val = random_val
        else:
            # Fix pop of sett
            start_val = random_val - 1
            if start_val == -1:
                start_val = 0

    travel_distant_tot.append(distant)

    # print every 100 run to see progress
    if i % 100 == 0:
        print(i)

# Printing some statistics
avg_time = int(sum(travel_distant_tot) / len(travel_distant_tot))
print("total travel time:", travel_distant_tot)
print("avg travel time:", avg_time)

# Plotting
plt.style.use('fivethirtyeight')
plt.plot(travel_distant_tot)
plt.xlabel('Random try')
plt.ylabel('Distances travelled')

plt.show()
