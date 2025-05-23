import tkinter as tk
import json
import os
from PIL import Image, ImageTk, ImageOps


root = tk.Tk()
root.title("Granblue Fantasy Collection")
root.configure(background="grey8")
root.geometry("1080x720")
root.resizable(False, False)
frm = tk.Frame(root, bg="grey8")
frm.grid(column=0, row=0, sticky="nsew")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

with open('data/characters.json', 'r') as file:
    characters = json.load(file)

class ScreenUtils:
    def __init__(self, frame):
        self.frame = frame
    
    def clear(self):
        for widget in self.frame.winfo_children():
            try:
                widget.grid_forget()
            except tk.TclError:
                 pass
            try:
                 widget.place_forget()
            except tk.TclError:
                 pass
            

    def back_button(self, callback):
         back_button = tk.Button(self.frame, text="Back", command=callback, bg="#333", fg="white", width=8, relief=tk.RAISED, borderwidth=3)
         back_button.place(relx=0.55, rely=0.95, anchor='center')

    def home_button(self):
        home_buttom = tk.Button(self.frame, text="Home", command=homescreen, bg="#333", fg="white", width=8, relief=tk.RAISED, borderwidth=3)
        home_buttom.place(relx=0.45, rely=0.95, anchor='center')

    def page_title(self, text):
         title = tk.Label(frm, text=text, font=("Arial", 14), fg="white", bg="grey8")
         title.place(relx=0.5, rely=0.05, anchor='center')
      
screen_utils = ScreenUtils(frm)


def initialize_widgets(frm):
    if not hasattr(frm, 'widgets_initialized') or not frm.widgets_initialized:
        frm.widgets_initialized = True
        kumbhi_image = Image.open("assets/misc/Kumbhira_my_love.png")
        photo_kumbhi = ImageTk.PhotoImage(kumbhi_image)

        frm.kumbhi = tk.Label(frm, image=photo_kumbhi, bg="grey8")
        frm.kumbhi_photo = photo_kumbhi
        frm.chars = tk.Button(frm, text="Characters", command=owned_chars, bg="#333", fg="white", width=15, relief=tk.RAISED, borderwidth=3)
        frm.add = tk.Button(frm, text="Manage", command=manage_characters, bg="#333", fg="white", width=15, relief=tk.RAISED, borderwidth=3)
        frm.search = tk.Button(frm, text="Search Chars", command=search_menu, bg="#333", fg="white", width=15, relief=tk.RAISED, borderwidth=3)


def homescreen():
    screen_utils.clear()
    initialize_widgets(frm)

    frm.kumbhi.place(relx=0.15, rely=0)
    frm.chars.place(relx=0.15, rely=0.3, anchor='center')
    frm.add.place(relx=0.15, rely=0.54, anchor='center')
    frm.search.place(relx=0.15, rely=0.62, anchor='center')
    

def owned_chars():
    screen_utils.clear()
    screen_utils.page_title("Character List")

    canvas = tk.Canvas(frm, bg="grey8")
    scrollbar = tk.Scrollbar(frm, orient="vertical", command=canvas.yview)

    canvas.place(relx=0.5, rely=0.2, anchor='n', relwidth=0.9, relheight=0.7)
    scrollbar.place(relx=0.95, rely=0.2, anchor='n', relheight=0.7)

    canvas.configure(yscrollcommand=scrollbar.set)

    char_frame = tk.Frame(frm, bg="grey8")
    canvas.create_window((0, 0), window=char_frame, anchor="nw")

    screen_utils.back_button(homescreen)
    details = tk.Label(frm, text="click portrait for character details", font=("Arial", 10), fg="white", bg="grey8")
    details.place(relx=0.1, rely=0.97, anchor='w')

    frm.photo_references = []
    frm.char_labels = {}

    chars_per_row = 10
    displayed_count = 0

    for i, char in enumerate(characters):
        row = displayed_count // chars_per_row
        col = displayed_count % chars_per_row

        if char.get('obtained', False) == True:
            error_displayed = False
            if not char.get("image") or char.get("image") and not os.path.isfile(char["image"]):
                error = tk.Label(char_frame, text=f"{char.get('name')} \n Image \n Not Found", font=("Arial", 8), fg="white", bg="grey8", width=12)
                error.grid(row=row, column=col, padx=4, pady=5)
                error_displayed = True
            if not error_displayed:
                img = ImageTk.PhotoImage(Image.open(char["image"]))
                frm.photo_references.append(img)

                char_image = tk.Label(char_frame, image=img, bg="grey8")
                char_image.bind("<Button-1>", lambda event, c=char: show_char_detail(c))
                char_image.grid(row=row, column=col, padx=5, pady=5)

                frm.char_labels[displayed_count] = {"label": char_image, "char": char}

            displayed_count += 1

    char_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    filter_ele()
       

