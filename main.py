# import library
import random

# Print a title and introduction so our user knows what is going on.
print("\n\n\t*** Training new cleaning robot ***\n")
print("\nHi I am Steve bot, and Iam using reinforment learning to train as a new night security robot at my home")
print("\nI am about move")
print("I can move the following directions.")
print("1 = north, 2 = south, 3 = east, 4 = west")

# function that moves robot manually per the user's input
def auto_robo():
    # a var thaht holds the amount of times a robot moves
    moves = 50
    # loop to move robot per user input
    print("\nI am about to move {moves} times on my own and record that movement.\n")
    for i in range(moves):
        # show moement on screen
        # Now I want to print out a random number for direction 1-4
        # Start with getting a random number an stuff the value into a valiable
        direction_number = random.randint(1,4)
        # tell user the move number
        print("\nOkay! now where's to next?! {i} of  {moves}.")

        # push direction number to file
        # Print the numeric direction our robot has moved
        print("\nI just moved " , direction_number)

        # open file to append
        with open("movement_history.txt", "a") as f:
            f.write(str(direction_number) + ",")


        # movement history
        print("This file IS GOING TO EXPLODE!!! With my movement data!!! ")
        # add movement to file


# function let user move bot manually
# one at a time
def manually_move_robo():



    #Loop
    # Create control variable booleen
    # set to yes to enter loop
    should_continue = "yes"
    #
    # loop
    while should_continue.lower() in ["yes", "y"]:
        
        # Now I want to print out a random number for direction 1-4
        # Start with getting a random number an stuff the value into a valiable
        direction_number = random.randint(1,4)


        # push direction number to file
        # Print the numeric direction our robot has moved
        print("\nI just moved " , direction_number)

        # open file to append
        with open("movement_history.txt", "a") as f:
            f.write(str(direction_number) + ",")


        # movement history
        print("This file the movement file noww ")
        # Ask bot to move again
        #collect user answer into booleen value
        should_continue = input("Would you like me to move again?")

# manual move function call
#manually_move_robo()
auto_robo()

