import os
from splitter import split_file
from mapper import run_mapper
from partitioner import partition_data
from sorter import sort_partitions
from reducer import run_reducer


def main():

    input_file = "input.txt"
    chunks_folder = "chunks"
    partitions_folder = "partitions"
    output_folder = "output"

    # Create folders
    os.makedirs(chunks_folder, exist_ok=True)
    os.makedirs(partitions_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    print("===== MAPREDUCE ENGINE STARTED =====")

    # Step 1: Split Input File
    chunk_files = split_file(input_file, chunks_folder, 2)

    # Step 2: Mapper
    mapper_output = []

    for chunk in chunk_files:
        mapper_output.extend(run_mapper(chunk))

    # Step 3: Partition
    partition_data(mapper_output, partitions_folder, 2)

    # Step 4: Sort
    sort_partitions(partitions_folder)

    # Step 5: Reduce
    run_reducer(partitions_folder, output_folder)

    print("===== MAPREDUCE ENGINE COMPLETED =====")
    print("Output saved in output/result.txt")


if __name__ == "__main__":
    main()