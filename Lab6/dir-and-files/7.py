with open("file.txt", "r") as file:
    content = file.read()
    print(content)

with open("file_to_copy.txt", "w") as file:
    file.write(content)