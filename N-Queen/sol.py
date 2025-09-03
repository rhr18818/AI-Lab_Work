class Solution:
    def solveNQueens(self, n: int):
        result = []

        def isValid(board, row, col):
            # check vertically up
            for i in range(row):
                if board[i][col] == 'Q':
                    return False
            
            # check left diagonal upwards
            i, j = row, col
            while i >= 0 and j >= 0:
                if board[i][j] == 'Q':
                    return False
                i -= 1
                j -= 1

            # check right diagonal upwards
            i, j = row, col
            while i >= 0 and j < n:
                if board[i][j] == 'Q':
                    return False
                i -= 1
                j += 1
            
            return True

        def solve(board, row):
            # base case: if all rows are filled
            if row == n:
                result.append(["".join(r) for r in board])  # store a valid board
                return

            for col in range(n):
                if isValid(board, row, col):
                    board[row][col] = 'Q'   # place queen
                    solve(board, row + 1)   # move to next row
                    board[row][col] = '.'   # backtrack

        # initialize board with '.'
        board = [["." for _ in range(n)] for _ in range(n)]
        solve(board, 0)
        return result
