import tkinter as tk
import json
from PIL import Image, ImageTk, ImageOps
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

class ScreenUtils:
    def __init__(self, frame):
        self.frame = frame
    
    def clear(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def back_button(self, callback):
         back_button = tk.Button(self.frame, text="Back", command=callback, bg="#333", fg="white", width=8, relief=tk.RAISED, borderwidth=3)
         back_button.place(relx=0.57, rely=0.9, anchor='center')

    def home_button(self):
        home_buttom = tk.Button(self.frame, text="Home", command=homescreen, bg="#333", fg="white", width=8, relief=tk.RAISED, borderwidth=3)
        home_buttom.place(relx=0.42, rely=0.9, anchor='center')
  
screen_utils = ScreenUtils(frm)


def homescreen():
    screen_utils.clear()
    
    kumbhi_image = Image.open("assets/misc/Kumbhira_my_love.png")
    kumbhi_image = kumbhi_image.crop((70, 90, kumbhi_image.width-50, kumbhi_image.height-50))
    photo_kumbhi = ImageTk.PhotoImage(kumbhi_image)
    kumbhi = tk.Label(frm, image=photo_kumbhi, bg="black")
    kumbhi.place(relx=0.1, rely=0)
    frm.kumbhi_photo = photo_kumbhi

    chars = tk.Button(frm, text="Characters", command=owned_chars, bg="#333", fg="white", width=15, relief=tk.RAISED, borderwidth=3)
    chars.place(relx=0.15, rely=0.3, anchor='center')

    add = tk.Button(frm, text="Manage Chars", command=add_item, bg="#333", fg="white", width=15, relief=tk.RAISED, borderwidth=3)
    add.place(relx=0.15, rely=0.54, anchor='center')

    search = tk.Button(frm, text="Search Chars", command=search_menu, bg="#333", fg="white", width=15, relief=tk.RAISED, borderwidth=3)
    search.place(relx=0.15, rely=0.62, anchor='center')

def owned_chars():
    screen_utils.clear()
    
    char_title = tk.Label(frm, text="Character List", font=("Arial", 14), fg="white", bg="black")
    char_title.place(relx=0.5, rely=0.05, anchor='center')

    char_frame = tk.Frame(frm, bg="black")
    char_frame.place(relx=0.05, rely=0.2)

    screen_utils.back_button(homescreen)

    frm.photo_references = []
    frm.char_labels = {}

    chars_per_row = 5

    for i, char in enumerate(characters):
        row = i // chars_per_row
        col = i % chars_per_row

        if char["obtained"] == True:
            img = ImageTk.PhotoImage(Image.open(char["image"]))
            frm.photo_references.append(img)

            char_image = tk.Label(char_frame, image=img, bg="black")
            char_image.bind("<Button-1>", lambda event, c=char: show_char_detail(c))
            char_image.grid(row=row, column=col)

            frm.char_labels[i] = {"label": char_image, "char": char}

    filter_ele()
       

def add_item():
    screen_utils.clear()
    
    add_title = tk.Label(frm, text="Manage Characters", font=("Arial", 14), fg="white", bg="black")
    add_title.place(relx=0.5, rely=0.05, anchor='center')

    char_frame = tk.Frame(frm, bg="black")
    char_frame.place(relx=0.05, rely=0.2)

    screen_utils.back_button(homescreen)

    frm.photo_references = []
    frm.char_labels = {}

    chars_per_row = 5
    
    for i, char in enumerate(characters):
        row = i // chars_per_row
        col = i % chars_per_row
        
        orig_img = Image.open(char["image"])
        grey_img = ImageOps.grayscale(orig_img)
        grey_img = ImageOps.colorize(grey_img, black="black", white="grey")                     
        img = ImageTk.PhotoImage(orig_img)
        grey_photo = ImageTk.PhotoImage(grey_img)
        frm.photo_references.append(img)
        frm.photo_references.append(grey_photo)

        checkbox_var = tk.BooleanVar(value=char.get("obtained", False))
        checkbox = tk.Checkbutton(char_frame, image=grey_photo, selectimage=img, bg="black", variable=checkbox_var, command=lambda i=i, var=checkbox_var: update_character(i, var.get()))
        checkbox.grid(row=row, column=col)

        frm.char_labels[i] = {"label": checkbox, "char": char}

    def update_character(index, obtained):
        characters[index]["obtained"] = obtained
        with open('data/characters.json', 'w') as file:
            json.dump(characters, file, indent=2)

    filter_ele()


def search_menu():
    screen_utils.clear()
    
    vyrn_img = ImageTk.PhotoImage(Image.open("assets/misc/Vyrn.webp"))
    vyrn = tk.Label(frm, image=vyrn_img, bg="black")
    
    lyria_image = Image.open("assets/misc/lyria_reading.webp")
    lyria_image = lyria_image.crop((70, 0, lyria_image.width-70, lyria_image.height-20))
    photo_lyria = ImageTk.PhotoImage(lyria_image)
    lyria = tk.Label(frm, image=photo_lyria, bg="black")
   
    vyrn.place(relx=0.73, rely=0.5, anchor='center')
    lyria.place(relx=0.27, rely=0.5, anchor='center')

    screen_utils.back_button(homescreen)

    label = tk.Label(frm, text="Character Name :", font=("Arial", 14), fg="white", bg="black")
    
    search_term = tk.StringVar()
    search_box = tk.Entry(frm, textvariable=search_term)

    label.place(relx=0.33, rely=0.1, anchor='center')
    search_box.place(relx=0.59, rely=0.1, anchor='center')

    frm.vyrn_photo = vyrn_img
    frm.lyria_photo = photo_lyria

    def search_results():
        screen_utils.clear()
        
        search = search_term.get()
        search_pic = ""
        
        for item in characters:
            if search == item["name"].lower():
                search_pic = item["big_pic"]
                
        if search_pic:
            search_image = Image.open(search_pic)
            search_image = search_image.resize((int(search_image.width//1.75), int(search_image.height//1.75)))
            search_photo = ImageTk.PhotoImage(search_image)
            char_pic = tk.Label(frm, image=search_photo, bg="black")

            frm.search = search_photo
            char_pic.place(relx=0.5, rely=0.5, anchor='center')

        else:
            siero_pic = Image.open("assets/misc/Sierokarte_NPC.webp")
            result_pic = siero_pic.resize((int(siero_pic.width//1.2), int(siero_pic.height//1.2)))
            siero_result = ImageTk.PhotoImage(result_pic)
            siero = tk.Label(frm, image=siero_result, bg="black")
            siero.place(relx=0.5, rely=0.5, anchor='center')

            frm.siero = siero_result

        screen_utils.back_button(search_menu)
        screen_utils.home_button()
        
 
    def on_entry(event):
        search_results()

    search_box.bind('<Return>', on_entry)


def filter_ele():
    fire_var = tk.StringVar()
    water_var = tk.StringVar()
    earth_var = tk.StringVar()
    wind_var = tk.StringVar()
    light_var = tk.StringVar()
    dark_var = tk.StringVar()

    def filter_by_element():
            selected_elements = []
            if fire_var.get():
                selected_elements.append('fire')
            if water_var.get():
                    selected_elements.append('water')
            if earth_var.get():
                    selected_elements.append('earth')
            if wind_var.get():
                    selected_elements.append('wind')
            if light_var.get():
                    selected_elements.append('light')
            if dark_var.get():
                    selected_elements.append('dark')
            
            for char in frm.char_labels.values():
                    if not selected_elements:
                            char["label"].grid()
                    elif char["char"]["element"] in selected_elements:
                            char["label"].grid()
                    else:
                        char["label"].grid_remove()

    def reset_search():
        fire_var.set('')
        water_var.set('')
        earth_var.set('')
        wind_var.set('')
        light_var.set('')
        dark_var.set('')
        filter_by_element()

    fire = tk.Checkbutton(frm, text="Fire", command=filter_by_element, width=4, variable=fire_var, onvalue='fire', offvalue='')
    water = tk.Checkbutton(frm, text="Water", command=filter_by_element, width=4, variable=water_var, onvalue='water', offvalue='')
    earth = tk.Checkbutton(frm, text="Earth", command=filter_by_element, width=4, variable=earth_var, onvalue='earth', offvalue='')
    wind = tk.Checkbutton(frm, text="Wind", command=filter_by_element, width=4, variable=wind_var, onvalue='wind', offvalue='')
    light = tk.Checkbutton(frm, text="Light", command=filter_by_element, width=4, variable=light_var, onvalue='light', offvalue='')
    dark = tk.Checkbutton(frm, text="Dark", command=filter_by_element, width=4, variable=dark_var, onvalue='dark', offvalue='')

    clear = tk.Button(frm, text="Reset", width=4, command=reset_search)
    clear.place(relx=0.85, rely=0.12, anchor='center')

    fire.place(relx=0.25, rely=0.12, anchor='center')
    water.place(relx=0.35, rely=0.12, anchor='center')
    earth.place(relx=0.45, rely=0.12, anchor='center')
    wind.place(relx=0.55, rely=0.12, anchor='center')
    light.place(relx=0.65, rely=0.12, anchor='center')
    dark.place(relx=0.75, rely=0.12, anchor='center')


def show_char_detail(character):
    screen_utils.clear()
    
    big_pic = character["big_pic"]
    char_image = Image.open(big_pic)
    char_image = char_image.resize((int(char_image.width//1.75), int(char_image.height//1.75)))
    char_photo = ImageTk.PhotoImage(char_image)
    char_pic = tk.Label(frm, image=char_photo, bg="black")

    frm.char_pic = char_photo

    char_pic.place(relx=0.5, rely=0.5, anchor='center')

    screen_utils.back_button(owned_chars)
    screen_utils.home_button()



if __name__ == "__main__":
    homescreen()
    root.mainloop()