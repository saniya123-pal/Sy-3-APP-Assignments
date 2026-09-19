
# File Handling Program

input_file = "APP2.txt"
output_file = "op.txt"

# Read the input file
with open(input_file, "r") as f:
    lines = f.readlines()

# Count lines
print("Number of lines:", len(lines))

# Write first two lines to output file
with open(output_file, "w") as f:
    f.writelines(lines[:2])

print("First two lines written to", output_file)