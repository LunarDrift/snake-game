from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 50 # Lower the number, faster the game
SPACE_SIZE = 50
BODY_PARTS = 3 # Starting number of body parts snake has
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BG_COLOR = "#000000"

blink_job = None

class Snake:
    
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0]) # Snake should start at top left corner

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag='snake')
            self.squares.append(square)

class Food:
    
    def __init__(self):

        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

# High Scores
def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0
    
def save_high_score(new_high_score):
    with open("highscore.txt", "w") as file:
        file.write(str(new_high_score))



def next_turn(snake, food):
    global score, high_score
    
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score

        score += 1

        if score > high_score:
            high_score = score
            save_high_score(high_score)

        label.config(text='Score:{} High Score: {}'.format(score, high_score))

        canvas.delete("food")

        food = Food()

    else:    

        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction    
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction            

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
        
    return False

def game_over():
    global score, high_score

    canvas.delete(ALL)

    #GAME OVER text on screen
    canvas.create_text(
        canvas.winfo_width() / 2, # Center text on screen width
        canvas.winfo_height() / 2 - 100, 
        font=('consolas', 70), # Font and size
        text="GAME OVER",
        fill="red",
        tag="gameover"
    )
    
    # Show final score
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        font=('consolas', 30),
        text=f"Score: {score}",
        fill="white",
        tag="score"
    )

    # Show high score
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2 + 40,
        font=('consolas', 30),
        text=f"High Score: {high_score}",
        fill="white",
        tag="highscore"
    )    


    # Create blinking restart text
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2 + 100,
        font=('consolas', 30),
        text="Press Enter to restart",
        fill="white",
        tag="restart"
    )

    fade_text() # Start fading animation

def restart_game():
    global snake, food, score, direction, blink_job

    # Cancel running blink job if it exists (So restart text doesn't blink faster and faster after each restart)
    if blink_job is not None:
        window.after_cancel(blink_job)
        blink_job = None

    canvas.delete(ALL) # Remove GAME OVER and existing snake/food

    # Reset score and starting direction
    score = 0
    direction = 'down'

    label.config(text='Score: {} High Score: {}'.format(score, high_score))

    snake = Snake()
    food = Food()

    next_turn(snake, food)

def fade_text(alpha=0, direction=1):
    global blink_job

    # Parse background color
    bg_r = int(BG_COLOR[1:3], 16)
    bg_g = int(BG_COLOR[3:5], 16)
    bg_b = int(BG_COLOR[5:7], 16)

    # Interpolate between BG_COLOR and white
    r = int(bg_r + (255 - bg_r) * alpha)
    g = int(bg_g + (255 - bg_g) * alpha)
    b = int(bg_b + (255 - bg_b) * alpha)

    color = f'#{r:02x}{g:02x}{b:02x}'
    canvas.itemconfig("restart", fill=color)

    # Reverse direction at edges
    if alpha >= 1:
        direction = -1
    elif alpha <= 0:
        direction = 1

    # Adjust fade speed (smaller step = smoother)
    alpha += direction * 0.05

    blink_job = window.after(50, fade_text, alpha, direction)


window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = 'down'
high_score = load_high_score()

label = Label(window, text="Score:{} High Score: {}".format(score, high_score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg = BG_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<Return>', lambda event: restart_game())


snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()