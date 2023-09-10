import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import logging

logging.basicConfig(filename='VIM.log', encoding='utf-8', level=logging.DEBUG)
logging.info('Veering Image Loader Opened')

global IMG_DIR
global IMG_INDEX
global FILE_NAMES
global IMG_PATH

global ORIG_WIDTH
global ORIG_HEIGHT
global DISPLAY_HEIGHT
global DISPLAY_WIDTH

global REF_LENGTH_PIXCELS
global REF_LENGTH_MM

global REFERENCE_AREA_FRACTION
global MARKER_AREA_FRACTION

IMG_DIR = "no directory selected"
IMG_INDEX = 0
FILE_NAMES = []

DISPLAY_WIDTH = 500
DISPLAY_HEIGHT = 750

class TopFrame():
    def __init__(self, master):

        self.master = master
        self.frame = tk.Frame(self.master)

        ## Define class variables
        self.thumbnail_width = 200
        self.thumbnail_height = 150
        self.img_index = 0

        ## Define Buttons
        self.image_folder = tk.Button(self.frame, width=20, text='Image Folder', font='none 12', command=self.On_Image_Folder)
        self.foward_1 = tk.Button(self.frame, width = 20, text= 'Skip Foward 1', font = 'none 12', command=lambda:self.On_plus(1))
        self.foward_10 = tk.Button(self.frame, width = 20, text= 'Skip Foward 10', font = 'none 12', command=lambda:self.On_plus(10))
        self.foward_100 = tk. Button(self.frame, width = 20, text= 'Skip Foward 100', font = 'none 12', command=lambda:self.On_plus(100))
        self.back_1 = tk.Button(self.frame, width = 20, text= 'Skip Back 1', font = 'none 12', command=lambda:self.On_plus(-1))
        self.back_10 = tk.Button(self.frame, width = 20, text= 'Skip Back 10', font = 'none 12', command=lambda:self.On_plus(-10))
        self.back_100 = tk. Button(self.frame, width = 20, text= 'Skip Back 100', font = 'none 12', command=lambda:self.On_plus(-100))

        ## Grid buttons
        self.image_folder.grid(column=0, row=0)
        self.back_100.grid(column=0, row = 2)
        self.back_10.grid(column=0, row=3)
        self.back_1.grid(column=0, row=4)
        self.foward_1.grid(column=0, row=5)
        self.foward_10.grid(column=0, row=6)
        self.foward_100.grid(column=0, row=7)
        self.frame.grid()

        ## define StringVars
        self.thumbnail_stringVar = tk.StringVar()
        self.thumbnail_stringVar.set('No Image'
                                     )
        ## Define Thumbnail
        self.thumbnail_canvas = tk.Canvas(self.frame, width=self.thumbnail_width, height=self.thumbnail_height, bg='#C8C8C8')
        self.thumbnail_label = tk.Label(self.frame, textvariable=self.thumbnail_stringVar, font=('none 12'))

        ## Grid Thumbnail
        self.thumbnail_canvas.grid(column=1, row=1, rowspan=7)
        self.thumbnail_label.grid(column=1, row=0)

        ## define Stringvars for labels
        self.img_dir_stringVar = tk.StringVar()
        self.img_dir_stringVar.set('No Directory Selected')
        self.total_stringVar = tk.StringVar()
        self.total_stringVar.set('No Images Found')
        self.dimension_stringVar = tk.StringVar()
        self.dimension_stringVar.set('')
        self.size_stringVar = tk.StringVar()
        self.size_stringVar.set('')

        ## define labels
        self.dir_label = tk.Label(self.frame, text= 'The Selected directory is', font=('none 12 bold'))
        self.dir_txt = tk.Label(self.frame, textvariable=self.img_dir_stringVar, font=('none 12'))
        self.total_label = tk.Label(self.frame,  text= 'Image Count', font=('none 12 bold'))
        self.total_txt = tk.Label(self.frame, textvariable=self.total_stringVar, font=('none 12'))
        self.dimension_label = tk.Label(self.frame, text='Image Original Dimension', font=('none 12 bold'))
        self.dimension_txt = tk.Label(self.frame, textvariable=self.dimension_stringVar, font=('none 12'))
        self.size_label = tk.Label(self.frame, text='Original File Size', font=('none 12 bold'))
        self.size_txt = tk.Label(self.frame, textvariable=self.size_stringVar, font=('none 12'))

        ## grid labels
        self.dir_label.grid(column=2, row=0)
        self.dir_txt.grid(column=2, row=1)
        self.total_label.grid(column=2, row=2)
        self.total_txt.grid(column=2, row=3)
        self.dimension_label.grid(column=2, row=4)
        self.dimension_txt.grid(column=2, row=5)
        self.size_label.grid(column=2, row=6)
        self.size_txt.grid(column=2, row=7)

        ## define Stringvars for labels
        self.ratio_stringVar = tk.StringVar()
        self.ratio_stringVar.set('')
        self.new_dimension_stringVar = tk.StringVar()
        self.new_dimension_stringVar.set('')
        self.new_size_stringvar = tk.StringVar()
        self.new_size_stringvar.set('')

        ## define labels
        self.ref_ratio_label = tk.Label(self.frame, text='Pixcel / mm Reference', font=('none 12 bold'))
        self.ref_ratio_txt = tk.Label(self.frame, textvariable=self.ratio_stringVar, font=('none 12'))
        self.new_dimension_label = tk.Label(self.frame, text='Image New Dimension', font=('none 12 bold'))
        self.new_dimension_txt = tk.Label(self.frame, textvariable=self.new_dimension_stringVar, font=('none 12'))
        self.new_size_label = tk.Label(self.frame, text='New File Size', font=('none 12 bold'))
        self.new_size_txt = tk.Label(self.frame, textvariable=self.new_size_stringvar, font=('none 12'))

        ## grid labels
        self.ref_ratio_label.grid(column=3, row=2)
        self.ref_ratio_txt.grid(column=3, row=3)
        self.new_dimension_label.grid(column=3, row=4)
        self.new_dimension_txt.grid(column=3, row=5)
        self.new_size_label.grid(column=3, row=6)
        self.new_size_txt.grid(column=3, row=7)

    def Load_Thumbnail(self):
        global IMG_PATH
        global ORIG_WIDTH
        global ORIG_HEIGHT

        fileName = self.file_names[self.img_index]
        img_path = os.path.join(self.img_dir,fileName)
        try:
            image = Image.open(img_path)
            width, height = image.size
            self.thumbnail_height = height * (self.thumbnail_width/width)
            image = image.resize((int(self.thumbnail_width), int(self.thumbnail_height)), Image.Resampling.LANCZOS)
            image = ImageTk.PhotoImage(image)
            self.thumb_img = image
            self.thumbnail_canvas.create_image(0,0, image=self.thumb_img, anchor='nw')

        except Exception as e:
            logging.error(e)
            logging.error('Failed to Load Image')

        dimension = str(width)+' x '+str(height)
        fileSize = width * height * len(self.file_names) * 16 * 0.125 * 0.000000001

        self.dimension_stringVar.set(dimension)
        self.size_stringVar.set(str(fileSize))
        self.thumbnail_stringVar.set(fileName)
        self.img_path = img_path

        IMG_PATH = img_path
        ORIG_WIDTH = width
        ORIG_HEIGHT = height


    def Load_File_Names(self):
        global FILE_NAMES

        try:
            file_names = os.listdir(self.img_dir)
            file_names = [file for file in file_names if '.JPG' in file]
            if len(file_names) == 0:
                logging.warning('No .jpg found')

            else:
                self.total_stringVar.set(str(len(file_names)))
                self.file_names = file_names

                FILE_NAMES = file_names

        except Exception as e:
            logging.error(e)
            logging.error('Failed to load file names in Def_File_Names')

    def Define_Source_Folder(self):
        global IMG_DIR

        img_dir = filedialog.askdirectory()
        self.img_dir = img_dir
        self.img_dir_stringVar.set(img_dir)

        IMG_DIR = img_dir

    def On_Image_Folder(self):
        self.Define_Source_Folder()
        self.Load_File_Names()
        self.Load_Thumbnail()

    def Index_in_Range(self, increment):
        global IMG_INDEX

        new_index = self.img_index + increment
        if (new_index) > (len(self.file_names)-1):
            while (new_index) > (len(self.file_names)-1):
                new_index = new_index - len(self.file_names)

        elif (new_index) < 0:
            while (new_index) < 0:
                new_index = new_index + len(self.file_names)

        else:
            logging.error("index range failed 1")

        if (len(self.file_names)) < new_index < 0:
            logging.error('Index range 2')

        self.img_index = new_index

        IMG_INDEX = new_index

    def On_plus(self,increment):
        try:
            self.Index_in_Range(increment)
            self.Load_Thumbnail()

        except Exception as e:
            logging.error(e)


