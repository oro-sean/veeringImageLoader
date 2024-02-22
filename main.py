import os
import tkinter as tk
from tkinter import filedialog

import numpy as np
from PIL import Image
from PIL import ImageTk
import logging
import h5py
import threading

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
global TARGET_RESOLUTION

global REFERENCE_AREA
global MARKER_AREA
global REFERENCE_AREA_FRAC
global MARKER_AREA_FRAC

global LEFT
global RIGHT
global TOP
global BOTTOM

global IMPORT_CROP_TOP
global IMPORT_CROP_BOTTOM
global IMPORT_CROP_LEFT
global IMPORT_CROP_RIGHT
global IMPORT_SCALE

IMG_DIR = "no directory selected"
IMG_INDEX = 0
FILE_NAMES = []

DISPLAY_WIDTH = 666
DISPLAY_HEIGHT = 500

LEFT = 0
RIGHT = DISPLAY_WIDTH
TOP = 0
BOTTOM = DISPLAY_HEIGHT


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
        self.thumbnail_stringVar.set('No Image')

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
        self.area_frac_stringvar = tk.StringVar()
        self.area_frac_stringvar.set('')

        ## define labels
        self.area_frac_labels = tk.Label(self.frame, text='Ratio of Reference Area & Marker Area', font=('none 12 bold'))
        self.area_frac_txt = tk.Label(self.frame, textvariable=self.area_frac_stringvar, font=('none 12'))
        self.ref_ratio_label = tk.Label(self.frame, text='Pixcel / mm Reference', font=('none 12 bold'))
        self.ref_ratio_txt = tk.Label(self.frame, textvariable=self.ratio_stringVar, font=('none 12'))
        self.new_dimension_label = tk.Label(self.frame, text='Image New Dimension', font=('none 12 bold'))
        self.new_dimension_txt = tk.Label(self.frame, textvariable=self.new_dimension_stringVar, font=('none 12'))
        self.new_size_label = tk.Label(self.frame, text='New File Size', font=('none 12 bold'))
        self.new_size_txt = tk.Label(self.frame, textvariable=self.new_size_stringvar, font=('none 12'))

        ## grid labels
        self.area_frac_labels.grid(column=3, row=0)
        self.area_frac_txt.grid(column=3, row=1)
        self.ref_ratio_label.grid(column=3, row=2)
        self.ref_ratio_txt.grid(column=3, row=3)
        self.new_dimension_label.grid(column=3, row=4)
        self.new_dimension_txt.grid(column=3, row=5)
        self.new_size_label.grid(column=3, row=6)
        self.new_size_txt.grid(column=3, row=7)

        ## define Buttons
        self.calc_new_image = tk.Button(self.frame, width=20, text='Calc New Image', font='none 12',
                                  command=self.Calc_New_Image)
        self.load_and_process = tk.Button(self.frame, width=20, text='Load and Process', font='none 12',
                                          command=self.Load_and_Process)

        ## grid buttons
        self.calc_new_image.grid(column=4,row=0)
        self.load_and_process.grid(column=4,row=1)

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
            file_names = [file for file in file_names if '.jpg' in file]
            if len(file_names) == 0:
                logging.warning('No .jpg found')
                self.file_names = []

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
        print("on Image Folder")
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
    def Calc_New_Image(self):
        global IMPORT_SCALE
        global IMPORT_CROP_TOP
        global IMPORT_CROP_BOTTOM
        global IMPORT_CROP_LEFT
        global IMPORT_CROP_RIGHT
        global REFERENCE_AREA_FRAC
        global MARKER_AREA_FRAC

        try:
            display_scale_x = DISPLAY_WIDTH/ORIG_WIDTH
            display_scale_y = DISPLAY_HEIGHT/ORIG_HEIGHT
            display_scale = (display_scale_y+display_scale_x)/2

            IMPORT_SCALE = (REF_LENGTH_MM/(TARGET_RESOLUTION*0.5))/(REF_LENGTH_PIXCELS / display_scale)

            scale_change = IMPORT_SCALE/display_scale

            IMPORT_CROP_TOP = int(TOP*scale_change)
            IMPORT_CROP_BOTTOM = int(BOTTOM*scale_change)
            IMPORT_CROP_LEFT = int(LEFT*scale_change)
            IMPORT_CROP_RIGHT = int(RIGHT*scale_change)

            reference_p_mm = (REF_LENGTH_PIXCELS*scale_change)/REF_LENGTH_MM

            display_area_pixcels = (BOTTOM-TOP)*(RIGHT-LEFT)

            REFERENCE_AREA_FRAC = REFERENCE_AREA/display_area_pixcels
            MARKER_AREA_FRAC = MARKER_AREA/display_area_pixcels

            self.area_frac_stringvar.set(str(REFERENCE_AREA_FRAC)+ ' - '+str(MARKER_AREA_FRAC))
            self.ratio_stringVar.set(str(reference_p_mm))

            width = IMPORT_CROP_RIGHT-IMPORT_CROP_LEFT
            height = IMPORT_CROP_BOTTOM-IMPORT_CROP_TOP

            self.new_dimension_stringVar.set(str(width)+' x '+str(height))

            fileSize = width * height * len(self.file_names) * 16 * 0.125 * 0.000000001

            self.new_size_stringvar.set(str(fileSize))

        except Exception as e:
            logging.error(e)
            logging.error("Failed to Calc new image")

    def Load_into_Array(self):
        self.timeStamps = []
        for i in range(len(FILE_NAMES)):

            fileName = FILE_NAMES[i]
            img_path = os.path.join(IMG_DIR, fileName)

            try:
                image = Image.open(img_path)
                print("processing "+str(i)+" of "+str(len(FILE_NAMES)))
                ts = image._getexif()[36867]
                self.timeStamps.append(ts)
                width, height = image.size
                width = width*IMPORT_SCALE
                height = height*IMPORT_SCALE
                image = image.resize((int(width), int(height)), Image.Resampling.LANCZOS)
                image = image.crop((IMPORT_CROP_LEFT, IMPORT_CROP_TOP, IMPORT_CROP_RIGHT, IMPORT_CROP_BOTTOM))

                if i == 0:
                    w,h = image.size
                    img_array = np.zeros((h,w,3,len(FILE_NAMES)), dtype='float32')

                img_array[:,:,:,i] = np.array(image)

            except Exception as e:
                logging.error(e)
                logging.error('failed to load image in for loop - ' + str(img_path))

            self.img_array = img_array

    def Load_and_Process(self):
        try:
            exp_dir = filedialog.askdirectory()
            exp_path = os.path.join(exp_dir, 'export.h5')
            self.Load_into_Array()
            hf = h5py.File(exp_path, 'w')
            hf.create_dataset('IMG_ARRAY', data=self.img_array)
            hf.create_dataset('TIME_STAMPS', data=self.timeStamps)
            vSp_params = [REFERENCE_AREA_FRAC, MARKER_AREA_FRAC, REF_LENGTH_PIXCELS, REF_LENGTH_MM, TARGET_RESOLUTION]
            hf.create_dataset('VSP_PARAMS', data=vSp_params)
            hf.close()
        except Exception as e:
            logging.error(e)
            logging.error("Failed to load and process")










