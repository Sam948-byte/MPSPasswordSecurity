import json

with open("data/data.json", "r") as f:
    data = json.load(f)

for datum in data:
    hours, minutes, seconds = datum["Elapsed Time"].split(":")
    datum["Elapsed Time"] = int(hours) * 3600 + int(minutes) * 60 + int(seconds)

with open("data/data.json", "w") as f:
    json.dump(data, f)