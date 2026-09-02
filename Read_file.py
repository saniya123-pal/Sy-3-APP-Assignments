# Open APP2.txt in read mode
File1 = open("APP2.txt", "r")

# Read all lines
lines = File1.readlines()

# Close the file
File1.close()

# Display total number of lines
print("Total Number of lines in APP2.txt:", len(lines))

# Get first two lines
first_two_lines = lines[:2]

# Display first two lines
print("\nFirst Two Lines of APP2.txt file:\n")

for i in first_two_lines:
    print(i)

# Open Output.txt in append mode
File2 = open("Output.txt", "a")

# Write first two lines into Output.txt
File2.writelines(first_two_lines)

# Close Output.txt
File2.close()

print("\nFirst two lines from APP2.txt are written in Output.txt")
