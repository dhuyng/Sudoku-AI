from heapq import heappop, heappush
from random import choice, randint
import time
from third_party import psutil


def heuristic_search(matrix, gui=None):
     # start_time = time.time()  # Bắt đầu đo thời gian
    initial_memory = psutil.virtual_memory().used / (1024*1024)
    solved_matrix = A_star_solve(matrix, gui)
    final_memory = psutil.virtual_memory().used / (1024*1024)
    memory_consumption = (final_memory - initial_memory) 
    # end_time = time.time()  # Kết thúc đo thời gian
    # elapsed_time = end_time - start_time
    #print("DFS Execution Time:", elapsed_time, "seconds")
    print("DFS Memory Consumption::", abs(memory_consumption), "MB")

    if gui:
        gui.control_buttons(True)
    return solved_matrix


def A_star_solve(matrix, gui):
    time_sleep = 0.2
    open_set = [(0, matrix)]           
    while open_set:
        _, current_matrix = heappop(open_set) 
        if is_solution(current_matrix):
            return current_matrix
        row, col = get_best_empty_box(current_matrix)
        possible_solutions = get_valid_values(current_matrix, row, col)
        if possible_solutions:
            for number in possible_solutions:
                new_matrix = [row[:] for row in current_matrix]
                new_matrix[row][col] = number
                if gui:
                    gui.update_box(row, col, "Green", number)
                    time.sleep(time_sleep)
                heappush(open_set, (heuristic(new_matrix), new_matrix))
    return matrix


def heuristic(matrix):
    return sum(row.count(0) for row in matrix)

def get_best_empty_box(matrix):
    best_choices = 10  
    best_square = None
    for row in range(9):
        for col in range(9):
            if matrix[row][col] == 0:
                choices = len(get_valid_values(matrix, row, col))
                if choices < best_choices:
                    best_choices = choices
                    best_square = (row, col)
    return best_square



def get_valid_values(matrix, row, col):
    return row_value(matrix, row, col) & col_value(matrix, row, col) & square_value(matrix, row, col)


def row_value(matrix, row, col):
    domain = {1,2,3,4,5,6,7,8,9}
    for index, item in enumerate(matrix[row]):
        if index == col:
            continue
        elif item in domain:
            domain.remove(item)
    return domain


def col_value(matrix, row, col):
    domain = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    for row_index in range(9):
        if row_index == row:
            continue
        square = matrix[row_index][col]
        if square in domain:
            domain.remove(square)
    return domain


def square_value(matrix, row, col):
    domain = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    start_x = (col // 3) * 3
    start_y = (row // 3) * 3
    for y in range(start_y, start_y + 3):
        for x in range(start_x, start_x + 3):
            square_value = matrix[y][x]
            if y == row and x == col:
                continue
            elif square_value in domain:
                domain.remove(square_value)
    return domain

def is_solution(matrix):
    for row in range(9):
        for col in range(9):
            if matrix[row][col] not in get_valid_values(matrix, row, col):
                return False
    return True



def generate_new_matrix():
    new_matrix = [[0] * 9 for _ in range(9)]
    possible_numbers = [1,2,3,4,5,6,7,8,9]
    row = randint(0,8)
    for col in range(9):
        value = choice(possible_numbers)
        possible_numbers.remove(value)
        new_matrix[row][col] = value

    new_matrix = heuristic_search(new_matrix, None)

    for row in range(9):
        num_squares_to_delete = randint(7,9)
        for _ in range(num_squares_to_delete):
            col = randint(0,8)
            new_matrix[row][col] = 0

    return new_matrix
