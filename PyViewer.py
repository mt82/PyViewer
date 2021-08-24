import os
import tkinter as tk
import paphra_tktable.table as tb
import mimetypes

from tkinter import filedialog
from PIL import Image
from subprocess import PIPE, Popen

exiftoolcmd = r"C:\Users\tenti\OneDrive - Istituto Nazionale di Fisica Nucleare\PyViewer\tools\exiftool-12.30\exiftool.exe"

class PyViewer(tk.Tk):
    def __init__(self, *args):
        self.Tk = super(PyViewer, self)
        self.Tk.__init__(*args)
        self.Tk.title("PyViewer")
        self.geometry("1200x400")
        self.current_directory = None
        self.create_menu()
        self.create_layout()
        self.create_table()
        self.create_display()
        self.create_notebook()
    
    def onOpenFolder(self):
        self.current_directory = filedialog.askdirectory(initialdir = self.current_directory,title = "Open folder", mustexist = True)
        self.getListOfFilesWithInfo()
    
    def getListOfFilesWithInfo(self):
        # dictionary with images and videos
        # each items has filename, path and creation date
        items = {"image" : [], 
                 "video" : [] }
        
        # if current dicrectory is not initialized return empty lists else
        # 1 - list content of the directory
        # 2 - filter images and videos
        # 3 - retrieve information
        if self.current_directory is None:
            return items
        else:
            items_in_folder = os.listdir(self.current_directory)
            files_in_folder = [x for x in items_in_folder if os.path.isfile(os.path.join(self.current_directory,x))]
            image_in_folder = [x for x in files_in_folder if "image" in mimetypes.guess_type(x)[0]]
            video_in_folder = [x for x in files_in_folder if "video" in mimetypes.guess_type(x)[0]]
            items["image"] = [{"name": img,
                               "path": os.path.join(self.current_directory,img),
                               "date": Image.open(os.path.join(self.current_directory,img)).getexif().get(306)} for img in image_in_folder]
            videos = []
            for vid in video_in_folder:
                path = os.path.join(self.current_directory,vid)
                path_raw = r'{}'.format(path)
                process = Popen([exiftoolcmd , path_raw], stdout=PIPE, stderr=None, shell=True)
                out = process.communicate()[0].decode("utf-8")
                date = [x.split(" : ")[1].strip() for x in out.split('\r\n')[:-1] if x.split(" : ")[0].strip() == 'Create Date']
                videos.append({"name": vid,
                               "path": path,
                               "date": date[0] if len(date) > 0 else ""})
            items["video"] = videos
            
    
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
        self.grid()
    
    def create_table(self):
        keys = ["filename","date"]
        titles = [
            {"text": "filename", "width": 10, "type": 'l'},
            {"text": "date", "width": 10, "type": 'l'}
        ]
        rows = [
            {"filename": "pic.png", "date": "21/05/2021"}
        ]
        self.tb = tb.Table(self.frame1, _keys_ = keys, titles = titles)
        self.tb.add_rows(rows)
    
    def create_display(self):
        self.canvas = tk.Canvas(self.frame2) 

    def create_notebook(self):
        self.notebook = tk.ttk.Notebook(self.frame3)

if __name__ == "__main__":
    # execute only if run as a script
    app = PyViewer()
    app.mainloop()