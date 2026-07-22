def run_mapper(chunk_file):
    mapper_output = []

    # Read the chunk file
    with open(chunk_file, "r") as file:
        for line in file:
            word = line.strip()

            # Ignore empty lines
            if word:
                mapper_output.append((word, 1))

    print(f"Mapper completed for {chunk_file}")

    return mapper_output


# Test the mapper separately
if __name__ == "__main__":
    output = run_mapper("chunks/chunk1.txt")

    print("\nMapper Output:")
    for item in output:
        print(item)