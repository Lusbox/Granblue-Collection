import tkinter as tk
from PIL import Image, ImageTk
from test_inventory import *


root = tk.Tk()
root.title("Granblue Fantasy Search")
root.configure(background="black")
root.geometry("720x480")
root.resizable(False, False)

frm = tk.Frame(root, bg="black")
frm.grid(column=0, row=0, sticky="nsew")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

def homescreen():
    for widget in frm.winfo_children():
        widget.destroy()
    

    kumbhi_image = Image.open("assets/Kumbhira_my_love.png")
    kumbhi_image = kumbhi_image.crop((70, 90, kumbhi_image.width-50, kumbhi_image.height-50))
    photo_kumbhi = ImageTk.PhotoImage(kumbhi_image)
    kumbhi = tk.Label(frm, image=photo_kumbhi, bg="black")
    kumbhi.place(relx=0.1, rely=0)
    frm.kumbhi_photo = photo_kumbhi

    chars = tk.Button(frm, text="Characters", command=False, bg="#333", fg="white", width=15, relief=tk.RAISED, borderwidth=3)
    chars.place(relx=0.15, rely=0.3, anchor='center')

    weapons = tk.Button(frm, text="Weapons", command=False, bg="#333", fg="white", width=15, relief=tk.RAISED, borderwidth=3)
    weapons.place(relx=0.15, rely=0.38, anchor='center')

    summons = tk.Button(frm, text="Summons", command=False, bg="#333", fg="white", width=15, relief=tk.RAISED, borderwidth=3)
    summons.place(relx=0.15, rely=0.46, anchor='center')

    search = tk.Button(frm, text="Search Inventory", command=search_menu, bg="#333", fg="white", width=15, relief=tk.RAISED, borderwidth=3)
    search.place(relx=0.15, rely=0.54, anchor='center')

def search_menu():
    for widget in frm.winfo_children():
        widget.destroy()

    

    vyrn_img = ImageTk.PhotoImage(Image.open("assets/Vyrn.webp"))
    vyrn = tk.Label(frm, image=vyrn_img, bg="black")
    
    lyria_image = Image.open("assets/lyria_reading.webp")
    lyria_image = lyria_image.crop((70, 0, lyria_image.width-70, lyria_image.height-20))
    photo_lyria = ImageTk.PhotoImage(lyria_image)
    lyria = tk.Label(frm, image=photo_lyria, bg="black")

    
    vyrn.place(relx=0.73, rely=0.5, anchor='center')
    lyria.place(relx=0.27, rely=0.5, anchor='center')

    label = tk.Label(frm, text="Item Name :",
                     font=("Arial", 14),
                     fg="white",
                     bg="black")
    
    search_term = tk.StringVar()
    search_box = tk.Entry(frm, textvariable=search_term)

    label.place(relx=0.35, rely=0.1, anchor='center')
    search_box.place(relx=0.57, rely=0.1, anchor='center')

    frm.vyrn_photo = vyrn_img
    frm.lyria_photo = photo_lyria

    back_button = tk.Button(frm, text="Back", command=homescreen, bg="#333", fg="white", width=8, relief=tk.RAISED, borderwidth=3)
    back_button.place(relx=0.5, rely=0.9, anchor='center')

    

    def search_results():
        for widget in frm.winfo_children():
            widget.destroy()

        weapon_count = 0
        weapon = search_term.get().lower()
        weapon_pic = ""
        
        for item in gbf_invent:
            if item["name"] == weapon:
                weapon_count += 1
                weapon_pic = item["image"]
                
        if weapon_pic:
            weapon_image = Image.open(weapon_pic)
            weapon_image = weapon_image.resize((int(weapon_image.width//1.75), int(weapon_image.height//1.75)))
            weapon_photo = ImageTk.PhotoImage(weapon_image)
            weapon = tk.Label(frm, image=weapon_photo, bg="black")

            lyria = Image.open("assets/lyria_jump.png")
            lyria = lyria.resize((int(lyria.width//1.75), int(lyria.height//1.75)))
            lyria_result = ImageTk.PhotoImage(lyria)
            lyria = tk.Label(frm, image=lyria_result, bg="black")

            frm.weapon = weapon_photo
            frm.lyria = lyria_result

            weapon.place(relx=0.3, rely=0.5, anchor='center')
            lyria.place(relx=0.7, rely=0.5, anchor='center')

        else:
            siero_pic = Image.open("assets/Sierokarte_NPC.webp")
            result_pic = siero_pic.resize((int(siero_pic.width//1.2), int(siero_pic.height//1.2)))
            siero_result = ImageTk.PhotoImage(result_pic)
            siero = tk.Label(frm, image=siero_result, bg="black")
            siero.place(relx=0.5, rely=0.5, anchor='center')

            frm.siero = siero_result


        result = tk.Label(frm, text=f"Number of {search_term.get()} in inventory : {weapon_count}",
                        font=("Arial", 14),
                        fg="white",
                        bg="black")
        
        back_button = tk.Button(frm, text="Back", command=search_menu, bg="#333", fg="white", width=8, relief=tk.RAISED, borderwidth=3)
        back_button.place(relx=0.57, rely=0.9, anchor='center')
        home_buttom = tk.Button(frm, text="Home", command=homescreen, bg="#333", fg="white", width=8, relief=tk.RAISED, borderwidth=3)
        home_buttom.place(relx=0.42, rely=0.9, anchor='center')
        result.place(relx=0.5, rely=0.1, anchor='center')


    

    def on_entry(event):
        search_results()

    search_box.bind('<Return>', on_entry)



homescreen()
root.mainloop()