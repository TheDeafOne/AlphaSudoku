import csv

def rewrite():
    
    f = open('./initial_boards/sudoku_dataset.csv')
    reader = csv.reader(f)
    fNo = 1
    file = open('./initial_boards/sudoku_dataset_' + str(fNo) +'.csv','w', newline='')
    writer = csv.writer(file)
    cnt = 1
    for row in reader:
        if cnt % 1000001 == 0:
            fNo += 1
            file = open('./initial_boards/sudoku_dataset_' + str(fNo) +'.csv','w', newline='')
            writer = csv.writer(file)
        # print(sr)
        writer.writerow([row[0]])
        cnt += 1
    
            

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
    rewrite()
    # read_sudoku_set()
    pass