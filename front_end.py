from tkinter import *
from tkinter import filedialog

import read_work as rw
import write_work as ww


def open():
    root.filename = filedialog.askopenfilename(initialdir="/animalcrossing_amiibos/Animal Crossing/Cards/", 
    title="Select you character", 
    filetypes=(("bin files", "*.bin"), ("all files", "*")))
    
    correct_filepath = root.filename.replace("/", "\\")
    output = rw.main(correct_filepath)
    ww.safe_mode()
    ww.main(output)

    # safe mode
    print("Now switching to safe mode.")
    ww.safe_mode()
    print("Safe mode ON.")


def quit():
    root.destroy()


root = Tk()
root.title("Amiibo Helper")

select_lbl = Label(text="Please select an amiibo to create: ")
select_lbl.grid(row=1, column=0)

my_btn = Button(root, text="Choose amiibo", command=open)
my_btn.grid(row=1, column=1)

quit_btn = Button(root, text="Quit", command=quit)
quit_btn.grid(row=2, column=1, sticky="nsew")

root.mainloop()