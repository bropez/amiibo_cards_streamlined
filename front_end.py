from tkinter import *
from tkinter import filedialog

import read_work as rw
import write_work as ww


root = Tk()
root.title("Amiibo Helper")


def open():
    root.filename = filedialog.askopenfilename(initialdir="/animalcrossing_amiibos/Animal Crossing/Cards/", 
    title="Select you character", 
    filetypes=(("bin files", "*.bin"), ("all files", "*")))
    
    correct_filepath = root.filename.replace("/", "\\")
    output = rw.main(correct_filepath)
    ww.main(output)

    # safe mode
    print("Now switching to safe mode.")
    rw.upload_reader()
    print("Safe mode ON.")


my_btn = Button(root, text="Choose amiibo to create", command=open).pack()

root.mainloop()
