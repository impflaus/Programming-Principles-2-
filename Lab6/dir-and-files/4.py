with open("demofile.txt", "r") as file:
    lines = file.readlines()
    print(lines)
    print(len(lines))