# import libraries
import tkinter as tk
# random library
import random

# main window
window = tk.Tk()
# attributes title
window.title("Help Astro-boy move to another tile")

# cell size
cell_size = 100

# state of cleaner robot
# 0,0 is top left
robot_row = 0
robot_col = 0

# canvas to draw on
canvas = tk.Canvas(window, width=400, height=400, bg="lightblue")
# pack the canvas
canvas.pack()

# draw grid on screen
def draw_grid():
    # looping 5 lines, starting with 0-4
    for i in range(5):
        # draw horizontal lines
        canvas.create_line(0, i * cell_size, 400, i * cell_size, fill="black")
        # draw vertical lines
        canvas.create_line(i * cell_size, 0, i * cell_size, 400, fill="black")

# draw robot on grid
def draw_robot():
    # delete everything once called
    canvas.delete('all')
    # redraw grid
    draw_grid()
    # calculate robot position
    # calculate x pos on left side
    x1 = robot_col * cell_size
    # calculate y pos on top side
    y1 = robot_row * cell_size
    # calculate the x pos on right side
    x2 = x1 + cell_size
    # calaculate y pos on bottom side
    y2 = y1 + cell_size
    # draw robot (text sqare/ picture later)
    canvas.create_rectangle(x1,y1,x2,y2, fill="lightgreen")


    # add robot image
    # an addition by a.i.
    try:
        # Load your robot image (place image file in same folder as this script)
        robot_image = tk.PhotoImage(file="D://Wamp333//A.I._class//added pics//chibi_boy.png")  
        robot_image = robot_image.subsample(12, 11)  # resize the image
        canvas.create_image(x1 + cell_size//2, y1 + cell_size//2, image=robot_image)
        # Keep reference to prevent garbage collection
        canvas.image = robot_image
    except:
        # Fallback to text if image not found
        canvas.create_text(x1 + cell_size//2, y1 + cell_size//2, text="Robot", fill="black", font=("Arial",12,"bold"))
        # end of a.i. addition


# move robot
def move_robot():
    global robot_row, robot_col

    # directions for robot to move
    directions = ["up", "down", "left", "right"]
    # choose random direction
    directions = random.choice(directions)

    # random directions
    # evaluate direction and movement of robot
    if directions == "up":
        # move by decreasing # till 0
        robot_row = max(0, robot_row - 1)
    elif directions == "down":
        # move down row by increasing number
        robot_row = min(3, robot_row + 1)
    elif directions == "left":
        # move left by decreasing col # till 0
        robot_col = max(0, robot_col - 1)
    elif directions == "right":
        # move right row by increasing number
        robot_col = min(3, robot_col + 1)

    # redraw robot in new position
    draw_robot()
    # print to user the move
    print(f"This Robot just moved {directions} new position: Row {robot_row}, Column {robot_col}")

# function to handle calls by the user
def move_multiple_times():
    # the # will shape the movement of the robot
    num_moves = int(entry.get())
    # loop the # of moves
    for i in range(num_moves):
        # each move
        move_robot()
        # update window
        window.update()
        # delay for visibility
        window.after(350)

# creates label to inform user
label = tk.Label(window, text="Hey Right Here!" + "\n" + "Let's move Astro-boy" + "\n" + "You say the number okay?", font=("Arial", 12))
# pack label to show on screen
label.pack()

# text box for # of moves
entry = tk.Entry(window, font=("Arial", 12))
# pack item to show on screen
entry.pack()

# button to move robot
button = tk.Button(window, text="Let's move!", command=move_multiple_times, font=("Arial", 12), bg="lightgreen")
# pack button to show on screen
button.pack()

# 
draw_grid()
draw_robot()

# show on window
print("Robot awake and ready to clean!")
print(f"Robot stating pos Row: {robot_row}, Column: {robot_col}")

# main loop 
window.mainloop()
