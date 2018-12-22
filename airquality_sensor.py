import datetime
from log import warning, info

def read(filePath, outputFormat):
	content = None
	with open(filePath) as f:
	    content = f.readlines()
	content = [x.strip() for x in content] 
	return readStrippedLines(content, outputFormat)

def readStrippedLines(strippedLines, outputFormat):
	if(len(strippedLines) < 1):
		warning('[air quality sensor] nothing to read')
		return None
	lst = strippedLines[0].split(",")
	if len(lst)!=2:
		return None
	return (parse_airquality_tstamp(lst[0]).strftime(outputFormat), int(float(lst[1])))

#2017-05-19T20:50:21.776442,462.00
def parse_airquality_tstamp(tstampStr):
	return datetime.datetime.strptime(tstampStr, "%Y-%m-%dT%H:%M:%S.%f")
