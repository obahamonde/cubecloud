import os


def get_dir_size(path="."):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total


def build_file_tree(root_dir):
    file_tree = {
        "name": os.path.basename(root_dir),
        "type": "directory",
        "children": [],
    }

    for file_name in os.listdir(root_dir):
        file_path = os.path.join(root_dir, file_name)

        if os.path.isdir(file_path):
            file_tree["children"].append(build_file_tree(file_path))
        else:
            try:
                with open(file_path, "r") as f:
                    file_content = f.read()
            except UnicodeDecodeError:
                with open(file_path, "rb") as f:
                    file_content = f.read()

            file_tree["children"].append(
                {"name": file_name, "type": "file", "content": file_content}
            )

    return file_tree


print(build_file_tree("./api"))
