
# Read data from APP2.txt
with open("APP2.txt", "r") as file:
    lines = file.readlines()

# Count the number of lines
line_count = len(lines)

# Extract the first two lines
first_two_lines = lines[:2]

# Display line count
print("Number of lines:", line_count)

# Write first two lines into op.txt
with open("op.txt", "w") as file:
    file.writelines(first_two_lines)

print("First two lines written to op.txt")
