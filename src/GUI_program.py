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

class GUI:
    root = tk.Tk()
    root.title("Peg Solitaire")
    root.geometry("1000x500")

    #frame = tk.Frame(root, height=500, width=1000)
    #frame.pack(padx=10, pady=10)

    label = tk.Label(root, text="Peg Solitaire")
    #label.pack()
    label.grid(row=0, column=0, sticky='n')

    canvas = tk.Canvas(root, height=30, width=400)
    line1 = canvas.create_line(100, 10, 400, 10, fill="black")
    line2 = canvas.create_line(120, 20, 380, 20, fill="black")
    #canvas.pack()
    canvas.grid(row=0, column=1)

    button_frame = tk.Frame(root)
    type_label = tk.Label(button_frame, text="Board Type")
    type_label.pack(anchor="w")
    var = tk.StringVar(button_frame, "1")
    buttons = {"English": "1", "Hexagon": "2", "Diamond": "3"}
    for (text, value) in buttons.items():
        (tk.Radiobutton(button_frame, text=text, variable=var, value=value)
        .pack(anchor="w"))
    button_frame.grid(row=1, column=0, padx=5)


    root.mainloop()