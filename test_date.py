import dateutil
import datetime
from dateutil import parser
date = parser.parse("2000-04-21")
now = datetime.datetime.utcnow()

now = now.date()

# Get the difference between the current date and the birthday
age = dateutil.relativedelta.relativedelta(now, date)
age = age.years
print(age)
