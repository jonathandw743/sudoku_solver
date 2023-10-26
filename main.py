import math
su = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0]]


##for i in range(len(su)):
##    for j in range(len(su[i])):
##        print("row:", i, "col:", j)
##        num = input()
##        while not ((num.isnumeric() and 0 < int(num) < 10) or num == ""):
##            num = input()
##
##        if num == "":
##            su[i][j] = 0
##        else:
##            su[i][j] = int(num)

def create_sudoku():
    sudoku = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
              [6, 0, 0, 1, 9, 5, 0, 0, 0],
              [0, 9, 8, 0, 0, 0, 0, 6, 0],
              [8, 0, 0, 0, 6, 0, 0, 0, 3],
              [4, 0, 0, 8, 0, 3, 0, 0, 1],
              [7, 0, 0, 0, 2, 0, 0, 0, 6],
              [0, 6, 0, 0, 0, 0, 2, 8, 0],
              [0, 0, 0, 4, 1, 9, 0, 0, 5],
              [0, 0, 0, 0, 8, 0, 0, 7, 9]]

    return sudoku

    code = input()
    code = code.split(",")

    for i in range(len(code)):
        code[i] = int(code[i])
    print(code)

    mode = 0

    codeIndex = 0
    i=0
    while i < 81:
        if mode % 2 == 1:
            sudoku[math.floor(i/9)][int(i%9)] = code[codeIndex]
            print("change")
        else:
            i += code[codeIndex]
            print(i)
            print("space")
        codeIndex += 1
        mode += 1
        if codeIndex == len(code):
            break
    return sudoku

def printa(a):
    print("start")
    for row in a:
        print(row)
    print("end")

def is_possible(s):
    #for each row
    for row in s:
        #for each number in that row
        #not using regular "for each in a list" because index must be stored
        for i in range(len(row)):
            #if it's not 0 (ie it's filled in)
            if row[i] != 0:
                #store the number
                e = row[i]
                #store the index of that number
                index = i
                #for each number in the row
                #not using regular "for each in a list" because index must be known
                for j in range(len(row)):
                    #if we're not looking at the same element
                    if j != index:
                        #if the stored number and the current number are the same
                        if row[j] == e:
                            #it's not possible
                            return False

    #for each column
    for colNo in range(len(s[0])):
        #for each number in that column
        #not using regular "for each in a list" because index must be stored
        for i in range(len(s)):
            #if it's not 0 (ie it's filled in)
            if s[i][colNo] != 0:
                #store the number
                e = s[i][colNo]
                #store the index of that number
                index = i
                #for each number in the row
                #not using regular "for each in a list" because index must be known
                for j in range(len(s)):
                    #if we're not looking at the same element
                    if j != index:
                        #if the stored number and the current number are the same
                        if s[j][colNo] == e:
                            #it's not possible
                            return False

    #for each 3x3 square
    for squareRowNo in range(0, len(s), 3):
        for squareColNo in range(0, len(s[squareRowNo]), 3):
            #convert it into a list
            square = []
            for i in range(squareRowNo, squareRowNo + 3):
                for j in range(squareColNo, squareColNo + 3):
                    square.append(s[i][j])
            #for each number in that square
            #not using regular "for each in a list" because index must be stored
            for i in range(len(square)):
                #if it's not 0 (ie it's filled in)
                if square[i] != 0:
                    #store the number
                    e = square[i]
                    #store the index of that number
                    index = i
                    #for each number in the row
                    #not using regular "for each in a list" because index must be known
                    for j in range(len(square)):
                        #if we're not looking at the same element
                        if j != index:
                            #if the stored number and the current number are the same
                            if square[j] == e:
                                #it's not possible
                                return False

    #if it's done everything and never returned false then it is possible
    return True

