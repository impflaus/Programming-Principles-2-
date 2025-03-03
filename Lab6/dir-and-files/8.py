import os

def delete_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return

    if not os.access(file_path, os.W_OK):
        print(f"Error: No permission to delete '{file_path}'.")
        return

    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    except Exception as e:
        print(f"Error: Unable to delete '{file_path}'. Reason: {e}")

file_path = "/Users/daurenkaztay/Desktop/Workshop/test.cpp"
delete_file(file_path)