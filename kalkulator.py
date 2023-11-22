import tkinter as tk  # zaimportowanie biblioteki tkinter 

# Funkcja odpowiadajaca za sprawdzanie jak przycisk zostal wcisniety


def button_click(value):
    current_text = display_data.get()
    display_data.set(current_text + str(value))

# Funkcja odpowiadajaca za usuniencie wszystkiego z zmiennej display_data
def clear_command():
    display_data.set("")

# Funkcja odpowiadajanca za obliczenie rownania
def calculate():
    try:
        result = eval(display_data.get())
        display_data.set(result)
    except Exception as e:
        display_data.set("Math_Error")

# Utworzenie okna tkinter
root = tk.Tk()
root.title("Kalkulator")
root.resizable(0, 0)
root.config(background="black")

def quit():
    root.destroy()
quit_button =  tk.Button(root, width=15, height=2, text = "Wyjdz", command=quit, background="black" , foreground="red")
quit_button.grid(row=0, column=0)

# Zmienna przechowojaca rownanie 
display_data = tk.StringVar()
display_data.set("")

# Zmienna wyswietlajaca rownanie 
display = tk.Label(root, width=15, height=2, textvariable=display_data, background="black", foreground="white")
display.grid(row=0, column=1)

# Zmienna wyswietlajca przycisk usuwania 
clear = tk.Button(root, width=15, height=2, text="AC", command=clear_command, foreground="black", background="red")
clear.grid(row=4, column=0)

# Lista liczb
buttons = [
    "1", "2", "3",
    "4", "5", "6",
    "7", "8", "9",
]

row_val = 1
col_val = 0

# Funkcja odpowiadajca z tworzenie przyciskow liczb od 1 - 9
for button_text in buttons:
    button = tk.Button(root, width=15, height=2, text=button_text, command=lambda bt=button_text: button_click(bt),  foreground="white", background="grey")
    button.grid(row=row_val, column=col_val)
    col_val += 1
    if col_val > 2:
        col_val = 0
        row_val += 1

# Przycisk 0
button_0 = tk.Button(root, width=15, height=2, text="0", command=lambda bt="0": button_click(bt), foreground="white", background="grey")
button_0.grid(row=4, column=1)

operators = ["+", "-", "*", "/"]

row_val = 1
col_val = 3

# Funkcja odpowiadajanca za tworzenie przyciskow operatorow
for operator in operators:
    button = tk.Button(root, width=7, height=2, text=operator, command=lambda op=operator: button_click(op),background="darkorange", foreground="black")
    button.grid(row=row_val, column=col_val)
    row_val += 1

#Przycisk rowna sie
equal = tk.Button(root, width=15, height=2, text="=", command=calculate, foreground="black", background="green")
equal.grid(row=4, column=2)

root.mainloop()  # zamkniecie okna tkinter