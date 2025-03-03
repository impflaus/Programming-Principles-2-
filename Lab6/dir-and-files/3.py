import os

def check_path(path):
    if os.path.exists(path):
        print(f"The path '{path}' exists.")
        directory = os.path.dirname(path)
        filename = os.path.basename(path)
        print(f"Directory: {directory}")
        print(f"Filename: {filename}")
    else:
        print(f"The path '{path}' does not exist.")

path = input("Enter a file or directory path: ")
check_path(path)