import random

class LightsOut:
    def __init__(self, size=5):
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]  # 空の盤面で初期化
        self.generate_solvable_board()

    def display_board(self):
        for row in self.board:
            print(' '.join(str(cell) for cell in row))

    def toggle(self, row, col):
        if 0 <= row < self.size and 0 <= col < self.size:
            self.board[row][col] = 1 - self.board[row][col]
            if row > 0:
                self.board[row-1][col] = 1 - self.board[row-1][col]
            if row < self.size-1:
                self.board[row+1][col] = 1 - self.board[row+1][col]
            if col > 0:
                self.board[row][col-1] = 1 - self.board[row][col-1]
            if col < self.size-1:
                self.board[row][col+1] = 1 - self.board[row][col+1]

    def is_solved(self):
        return all(cell == 0 for row in self.board for cell in row)

    def generate_solvable_board(self):
        for _ in range(random.randint(0, self.size**6)):  # ランダムな回数でトグルを実行
            row = random.randint(0, self.size-1)
            col = random.randint(0, self.size-1)
            self.toggle(row, col)

    def reset_board(self):
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]  # 空の盤面で再初期化
        self.generate_solvable_board()
        
#ここからウィンドウアプリケーション用
import tkinter as tk
from tkinter import messagebox

class LightsOutApp(tk.Tk):
  def __init__(self, game):
    try:
      super().__init__()
    except tk.TclError as e:
      print(f"Error initializing Tkinter application;{e}")
      exit()
    self.game = game
    self.title("Lights Out Game")
    self.geometry("400x400")
    self.buttons = [[None for _ in range(game.size)] for _ in range(game.size)]
    self.initialize_ui()

  def initialize_ui(self):
    for row in range(self.game.size):
      for col in range(self.game.size):
        button = tk.Button(self, width=4, height=2,
          command=lambda r=row, c=col: self.on_button_click(r, c))
        button.grid(row=row, column=col)
        self.buttons[row][col] = button
    self.update_buttons()

  def on_button_click(self, row, col):
    self.game.toggle(row, col)
    self.update_buttons()
    if self.game.is_solved():
      messagebox.showinfo("Congratulations!", "You've solved the puzzle!")
      self.game.reset_board()
      self.update_buttons()

  def update_buttons(self):
    for row in range(self.game.size):
      for col in range(self.game.size):
        button = self.buttons[row][col]
        if self.game.board[row][col] == 1:
          button.config(bg="black", fg="white")
        else:
          button.config(bg="white", fg="black")
          
  def reset_to_initial_state(self):
    self.game.reset_board()
    self.update_buttons()
  
  def initialize_ui(self):
    for row in range(self.game.size):
        for col in range(self.game.size):
            button = tk.Button(self, width=4, height=2,
                               command=lambda r=row, c=col: self.on_button_click(r, c))
            button.grid(row=row, column=col)
            self.buttons[row][col] = button
    self.update_buttons()
    reset_button = tk.Button(self, text="Reset", command=self.reset_to_initial_state)
    reset_button.grid(row=self.game.size, columnspan=self.game.size)

if __name__ == "__main__":
    game = LightsOut()
    app = LightsOutApp(game)
    app.mainloop()
