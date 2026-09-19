
import re

# 1. Email Pattern
EMAIL_PATTERN = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+'

# 2. Find all emails
def find_emails(text):
    return re.findall(EMAIL_PATTERN, text)

# 3. Validate one email
def is_valid_email(candidate):
    return re.fullmatch(EMAIL_PATTERN, candidate) is not None

# 4. Main Program
if __name__ == "__main__":

    sample_text = """
    Contact support@example.com
    Sales: sales.team@business.co.in
    Personal: rahul_23@gmail.com
    Invalid: not-an-email
    """

    # Find emails
    found = find_emails(sample_text)

    print("Emails Found:")
    for email in found:
        print(email)

    # Validate emails
    test_cases = [
        "john.doe@example.com",
        "invalid-email",
        "user@site",
        "user@site.com",
        "plain.text@"
    ]

    print("\nEmail Validation:")

    for candidate in test_cases:
        if is_valid_email(candidate):
            print(candidate, "-> VALID")
        else:
            print(candidate, "-> INVALID")