def manage_characters():
    screen_utils.clear()
    screen_utils.page_title("Manage Characters")
    
    canvas = tk.Canvas(frm, bg="grey8")
    scrollbar = tk.Scrollbar(frm, orient="vertical", command=canvas.yview)

    canvas.place(relx=0.5, rely=0.2, anchor='n', relwidth=0.91, relheight=0.7)
    scrollbar.place(relx=0.96, rely=0.2, anchor='n', relheight=0.7)

    canvas.configure(yscrollcommand=scrollbar.set)

    char_frame = tk.Frame(frm, bg="grey8")
    canvas.create_window((0, 0), window=char_frame, anchor="nw")

    screen_utils.back_button(homescreen)

    frm.photo_references = []
    frm.char_labels = {}

    chars_per_row = 10
    
    for i, char in enumerate(characters):
        row = i // chars_per_row
        col = i % chars_per_row

        error_displayed = False
        if not char.get("image") or char.get("image") and not os.path.isfile(char["image"]):
            error = tk.Label(char_frame, text="Character Not \n Found", font=("Arial", 8), fg="white", bg="grey8", width=12)
            error.grid(row=row, column=col, padx=4, pady=5)
            error_displayed = True

        if not error_displayed:
        
            orig_img = Image.open(char["image"])
            grey_img = ImageOps.grayscale(orig_img)
            grey_img = ImageOps.colorize(grey_img, black="black", white="grey")                     
            img = ImageTk.PhotoImage(orig_img)
            grey_photo = ImageTk.PhotoImage(grey_img)
            frm.photo_references.append(img)
            frm.photo_references.append(grey_photo)

            if char['obtained'] == True:
                current_img = img
            else:
                current_img = grey_photo

            checkbox_var = tk.BooleanVar(value=char.get("obtained", False))
            checkbox = tk.Button(char_frame, image=current_img, bg="grey8")
            checkbox.configure(command=lambda i=i, var=checkbox_var, btn=checkbox, img=img, grey_img=grey_photo: update_character(i, var, btn, img, grey_img))
            checkbox.grid(row=row, column=col, padx=4, pady=5)

            frm.char_labels[i] = {"label": checkbox, "char": char}

    def update_character(index, var, btn, img, grey_img):
        if btn.cget('image') == str(img):
             btn.configure(image=grey_img)
             var.set(False)
        else:
             btn.configure(image=img)
             var.set(True)

        characters[index]["obtained"] = var.get()
        with open('data/characters.json', 'w') as file:
            json.dump(characters, file, indent=2)

    char_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    filter_ele()


def search_menu():
    screen_utils.clear()
    
    vyrn_img = ImageTk.PhotoImage(Image.open("assets/misc/Vyrn.webp"))
    vyrn = tk.Label(frm, image=vyrn_img, bg="grey8")
    
    lyria_image = Image.open("assets/misc/lyria_reading.webp")
    photo_lyria = ImageTk.PhotoImage(lyria_image)
    lyria = tk.Label(frm, image=photo_lyria, bg="grey8")
   
    vyrn.place(relx=0.73, rely=0.5, anchor='center')
    lyria.place(relx=0.27, rely=0.5, anchor='center')

    screen_utils.back_button(homescreen)

    label = tk.Label(frm, text="Character Name :", font=("Arial", 14), fg="white", bg="grey8")
    
    search_term = tk.StringVar()
    search_box = tk.Entry(frm, textvariable=search_term)

    label.place(relx=0.36, rely=0.1, anchor='center')
    search_box.place(relx=0.56, rely=0.1, anchor='center')

    frm.vyrn_photo = vyrn_img
    frm.lyria_photo = photo_lyria

    def search_results():
        screen_utils.clear()
        
        search = search_term.get()
        found = False
        
        for item in characters:
            if search == item["name"].lower():
               show_char_detail(item)
               found = True
               break

        if not found:
            siero_pic = Image.open("assets/misc/Sierokarte_NPC.webp")
            siero_result = ImageTk.PhotoImage(siero_pic)
            siero = tk.Label(frm, image=siero_result, bg="grey8")
            siero.place(relx=0.5, rely=0.5, anchor='center')
            not_found = tk.Label(frm, text="Character not found", bg="grey8", font=("Arial", 16), fg="white")
            not_found.place(relx=0.5, rely=0.1, anchor='center')

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
    ssr_var = tk.StringVar()
    sr_var = tk.StringVar()
    r_var = tk.StringVar()

    def filter_by_element():
            selected_filter = []
            if fire_var.get():
                selected_filter.append('Fire')
            if water_var.get():
                    selected_filter.append('Water')
            if earth_var.get():
                    selected_filter.append('Earth')
            if wind_var.get():
                    selected_filter.append('Wind')
            if light_var.get():
                    selected_filter.append('Light')
            if dark_var.get():
                    selected_filter.append('Dark')
            if ssr_var.get():
                    selected_filter.append('SSR')
            if sr_var.get():
                    selected_filter.append('SR')
            if r_var.get():
                    selected_filter.append('R')

            
            for char in frm.char_labels.values():
                    char_element = char["char"].get("element")
                    char_rarity = char["char"].get("rarity")

                    if not selected_filter:
                        char["label"].grid()
                    elif any(ele in selected_filter for ele in ['Fire', 'Water', 'Earth', 'Wind', 'Light', 'Dark']) and \
                        any(rar in selected_filter for rar in ['SSR', 'SR', 'R']):
                        if char_element in selected_filter and char_rarity in selected_filter:
                            char["label"].grid()
                        else:
                             char["label"].grid_remove()
                    elif char_element in selected_filter:
                        char["label"].grid()
                    elif char_rarity in selected_filter:
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
        ssr_var.set('')
        sr_var.set('')
        r_var.set('')
        filter_by_element()

    filter_frame = tk.Frame(frm, bg="grey8")
    filter_frame.place(relx=0.3, rely=0.08)

    fire = tk.Checkbutton(filter_frame, text="Fire", command=filter_by_element, width=4, variable=fire_var, onvalue='Fire', offvalue='')
    water = tk.Checkbutton(filter_frame, text="Water", command=filter_by_element, width=4, variable=water_var, onvalue='Water', offvalue='')
    earth = tk.Checkbutton(filter_frame, text="Earth", command=filter_by_element, width=4, variable=earth_var, onvalue='Earth', offvalue='')
    wind = tk.Checkbutton(filter_frame, text="Wind", command=filter_by_element, width=4, variable=wind_var, onvalue='Wind', offvalue='')
    light = tk.Checkbutton(filter_frame, text="Light", command=filter_by_element, width=4, variable=light_var, onvalue='Light', offvalue='')
    dark = tk.Checkbutton(filter_frame, text="Dark", command=filter_by_element, width=4, variable=dark_var, onvalue='Dark', offvalue='')
    ssr = tk.Checkbutton(filter_frame, text="SSR", command=filter_by_element, width=4, variable=ssr_var, onvalue='SSR', offvalue='')
    sr = tk.Checkbutton(filter_frame, text="SR", command=filter_by_element, width=4, variable=sr_var, onvalue='SR', offvalue='')
    r = tk.Checkbutton(filter_frame, text="R", command=filter_by_element, width=4, variable=r_var, onvalue='R', offvalue='')

    clear = tk.Button(frm, text="Reset", width=4, command=reset_search)
    clear.place(relx=0.85, rely=0.12, anchor='center')


    fire.grid(row=0, column=0, padx=5, pady=5)
    water.grid(row=0, column=1, padx=5, pady=5)
    earth.grid(row=0, column=2, padx=5, pady=5)
    wind.grid(row=0, column=3, padx=5, pady=5)
    light.grid(row=0, column=4, padx=5, pady=5)
    dark.grid(row=0, column=5, padx=5, pady=5)
    ssr.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
    sr.grid(row=1, column=2, columnspan=2, padx=5, pady=5)
    r.grid(row=1, column=3, columnspan=2, padx=5, pady=5)


