import tkinter as tk

root = tk.Tk()
root.title("Ventana de prueba")
root.geometry("300x100")
label = tk.Label(root, text="¡Tkinter está funcionando!")
label.pack()
root.mainloop()
