# Python script to parse file and print lines containing 'gps'

def parse_gps_lines(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if 'GPS' in line:
            print(line.strip())

if __name__ == "__main__":
    filename = 'fack.txt'  # replace with your actual filename
    parse_gps_lines(filename)

