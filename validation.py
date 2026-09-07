import re
from datetime import datetime

def get_positive_int(message):
    while True:
        try:
            value = int(input(message))
            if value > 0:
                return value
        except ValueError:
            pass
        print("Please enter a valid number greater than 0.")

def get_positive_float(message):
    while True:
        try:
            value = float(input(message))
            if value > 0:
                return value
        except ValueError:
            pass
        print("Please enter a valid number greater than 0.")

def get_valid_email():
    while True:
        email = input("Enter your email: ").strip()
        if re.fullmatch(r"[\w.\-]+@[\w.\-]+\.\w+", email):
            return email
        print("Please enter a valid email address.")

def get_date_range():
    while True:
        try:
            start = input("Start date (YYYY-MM-DD): ").strip()
            end = input("End date (YYYY-MM-DD): ").strip()
            s = datetime.strptime(start, "%Y-%m-%d")
            e = datetime.strptime(end, "%Y-%m-%d")
            if e >= s:
                return start, end
            print("End date cannot be before start date.")
        except ValueError:
            print("Please enter valid dates in YYYY-MM-DD format.")
