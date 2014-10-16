# Thanks sanchitgangwar @GitHub for the initial Interface of the Snake Game


# SNAKES GAME
# Use ARROW KEYS to play, SPACE BAR for pausing/resuming and Esc Key for exiting
 
import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
 
H = 20 # Final Constant Height                                                        
W = 40 # Final Constant Width                                                        
GAMESPEED = 50 # The initial GameSpeed

# Initialize Interface
curses.initscr()
win = curses.newwin(H, W, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1) 
 
key = KEY_RIGHT # Initializing values
score = 0
init_x = randint(5, H - 5)                                      
init_y = randint(5, W - 5)
food_x = randint(3, H - 3)
food_y = randint(3, W - 3)

snake = [[init_x, init_y],
         [init_x, init_y - 1],
         [init_x, init_y - 2]] # Initial snake co-ordinates                                   
food = [food_x, food_y] # First food co-ordinates                                          

win.addch(food[0], food[1], '#') # Prints the food
 
while key != 27: # While Esc key is not pressed                                                  
    win.border(0)
    win.addstr(0, 2, ' Score : ' + str(score) + ' ')    # Printing 'Score' and                
    win.addstr(0, W / 2 - 2, ' SNAKE ')                 # 'SNAKE' strings                                 
    win.timeout(GAMESPEED - (len(snake)/5 + len(snake)/10)%120) # Increases the speed of Snake as its length increases
    
    prevKey = key # Previous key pressed
    event = win.getch()
    key = key if event == -1 else event 
 
 
    if key == ord(' '): # If SPACE BAR is pressed, wait for another
        key = -1        # one (Pause/Resume)
        while key != ord(' '):
            key = win.getch()
        key = prevKey
        continue
 
    if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]: # If an invalid key is pressed
        key = prevKey
 
    # Calculates the new coordinates of the head of the snake. NOTE: len(snake) increases.
    # This is taken care of later at [1].
    snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1),
                     snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])
 
    # If snake crosses the boundaries, make it enter from the other side
    if snake[0][0] == 0: snake[0][0] = H - 2
    if snake[0][1] == 0: snake[0][1] = W - 2
    if snake[0][0] == H - 1: snake[0][0] = 1
    if snake[0][1] == W - 1: snake[0][1] = 1
    
    # If snake runs over itself
    # This line of code contains a lot of problems I think
    if snake[0] in snake[1:]: break
    
    if snake[0] == food: # When snake eats the food
        food = []
        score += 1
        while food == []:
            food = [randint(1, H - 2), randint(1, W - 2)] # Calculating next food's coordinates
            if food in snake: food = []
        win.addch(food[0], food[1], '#')
    else:    
        last = snake.pop() # [1] If it does not eat the food, length decreases
        win.addch(last[0], last[1], ' ')
    win.addch(snake[0][0], snake[0][1], '*')


    # The following four if/else statement is used to determine where is
    # the food and where the snake should go.
    # There is several bad thing about these lines of code:
    #   If the next food is on the same line with the snake, break
    #   The snake do not have its own selfawareness
    #   Other problems are still waiting for determination 
    if snake[0][0] == food[0] and snake[0][1] > food[1]:
        key = KEY_LEFT
    elif snake[0][0] == food[0] and snake[0][1] < food[1]:
        key = KEY_RIGHT
    elif snake[0][1] == food[1] and snake[0][0] > food[0]:
        key = KEY_UP
    elif snake[0][1] == food[1] and snake[0][0] < food[0]:
        key = KEY_DOWN
        
curses.endwin()

print("\nScore - " + str(score))
