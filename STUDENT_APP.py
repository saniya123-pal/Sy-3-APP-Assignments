import pandas as pd
import matplotlib.pyplot as plt

# Read CSV file
df = pd.read_csv("STUDENT.csv")

# Display first five records
print("First five records:")
print(df.head())

# Display dataset information
print("\nDataset Information:")
df.info()

# Calculate marks
print("\nAverage Marks:", df["marks"].mean())
print("Maximum Marks:", df["marks"].max())
print("Minimum Marks:", df["marks"].min())

# Students scoring more than 75
print("\nStudents scoring more than 75 marks:")
print(df[df["marks"] > 75])

# Bar chart
plt.bar(df["name"], df["marks"])
plt.xlabel("Student Name")
plt.ylabel("Marks")
plt.title("Student Marks")
plt.show()

# Histogram
plt.hist(df["marks"], bins=5, edgecolor="black")
plt.xlabel("Marks")
plt.ylabel("Number of Students")
plt.title("Distribution of Marks")
plt.show()

# Scatter plot
plt.scatter(df["study_hours"], df["marks"])
plt.xlabel("Study Hours")
plt.ylabel("Marks")
plt.title("Study Hours vs Marks")
plt.show()