def show_char_detail(character):
    screen_utils.clear()
    error_displayed = False
    if not character.get("big_pic") or character.get("big_pic") and not os.path.isfile(character["big_pic"]):
         error_displayed = display_error_img()
    
    if not error_displayed:
        try:
            big_pic = character["big_pic"]
            char_image = Image.open(big_pic)
            char_photo = ImageTk.PhotoImage(char_image)
            char_pic = tk.Label(frm, image=char_photo, bg="grey8")
            char_pic.place(relx=0.58, rely=0.55, anchor='center')
            frm.char_pic = char_photo
        except FileNotFoundError:
            display_error_img()

    char_details_frame = tk.LabelFrame(frm, relief=tk.RAISED, bg="grey8", fg="white")
    char_details_frame.place(relx=0.03, rely=0.25)

    char_name = tk.Label(char_details_frame, text=f"Name:   {character.get('name', 'Unknown')}", font=("Arial", 12), fg="white", bg="grey8")
    char_name.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    char_rarity = tk.Label(char_details_frame, text=f"Rarity:   {character.get('rarity', 'Unknown')}", font=("Arial", 12), fg="white", bg="grey8")
    char_rarity.grid(row=1, column=0, padx=5, pady=5, sticky='w')

    char_element = tk.Label(char_details_frame, text=f"Element:   {character.get('element', 'Unknown')}", font=("Arial", 12), fg="white", bg="grey8")
    char_element.grid(row=2, column=0, padx=5, pady=5, sticky='w')
    
    char_race = tk.Label(char_details_frame, text=f"Race:   {character.get('race', 'Unknown')}", font=("Arial", 12), fg="white", bg="grey8")
    char_race.grid(row=3, column=0, padx=5, pady=5, sticky='w')

    char_owned = tk.Label(char_details_frame, text=f"Owned:   {'Yes' if character['obtained'] else 'No'}", font=("Arial", 12), fg="white", bg="grey8")
    char_owned.grid(row=4, column=0, padx=5, pady=5, sticky='w')

    screen_utils.back_button(owned_chars)
    screen_utils.home_button()


def display_error_img():
    error_img = Image.open("assets/misc/error.png")
    error_photo = ImageTk.PhotoImage(error_img)
    error = tk.Label(frm, image=error_photo, bg="grey8")
    error.place(relx=0.5, rely=0.5, anchor='center')
    frm.error = error_photo
    return True


if __name__ == "__main__":
    homescreen()
    root.mainloop()