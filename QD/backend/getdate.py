from datetime import datetime, timedelta

# Get the current date and time
current_date = datetime.now()

# Subtract 5 days from the current date
five_days_before = current_date - timedelta(days=5)

# Format the date as a string (optional)
formatted_date = five_days_before.strftime("%Y-%m-%d")

print("Current Date:", current_date.strftime("%Y-%m-%d"))
print("Date 5 Days Before:", formatted_date)
