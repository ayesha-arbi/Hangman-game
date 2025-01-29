import random
from tkinter import *
from tkinter import messagebox

# Initialize root
root = Tk()
root.title("Hangman")
icon_image = PhotoImage(file="logo.png.png")  # Update path if needed
root.iconphoto(True, icon_image)
root.geometry('800x500+350+120')
root.config(background="#BAFFF9")

# ----------------------------------------------------------------------------------------Frames
frameright = Frame(root, width=340, height=350, bg="#6EBCC7", bd=5, relief="ridge")
frameright.place(x=400, y=100)

frameleft = Frame(root, width=340, height=350, bg="#6EBCC7", bd=5, relief="ridge")
frameleft.place(x=50, y=100)

# ---------------------------------------------------------------------------------------Labels
hangman = Label(root, text="Hangman", font=("Georgia", 40, "bold"), background="#BAFFF9", fg="black")
hangman.place(relx=0.5, rely=0.1, anchor="center")

# Right frame labels
wordlabel = Label(frameright, text="", font=("Arial", 20), bg="#6EBCC7", fg="black")
wordlabel.place(relx=0.5, rely=0.2, anchor="center")

chances = Label(frameright, text="", font=("Arial", 13), bg="#6EBCC7", fg="black")
chances.place(relx=0.5, rely=0.4, anchor="center")

incorrect_guesses_label = Label(frameright, text="Incorrect Guesses:", font=("Arial", 13), bg="#6EBCC7", fg="black")
incorrect_guesses_label.place(relx=0.5, rely=0.5, anchor="center")

incorrect_guesses = Label(frameright, text="", font=("Arial", 12), bg="#6EBCC7", fg="black")
incorrect_guesses.place(relx=0.5, rely=0.6, anchor="center")

final = Label(frameright, text="", font=("Arial", 13, "bold"), bg="#6EBCC7", fg="black")
final.place(relx=0.5, rely=0.7, anchor="center")

# ---------------------------------------------------------------------------------------Entry Box
input = StringVar()

def validate_input(char, value):
    """This function validates that only a single alphabet character can be entered"""
    if len(value) > 1:
        return False  # Reject if more than one character is entered
    if char.isalpha():  # Only accept alphabetic characters
        return True
    return False

# Add validation to Entry widget
vcmd = (root.register(validate_input), "%S", "%P")
enter = Entry(frameright, background="white", fg="black", font=("Arial", 12), width=13, justify="center", textvariable=input, validate="key", validatecommand=vcmd)
enter.focus_set()
enter.place(relx=0.5, rely=0.8, anchor="center")

# ---------------------------------------------------------------------------------------Button
Guess = Button(frameright, text="Guess", font=("Arial", 13), bg="#BAFFF9", fg="black", activebackground="#6EBCC7", command=lambda: hangman1())
Guess.place(relx=0.5, rely=0.9, anchor="center")

# --------------------------------------------------------------------------------------Backend Logic
wordlst = ["flower","program","pencil","market","game","hangman","turtle", "banana", "desert", "rocket", "garden", "basket", "puzzle", "castle", "shadow", "thunder"]

wordchosen = ""
dash = []
remaining_attempts = 6
incorrect_guess_list = []  # List to keep track of incorrect guesses

def chooseword():
    global wordchosen, dash, remaining_attempts
    wordchosen = random.choice(wordlst)
    dash = ["_"] * len(wordchosen)
    remaining_attempts = 6  # Resetting chances
    chances.configure(text="Chances Left: {}".format(remaining_attempts))
    update_word_display()


def update_word_display():
    wordlabel.configure(text=" ".join(dash))


def hangman1():
    global remaining_attempts
    guess = input.get().lower()
    enter.delete(0, END)

    if remaining_attempts > 0 and "_" in dash:
        if guess in wordchosen:
            for i, letter in enumerate(wordchosen):
                if letter == guess:
                    dash[i] = letter
            update_word_display()
        else:
            remaining_attempts -= 1
            incorrect_guess_list.append(guess)  # Add incorrect guess to the list
            update_incorrect_guesses()  # Update the display for incorrect guesses
            draw_hangman()  # Draw hangman on each incorrect guess

        chances.configure(text="Chances Left: {}".format(remaining_attempts))

        if "_" not in dash:
            final.configure(text="YOU WON!")
            ask_retry()  # Show retry message box after winning
        elif remaining_attempts == 0:
            final.configure(text=f"YOU LOST! Word was: {wordchosen}")
            ask_retry()  # Show retry message box after losing
    else:
        final.configure(text="Game Over!")


def fff(event):
    hangman1()


# Initialize the word and bind Enter key
chooseword()
root.bind("<Return>", fff)  # Correct case and format for the Return key

# Hangman drawing in the left frame
hangman_canvas = Canvas(frameleft, width=300, height=300, bg="#6EBCC7")
hangman_canvas.place(relx=0.5, rely=0.5, anchor="center")

# Draw hangman based on incorrect guesses
def draw_hangman():
    if remaining_attempts == 5:
        hangman_canvas.create_line(100, 50, 200, 50, width=3)  # Horizontal top of the gallows
        hangman_canvas.create_line(150, 50, 150, 150, width=3)  # Vertical post
    elif remaining_attempts == 4:
        hangman_canvas.create_line(150, 150, 200, 150, width=3)  # Crossbeam
    elif remaining_attempts == 3:
        hangman_canvas.create_oval(120, 150, 180, 210, width=3)  # Head
    elif remaining_attempts == 2:
        hangman_canvas.create_line(150, 210, 150, 250, width=3)  # Body
    elif remaining_attempts == 1:
        hangman_canvas.create_line(150, 250, 100, 300, width=3)  # Left leg
        hangman_canvas.create_line(150, 250, 200, 300, width=3)  # Right leg
    elif remaining_attempts == 0:
        hangman_canvas.create_line(150, 220, 100, 200, width=3)  # Left arm
        hangman_canvas.create_line(150, 220, 200, 200, width=3)  # Right arm

def update_incorrect_guesses():
    incorrect_guesses.configure(text=", ".join(incorrect_guess_list))

# Function to show message box for retry
def ask_retry():
    retry = messagebox.askyesno("Game Over", "Do you want to play again?")
    if retry:
        chooseword()  # Reset game and choose new word
        final.configure(text="")
        incorrect_guess_list.clear()  # Clear incorrect guesses
        update_incorrect_guesses()
        hangman_canvas.delete("all")  # Clear hangman drawing
    else:
        root.quit()  # Close the application

root.mainloop()
