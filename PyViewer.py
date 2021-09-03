import os
import tkinter as tk
import paphra_tktable.table as tb
import mimetypes

from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk,Image 
from subprocess import PIPE, Popen


exiftoolcmd_mt    = r"C:\Users\tenti\OneDrive - Istituto Nazionale di Fisica Nucleare\PyViewer\tools\exiftool-12.30\exiftool.exe"
exiftoolcmd_tenti = r"C:\Users\mt\OneDrive - Istituto Nazionale di Fisica Nucleare\PyViewer\tools\exiftool-12.30\exiftool.exe"

exiftoolcmd = exiftoolcmd_mt if os.path.exists(exiftoolcmd_mt) else exiftoolcmd_tenti

def getVideoInfo(filepath):
    # get video info: path, filename, date
    path_raw = r'{}'.format(filepath)
    process = Popen([exiftoolcmd , path_raw], stdout=PIPE, stderr=None, shell=True)
    out = process.communicate()[0].decode("utf-8")
    date = [x.split(" : ")[1].strip() for x in out.split('\r\n')[:-1] if x.split(" : ")[0].strip() == 'Create Date']
    return {"name": os.path.basename(filepath),
            "path": filepath,
            "date": date[0] if len(date) > 0 else ""}

def getImageInfo(filepath):
    # get image info: path, filename, date
    return {"name": os.path.basename(filepath),
            "path": filepath,
            "date": Image.open(filepath).getexif().get(306)}

    
def get_selected_frame(list_canvas, label):
    for frame in list_canvas.winfo_children():
        for it in frame.winfo_children():
            if it.winfo_name() == label.winfo_name() and \
                frame.winfo_name() == label.winfo_parent().split('.')[-1]:
                return frame
    return None

def get_sized_img(filename, w, h):
    img = Image.open(filename)
    img_h, img_w = img.size
    scale = min([h/img_h, w/img_w])
    img = img.resize((int(h*scale),int(w*scale)))
    return img

def get_file_from_frame(frame):
    return frame.winfo_children()[1].cget('text')
    
def inspect(item, level = 0):
    prefix = "  " * (level + 1)
    print(f"{prefix}{item.winfo_name()}: {item.winfo_width()} x {item.winfo_height()} [{item.winfo_class()}] => {item.grid_size()}")
    for child in item.winfo_children():
        inspect(child, level + 1)
    
class PyViewer(tk.Tk):
    def __init__(self, *args):
        self.Tk = super(PyViewer, self)
        self.Tk.__init__(*args)
        self.Tk.title("PyViewer")
        self.geometry("1200x400")
        self.current_directory = None
        self.create_menu()
        self.create_layout()
        self.create_table([])
        self.create_display()
        self.create_notebook()
    
    def onOpenFolder(self):
        # dialog window to select folder
        self.current_directory = filedialog.askdirectory(initialdir = self.current_directory,title = "Open folder", mustexist = True)
        items = self.getListOfFilesWithInfo()
        self.create_table(items['image'])
    
    def getListOfFilesWithInfo(self):
        # dictionary with images and videos
        # each items has filename, path and creation date
        items = {"image" : [], 
                 "video" : [] }
        
        # if current dicrectory is not initialized return empty lists else
        # 1 - list content of the directory
        # 2 - filter images and videos
        # 3 - retrieve information
        if self.current_directory is not None and \
           self.current_directory != '':
            items_in_folder = os.listdir(self.current_directory)
            files_in_folder = [x for x in items_in_folder if os.path.isfile(os.path.join(self.current_directory,x))]
            image_in_folder = [x for x in files_in_folder if "image" in mimetypes.guess_type(x)[0]]
            video_in_folder = [x for x in files_in_folder if "video" in mimetypes.guess_type(x)[0]]
            items["image"] = [getImageInfo(os.path.join(self.current_directory,img)) for img in image_in_folder]
            items["video"] = [getVideoInfo(os.path.join(self.current_directory,vid)) for vid in video_in_folder]
            # print(" == IMAGES ==")
            # for it in items["image"]:
            #     print(f"{it['name']}\t {it['date']}")
            # print(" == VIDEOS ==")
            # for it in items["video"]:
            #     print(f"{it['name']}\t {it['date']}")
        return items
    
    def create_menu(self):
        # create menu
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar)
        self.filemenu.add_command(label="Open Folder",command=self.onOpenFolder)
        self.filemenu.add_command(label="Exit",command=self.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.config(menu=self.menubar)

    def create_layout(self):
        # create meain layout
        self.frame1 = tk.Frame(self)
        self.frame2 = tk.Frame(self)
        self.frame3 = tk.Frame(self)
        self.frame1.grid(row=0, column=0, sticky='NESW')
        self.frame2.grid(row=0, column=1, sticky='NESW')
        self.frame3.grid(row=0, column=2, sticky='NESW')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid()
    
    def onClickItem(self, event):
        inspect(self)
        selected_frame = get_selected_frame(self.tb.list_canvas, event.widget)
        filename = get_file_from_frame(selected_frame)
        print(f"{filename}")
    
    def create_table(self, rows):
        self.frame1.config(background='red')
        # create table and fill it with itmes
        keys = ["name","date"]
        titles = [
            {"text": "filename", "width": 30, "type": 'l'},
            {"text": "date", "width": 30, "type": 'l'}
        ]
        self.tb = tb.Table(self.frame1, _keys_ = keys, titles = titles)
        self.tb.add_rows(rows)
        self.frame1.columnconfigure(0, weight=1)
        self.frame1.rowconfigure(0, weight=1)
        self.frame1.grid()

        # function to iteratively bind onClick event 
        # on all label of the table
        # def bind_function_on_double_click(widget):
        #     if widget.winfo_class() == "TLabel":
        #         widget.bind('<Button-1>', self.onClickItem)
        #     for child in widget.winfo_children():
        #         bind_function_on_double_click(child)
        
        # bind_function_on_double_click(self.tb.host)
    
    def create_display(self):
        self.frame2.config(background='blue')
        # create display of the images/videos
        self.canvas = tk.Canvas(self.frame2)
        self.canvas.grid(row=0, column=0, sticky='NESW')
        self.canvas.columnconfigure(0, weight=1)
        self.canvas.rowconfigure(0, weight=1)
        self.frame2.grid()

    def create_notebook(self):
        self.frame3.config(background='green')
        # create notebook to display info about items
        self.notebook = tk.ttk.Notebook(self.frame3)
        self.notebook.grid(row=0, column=0, sticky='NESW')
        self.notebook.columnconfigure(0, weight=1)
        self.notebook.rowconfigure(0, weight=1)
        self.frame3.grid()

if __name__ == "__main__":
    # execute only if run as a script
    app = PyViewer()
    app.mainloop()