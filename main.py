def create_board_from_string(s: str) -> [[[int]]]:
    if len(s) != 81:
        raise Exception("to create a board, string length must be 81")
    flattened_board = [l for l in s]
    for i in range(81):
        if flattened_board[i] in "123456789":
            flattened_board[i] = [int(flattened_board[i])]
        else:
            flattened_board[i] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    board = []
    for i in range(9):
        board.append([])
        for j in range(9):
            board[i].append(flattened_board[i * 9 + j])
    return board


def board_display_string(board: [[[int]]], placeholder_char: str) -> str:
    if len(placeholder_char) != 1:
        raise Exception("place holder char must be of length 1")
    s = "+-------+-------+-------+\n"
    for i in range(3):
        for j in range(3):
            s += "|"
            for k in range(3):
                s += " "
                for l in range(3):
                    number = board[i * 3 + j][k * 3 + l]
                    if len(number) > 1:
                        s += placeholder_char
                    else:
                        s += str(number[0])
                    s += " "
                s += "|"
            s += "\n"
        s += "+-------+-------+-------+\n"
    return s[:-1]


def is_board_valid(board: [[[int]]]) -> bool:
    for i in range(9):
        numbers_found = []
        for j in range(9):
            number = board[i][j]
            if len(number) > 1:
                continue
            if number[0] in numbers_found:
                return False
            numbers_found.append(number[0])
    for j in range(9):
        numbers_found = []
        for j in range(9):
            number = board[j][i]
            if len(number) > 1:
                continue
            if number[0] in numbers_found:
                return False
            numbers_found.append(number[0])
    for i in range(3):
        for j in range(3):
            numbers_found = []
            for k in range(3):
                for l in range(3):
                    number = board[i * 3 + k][j * 3 + l]
                    if len(number) > 1:
                        continue
                    if number[0] in numbers_found:
                        return False
                    numbers_found.append(number[0])
    return True


def copy_board(board: [[[int]]]) -> [[[int]]]:
    new_board = []
    for i in range(9):
        new_board.append([])
        for j in range(9):
            new_board[i].append([])
            for n in board[i][j]:
                new_board[i][j].append(n)
    return new_board


def next_free_space(board: [[int]]) -> (int, int):
    for i in range(9):
        for j in range(9):
            if len(board[i][j]) > 1:
                return (i, j)
    return None

def partial_solve_iteration(board: [[[int]]]) -> ([[[int]]], int):
    """
    there are many more techniques to use but this is enough to speed up the brute force
    """
    new_board = copy_board(board)
    changes_made = 0
    for row_no in range(9):
        for col_no in range(9):
            if len(board[row_no][col_no]) > 1:
                free_space = (row_no, col_no)
                square_pos = ((free_space[0] // 3) * 3, (free_space[1] // 3) * 3)
                # row
                for i in range(9):
                    if i == free_space[1]:
                        continue
                    number = new_board[free_space[0]][i]
                    if len(number) > 1:
                        continue
                    if number[0] in new_board[free_space[0]][free_space[1]]:
                        if len(new_board[free_space[0]][free_space[1]]) == 1:
                            return None
                        new_board[free_space[0]][free_space[1]].remove(number[0])
                        changes_made += 1
                # col
                for i in range(9):
                    if i == free_space[0]:
                        continue
                    number = new_board[i][free_space[1]]
                    if len(number) > 1:
                        continue
                    if number[0] in new_board[free_space[0]][free_space[1]]:
                        if len(new_board[free_space[0]][free_space[1]]) == 1:
                            return None
                        new_board[free_space[0]][free_space[1]].remove(number[0])
                        changes_made += 1
                # square
                for i in range(3):
                    for j in range(3):
                        if (square_pos[0] + i) == free_space[0] and (
                            square_pos[1] + j
                        ) == free_space[1]:
                            continue
                        number = new_board[square_pos[0] + i][square_pos[1] + j]
                        if len(number) > 1:
                            continue
                        if number[0] in new_board[free_space[0]][free_space[1]]:
                            if len(new_board[free_space[0]][free_space[1]]) == 1:
                                return None
                            new_board[free_space[0]][free_space[1]].remove(number[0])
                            changes_made += 1
    return (new_board, changes_made)


def partial_solve(board: [[[int]]]) -> [[[int]]]:
    new_board = copy_board(board)
    i = 0
    while True:
        partial_solve_iteration_result = partial_solve_iteration(new_board)
        if partial_solve_iteration_result is None:
            return None
        (new_board, changes_made) = partial_solve_iteration_result
        if changes_made == 0:
            print(f"{i} partial solve iterations")
            return new_board
        i += 1
        if i > 1_000_000:
            print(
                """
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
something has gone terribly wrong
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
            )
            exit()


class IntW:
    def __init__(self):
        self.x = 0


def solve(board: [[[int]]], curr_depth=0) -> [[[int]]]:
    """
    partially sove for optimisation
    go to an undefined place
    set it to 1
    repeat for 1 to 9 {
        if it is valid:
            sol = solve(new_board)
            if sol is not None:
                return sol
        go to next number
    }
    return None, its an unsolvable board
    """

    new_board = partial_solve(board)
    if new_board is None:
        return None
    print(board_display_string(new_board, " "))
    free_space = next_free_space(new_board)
    if free_space is None:
        return new_board
    for number in new_board[free_space[0]][free_space[1]]:
        new_board_2 = copy_board(new_board)
        new_board_2[free_space[0]][free_space[1]] = [number]
        if is_board_valid(new_board_2):
            solution = solve(new_board_2, curr_depth=curr_depth + 1)
            if solution is not None:
                return solution
    return None

with open("board_strings.txt") as f:
    board_strings = [line.strip() for line in f.readlines()]

for i, board_string in enumerate(board_strings):
    print(f"[{i}] {board_string}")

n = len(board_strings)
while n >= len(board_strings):
    try:
        n = int(input("Enter the number of the board to solve: "))
    except:
        pass

board = create_board_from_string(board_strings[n])

print("initial board:")
print(board_display_string(board, " "))
board = solve(board)
print("final board")
print(board_display_string(board, " "))
if is_board_valid(board):
    print("final board is valid")
else:
    print("final board is not valid, something has gone terribly wrong")
