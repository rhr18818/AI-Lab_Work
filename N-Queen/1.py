def solve_n_queens(n):
    def is_safe(board, row, col):
        for i in range(row):
            if board[i] == col:
                return False
            if abs(board[i] - col) == abs(i - row):
                return False
        return True
    
    def backtrack(board, row):
        if row == n:
            result.append(create_board(board))
            return
        
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(board, row + 1)
                board[row] = -1
    
    def create_board(board):
        result_board = []
        for i in range(n):
            row = ['.'] * n
            row[board[i]] = 'Q'
            result_board.append(''.join(row))
        return result_board
    
    result = []
    board = [-1] * n
    backtrack(board, 0)
    return result

def print_solution(solution, solution_num):
    print(f"Solution {solution_num}:")
    for row in solution:
        print(row)
    print()

def main():
    n = int(input("Enter the size of the chessboard (N): "))
    solutions = solve_n_queens(n)
    
    print(f"Total number of solutions for {n}-Queens: {len(solutions)}")
    print()
    
    if solutions:
        print("First few solutions:")
        for i, solution in enumerate(solutions[:3], 1):
            print_solution(solution, i)
    else:
        print("No solutions found.")

if __name__ == "__main__":
    main()# N - queen backtracking need to be implemented !

