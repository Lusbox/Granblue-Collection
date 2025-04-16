from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

root = Tk()
root.title("Granblue Fantasy Search")
root.configure(background="black")

style = ttk.Style()
style.configure("TFrame", background="black")
style.configure("TLabel", background="black", foreground="white")
style.configure("TEntry", fieldbackground="white", foreground="black")

frm = ttk.Frame(root, style="TFrame", padding=10)
frm.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


label = ttk.Label(frm, text="Item Name :", style="TLabel")
photo_vyrn = ImageTk.PhotoImage(Image.open("assets/325px-Vyrn_Anime.webp"))
vyrn = ttk.Label(frm, image=photo_vyrn)

lyria_image = Image.open("assets/lyria_reading.webp")
lyria_image = lyria_image.crop((70, 0, lyria_image.width-70, lyria_image.height))
photo_lyria = ImageTk.PhotoImage(lyria_image)
lyria = ttk.Label(frm, image=photo_lyria)


search_term = StringVar()
search_box = ttk.Entry(frm, textvariable=search_term)


label.grid(column=0, row=0, padx=5, pady=5)
search_box.grid(column=0, row=0, columnspan=2, padx=5, pady=5)
vyrn.grid(column=1, row=1, padx=5, pady=5)
lyria.grid(column=0, row=1, padx=5, pady=5)

frm.vyrn_photo = photo_vyrn
frm.lyria_photo = photo_lyria

def on_entry(event):
    root.destroy()

search_box.bind('<Return>', on_entry)

root.mainloop()