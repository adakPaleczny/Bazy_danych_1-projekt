import random

file1 = open('nocleg_insert.txt', 'w')
file2 = open('pole_namiotowe_insert.txt', 'w')
file = open('nazwy_ulic_dla_nocleg.txt', 'r')
# Read from the file
# with open('nazwy_ulic_dla_nocleg.txt', 'r') as file:
id = 1

for line in file:
    output1 = ""
    output2 = ""
    array = line.split(",")
    name, number, size = array
    size = size.replace("\n","")
    output1 += f"({id}, {name}, {number}, {id})\n"
    output2 += f"({id}, {size})\n"
    # id += 1

    file1.write(output1)

    # with open('pole_namiotowe_insert.txt', 'w') as file2:
    file2.write(output2)

    # Do something with the country, name, university, and car number
    # print(f"({id}, {name}, {number}, {size})")
    id += 1

file.close()
file1.close()
file2.close()
