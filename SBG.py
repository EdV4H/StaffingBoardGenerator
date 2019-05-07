import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk, ImageFont, ImageDraw
import os

class Preference (ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)

        self.string_photo = tk.StringVar()
        self.string_photo.set("")

        self.string_name1 = tk.StringVar()
        self.string_name1.trace("w", lambda name, index, mode, string_name1=string_name1: set_name1(string_name1))

        label_photo = ttk.Label(self, text="Photo")
        entry_photo = ttk.Entry(self, textvariable=self.string_photo)
        butotn_photo = ttk.Button(self, text="Reference", command=self.load_image)

        label_name1 = ttk.Label(self, text="Name(Roman)")
        entry_name1 = ttk.Entry(self, textvariable=self.string_name1)

        label_name2 = ttk.Label(self, text="Name")
        entry_name2 = ttk.Entry(self)

        label_buddy = ttk.Label(self, text="buddy")
        entry_buddy = ttk.Entry(self)

        button_generate = ttk.Button(self, text="Generate")

        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)

        label_photo.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        entry_photo.grid(row=1, column=0, sticky=tk.W + tk.E)
        butotn_photo.grid(row=1, column=1, sticky=tk.E)

        label_name1.grid(row=2, column=0, columnspan=2, sticky=tk.W)
        entry_name1.grid(row=3, column=0, columnspan=2, sticky=tk.W + tk.E)

        label_name2.grid(row=4, column=0, columnspan=2, sticky=tk.W)
        entry_name2.grid(row=5, column=0, columnspan=2, sticky=tk.W + tk.E)

        label_buddy.grid(row=6, column=0, columnspan=2, sticky=tk.W)
        entry_buddy.grid(row=7, column=0, columnspan=2, sticky=tk.W + tk.E)

        button_generate.grid(row=8, column=1, sticky=tk.E, pady=10)

    def load_image (self):
        fTyp = [("","*")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        file = tk.filedialog.askopenfilename(filetypes = fTyp, initialdir = iDir)
        self.string_photo.set(file)

    def set_name1 (name):
        Preview.set_name1(name)



class Preview (ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)

        label_title = ttk.Label(self, text="Preview")

        self.template = Image.open("template.png").copy()
        self.name1 = "noname"

        self.reflect_image()

        label_tmp = ttk.Label(self, image=self.img)

        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0,1), weight=1)

        label_title.grid(row=0, column=0)
        label_tmp.grid(row=1, column=0, sticky=tk.N)

    def reflect_image (self):
        base_img = Image.open("template.png").copy()
        text = "text"
        font_path = "meryo.ttc"
        font_size = 10
        font_color = (0,0,0)
        height = 200
        width = 10
        production = self.add_text_to_image(img=base_img,text=text,font_path=font_path,font_size=font_size,font_color=font_color,height=height,width=width,max_length=210)
        self.img = ImageTk.PhotoImage(production)

    def add_text_to_image (img, text, font_path, font_size, font_color, height, width, max_length=210):
        position = (width, height)
        font = ImageFont.truetype(font_path, font_size)
        draw = ImageDraw.Draw(img)
        if draw.textsize(text, font=font)[0] > max_length:
            while draw.textsize(text + '.', font=font)[0] > max_length:
                text = text[:-1]
            text = text + '.'

        draw.text(position, text, font_color, font=font)
        return img

    @staticmethod
    def set_name1 (name):
        self.name1 = name


if __name__ == "__main__":
    root = tk.Tk()
    root.title(u'StaffingBoardGenerator')
    root.geometry("640x400")

    root.grid_columnconfigure((0,1), weight=1)
    root.grid_rowconfigure(0, weight=1)

    preview = Preview(master=root)
    preview.grid(row=0, column=0, sticky=tk.N + tk.S)

    preference = Preference(master=root)
    preference.grid(row=0, column=1, sticky=tk.N + tk.W + tk.E + tk.S, padx=10, pady=10)

    root.mainloop()