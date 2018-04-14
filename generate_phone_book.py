
import random

def generate_phone_book():

# open three external files for reading
# you can access each line of the file via its assoc. variable

    female_file = open('names.female', "r")
    male_file = open('names.male')
    family_file = open ('names.family')

# create some empty lists of female, male & surnames
    female_list = []
    male_list = []
    family_list = []

# add the names from the files to each list
    for line in female_file:
        fname = line.rstrip()
        female_list = female_list + [fname]

    for line in male_file:
        mname = line.rstrip()
        male_list = male_list + [mname]

    for line in family_file:
        aname = line.rstrip()
        family_list = family_list + [aname]

# files should be closed when you're finished with them

    female_file.close()
    male_file.close()
    family_file.close()



# now open a file to write the results to
# if the file doesn't already exist, it is created

    out = open("phone_book.txt", "w")

# randomly choose a surname
# once used, remove it from the surname list

    while len(family_list):
        surname = family_list[random.randrange(len(family_list))]
        family_list.remove(surname)

# randomly 50% should be male, 50% female
# once gender is decided, randomly pick a male or female name

        if random.randrange(1) == 1:
            index = random.randrange(len(male_list))
            first_name = male_list[index]
        else:
            index = random.randrange(len(female_list))
            first_name = female_list[index]
        
        print (first_name + " " + surname + " : ", end="", file=out)

# randomly generate a phone number

        for n in range(1,10) :
            print (random.randrange(start=1, stop=10), end="", file=out)

        print ("\n", end='', file=out)
    out.close()
        
        
generate_phone_book ()
        
