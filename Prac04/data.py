from datetime import datetime, timedelta

# 1. Subtract five days from current date
today = datetime.now()
five_days_ago = today - timedelta(days=5)
print("Five days ago:", five_days_ago)

# 2. Print yesterday, today, tomorrow
today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)

# 3. Drop microseconds from datetime
now = datetime.now()
without_microseconds = now.replace(microsecond=0)
print("Without microseconds:", without_microseconds)

# 4. Calculate difference between two dates in seconds
date1 = datetime(2025, 1, 1)
date2 = datetime(2025, 1, 2)

difference = date2 - date1
print("Difference in seconds:", difference.total_seconds())