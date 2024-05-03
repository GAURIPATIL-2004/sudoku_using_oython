import tkinter as tk
from tkinter import messagebox, font
import time

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.points = 0
        self.board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        self.solution = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]
        self.entries = [[0]*9 for _ in range(9)]
        self.create_board()

    def create_board(self):
        # Create font
        entry_font = font.Font(size=16, weight='bold')
        button_font = font.Font(size=14, weight='bold')

        # Create colors
        bg_color = "#F0F0F0"  # Light gray
        entry_color = "#FFFFFF"  # White
        button_color = "#4CAF50"  # Green
        text_color = "#000000"   # Black

        # Create frame for the Sudoku grid
        sudoku_frame = tk.Frame(self.root, bg=bg_color)
        sudoku_frame.grid(row=0, column=0, padx=10, pady=10)

        for i in range(9):
            for j in range(9):
                # Create frame for each cell
                cell_frame = tk.Frame(sudoku_frame, bg=bg_color, highlightbackground="black", highlightthickness=1)
                cell_frame.grid(row=i, column=j, padx=1, pady=1)

                # Create entry or label for each cell
                if self.board[i][j] != 0:
                    self.entries[i][j] = tk.Label(cell_frame, text=self.board[i][j], font=entry_font, width=2, bg=entry_color, fg=text_color)
                    self.entries[i][j].pack(padx=5, pady=5)
                else:
                    self.entries[i][j] = tk.Entry(cell_frame, font=entry_font, width=2, bg=entry_color, fg=text_color, bd=0, highlightthickness=0)
                    self.entries[i][j].pack(padx=5, pady=5)

        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg=bg_color)
        buttons_frame.grid(row=1, column=0, padx=10, pady=(0, 10))

        # Solve button
        solve_button = tk.Button(buttons_frame, text="Solve", font=button_font, command=self.solve, bg=button_color, fg="white", padx=10, pady=5)
        solve_button.pack(side=tk.LEFT, padx=5)

        # Check button
        check_button = tk.Button(buttons_frame, text="Check", font=button_font, command=self.check, bg=button_color, fg="white", padx=10, pady=5)
        check_button.pack(side=tk.LEFT, padx=5)

        # Points label
        self.points_label = tk.Label(buttons_frame, text="Correct Cells: 0/81", font=font.Font(size=14, weight='bold'), bg=bg_color, fg=text_color)
        self.points_label.pack(side=tk.RIGHT, padx=5)

        # Set background color for root window
        self.root.configure(bg=bg_color)

    def is_valid(self, num, row, col):
        # Check row
        for i in range(9):
            if isinstance(self.entries[row][i], tk.Entry) and self.entries[row][i].get() == str(num):
                return False

        # Check column
        for i in range(9):
            if isinstance(self.entries[i][col], tk.Entry) and self.entries[i][col].get() == str(num):
                return False

        # Check 3x3 box
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if isinstance(self.entries[i + start_row][j + start_col], tk.Entry) and self.entries[i + start_row][j + start_col].get() == str(num):
                    return False

        return True

    def solve(self):
        if self.solve_sudoku():
            self.animate_solve_button()
            for i in range(9):
                for j in range(9):
                    if isinstance(self.entries[i][j], tk.Entry):
                        self.entries[i][j].config(state='normal')
                        self.entries[i][j].delete(0, 'end')
                        self.entries[i][j].insert(0, str(self.board[i][j]))
                        self.entries[i][j].config(state='disabled')
        else:
            messagebox.showinfo("Sudoku Solver", "No solution exists.")

    def animate_solve_button(self):
        for _ in range(3):
            self.root.update()
            time.sleep(0.1)
            self.root.config(bg="green")
            self.root.update()
            time.sleep(0.1)
            self.root.config(bg="#F0F0F0")

    def solve_sudoku(self):
        empty_cell = self.find_empty()
        if not empty_cell:
            return True
        else:
            row, col = empty_cell

        for num in range(1, 10):
            if self.is_valid(num, row, col):
                self.board[row][col] = num
                if isinstance(self.entries[row][col], tk.Entry):
                    self.entries[row][col].config(state='normal')
                    self.entries[row][col].delete(0, 'end')
                    self.entries[row][col].insert(0, str(num))
                    self.entries[row][col].config(state='disabled')

                if self.solve_sudoku():
                    return True

                self.board[row][col] = 0
                if isinstance(self.entries[row][col], tk.Entry):
                    self.entries[row][col].config(state='normal')
                    self.entries[row][col].delete(0, 'end')
                    self.entries[row][col].insert(0, "")
                    self.entries[row][col].config(state='disabled')

        return False

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if isinstance(self.entries[i][j], tk.Entry) and self.entries[i][j].get() == "":
                    return i, j
        return None

    def check(self):
        correct_cells = 0
        for i in range(9):
            for j in range(9):
                if isinstance(self.entries[i][j], tk.Entry):
                    if self.entries[i][j].get() == str(self.solution[i][j]):
                        correct_cells += 1
                    else:
                        self.entries[i][j].config(fg="red")
        self.points_label.config(text=f"Correct Cells: {correct_cells}/81")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")
    app = SudokuGUI(root)
    root.mainloop()
