import os

def run_reducer(partitions_folder, output_folder):
    output_file = os.path.join(output_folder, "result.txt")

    with open(output_file, "w") as out:

        # Process each partition file
        for file_name in sorted(os.listdir(partitions_folder)):
            if file_name.startswith("partition") and file_name.endswith(".txt"):

                file_path = os.path.join(partitions_folder, file_name)

                counts = {}

                # Read partition file
                with open(file_path, "r") as file:
                    for line in file:
                        parts = line.strip().split()

                        if len(parts) == 2:
                            key = parts[0]
                            value = int(parts[1])

                            counts[key] = counts.get(key, 0) + value

                # Write final counts
                for key in sorted(counts):
                    out.write(f"{key} {counts[key]}\n")

                print(f"{file_name} reduced successfully.")

    print(f"\nFinal output saved in {output_file}")


# Test the reducer separately
if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    run_reducer("partitions", "output")