import os
import tkinter as tk
import paphra_tktable.table as tb
import mimetypes

from tkinter import filedialog
from PIL import Image
from subprocess import PIPE, Popen

exiftoolcmd = r"C:\Users\tenti\OneDrive - Istituto Nazionale di Fisica Nucleare\PyViewer\tools\exiftool-12.30\exiftool.exe"

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

class PyViewer(tk.Tk):
    def __init__(self, *args):
        self.Tk = super(PyViewer, self)
        self.Tk.__init__(*args)
        self.Tk.title("PyViewer")
        self.geometry("1200x400")
        self.current_directory = None
        self.create_menu()
        self.create_layout()
        #self.create_table()
        #self.create_display()
        #self.create_notebook()
    
    def onOpenFolder(self):
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
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar)
        self.filemenu.add_command(label="Open Folder",command=self.onOpenFolder)
        self.filemenu.add_command(label="Exit",command=self.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.config(menu=self.menubar)

    def create_layout(self):
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
    
    def create_table(self, rows):
        keys = ["name","date"]
        titles = [
            {"text": "filename", "width": 30, "type": 'l'},
            {"text": "date", "width": 30, "type": 'l'}
        ]
        self.tb = tb.Table(self.frame1, _keys_ = keys, titles = titles)
        self.tb.host.grid(row=0, column=0, sticky='NESW')
        self.frame1.columnconfigure(0, weight=1)
        self.frame1.rowconfigure(0, weight=1)
        self.frame1.grid()
        self.tb.add_rows(rows)
    
    def create_display(self):
        self.canvas = tk.Canvas(self.frame2) 

    def create_notebook(self):
        self.notebook = tk.ttk.Notebook(self.frame3)

if __name__ == "__main__":
    # execute only if run as a script
    app = PyViewer()
    app.mainloop()