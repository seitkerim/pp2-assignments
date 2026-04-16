#1 add 30 days to the given date
from datetime import datetime, timedelta
date_str = input().strip()
duration = int(input())
start_date = datetime.strptime(date_str, "%Y-%m-%d")
expiry_date = start_date + timedelta(days=duration)
print(expiry_date.strftime("%Y-%m-%d"))
#2 find discriminant of a quadratic equation
import math
a,b,c = map(int, input().split())
discriminant = b**2 - 4*a*c
print(math.sqrt(discriminant))
#3 find the number of days between two dates
from datetime import datetime   
date1_str = input().strip()
date2_str = input().strip()
date1 = datetime.strptime(date1_str, "%Y-%m-%d")
date2 = datetime.strptime(date2_str, "%Y-%m-%d")
delta = abs((date2 - date1).days)
print(delta)

