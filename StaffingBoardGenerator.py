import os, sys
import tkinter as tk
from tkinter import ttk, filedialog, Toplevel, StringVar
from PIL import Image, ImageFont, ImageDraw, ImageTk

class Application (ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        
        self.file = ""
        self.var_name_roman = StringVar()
        self.var_name = StringVar()
        self.var_buddy = StringVar()
        self.crop_x = -1.0
        self.crop_y = -1.0
        self.crop_h = -1.0
        self.crop_zoom = -1.0

        self.var_name_roman.set("noname")
        self.var_name.set("NONAME")

        self.var_name_roman.trace("w", self.change_entry)
        self.var_name.trace("w", self.change_entry)
        self.var_buddy.trace("w", self.change_entry)

        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_widget()

    def create_widget (self):
        frame_preview = ttk.Frame(self, width=210, height=330)
        frame_preview.grid_columnconfigure(0, weight=1)
        frame_preview.grid_rowconfigure((0,1), weight=1)

        frame_property = ttk.Frame(self)
        frame_property.grid_columnconfigure((0,1,2), weight=1)
        frame_property.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=1)

        label_preview_title = ttk.Label(frame_preview, text="Preview")
        label_picture = ttk.Label(frame_property, text="(1) Select a picture")
        label_name_roman = ttk.Label(frame_property, text="(2) Input name(roman)")
        label_name = ttk.Label(frame_property, text="(3) Input name")
        label_buddy = ttk.Label(frame_property, text="(4) Input buddy name")

        button_reference = ttk.Button(frame_property, text="reference", command=self.load_image)
        button_load = ttk.Button(frame_property, text="load", command=self.load_data)
        button_save = ttk.Button(frame_property, text="save", command=self.save_data)
        button_output = ttk.Button(frame_property, text="output", command=self.output_image)

        entry_name_roman = ttk.Entry(frame_property, textvariable=self.var_name_roman)
        entry_name = ttk.Entry(frame_property, textvariable=self.var_name)
        entry_buddy = ttk.Entry(frame_property, textvariable=self.var_buddy)

        img_base = self.generate_image()
        self.img = ImageTk.PhotoImage(img_base)
        self.imageview_preview = ttk.Label(frame_preview, image=self.img)
        #self.imageview_preview.bind("<Button-1>", self.reflect_image)

        frame_preview.grid(row=0, column=0, padx=30)
        frame_property.grid(row=0, column=1, padx=30)
        
        label_preview_title.grid(row=0, column=0)
        self.imageview_preview.grid(row=1, column=0)

        label_picture.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        button_reference.grid(row=0, column=2)
        label_name_roman.grid(row=1, column=0, columnspan=3, sticky=tk.W)
        entry_name_roman.grid(row=2, column=0, columnspan=3, sticky=tk.W+tk.E)
        label_name.grid(row=3, column=0, columnspan=3, sticky=tk.W)
        entry_name.grid(row=4, column=0, columnspan=3, sticky=tk.W+tk.E)
        label_buddy.grid(row=5, column=0, columnspan=3, sticky=tk.W)
        entry_buddy.grid(row=6, column=0, columnspan=3, sticky=tk.W+tk.E)
        button_load.grid(row=7, column=0, pady=15)
        button_save.grid(row=7, column=1, padx=5)
        button_output.grid(row=7, column=2)

    def load_image (self):
        fTyp = [("","*")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        self.file = tk.filedialog.askopenfilename(filetypes = fTyp, initialdir = iDir)
        self.trimming(file=self.file)

    def trimming (self, file):
        window_trimming = Toplevel(master = self.master)
        window_trimming.focus_set()
        window_trimming.grid_columnconfigure((0,1), weight=1)
        window_trimming.grid_rowconfigure(0, weight=1)

        frame_tool = ttk.Frame(window_trimming)
        frame_tool.grid_columnconfigure(0, weight=1)
        frame_tool.grid_rowconfigure((0,1,2), weight=1)

        img_base = Image.open(file)
        exif = img_base._getexif() 
        orientation = exif.get(0x112, 1) 
        convert_image = {
            1: lambda img: img, 
            2: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT),
            3: lambda img: img.transpose(Image.ROTATE_180),
            4: lambda img: img.transpose(Image.FLIP_TOP_BOTTOM),
            5: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_90),
            6: lambda img: img.transpose(Image.ROTATE_270),
            7: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_270),
            8: lambda img: img.transpose(Image.ROTATE_90),
        } 
        img_base = convert_image[orientation](img_base)
        img_base.thumbnail((600,600), Image.ANTIALIAS)
        w, h = img_base.size
        self.img_face = ImageTk.PhotoImage(img_base)
        canvas_crop = tk.Canvas(window_trimming, width=w, height=h, bg="white")
        canvas_crop.create_image(w/2,h/2, image=self.img_face)
        canvas_crop.bind("<Button-1>", self.target)

        button_reset = ttk.Button(frame_tool, text="reset", command=self.reset_crop)
        button_info = ttk.Button(frame_tool, text="info", command=self.show_info)
        button_crop = ttk.Button(frame_tool, text="crop", command=self.crop_image)

        frame_tool.grid(row=0, column=0, sticky=tk.N)
        canvas_crop.grid(row=0, column=1)

        button_reset.grid(row=0, column=0)
        button_info.grid(row=1, column=0)
        button_crop.grid(row=2, column=0)

    def target (self, event):
        if (self.crop_x < 0 and self.crop_y < 0):    
            self.crop_x = event.x
            self.crop_y = event.y
            print (str(self.crop_x) + " , " + str(self.crop_y))
        else:
            self.crop_h = self.crop_y - event.y
            print (str(self.crop_h))

    def change_entry (self, *args):
        self.reflect_image()

    def load_data (self):
        fTyp = [("","*.sbd")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        data_file = tk.filedialog.askopenfilename(filetypes = fTyp, initialdir = iDir)
        with open(data_file, mode="r") as f:
            self.file = f.readline()
            self.var_name_roman.set(f.readline().rstrip("\r\n"))
            self.var_name.set(f.readline().rstrip("\r\n"))
            self.var_buddy.set(f.readline().rstrip("\r\n"))
            self.crop_x = int(f.readline().rstrip("\r\n"))
            self.crop_y = int(f.readline().rstrip("\r\n"))
            self.crop_h = int(f.readline().rstrip("\r\n"))
        print ("load_data")

    def save_data (self):
        data_list = [self.file, self.var_name_roman.get(), self.var_name.get(), self.var_buddy.get(), str(self.crop_x), str(self.crop_y), str(self.crop_h)]
        with open("data/" + self.var_name_roman.get() + ".sbd", mode="w") as f:
            f.write('\n'.join(data_list))
        print ("save_data")

    def output_image (self):
        self.generate_image().save("output/" + self.var_name_roman.get() + ".png")
        print ("output_image")

    def reset_crop (self):
        self.crop_x = -1.0
        self.crop_y = -1.0
        self.crop_h = -1.0
        print ("reset_crop")

    def crop_image (self):
        self.reflect_image()
        print ("crop_image")

    def show_info (self):
        window_info = Toplevel(master=self.master)
        window_info.focus_set()

        label_msg = ttk.Label(window_info, text="information.")
        button_ok = ttk.Button(window_info, text="OK")

        label_msg.pack()
        button_ok.pack()

    def reflect_image (self):
        img_base = self.generate_image()
        self.img = ImageTk.PhotoImage(img_base)
        self.imageview_preview.configure(image=self.img)
        self.imageview_preview.image = img_base
        self.imageview_preview.grid_forget()
        self.imageview_preview.grid(row=1, column=0)

    def generate_image (self):
        image_base = Image.open("template.png").copy()
        try:
            image_face = Image.open(self.file)
            exif = image_face._getexif() 
            orientation = exif.get(0x112, 1) 
            convert_image = {
                1: lambda img: img, 
                2: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT),
                3: lambda img: img.transpose(Image.ROTATE_180),
                4: lambda img: img.transpose(Image.FLIP_TOP_BOTTOM),
                5: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_90),
                6: lambda img: img.transpose(Image.ROTATE_270),
                7: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_270),
                8: lambda img: img.transpose(Image.ROTATE_90),
            }
            image_face = convert_image[orientation](image_face)
            image_face.thumbnail((600,600), Image.ANTIALIAS)
            crop_w = self.crop_h * 185.0 / 191.0
            image_face_crop = crop_under_center(image_face, self.crop_x, self.crop_y, crop_w, self.crop_h)
            #image_face_crop = image_face
            image_face_crop = image_face_crop.resize((185,191), Image.LANCZOS)
            image_base.paste(image_face_crop, (11,28))
            print("img_face paste.")
            #return image_face_crop
        except AttributeError:
            print ("noimage")

        roman_path = "OPTITimes-Roman.otf"
        name_path = "meiryo.ttc"

        image_base = add_text_to_image_center(image_base, self.var_name_roman.get(), roman_path, 10, (0,0,0), 230, 210)
        image_base = add_text_to_image_center(image_base, self.var_name.get(), name_path, 24, (0,0,0), 250, 210)

        return image_base

def add_text_to_image_center(img, text, font_path, font_size, font_color, height, max_length):
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(img)
    text_width, text_height = draw.textsize(text, font)
    position = ((max_length -text_width)/2, height)
    if draw.textsize(text, font=font)[0] > max_length:
        while draw.textsize(text + '…', font=font)[0] > max_length:
            text = text[:-1]
        text = text + '…'

    draw.text(position, text, font_color, font=font)
    return img

def crop_under_center (img, anchor_x, anchor_y, width, height):
    print (str(anchor_x) + " " + str(anchor_y) + " " + str(width) + " " + str(height))
    return img.crop(((anchor_x - (width/2)),(anchor_y - height),(anchor_x + (width/2)),anchor_y))

if __name__ == "__main__":
    root = tk.Tk()
    root.title(u"StaffingBoardGenerator")
    root.geometry("600x400")

    app = Application(master=root)
    app.pack()

    root.mainloop()