import os

def split_file(input_file, output_folder, num_chunks=2):
    # Read all lines from input file
    with open(input_file, "r") as file:
        lines = file.readlines()

    total_lines = len(lines)
    chunk_size = (total_lines + num_chunks - 1) // num_chunks

    chunk_files = []

    for i in range(num_chunks):
        start = i * chunk_size
        end = start + chunk_size

        chunk_lines = lines[start:end]

        if chunk_lines:
            chunk_file = os.path.join(output_folder, f"chunk{i+1}.txt")

            with open(chunk_file, "w") as out:
                out.writelines(chunk_lines)

            chunk_files.append(chunk_file)

    print(f"{len(chunk_files)} chunk(s) created successfully.")

    return chunk_files


# Test the splitter separately
if __name__ == "__main__":
    os.makedirs("chunks", exist_ok=True)
    split_file("input.txt", "chunks", 2)