import tkinter as tk
import json
from PIL import Image, ImageTk
from enum import Enum


root = tk.Tk()
root.title("Granblue Fantasy Collection")
root.configure(background="black")
root.geometry("720x480")
root.resizable(False, False)

frm = tk.Frame(root, bg="black")
frm.grid(column=0, row=0, sticky="nsew")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

with open('data/characters.json', 'r') as file:
    characters = json.load(file)

with open('data/weapons.json', 'r') as file:
    weapons = json.load(file)

def homescreen():
    for widget in frm.winfo_children():
        widget.destroy()
    
    kumbhi_image = Image.open("assets/misc/Kumbhira_my_love.png")
    kumbhi_image = kumbhi_image.crop((70, 90, kumbhi_image.width-50, kumbhi_image.height-50))
    photo_kumbhi = ImageTk.PhotoImage(kumbhi_image)
    kumbhi = tk.Label(frm, image=photo_kumbhi, bg="black")
    kumbhi.place(relx=0.1, rely=0)
    frm.kumbhi_photo = photo_kumbhi

    chars = tk.Button(frm, text="Characters", command=owned_chars, bg="#333", fg="white", width=15, relief=tk.RAISED, borderwidth=3)
    chars.place(relx=0.15, rely=0.3, anchor='center')

    weapons = tk.Button(frm, text="Weapons", command=False, bg="#333", fg="white", width=15, relief=tk.RAISED, borderwidth=3)
    weapons.place(relx=0.15, rely=0.38, anchor='center')

    summons = tk.Button(frm, text="Summons", command=False, bg="#333", fg="white", width=15, relief=tk.RAISED, borderwidth=3)
    summons.place(relx=0.15, rely=0.46, anchor='center')

    add = tk.Button(frm, text="Add Item", command=add_item, bg="#333", fg="white", width=15, relief=tk.RAISED, borderwidth=3)
    add.place(relx=0.15, rely=0.54, anchor='center')

    search = tk.Button(frm, text="Search Inventory", command=search_menu, bg="#333", fg="white", width=15, relief=tk.RAISED, borderwidth=3)
    search.place(relx=0.15, rely=0.62, anchor='center')

def owned_chars():
    for widget in frm.winfo_children():
        widget.destroy()
    
    char_title = tk.Label(frm, text="Character List", font=("Arial", 14), fg="white", bg="black")
    char_title.place(relx=0.5, rely=0.05, anchor='center')

    back_button = tk.Button(frm, text="Back", command=homescreen, bg="#333", fg="white", width=8, relief=tk.RAISED, borderwidth=3)
    back_button.place(relx=0.5, rely=0.9, anchor='center')

    char_frame = tk.Frame(frm, bg="black")
    char_frame.place(relx=0.05, rely=0.2)

    frm.photo_references = []

    chars_per_row = 5

    for i, char in enumerate(characters):
        row = i // chars_per_row
        col = i % chars_per_row
        
        if char["obtained"] == True:
            img = ImageTk.PhotoImage(Image.open(char["image"]))
            frm.photo_references.append(img)

            char_image = tk.Label(char_frame, image=img, bg="black")
            char_image.grid(row=row, column=col)

