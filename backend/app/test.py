from datetime import datetime

# Get current date and time
now = datetime.now()

# Format date
formatted_date = now.strftime("%b %d, %Y")
print(formatted_date)
