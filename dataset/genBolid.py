# import serial
import random

# Read from the file
with open('nazwy_blidow.txt', 'r') as file:
    rank = 5
    for line in file:
        numer = random.randint(1, 300)
        team = random.randint(1, 60)
        clas = random.randint(1, 3)
        if clas: clas_name = "EV"
        else: clas_name = "CV"
        line = line.replace("\n","")

        
        # Do something with the country, name, university, and car number
        print(f"({numer}, {team}, {clas}, {line}, {rank})")
        rank += 1
        
