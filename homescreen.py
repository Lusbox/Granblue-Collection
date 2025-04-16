import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Granblue Fantasy Search")
root.configure(background="black")
root.geometry("720x480")
root.resizable(width=False, height=False)
root.minsize(720, 480)
root.maxsize(720, 480)


frm = tk.Frame(root, bg="black")
frm.grid(column=0, row=0, sticky="nsew")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)



def homescreen():
    for widget in frm.winfo_children():
        widget.destroy()

    label = tk.Label(frm, text="Item Name :",
                     font=("Arial", 14),
                     fg="white",
                     bg="black")

    vyrn_img = ImageTk.PhotoImage(Image.open("assets/Vyrn.webp"))
    vyrn = tk.Label(frm, image=vyrn_img, bg="black")
    
    lyria_image = Image.open("assets/lyria_reading.webp")
    lyria_image = lyria_image.crop((70, 0, lyria_image.width-70, lyria_image.height))
    photo_lyria = ImageTk.PhotoImage(lyria_image)
    lyria = tk.Label(frm, image=photo_lyria, bg="black")

    search_term = tk.StringVar()
    search_box = tk.Entry(frm, textvariable=search_term)

    label.grid(column=0, row=0, padx=5, pady=5)
    search_box.grid(column=0, row=0, columnspan=2, padx=5, pady=5)
    vyrn.grid(column=1, row=1, padx=5, pady=5)
    lyria.grid(column=0, row=1, padx=5, pady=5)

    frm.vyrn_photo = vyrn_img
    frm.lyria_photo = photo_lyria

    def search_results():
        for widget in frm.winfo_children():
            widget.destroy()

        result = tk.Label(frm, text=f"Number of {search_term.get()} in inventory : 4",
                        font=("Arial", 14),
                        fg="white",
                        bg="black")

        weapon_image = Image.open("assets/Weapon_b_1040906400.png")
        weapon_image = weapon_image.resize((weapon_image.width//2, weapon_image.height//2))
        weapon_photo = ImageTk.PhotoImage(weapon_image)
        weapon = tk.Label(frm, image=weapon_photo, bg="black")

        lyria_result = ImageTk.PhotoImage(Image.open("assets/lyria_heat.png"))
        lyria = tk.Label(frm, image=lyria_result, bg="black")

        back_button = tk.Button(frm, text="Back", command=homescreen)

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