import yaml


def print_yaml(data, indent=0):
    space = "  " * indent
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{space}{key}:")
            print_yaml(value, indent + 1)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            print(f"{space}-")
            print_yaml(item, indent + 1)
    else:
        print(f"{space}{data}")

try:
    with open('file2.yaml', 'r') as file:
        data = yaml.safe_load(file)
        print_yaml(data)
except Exception as error:
    print("Error reading YAML file\n:", error)