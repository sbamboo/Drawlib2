import os

def reset_write_head(x=0,y=0):
  line = "\033[{};{}H".format(x,y)
  print(line)

def saveN0():
  print("\033[s\033[0;0H")

def loadN0():
  print("\033[0;0H\033[u")

def fill_terminal(char,addX=0,addY=0,savePos=False):
  char = str(char)
  # Save the current position of the write head
  if savePos == True: print("\033[s", end="")
  # Get the terminal size
  columns, rows = os.get_terminal_size()
  columns = columns+addX
  rows = rows+addY
  # Print the character repeatedly to fill the terminal
  print(char * columns)
  for i in range(rows - 1):
    print(char * columns)
  # Return the write head to the original position
  if savePos == True: print("\033[u", end="")


def draw(x,y,st):
  st = str(st)
  # ANSI escape code for moving the cursor to a specific position
  move_cursor_code = f"\033[{y};{x}H"
  # ANSI escape code for resetting the cursor position
  reset_cursor_code = "\033[H"
  # Print the move cursor code, the text, and reset cursor code
  print(move_cursor_code + st + reset_cursor_code, end='', flush=True)