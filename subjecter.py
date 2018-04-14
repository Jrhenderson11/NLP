words = open("files/sublist.txt", "r")
lines = words.readlines()
words.close()



subjects = set()
for line in lines:
	for part in line.split(" "):
		part = part.replace("&", "")
		part = part.replace(",", "")
		subjects.add(part.strip())

for sub in subjects:
	print sub.lower()