def solve(s):

    #set up possibilities map
    posMap = []
    print(len(s))
    for i in range(len(s)):
        posMap.append([])
        for j in s[i]:
            posMap[i].append([])

    printa(posMap)

    #set up solution
    newS = [row[:] for row in s]

    for i in range(len(newS)):
        for j in range(len(newS[i])):
            if newS[i][j] == 0:
                for num in range(1, 10):
                    posMap[i][j].append(num)
            else:
                posMap[i][j].append(newS[i][j])

    printa(posMap)

    changes = 1

    while changes > 0:

        changes = 0

        ###############################################################

        #NAKED PAIRS, TRIPLES, QUADS, QUINTS

        ###############################################################

        #for each row in the possibilities map
        for row in posMap:
            #for each item in this row
            for i in range(len(row)):#
                #set the list of indexes of subsets if this item to a blank list
                instances = []#
                #for each item in the row
                for j in range(len(row)):#
                    #if it a subset of the item we're checking 
                    if is_subset_of(row[i], row[j]):#
                        #add its index to the list
                        instances.append(j)#
                #if the length of the intances list (ie the number of instances)
                #is the length of the item we're checking
                if len(instances) >= len(row[i]):#
                    #go through each item in the row
                    for j in range(len(row)):#
                        #if the index of the current item is not in the instances list
                        #(ie the item does not count towards the instances)
                        if not (j in instances):
                            #go through each number from the item we're checking
                            for n in row[i]:#
                                #if its in the current item
                                if n in row[j]:#
                                    #remove it from the possiblities of that item
                                    row[j].remove(n)#
                                    #add to the changes made counter
                                    changes += 1

        #printa(posMap)

        for colNo in range(len(posMap[0])):
            for i in range(len(posMap)):
                instances = []
                for j in range(len(posMap)):
                    if is_subset_of(posMap[i][colNo], posMap[j][colNo]):
                        instances.append(j)
                if len(instances )>= len(posMap[i][colNo]):
                    for j in range(len(posMap)):
                        if not(j in instances):
                            for n in range(len(posMap[i][colNo])):
                                if posMap[i][colNo][n] in posMap[j][colNo]:
                                    posMap[j][colNo].remove(posMap[i][colNo][n])
                                    changes += 1

        #printa(posMap)
                           
        for squareRowNo in range(0, len(posMap), 3):
            for squareColNo in range(0, len(posMap[squareRowNo]), 3):
                square = []
                for i in range(squareRowNo, squareRowNo + 3):
                    for j in range(squareColNo, squareColNo + 3):
                        square.append(posMap[i][j])
                #printa(square)
                for i in range(len(square)):
                    instances = []
                    for j in range(len(square)):
                        if is_subset_of(square[i], square[j]):
                            instances.append(j)
                            #print(i, j)
                    if len(instances) >= len(square[i]):
                        #print("case")
                        for j in range(len(square)):
                            if not(j in instances):
                                for n in square[i]:
                                    if n in square[j]:
                                        #print("j", j)
                                        square[j].remove(n)
                                        #print("j", j)
                                        changes += 1
                #printa(square)
                for i in range(squareRowNo, squareRowNo + 3):
                    for j in range(squareColNo, squareColNo + 3):
                        #print(i * 3 + j)
                        posMap[i][j] = square[(i % 3) * 3 + (j % 3)]
                #printa(posMap)

        ######################################################################################

        #HIDDEN CANDIDATES

        ######################################################################################

        for squareRowNo in range(0, len(posMap), 3):
            for squareColNo in range(0, len(posMap[squareRowNo]), 3):
                square = []
                for i in range(squareRowNo, squareRowNo + 3):
                    for j in range(squareColNo, squareColNo + 3):
                        square.append(posMap[i][j])

                #for each number (1 to 9)
                for num in range(1, 10):
                    #clear instances list
                    instances = []
                    #for each item in the square
                    for i in range(len(square)):
                        #if this item contains that number
                        if num in square[i]:
                            #add the index of the item in the square list to the instances list
                            instances.append(i)

                    #for each row in the square
                    for i in range(0, 9, 3):
                        for j in range(len(instances)):
                            if not (i <= instances[j] < i + 3):
                                break
                            if j == len(instances) - 1:
                                for k in range(len(posMap[int(squareRowNo + i / 3)])):
                                    if not (squareColNo <= k < squareColNo + 3):
                                        if num in posMap[int(squareRowNo + i / 3)][k]:
                                            posMap[int(squareRowNo + i / 3)][k].remove(num)
                                            changes += 1

                    #for each column in the square
                    for i in range(3):
                        for j in range(len(instances)):
                            if ((instances[j] / 3) % 1) * 3 != i:
                                break
                            if j == len(instances) - 1:
                                for k in range(9):
                                    if not (squareRowNo <= k < squareRowNo + 3):
                                        if num in posMap[k][squareColNo + i]:
                                            posMap[k][squareColNo + i].remove(num)
                                            changes += 1
                
##                for i in range(squareRowNo, squareRowNo + 3):
##                    for j in range(squareColNo, squareColNo + 3):
##                        posMap[i][j] = square[(i % 3) * 3 + (j % 3)]
        
        printa(posMap)
        print("changes:", changes)
    
    for i in range(len(posMap)):
        for j in range(len(posMap[i])):
            newS[i][j] = posMap[i][j][0]

    return newS

def is_subset_of(mainset, subset):
    main = [e for e in mainset]
    sub = [e for e in subset]
    #print(main)
    #print(sub)
    if len(mainset) < len(subset):
        return False
    else:
        for subElement in subset:
            if subElement in main:
                sub.remove(subElement)
                main.remove(subElement)
                #print(main)
                #print(sub)
            else:
                return False
        if len(sub) != 0:
            return False
        
    return True
                    
##for i in range(2):
##    for j in range(9):
##        su = fill_in(su, i, j)
##        print_2D_array(su)

def is_board_valid(board):
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


def copy_board(board):
    new_board = []
    for i in range(9):
        new_board.append([])
        for j in range(9):
            new_board[i].append([])
            for n in board[i][j]:
                new_board[i][j].append(n)
    return new_board


def next_free_space(board):
    for i in range(9):
        for j in range(9):
            if len(board[i][j]) > 1:
                return (i, j)
    return None


def solve_with_backtracking(board, partial_solve, curr_depth=0):
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
    # printa(new_board)
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


su = create_sudoku()
printa(su)
solvedsu_logical = solve(su)
solvedsu_logical_and_backtracking = solve_with_backtracking(su, solve)

print("solved with logic:")
printa(solvedsu_logical)

print("solved with logic and backtracking:")
printa(solvedsu_logical_and_backtracking)

input("press enter to exit")

#print(sol == solvedsu)

##a = input()
##if a == "":
##    print("yes")

##a = [[[1, 6, 6], [3, 3, 6], [1, 3, 9]], [[7, 4, 1], [3, 5, 1], [9, 7, 8]], [[2, 2, 5] [5, 6, 3], [9, 2, 1]]]
##for i in a:
##    for j in i:
##        for k in j:
##            if 1 in j:
##                j.remove(1)
##print(a)

##a = [[[9, 1], [5, 1], [6, 3]], [[5, 1], [3, 7], [4, 1]], [[3, 6], [2, 5], [8, 1]]]
##for i in a:
##    for j in i:
##        if 1 in j:
##            j.remove(1)
##print(a)

##a = [[2, 4], [3, 6], [2, 1]]
##
##for row in a:
##    if 2 in row:
##        row.remove(2)
##
##print(a)

##a = [7, 8, 9]
##b = [7, 8]
##
##if is_subset_of(a, b):
##    print("sub")
