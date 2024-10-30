import json
import matplotlib
import matplotlib.pyplot

with open("data/data.json", "r") as f:
    data = json.load(f)

# print(data)

hashNames = {
        0: "MD5",
        1400: "SHA-256",
        1700: "SHA-512",
        17600: "SHA3-512",
        1711: "SHA3-512 Salted",
        1710: "SHA1-512 Salted",
    }


average_times = []

# Iterate through the data from data.json and calculate the average time for each hash type and store it in average_times along with the type
for datum in data:
    #Get name consisting of hash number + hash type
    name = hashNames[datum["Hash Type"]] + "#" + datum["Number of Hashes"].__str__()
    #Check if it's in average_times, and if so, add the time to the list of times for that name.  Otherwise add a new entry with the time
    found = False
    for average_time in average_times:
        if average_time["name"] == name:
            average_time["times"].append(datum["Elapsed Time"])
            found = True
            break
    if not found:
        average_times.append({"name": name, "times": [datum["Elapsed Time"]]})

print(average_times)

# Calculate the average time for each hash type
for average_time in average_times:
    sum = 0
    for time in average_time["times"]:
        sum += int(time)
    
    average_time["average"] = sum / len(average_time["times"])

print(average_times)

# Create a bar graph of the average times
names = []
times = []
for average_time in average_times:
    names.append(average_time["name"])
    times.append(average_time["average"])

fig, ax = matplotlib.pyplot.subplots()
ax.bar(names, times)
#label axes
matplotlib.pyplot.xlabel("Hash Type")
matplotlib.pyplot.ylabel("Average Time (s)")
matplotlib.pyplot.show()