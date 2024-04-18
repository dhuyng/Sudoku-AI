import time
import json
import os
import tkinter as tk  
from tkinter import font 
import threading  
import copy 
from DFS import * 
from A_STAR import *




class SudokuMatrix(tk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.var = tk.StringVar()
        self.config(textvariable=self.var)
        self.var.trace_add('write', self.validate_input)
        self.get = self.var.get
        self.set =  self.var.set
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

    def validate_input(self, *args):    # CheckInput 0 -> 9
        value = self.var.get()
        if value.isdigit() and 0 < int(value) < 10:
            self.var_value = value
            self.config(fg="blue")  # Thiết lập màu chữ thành màu xanh dương
        else:
            self.var.set('')

    def on_focus_in(self, event):
        self.config(bg="yellow")  

    def on_focus_out(self, event):
        self.config(bg="white")   

class Sudoku(): 


    def __init__(self, window):  
        self.window = window  
        self.matrix_gui = [] 
        self.buttons = [] 
        self.checked_response = None    
        self.set_GUI() 
        self.matrix_values = [
        [0, 0, 3, 0, 2, 0, 6, 0, 0],
        [9, 0, 0, 3, 0, 5, 0, 0, 1],
        [0, 0, 1, 8, 0, 6, 4, 0, 0],
        [0, 0, 8, 1, 0, 2, 9, 0, 0],
        [7, 0, 0, 0, 0, 0, 0, 0, 8],
        [0, 0, 6, 7, 0, 8, 2, 0, 0],
        [0, 0, 2, 6, 0, 9, 5, 0, 0],
        [8, 0, 0, 2, 0, 3, 0, 0, 9],
        [0, 0, 5, 0, 1, 0, 3, 0, 0]
    ]   
        self.set_SudokuMatrix_GUI(self.matrix_values) 
        self.testcase_num = 0

    def set_GUI(self): 
        self.window.title("Sudoku Puzzle")  
        self.set_windows()  
        self.create_SodokuMatrix() 
        self.create_buttons()  
        self.checked_response = tk.Label(self.window, text="")  
        self.checked_response.grid(column=11, row=5, columnspan=2)  

    def set_windows(self):  
        self.window.geometry('900x600')  
        self.window.columnconfigure(0, minsize=80) 
        self.window.columnconfigure(10, minsize=40)  
        self.window.rowconfigure(0, minsize=20) 
        self.window.rowconfigure(10, minsize=20)

    def create_buttons(self):  # Hàm tạo các nút
        NewPuzzle_button = tk.Button(self.window, text="New Puzzle", command=self.new_puzzle, font=('Times New Roman', 12, 'bold'))  
        CheckSolution_button = tk.Button(self.window, text="Check Solution", command=self.check_solution, font=('Times New Roman', 12, 'bold')) 
        ClearAll_button = tk.Button(self.window, text="Clear All", command=self.set_SudokuMatrix_GUI, font=('Times New Roman', 12 , 'bold'))  
        DFS_button = tk.Button(self.window, text="DFS Algorithm", command=self.DFS_Solve, font=('Times New Roman', 12, 'bold')) 
        AStar_button = tk.Button(self.window, text="A* Algorithm", command=self.ASTAR_Solve, font=('Times New Roman', 12, 'bold'))  

        NewPuzzle_button.grid(column=1, row=11, columnspan=3)  
        CheckSolution_button.grid(column=4, row=11, columnspan=3)  
        ClearAll_button.grid(column=7, row=11, columnspan=3)  
        DFS_button.grid(column=11, row=1) 
        AStar_button.grid(column=11, row=2) 
        self.buttons = [NewPuzzle_button, CheckSolution_button, ClearAll_button, DFS_button, AStar_button] 

    def create_SodokuMatrix(self):  
        for row in range(9):  
            self.matrix_gui.append([])  
            for col in range(9): 
                input_box = SudokuMatrix(self.window, width=3, font=('Times New Roman', 28), justify='center') 
                input_box.configure(highlightbackground="black", highlightcolor="black", highlightthickness=1)  
                pady = (10, 0) if row % 3 == 0 else 0  
                padx = (10, 0) if col % 3 == 0 else 0  
                input_box.grid(column=col + 1, row=row + 1, padx=padx, pady=pady)  
                self.matrix_gui[row].append(input_box) 

    def set_SudokuMatrix_GUI(self, matrix=None):  
        if matrix is None:  
            matrix = self.matrix_values  
        for row_index, row in enumerate(self.matrix_gui):  
            for column_index, box in enumerate(row): 
                value = matrix[row_index][column_index]  
                if value != 0:  
                    box.set(value) 
                    box.config(state='readonly')  
                else:  
                    box.set('') 
                    box.config(state="normal")  
        self.reset_matrix_colour() 

    def get_matrix_values_from_GUI(self):  
        matrix = []  
        for index, row in enumerate(self.matrix_gui):  
            matrix.append([])  
            for col in row:  
                value = col.get()  
                matrix[index].append(int(value)) if value != "" else matrix[index].append(0)  
        return matrix  

    def check_solution(self):  
        response_font = font.Font(size=18, weight="bold")
        matrix = self.get_matrix_values_from_GUI()  
        if is_solution(matrix):  
            self.checked_response.config(text="CORRECT :)", fg="Green", font = response_font)  
        else:  
            self.checked_response.config(text="WRONG :(", fg="Red" ,font = response_font) 

    def DFS_Solve(self):  
        self.control_buttons(False)  
        self.set_SudokuMatrix_GUI()  
        matrix = copy.deepcopy(self.matrix_values)  
        solve_thread = threading.Thread(target=blind_search, args=(matrix, self), daemon=True)  
        solve_thread.start()  
       
       

    def ASTAR_Solve(self):  
        self.control_buttons(False)  
        self.set_SudokuMatrix_GUI()  
        matrix = copy.deepcopy(self.matrix_values) 
        solve_thread = threading.Thread(target=heuristic_search, args=(matrix, self), daemon=True) 
        solve_thread.start()  
    

    """
    def new_puzzle(self): 
        
        self.matrix_values= generate_new_matrix()  
        self.set_SudokuMatrix_GUI(self.matrix_values) 
        self.reset_matrix_colour() 
    """

    
    
    def new_puzzle(self):  # Hàm tạo bảng mới
       
        self.testcase_num = (self.testcase_num % 20) + 1

        testcase_dir = 'testcase'


        filename = os.path.join(testcase_dir, f"{self.testcase_num}.json")

        if os.path.exists(filename):
            with open(filename, 'r') as file:
                data = json.load(file)
            
                matrix_values = data
            

        self.matrix_values = matrix_values
        self.set_SudokuMatrix_GUI(matrix_values)
        self.reset_matrix_colour()
        






    def update_box(self, row, col, colour, value=None): 
        self.matrix_gui[row][col].config(fg=colour)  
        if value is not None: 
            if value == 0: 
                value = ""  
            self.matrix_gui[row][col].set(value)  

    def reset_matrix_colour(self): 
        for row in self.matrix_gui:  
            for col in row:  
                col.config(fg="black")  

    def control_buttons(self, clickable): 
        for button in self.buttons:  
            button.config(state=tk.NORMAL if clickable else tk.DISABLED)  



if __name__ == "__main__":  
    window = tk.Tk() 
    Sudoku(window)  
    window.mainloop()  
