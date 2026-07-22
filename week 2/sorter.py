import os

def sort_partitions(partitions_folder):
    # Get all partition files
    partition_files = [
        f for f in os.listdir(partitions_folder)
        if f.startswith("partition") and f.endswith(".txt")
    ]

    for file_name in partition_files:
        file_path = os.path.join(partitions_folder, file_name)

        # Read all lines
        with open(file_path, "r") as file:
            lines = file.readlines()

        # Sort lines alphabetically
        lines.sort()

        # Write sorted data back
        with open(file_path, "w") as file:
            file.writelines(lines)

        print(f"{file_name} sorted successfully.")

    print("All partition files sorted.")


# Test the sorter separately
if __name__ == "__main__":
    sort_partitions("partitions")