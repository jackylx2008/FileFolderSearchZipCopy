import os


def traverse_one_level(directory):
    try:
        # List all items in the directory
        items = os.listdir(directory)

        for item in items:
            # Construct the full path of the item
            item_path = os.path.join(directory, item)

            # Check if it is a file or a subdirectory
            if os.path.isfile(item_path):
                print(f"File: {item}")
            elif os.path.isdir(item_path):
                print(f"Directory: {item_path}")
            else:
                print(f"Unknown: {item}")

    except OSError as e:
        print(f"Error: {e}")


# Example usage
directory_path = r"C:\Users\bcjt_\Desktop\新建文件夹"
traverse_one_level(directory_path)