class MidFrame():
    def __init__(self, master):

        self.master = master
        self.frame = tk.Frame(self.master)

        self.canvas_width = DISPLAY_WIDTH
        self.canvas_height = DISPLAY_HEIGHT

        ## Define Canvas and Scales
        self.main_canvas = tk.Canvas(self.frame, width=self.canvas_width, height=self.canvas_height, bg='#C8C8C8')
        self.top_scale = tk.Scale(self.frame, orient='horizontal', length=self.canvas_width, from_=0,
                                  to=self.canvas_width, command=self.On_Call_Transform)
        self.bottom_scale = tk.Scale(self.frame, orient='horizontal', length=self.canvas_width, from_=0,
                                     to=self.canvas_width, command=self.On_Call_Transform)
        self.left_scale = tk.Scale(self.frame, orient='vertical', length=self.canvas_height, from_=0,
                                   to=self.canvas_height, command=self.On_Call_Transform)
        self.right_scale = tk.Scale(self.frame, orient='vertical', length=self.canvas_height, from_=0,
                                    to=self.canvas_height, command=self.On_Call_Transform)

        ## Grid Canvas and scales
        self.main_canvas.grid(column=1, row=1)
        self.top_scale.grid(column=1, row=0)
        self.bottom_scale.grid(column=1, row=2)
        self.left_scale.grid(column=0, row=1)
        self.right_scale.grid(column=2, row=1)

        ## set scale default values
        self.bottom_scale.set(self.canvas_width)
        self.right_scale.set(self.canvas_height)

        ## define RHS frame
        self.rhs_frame = tk.Frame(self.frame)

        ## define buttons
        self.load_image = tk.Button(self.rhs_frame, width=20, text='Load Image', font='none 12',
                                      command=self.On_Call_Load)
        self.update = tk.Button(self.rhs_frame, width=20, text='Update', font='none 12',
                                        command=self.Draw_Lines)

        ## define Labels
        self.ref_label_start = tk.Label(self.rhs_frame, text= 'Define X and Y start values for reference region',
                                        font=('none 12 bold'))
        self.ref_label_end = tk.Label(self.rhs_frame, text='Define X and Y end values for reference region',
                                        font=('none 12 bold'))
        self.marker_label_start = tk.Label(self.rhs_frame, text='Define X and Y start values for marker region',
                                        font=('none 12 bold'))
        self.marker_label_end = tk.Label(self.rhs_frame, text='Define X and Y end values for marker region',
                                        font=('none 12 bold'))
        self.ref_length_label = tk.Label(self.rhs_frame, text='Length of reference in mm',
                                         font='none 12 bold')
        self.resolution_label = tk.Label(self.rhs_frame, text='Desired Resolution',
                                         font='none 12 bold')

        ## define spinboxes
        self.ref_start_x = tk.Spinbox(self.rhs_frame, width=5, from_=LEFT, to=RIGHT, command=self.Draw_Lines)
        self.ref_start_y = tk.Spinbox(self.rhs_frame, width=5, from_=TOP, to=BOTTOM, command=self.Draw_Lines)
        self.ref_end_x = tk.Spinbox(self.rhs_frame, width=5, from_=LEFT, to=RIGHT, command=self.Draw_Lines)
        self.ref_end_y = tk.Spinbox(self.rhs_frame, width=5, from_=TOP, to=BOTTOM, command=self.Draw_Lines)
        self.marker_start_x = tk.Spinbox(self.rhs_frame, width=5, from_=LEFT, to=RIGHT, command=self.Draw_Lines)
        self.marker_start_y = tk.Spinbox(self.rhs_frame, width=5, from_=TOP, to=BOTTOM, command=self.Draw_Lines)
        self.marker_end_x = tk.Spinbox(self.rhs_frame, width=5, from_=LEFT, to=RIGHT, command=self.Draw_Lines)
        self.marker_end_y = tk.Spinbox(self.rhs_frame, width=5, from_=TOP, to=BOTTOM, command=self.Draw_Lines)
        self.ref_length_mm = tk.Spinbox(self.rhs_frame, width=5, from_=0, to=200, command=self.Draw_Lines)
        self.resolution = tk.Spinbox(self.rhs_frame, width=5, from_=0.1, to=2, command=self.Draw_Lines)

        ## grid buttons and Spinboxes
        self.load_image.grid(column=0, row=0, columnspan=2, sticky='N')
        self.ref_label_start.grid(column=0,row=2, columnspan=2)
        self.ref_start_x.grid(column=0,row=3)
        self.ref_start_y.grid(column=1, row=3)
        self.ref_label_end.grid(column=0, row=4, columnspan=2)
        self.ref_end_x.grid(column=0, row=5)
        self.ref_end_y.grid(column=1, row=5)
        self.marker_label_start.grid(column=0, row=6, columnspan=2)
        self.marker_start_x.grid(column=0, row=7)
        self.marker_start_y.grid(column=1, row=7)
        self.marker_label_end.grid(column=0, row=8, columnspan=2)
        self.marker_end_x.grid(column=0, row=9)
        self.marker_end_y.grid(column=1, row=9)
        self.ref_length_label.grid(column=0, row=11)
        self.ref_length_mm.grid(column=1,row=11)
        self.resolution_label.grid(column=0, row=12)
        self.resolution.grid(column=1, row=12)
        self.update.grid(column=0, row=13,columnspan=2)

        self.rhs_frame.grid(column=3, row=1)

    def Load_Image(self):
        try:
            image = Image.open(IMG_PATH)
            width, height = image.size
            self.canvas_width = width * (self.canvas_height/height)
            self.image_pil_original = image.resize((int(self.canvas_width), int(self.canvas_height)),
                                                   Image.Resampling.LANCZOS)

        except Exception as e:
            logging.error(e)
            logging.error('Failed to Load Image - Mid Frame')
    def Crop_Image(self,image):
        global TOP
        global BOTTOM
        global LEFT
        global RIGHT

        try:
            left = self.top_scale.get()
            top = self.left_scale.get()
            right = self.bottom_scale.get()
            bottom = self.right_scale.get()
            TOP = top
            BOTTOM = bottom
            LEFT = left
            RIGHT = right
            image_pil_croped = image.crop((left, top, right, bottom))
            return image_pil_croped

        except Exception as e:
            logging.error(e)
            logging.error(('Failed to crop image'))
    def Transform_Image(self):
        try:
            image = self.image_pil_original
            image_pil_cropped = self.Crop_Image(image)
            self.image_pil_transformed = image_pil_cropped

        except Exception as e:
            logging.error(e)
            logging.error("Failed to transform image - midframe")
    def Draw_Lines(self):
        global REF_LENGTH_PIXCELS
        global REF_LENGTH_MM
        global REFERENCE_AREA
        global MARKER_AREA
        global TARGET_RESOLUTION

        ref_x1 = int(self.ref_start_x.get())
        ref_y1 = int(self.ref_start_y.get())
        ref_x2 = int(self.ref_end_x.get())
        ref_y2 = int(self.ref_end_y.get())
        mark_x1 = int(self.marker_start_x.get())
        mark_y1 = int(self.marker_start_y.get())
        mark_x2 = int(self.marker_end_x.get())
        mark_y2 = int(self.marker_end_y.get())

        self.Display_Image()
        self.main_canvas.create_line(ref_x1,ref_y1,ref_x2,ref_y2, width=4 )
        self.main_canvas.create_line(mark_x1, mark_y1, mark_x2, mark_y2, width=4)

        ref_area = (ref_x2-ref_x1)*(ref_y2-ref_y1)
        mark_area = (mark_x2-mark_x1)*(mark_y2-mark_y1)
        ref_length = ref_x2-ref_x1

        REFERENCE_AREA = ref_area
        MARKER_AREA = mark_area
        REF_LENGTH_PIXCELS = ref_length
        REF_LENGTH_MM = int(self.ref_length_mm.get())
        TARGET_RESOLUTION = float(self.resolution.get())
    def Display_Image(self):
        try:
            self.image_tk = ImageTk.PhotoImage(self.image_pil_transformed)
            try:
                horizontal_centre = int(((RIGHT-LEFT)/2)+LEFT)
                vertical_centre = int(((BOTTOM-TOP)/2)+TOP)

            except Exception as e:
                logging.error(e)
                logging.error('Failed finding image centre'+ str(LEFT)+ '' + str(RIGHT)+ '' +
                              str(TOP)+ '' + str(BOTTOM)+ '')

            self.main_canvas.create_image(horizontal_centre, vertical_centre, image=self.image_tk, anchor='center')

        except Exception as e:
            logging.error(e)
            logging.error("Image Failed to display")
    def On_Call_Transform(self):
        print("On_Call_Transform")
        try:
            self.Transform_Image()
            self.Display_Image()

        except Exception as e:
            logging.error(e)
            logging.error(("Failed On_Call_Transform"))
    def On_Call_Load(self):
        try:
            print("in on call load")
            self.Load_Image()
            self.On_Call_Transform()

        except Exception as e:
            logging.error(e)
            logging.error("Failed On_Call_Load")

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Veering Image Loader')
        self.geometry('1100x1000')
        self.mainframe = tk.Frame(self)
        self.mainframe.grid(column=0, row=0, sticky='N,W,S,E')
        self.top_frame = TopFrame(self.mainframe)
        self.top_frame.frame.grid(column=0, row=0)
        self.mid_frame = MidFrame(self.mainframe)
        self.mid_frame.frame.grid(column=0, row=1)
        self.main_scroll = tk.Scrollbar(self.mainframe, orient='vertical')

if __name__ == "__main__":
    app = App()
    app.mainloop()








