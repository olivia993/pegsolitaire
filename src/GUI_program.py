import tkinter as tk

root = tk.Tk()

label = tk.Label(root, text="Peg Solitaire")
label.pack()

canvas = tk.Canvas(root, height=60, width=500)
line1 = canvas.create_line(100, 20, 400, 20, fill="black")
line2 = canvas.create_line(120, 50, 380, 50, fill="black")
canvas.pack()

check1 = tk.IntVar()
check2 = tk.IntVar()

checkbox1 = tk.Checkbutton(root, text="Checkbox 1", variable=check1, onvalue=1,
                           offvalue=0)

checkbox2 = tk.Checkbutton(root, text="Checkbox 2", variable=check2, onvalue=1,
                           offvalue=0)
checkbox1.pack()
checkbox2.pack()

var = tk.StringVar(root, "1")
buttons = {"RadioButton 1" : "1", "RadioButton 2" : "2"}
for (text, value) in buttons.items():
    (tk.Radiobutton(root, text=text, variable=var, value=value)
     .pack())

root.mainloop()