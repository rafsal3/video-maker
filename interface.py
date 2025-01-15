from tkinter import *

def click_button():
    print("Button clicked!")

root = Tk()
root.title("My First GUI")

label = Label(root, text="Hello, World!")
label.pack()

button = Button(root, text="Click Me", command=click_button)
button.pack()

entry = Entry(root)
entry.pack()

root.mainloop()