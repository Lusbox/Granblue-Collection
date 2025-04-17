import tkinter as tk
from PIL import Image, ImageTk
from test_inventory import *

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

        weapon_count = 0
        weapon = search_term.get().lower()
        weapon_pic = ""
        result_pic = ""
        

        for item in gbf_invent:
            if item["name"] == weapon:
                weapon_count += 1
                weapon_pic = item["image"]
                lyria = Image.open("assets/lyria_jump.png")
                result_pic = lyria.resize((lyria.width//2, lyria.height//2))

            
        if weapon_pic:
            weapon_image = Image.open(weapon_pic)
            weapon_image = weapon_image.resize((weapon_image.width//2, weapon_image.height//2))
            weapon_photo = ImageTk.PhotoImage(weapon_image)
            weapon = tk.Label(frm, image=weapon_photo, bg="black")

            lyria_result = ImageTk.PhotoImage(result_pic)
            lyria = tk.Label(frm, image=lyria_result, bg="black")

            frm.weapon = weapon_photo
            frm.lyria = lyria_result

            
            weapon.place(x=50, rely=0.5, anchor='w')
            lyria.place(x=670, rely=0.5, anchor='e')

        else:
            siero_pic = Image.open("assets/Sierokarte_NPC.webp")
            result_pic = siero_pic.resize((int(siero_pic.width//1.75), int(siero_pic.height//1.75)))
            siero_result = ImageTk.PhotoImage(result_pic)
            siero = tk.Label(frm, image=siero_result, bg="black")
            siero.place(relx=0.5, rely=0.5, anchor='center')

            frm.siero = siero_result


        result = tk.Label(frm, text=f"Number of {search_term.get()} in inventory : {weapon_count}",
                        font=("Arial", 14),
                        fg="white",
                        bg="black")
        
        back_button = tk.Button(frm, text="Back", command=homescreen)
        back_button.place(relx=0.5, y=420, anchor='center')
        result.place(relx=0.5, y= 50, anchor='center')


    

    def on_entry(event):
        search_results()

    search_box.bind('<Return>', on_entry)

homescreen()
root.mainloop()