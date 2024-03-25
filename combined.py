import os

# Function to append file contents to another file
def append_file_contents(src_file, dest_file):
    with open(src_file, 'r') as f:
        dest_file.write(f"{src_file}:\n")
        dest_file.write(f.read())
        dest_file.write("\n\n")

# Directory containing files
directory = '/home/william/CODE/mpdignore/'

# Output file where contents will be appended
output_file = 'output.txt'

# Open output file in append mode
with open(output_file, 'a') as dest_file:
    # Iterate over files in the directory
    for filename in os.listdir(directory):
        if filename == 'combined.py' or filename == 'output.txt':
            continue  # Skip the file
        if os.path.isfile(os.path.join(directory, filename)):
            append_file_contents(os.path.join(directory, filename), dest_file)