class MidFrame():
    def __init__(self, master):

        self.master = master
        self.frame = tk.Frame(self.master)

        self.canvas_width = 1000
        self.canvas_height = 750

        ## Define Canvas and Scales
        self.main_canvas = tk.Canvas(self.frame, width=self.canvas_width, height=self.canvas_height, bg='#C8C8C8')
        self.top_scale = tk.Scale(self.frame, orient='horizontal', length=self.canvas_width, from_=0, to=self.canvas_width)
        self.bottom_scale = tk.Scale(self.frame, orient='horizontal', length=self.canvas_width, from_=0, to=self.canvas_width)
        self.left_scale = tk.Scale(self.frame, orient='vertical', length=self.canvas_height, from_=0, to=self.canvas_height)
        self.right_scale = tk.Scale(self.frame, orient='vertical', length=self.canvas_height, from_=0, to=self.canvas_height)

        ## Grid Canvas and scales
        self.main_canvas.grid(column=1, row=1)
        self.top_scale.grid(column=1, row=0)
        self.bottom_scale.grid(column=1, row=2)
        self.left_scale.grid(column=0, row=1)
        self.right_scale.grid(column=2, row=1)

    def Load_Image(self):
        try:
            image = Image.open(IMG_PATH)
            width, height = image.size
            self.canvas_width = width * (self.canvas_height/height)
            image = image.resize((int(self.canvas_width), int(self.canvas_height)), Image.Resampling.LANCZOS)
            image = ImageTk.PhotoImage(image)
            self.image = image
            self.main_canvas.create_image(0,0, image=self.image, anchor='nw')

        except Exception as e:
            logging.error(e)
            logging.error('Failed to Load Image')






class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Veering Image Loader')
        self.geometry('1250x1500')
        self.mainframe = tk.Frame(self)
        self.mainframe.grid(column=0, row=0, sticky='N,W,S,E')
        self.top_frame = TopFrame(self.mainframe)
        self.top_frame.frame.grid(column=0, row=0)
        self.mid_frame = MidFrame(self.mainframe)
        self.mid_frame.frame.grid(column=0, row=1)





if __name__ == "__main__":
    app = App()
    app.mainloop()








