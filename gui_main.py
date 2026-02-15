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

# trail to track previous positions
trail = []  # Will store (row, col) tuples
max_trail_length = 3  # How many previous positions to show

# Move counter variables
current_move = 0
total_moves = 0

# Animation variables
animation_steps = 5  # Number of frames for smooth movement
is_animating = False

# canvas to draw on
canvas = tk.Canvas(window, width=800, height=800, bg="lightblue")
# pack the canvas with expand and fill to make it responsive
canvas.pack(expand=True, fill='both')

# draw grid on screen
# the rows & columns of the grid
def draw_grid():
    # Calculate grid dimensions (8x8 cells)
    grid_width = cell_size * 8
    grid_height = cell_size * 8
    
    # looping 8 lines, starting with 0-7
    for i in range(8):
        # draw horizontal lines - only up to 8 cells worth
        canvas.create_line(0, i * cell_size, grid_width, i * cell_size, fill="black")
        # draw vertical lines - only up to 8 cells worth
        canvas.create_line(i * cell_size, 0, i * cell_size, grid_height, fill="black")

    # coordinates on each square
    for row in range(8):
        # loop for columns
        for col in range(8):
            # find middle of cell
            x = col * cell_size + cell_size // 2
            y = row * cell_size + cell_size // 2
            # Scale font size based on cell size
            font_size = max(6, cell_size // 10)
            canvas.create_text(x, y + cell_size // 3, text=f"R{row},C{col}", fill="gray", font=("Arial", font_size))

# draw robot on grid
def draw_robot(anim_offset_x=0, anim_offset_y=0):
    # delete everything once called
    canvas.delete('all')
    # redraw grid
    draw_grid()
    
    # Draw the trail (previous positions) with fading effect
    for i, (trail_row, trail_col) in enumerate(trail):
        # Calculate position
        x1 = trail_col * cell_size
        y1 = trail_row * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size
        
        # Calculate opacity - older positions are more faded
        # i=0 is oldest, higher i is newer
        fade_amount = i / max(len(trail) - 1, 1)  # 0.0 to 1.0
        
        # Green fading: darker green to lighter green (matching lightgreen theme)
        # Older = darker green (60,100,60), Newer = lighter green (144,238,144) approaching lightgreen
        red = int(60 + fade_amount * 84)     # 60 -> 144
        green = int(100 + fade_amount * 138) # 100 -> 238
        blue = int(60 + fade_amount * 84)    # 60 -> 144
        color = f"#{red:02x}{green:02x}{blue:02x}"
        
        # Draw faded rectangle for trail
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="green")
        
        # Try to draw faded robot image
        try:
            robot_image = tk.PhotoImage(file="added pics\\chibi_boy - Copy.png")
            # Scale subsample based on cell size (larger cell = less subsample)
            subsample_factor = max(1, 1200 // cell_size)
            robot_image = robot_image.subsample(subsample_factor, subsample_factor)
            # Create semi-transparent effect by drawing on green background
            canvas.create_image(x1 + cell_size//2, y1 + cell_size//2, image=robot_image)
            canvas.image_trail = robot_image
        except:
            emoji_size = max(8, cell_size // 5)
            canvas.create_text(x1 + cell_size//2, y1 + cell_size//2, 
                             text="moving", fill="green", font=("Arial", emoji_size))
    
    # calculate current robot position with animation offset
    # calculate x pos on left side
    x1 = robot_col * cell_size + anim_offset_x
    # calculate y pos on top side
    y1 = robot_row * cell_size + anim_offset_y
    # calculate the x pos on right side
    x2 = x1 + cell_size
    # calculate y pos on bottom side
    y2 = y1 + cell_size
    # draw robot (text square/ picture later)
    canvas.create_rectangle(x1, y1, x2, y2, fill="lightgreen")

    # add robot image
    try:
        # Load your robot image (place image file in same folder as this script)
        robot_image = tk.PhotoImage(file="added pics\\chibi_boy.png")  
        # Scale subsample based on cell size
        subsample_factor = max(1, 1200 // cell_size)
        robot_image = robot_image.subsample(subsample_factor, subsample_factor)
        canvas.create_image(x1 + cell_size//2, y1 + cell_size//2, image=robot_image)
        # Keep reference to prevent garbage collection
        canvas.image = robot_image
    except:
        # Fallback to text if image not found - scale emoji with cell size
        emoji_size = max(12, cell_size // 4)
        canvas.create_text(x1 + cell_size//2, y1 + cell_size//2, text="Robot", fill="black", font=("Arial", emoji_size, "bold"))

# Animate the robot movement smoothly
def animate_movement(start_row, start_col, end_row, end_col, step=0):
    global is_animating
    
    if step <= animation_steps:
        # Calculate progress (0.0 to 1.0)
        progress = step / animation_steps
        
        # Calculate offset from starting position
        offset_x = (end_col - start_col) * cell_size * progress
        offset_y = (end_row - start_row) * cell_size * progress
        
        # Draw with animation offset (relative to START position)
        # Temporarily move robot back to start position for drawing
        old_row, old_col = robot_row, robot_col
        globals()['robot_row'] = start_row
        globals()['robot_col'] = start_col
        
        draw_robot(int(offset_x), int(offset_y))
        
        # Restore actual position
        globals()['robot_row'] = old_row
        globals()['robot_col'] = old_col
        
        # Schedule next animation frame (35ms = ~30fps)
        window.after(35, animate_movement, start_row, start_col, end_row, end_col, step + 1)
    else:
        # Animation complete
        is_animating = False
        draw_robot()  # Final draw at exact position

# move robot - ANIMATION
def move_robot():
    global robot_row, robot_col, trail, current_move, is_animating

    # Don't move if currently animating
    if is_animating:
        return
    
    is_animating = True
    current_move += 1

    # Add current position to trail before moving
    trail.append((robot_row, robot_col))
    
    # Keep trail limited to max_trail_length
    if len(trail) > max_trail_length:
        trail.pop(0)  # Remove oldest position

    # Store old position for animation
    start_row, start_col = robot_row, robot_col
    
    # Keep trying until we actually move
    direction = ""
    while robot_row == start_row and robot_col == start_col:
        # directions for robot to move
        directions = ["up", "down", "left", "right"]
        # choose random direction
        direction = random.choice(directions)

        # evaluate direction and movement of robot
        if direction == "up" and robot_row > 0:
            # move by decreasing # till 0
            robot_row -= 1
        elif direction == "down" and robot_row < 7:
            # move down row by increasing number
            robot_row += 1
        elif direction == "left" and robot_col > 0:
            # move left by decreasing col # till 0
            robot_col -= 1
        elif direction == "right" and robot_col < 7:
            # move right row by increasing number
            robot_col += 1

    # Start smooth animation from start to end position
    animate_movement(start_row, start_col, robot_row, robot_col, 0)
    
    # print to user the move
    print(f"Robot just moved {direction} - new position: Row {robot_row}, Column {robot_col}")

# function to handle calls by the user
def move_multiple_times():
    global total_moves, current_move
    
    # the # will shape the movement of the robot
    try:
        num_moves = int(entry.get())
    except ValueError:
        print("Please enter a valid number!")
        return
    
    # Reset counters
    total_moves = num_moves
    current_move = 0
    
    # Recursive function to handle moves with proper GUI delays
    def do_move(moves_left):
        if moves_left > 0:
            # each move
            move_robot()
            # Wait for animation to complete (~350ms for 10 frames at 35ms each)
            # Plus a small pause between moves
            window.after(450, do_move, moves_left - 1)
    
    # Start the movement sequence
    do_move(num_moves)

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

# Bind Enter key to trigger movement
def on_enter(event):
    move_multiple_times()

entry.bind("<Return>", on_enter)

# Function to handle window resize
def on_resize(event):
    global cell_size
    # Get current canvas size
    canvas_width = event.width
    canvas_height = event.height
    
    # Calculate new cell size based on smallest dimension to keep squares uniform
    # This ensures we have 8 perfect squares that fit in the window
    new_cell_size = min(canvas_width, canvas_height) // 8
    
    # Only redraw if cell size actually changed
    if new_cell_size != cell_size and new_cell_size > 0:
        cell_size = new_cell_size
        # Center the grid if there's extra space
        draw_robot()

# Bind canvas resize event
canvas.bind("<Configure>", on_resize)

# Draw initial grid and robot
draw_grid()
draw_robot()

# show on window
print("Robot awake and ready to clean!")
print(f"Robot starting pos Row: {robot_row}, Column: {robot_col}")

# main loop 
window.mainloop()