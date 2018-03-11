import stocks
import datetime
import sys


# repeatStocks.py 13 
# 13 is number of days from now
nextNDays = int(sys.argv[1])
if nextNDays > 21:
	print "Number of days should be less than 21, whereas number of days entered was" + nextNDays

for i in range(0,nextNDays):
	d = datetime.date.today() + datetime.timedelta(days=i)
	if d.weekday() > 4:
		continue
	dateToPass = d.strftime("%Y") + "-" + d.strftime("%B")[0:3] + "-" + d.strftime("%d")
	stocks.enrtypoint(dateToPass)