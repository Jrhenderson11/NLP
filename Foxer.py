import NER


def sharednams():
	print ("abc".upper() == "ABC")
	print NER.filtermonths(["jan", "Jan", "January", "word"])

	names1 = NER.print_names_file("/home/james/Desktop/India.txt")

	names2 = NER.print_names_file('/home/james/Desktop/Tintin.txt')
	names11 = []
	names22 = []

	for name in names1:
		for part in name.split(" "):
			names11.append(part)



	for name in names2:
		for part in name.split(" "):
			names22.append(part)

	both = set(names11) & set(names22)


	print "Common names:"
	for x in both:
		print x











