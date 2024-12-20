import json
import matplotlib
import matplotlib.pyplot as plt

with open("data/data.json", "r") as f:
    data = json.load(f)


hashNames = {
    "0": "MD5",
    "1400": "SHA-256",
    "1410": "SHA-256 Salted",
    "1700": "SHA-512",
    "1710": "SHA-512 Salted",
    "17600": "SHA3-512",
    "1711": "SHA3-512 Salted",
    "1410": "SHA1-512 Salted",
}


average_times = []

# Iterate through the data from data.json and calculate the average time for each hash type and store it in average_times along with the type
for datum in data:
    # Get name consisting of hash number + hash type
    name = hashNames[datum["Hash Type"]] + "#" + datum["Number of Hashes"].__str__()
    # Check if it's in average_times, and if so, add the time to the list of times for that name.  Otherwise add a new entry with the time
    found = False
    for average_time in average_times:
        if average_time["name"] == name:
            average_time["times"].append(datum["Elapsed Time"])
            found = True
            break
    if not found:
        average_times.append({"name": name, "times": [datum["Elapsed Time"]]})


# Calculate the average time for each hash type
for average_time in average_times:
    sum = 0
    for time in average_time["times"]:
        sum += float(time)

    average_time["average"] = sum / len(average_time["times"])

# Create a bar graph of the average times
names = []
times = []
for average_time in average_times:
    names.append(average_time["name"])
    times.append(average_time["average"])

plt.figure(figsize=(10, 6))
bars = plt.bar(names, times, color='blue')

# Annotate bars with the average values
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval, round(yval, 2), va='bottom')

plt.xlabel('Hash Types')
plt.ylabel('Average Time')
plt.yscale('log')
plt.title('Average Time (seconds) for Each Hash Type')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()