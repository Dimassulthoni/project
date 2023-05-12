from tkinter import *
from tkinter import ttk

window = Tk()

#Window
lebar = 800
tinggi = 600

screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()

x = int((screenwidth/2)-(lebar/2))
y = int((screenheight/2)-(tinggi/2))

window.geometry(f"{lebar}x{tinggi}+{x}+{y}")
window.resizable(0,0)
window.title("BISIS")

#dropdown
Label(window, text='camera').grid(column=0)
ddbutton = ttk.Combobox(
    state="readonly",
    values=["default", "A", "B", "C"]
).grid(column=1, row=0)
Label(window, text='speaker').grid(column=2, row=0)
ddbutton = ttk.Combobox(
    state="readonly",
    values=["default", "A", "B", "C"]
).grid(column=3, row=0)
Button(window, text= "Mulai").grid(column=4, row= 0)
window.mainloop()