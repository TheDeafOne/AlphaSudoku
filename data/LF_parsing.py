import csv

def rewrite():
    file = open('./data/initial_boards/sudoku_dataset.csv','w', newline='')
    writer = csv.writer(file)
    f = open('./data/initial_boards/sudoku.csv')
    reader = csv.reader(f)
    
    vals = {}
    for line in reader:
        if len(line) > 0:
            cnt = line[0].count('0')
            if cnt in vals:
                vals[cnt].append(line)
            else:
                vals[cnt] = [line]

    for val in sorted(vals.keys()):
        for row in vals[val]:
            writer.writerow(row)

def read_sudoku_set():
    f = open('./data/initial_boards/sudoku_dataset.csv')
    reader = csv.reader(f)
    cnt = 0
    for row in reader:
        if cnt % 90000 == 0:
            print(len(''.join(row)))
            row = row[0]
            print(row, row.count('0'))
            
        cnt += 1

if __name__ == "__main__":
    # rewrite()
    # read_sudoku_set()
    pass