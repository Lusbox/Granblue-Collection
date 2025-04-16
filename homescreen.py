from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

root = Tk()
root.title("Granblue Fantasy Search")
root.configure(background="black")
root.geometry("720x480")
root.resizable(width=False, height=False)
root.minsize(720, 480)
root.maxsize(720, 480)

style = ttk.Style()
style.configure("TFrame", background="black")
style.configure("TLabel", background="black", foreground="white")
style.configure("TEntry", fieldbackground="white", foreground="black")

frm = ttk.Frame(root, style="TFrame")
frm.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

def homescreen():
    for widget in frm.winfo_children():
        widget.destroy()

    label = ttk.Label(frm, text="Item Name :", style="TLabel")

    vyrn_img = ImageTk.PhotoImage(Image.open("assets/Vyrn.webp"))
    vyrn = ttk.Label(frm, image=vyrn_img)
    
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

    frm.vyrn_photo = vyrn_img
    frm.lyria_photo = photo_lyria

    def search_results():
        for widget in frm.winfo_children():
            widget.destroy()

        result = ttk.Label(frm, text=f"Number of {search_term.get()} in inventory : 4")

        weapon_image = Image.open("assets/Weapon_b_1040906400.png")
        weapon_image = weapon_image.resize((weapon_image.width//2, weapon_image.height//2))
        weapon_photo = ImageTk.PhotoImage(weapon_image)
        weapon = ttk.Label(frm, image=(weapon_photo))

        lyria_result = ImageTk.PhotoImage(Image.open("assets/lyria_heat.png"))
        lyria = ttk.Label(frm, image=lyria_result)

        back_button = ttk.Button(frm, text="Back", command=homescreen)

        frm.weapon = weapon_photo
        frm.lyria = lyria_result
        
        result.place(relx=0.5, y= 50, anchor='center')
        weapon.place(x=50, rely=0.5, anchor='w')
        back_button.place(relx=0.5, y=420, anchor='center')
        lyria.place(x=670, rely=0.5, anchor='e')


    

    def on_entry(event):
        search_results()

    search_box.bind('<Return>', on_entry)

homescreen()
root.mainloop()