def add_item():
    for widget in frm.winfo_children():
        widget.destroy()

    add_title = tk.Label(frm, text="Add Item", font=("Arial", 14), fg="white", bg="black")
    add_title.place(relx=0.5, rely=0.05, anchor='center')

    back_button = tk.Button(frm, text="Back", command=homescreen, bg="#333", fg="white", width=8, relief=tk.RAISED, borderwidth=3)
    back_button.place(relx=0.5, rely=0.9, anchor='center')

    element = tk.StringVar()

    def available_chars():
        for widget in frm.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()

        char_frame = tk.Frame(frm, bg="black")
        char_frame.place(relx=0.05, rely=0.2)

        frm.photo_references = []

        chars_per_row = 5
        element_choice = element.get()

        for i, char in enumerate(characters):
            row = i // chars_per_row
            col = i % chars_per_row
            if char["element"] == element_choice:
                img = ImageTk.PhotoImage(Image.open(char["image"]))
                frm.photo_references.append(img)

                checkbox_var = tk.BooleanVar(value=char.get("obtained", False))
                checkbox = tk.Checkbutton(char_frame, image=img, bg="black", variable=checkbox_var, command=lambda i=i, var=checkbox_var: update_character(i, var.get()))
                checkbox.grid(row=row, column=col)

    def update_character(index, obtained):
        characters[index]["obtained"] = obtained
        with open('data/characters.json', 'w') as file:
            json.dump(characters, file, indent=2)

    fire = tk.Checkbutton(frm, text="Fire", command=available_chars, width=4, variable=element, onvalue='fire')
    water = tk.Checkbutton(frm, text="Water", command=available_chars, width=4, variable=element, onvalue='water')
    earth = tk.Checkbutton(frm, text="Earth", command=available_chars, width=4, variable=element, onvalue='earth')
    wind = tk.Checkbutton(frm, text="Wind", command=available_chars, width=4, variable=element, onvalue='wind')
    light = tk.Checkbutton(frm, text="Light", command=available_chars, width=4, variable=element, onvalue='light')
    dark = tk.Checkbutton(frm, text="Dark", command=available_chars, width=4, variable=element, onvalue='dark')

    fire.place(relx=0.25, rely=0.12, anchor='center')
    water.place(relx=0.35, rely=0.12, anchor='center')
    earth.place(relx=0.45, rely=0.12, anchor='center')
    wind.place(relx=0.55, rely=0.12, anchor='center')
    light.place(relx=0.65, rely=0.12, anchor='center')
    dark.place(relx=0.75, rely=0.12, anchor='center')


    

def search_menu():
    for widget in frm.winfo_children():
        widget.destroy()

    vyrn_img = ImageTk.PhotoImage(Image.open("assets/misc/Vyrn.webp"))
    vyrn = tk.Label(frm, image=vyrn_img, bg="black")
    
    lyria_image = Image.open("assets/misc/lyria_reading.webp")
    lyria_image = lyria_image.crop((70, 0, lyria_image.width-70, lyria_image.height-20))
    photo_lyria = ImageTk.PhotoImage(lyria_image)
    lyria = tk.Label(frm, image=photo_lyria, bg="black")

    
    vyrn.place(relx=0.73, rely=0.5, anchor='center')
    lyria.place(relx=0.27, rely=0.5, anchor='center')

    label = tk.Label(frm, text="Item Name :", font=("Arial", 14), fg="white", bg="black")
    
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

        search_count = 0
        search = search_term.get()
        search_pic = ""
        
        for item in weapons:
            if search in item["name"].lower():
                search_count += 1
                search_pic = item["image"]
                
        if search_pic:
            search_image = Image.open(search_pic)
            search_image = search_image.resize((int(search_image.width//1.75), int(search_image.height//1.75)))
            search_photo = ImageTk.PhotoImage(search_image)
            weapon = tk.Label(frm, image=search_photo, bg="black")

            lyria = Image.open("assets//misc/lyria_jump.png")
            lyria = lyria.resize((int(lyria.width//1.75), int(lyria.height//1.75)))
            lyria_result = ImageTk.PhotoImage(lyria)
            lyria = tk.Label(frm, image=lyria_result, bg="black")

            frm.search = search_photo
            frm.lyria = lyria_result

            weapon.place(relx=0.3, rely=0.5, anchor='center')
            lyria.place(relx=0.7, rely=0.5, anchor='center')

        else:
            siero_pic = Image.open("assets/misc/Sierokarte_NPC.webp")
            result_pic = siero_pic.resize((int(siero_pic.width//1.2), int(siero_pic.height//1.2)))
            siero_result = ImageTk.PhotoImage(result_pic)
            siero = tk.Label(frm, image=siero_result, bg="black")
            siero.place(relx=0.5, rely=0.5, anchor='center')

            frm.siero = siero_result


        result = tk.Label(frm, text=f"Number of {search_term.get()} in inventory : {search_count}",
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