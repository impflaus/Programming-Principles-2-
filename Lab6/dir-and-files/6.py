counter = 65
for i in range(26):
    with open(f"{chr(counter)}.txt", "w") as file:
        pass
    counter += 1