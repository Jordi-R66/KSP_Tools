from tkinter import *

from game import Body

root = Tk()

root.geometry("500x300")
root.title("KSP Tools")

root.columnconfigure(0, minsize=50, weight=1)
root.rowconfigure([0, 1, 2], minsize=50, weight=1)

# ---------------------------------------------------------------------------------------

upperFrame: Frame = Frame(root)
upperFrame.grid(row=0, column=0)

centerFrame: Frame = Frame(root)
centerFrame.grid(row=1, column=0)

lowerFrame: Frame = Frame(root)
lowerFrame.grid(row=2, column=0)

# ---------------------------------------------------------------------------------------

mainLabel: Label = Label(upperFrame, text="KSP Tools", justify="center")
mainLabel.pack()



closeButton: Button = Button(lowerFrame, text="Close", command=root.destroy, background="red")
closeButton.pack()

root.mainloop()
