import serial

# Read from the file
with open('teamy.csv', 'r') as file:
    iter = 2
    first = True
    for line in file:
        if(not first):
            array = line.split(",")
            country, uni, team_name, num, pit, insp = array

            # Do something with the country, name, university, and car number
            # print(f"({iter}, {team_name}, {uni}, {country}, )")
            iter = iter + 1
        else:
            first = False
