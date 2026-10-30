import re

# Read paragraph
paragraph = input("Enter a paragraph: ")

# Read the specified letter
letter = input("Enter the starting letter: ")

if len(letter) != 1 or not letter.isalpha():
    print("Please enter a single alphabet.")
else:
    # Find words beginning with the specified letter
    pattern = r"\b" + re.escape(letter) + r"\w*\b"

    words = re.findall(pattern, paragraph, re.IGNORECASE)

    print("Words beginning with", letter, ":")
    print(words)
    