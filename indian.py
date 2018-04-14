import re
import NER
file = open("files/Indian-Male-Names.csv")
lines = file.readlines()
file.close()


names = set()
for line in lines:
	line = line.split(",")[0]
	if " " in line:
		for part in line.split(" "):
			names.add(part.strip())
	else:
		names.add(line.strip())

for name in names:
	print name
