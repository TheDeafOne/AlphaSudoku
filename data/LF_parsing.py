import csv

def rewrite():
    file = open('./initial_boards/new_sudoku_dataset_tmp.csv','w', newline='')
    writer = csv.writer(file)
    f = open('./initial_boards/new_sudoku_dataset.csv')
    reader = csv.reader(f)
    for row in reader:
        sr = row[0]
        # print(sr)
        if len(sr) > 20:
            writer.writerow([sr])
    
            

def read_sudoku_set():
    f = open('./initial_boards/new_sudoku_dataset_tmp.csv')
    reader = csv.reader(f)
    cnt = 0
    lr = '80'
    for row in reader:
        # if 
        # if row[2] != lr:
        #     print(row[2], 'at',cnt)
        #     lr = row[2]
        if cnt % 10000 == 0:
            print(row)
        # print(len(''.join(row)))
        # row = row[0]
        # print(row, row.count('0'))
        cnt += 1
            
    print(cnt)

if __name__ == "__main__":
    # rewrite()
    read_sudoku_set()
    pass