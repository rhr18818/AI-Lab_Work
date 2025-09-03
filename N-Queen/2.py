## doing it myself


#step 3 --- is valid 
def isValid(board,row,col):
    #up
    for i in range(row):
        if board[i][col] == 'Q':
            return False
        
    #left-diagnal
    i, j = row, col
    while i >= 0 and j >= 0:
        if board[i][j] == 'Q':
            return False
        i -= 1
        j -= 1
        
    #right-diagnal
    i, j = row, col
    while i >= 0 and j < n:
        if board[i][j] == 'Q':
            return False
        i -= 1
        j += 1
        
    return True
        

#step 2 -- solve funciton

def solve(board,row,result):
    if row == n:
        result.append(["".join(r) for r in board])  # .join covert into string for better visual , r loop each row
        return
    for col in range(n):
        if isValid(board, row, col):
            board[row][col] = 'Q'   # place queen
            solve(board, row + 1,result)   # move to next row
            board[row][col] = '.' 
    
#step 1 create the board
n = int(input("Enter the size of the chessboard (N): "))    
result = []
board = [["." for _ in range(n)] for _ in range(n)]
solve(board,0,result)
#print(board)
print(f"Total number of solutions for {n}-Queens: {len(result)}")
print()
print(result)