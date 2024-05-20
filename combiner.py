with open("wordlists/datelist.txt", "r") as file:
    dates = file.read().splitlines()

with open("wordlists/wordnet4and5.txt", "r") as file:
    words = file.read().splitlines()

with open("wordlists/combined.txt", "w") as file:
    for date in dates:
        for word in words:
            file.write(date + word + "\n")