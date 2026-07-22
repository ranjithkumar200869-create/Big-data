import os

def partition_data(mapper_output, partitions_folder, num_reducers=2):
    # Create partition files
    partition_files = []

    for i in range(num_reducers):
        file_path = os.path.join(partitions_folder, f"partition{i}.txt")
        partition_files.append(file_path)

        # Clear old data
        open(file_path, "w").close()

    # Partition the mapper output
    for key, value in mapper_output:
        partition_number = hash(key) % num_reducers

        with open(partition_files[partition_number], "a") as file:
            file.write(f"{key} {value}\n")

    print(f"{num_reducers} partition file(s) created successfully.")


# Test the partitioner separately
if __name__ == "__main__":
    sample_data = [
        ("Apple", 1),
        ("Orange", 1),
        ("Apple", 1),
        ("Banana", 1),
        ("Mango", 1)
    ]

    os.makedirs("partitions", exist_ok=True)
    partition_data(sample_data, "partitions", 2)