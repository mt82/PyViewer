import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
import os
from datetime import datetime
from PIL import ImageTk,Image 
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
import json
import getpass
from pathlib import Path

#https://stackoverflow.com/questions/46898749/tkinter-grid-not-resizing-based-on-window-size

home = str(Path.home())
current_directory = f"{home}/OneDrive - Istituto Nazionale di Fisica Nucleare/Pictures/from Google/Takeout/Google Photos/AcetAia 2018"
#current_directory = "."

this_tree = None
this_canvas = None
this_img_id = None
this_img = None
this_text = None
this_text1 = None
this_text2 = None
this_tysb = None
this_txsb = None
this_nb = None

def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging

extensions = ["jpg","jpeg","png","mp4","3gp","dng","gif","webp"]
img_format = ["jpg","jpeg","png","dng","gif"]
vid_format = ["mp4","3gp","webp"]
units = ["Byte","kB","MB","GB","TB","PB"]

def get_size(item):
    unit = 0
    size = os.path.getsize(item)
    while(size > 10000):
        size /= 1000
        unit += 1
    size = f"{int(size)} {units[unit]}"
    return size

def get_info(item):
    date = datetime.fromtimestamp(os.path.getctime(item)).strftime('%Y-%m-%d %H:%M:%S')
    size = get_size(item)
    fname, fext = os.path.splitext(item)
    fname = os.path.basename(item)
    return date, size, fext[1:], fname

def get_ext(item, tree):
    return tree.item(item,'values')[2]

def is_folder(item, tree):
    return get_ext(item, tree) == ""

def get_fname(item, tree):
    fname = tree.item(item,"text")
    parent = tree.parent(item)
    while(parent):
        fname = f"{tree.item(parent,'text')}/{fname}"
        parent = tree.parent(parent)
    if current_directory != ".":
        fname = f"{os.path.dirname(current_directory)}/{fname}"
    return fname

def is_image(item, tree):
    return tree.item(item,'values')[2] in img_format

def draw_image(fname):
    global this_canvas
    global this_img_id
    global this_img
    img = Image.open(fname)
    h,w = img.size
    hh, ww = this_canvas.winfo_height(), this_canvas.winfo_width()
    scale = min([ww/h,hh/w])
    h, w = int(h*scale),int(w*scale)
    img = img.resize((h,w))
    this_img = ImageTk.PhotoImage(img)
    this_canvas.itemconfig(this_img_id, image = this_img)
    return img

def print_json(fname):
    global this_text2
    this_text2.delete(1.0,tk.END)
    fjson = fname + ".json"
    if os.path.isfile(fjson):
        json_info = json.load(open(fjson))
        this_text2.insert(1.0,json.dumps(json_info, indent=4, separators=(". ", " = ")))

def print_metadata(img):
    global this_text1
    tt = ""
    exifdata = img.getexif()
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes 
        if not isinstance(data, bytes):
            #data = data.decode('utf-8', errors='ignore')
            tt += f"{tag:30}: {data}\n"
    this_text1.delete(1.0,tk.END)
    this_text1.insert(1.0,tt)

def onClickedItem(event):
    tree = event.widget
    item = tree.focus()
    if not is_folder(item, tree):
        fname = get_fname(item, tree)
        if is_image(item, tree):
            img = draw_image(fname)
            print_json(fname)
            print_metadata(img)

def onNotebookTabChange(event):
    global this_txsb
    global this_tysb
    global this_text1
    global this_text2
    global this_nb
    if this_nb.tab(this_nb.select(), "text") == "JSON":
        this_tysb.configure(command=this_text2.yview)
        this_txsb.configure(command=this_text2.xview)
        this_text2.configure(yscroll=this_tysb.set, xscroll=this_txsb.set)
    elif this_nb.tab(this_nb.select(), "text") == "Metadata":
        this_tysb.configure(command=this_text1.yview)
        this_txsb.configure(command=this_text1.xview)
        this_text1.configure(yscroll=this_tysb.set, xscroll=this_txsb.set)


def onOpenFolder():
    global current_directory
    global this_tree
    this_tree.delete(*this_tree.get_children())
    current_directory = filedialog.askdirectory(initialdir = current_directory,title = "Open folder", mustexist = True)
    date, size, fext, fname = get_info(current_directory)
    root_node = this_tree.insert('', 'end', values=(date,size,fext), text=fname, open=True)
    process_directory(root_node, current_directory,this_tree)

def process_directory(parent, path, tree):
    for p in os.listdir(path):
        abspath = os.path.join(path, p)
        date, size, fext, fname = get_info(abspath)
        isdir = os.path.isdir(abspath)
        if fext in extensions or isdir:
            oid = tree.insert(parent, 'end', values=(date,size,fext), text=fname, open=False)
            if isdir:
                process_directory(oid, abspath, tree)

def onResize(event):
    frame.pack(fill="both", expand=True)

root = tk.Tk()
root.title("PyViewer")
root.bind("<Configure>",onResize)

# frames
frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

# menu bar
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar)
filemenu.add_command(label="Open Folder",command=onOpenFolder)
filemenu.add_command(label="Exit",command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)


# tree viewer
this_tree = ttk.Treeview(frame)
ysb = ttk.Scrollbar(frame, orient='vertical', command=this_tree.yview)
xsb = ttk.Scrollbar(frame, orient='horizontal', command=this_tree.xview)
this_tree.configure(yscroll=ysb.set, xscroll=xsb.set)
this_tree["columns"] = ("1","2","3")
this_tree.column("#0",width=150,minwidth=10)
this_tree.column("1",width=50,minwidth=10)
this_tree.column("2",width=50,minwidth=10)
this_tree.column("3",width=50,minwidth=10)
this_tree.heading('#0', text="Name", anchor='w')
this_tree.heading('1', text="Date", anchor='w')
this_tree.heading('2', text="Size", anchor='w')
this_tree.heading('3', text="Extension", anchor='w')

date, size, fext, fname = get_info(current_directory)
root_node = this_tree.insert('', 'end', values=(date,size,fext), text=fname, open=True)
this_tree.bind('<<TreeviewSelect>>', onClickedItem)
process_directory(root_node, current_directory,this_tree)

# canvas
this_canvas = tk.Canvas(frame) 

# notebook
this_nb = ttk.Notebook(frame)
this_text1 = tk.Text(this_nb, height=15, wrap='none')
this_nb.add(this_text1,text="Metadata")
this_text2 = tk.Text(this_nb, height=15, wrap='none')
this_nb.add(this_text2,text="JSON")
this_tysb = ttk.Scrollbar(frame, orient='vertical', command=this_text1.yview)
this_txsb = ttk.Scrollbar(frame, orient='horizontal', command=this_text1.xview)
this_text1.configure(yscroll=this_tysb.set, xscroll=this_txsb.set)
this_nb.bind("<<NotebookTabChanged>>", onNotebookTabChange)
this_nb.enable_traversal()

# grid
this_tree.grid(row=0, column=0, columnspan=2, sticky='NESW')
ysb.grid(row=0, column=2, sticky='NS')
xsb.grid(row=1, column=0, columnspan=2, sticky='EW')
this_canvas.grid(row=2,column=0, rowspan=2, sticky='NESW')
this_nb.grid(row=2,column=1,sticky="NESW")
this_tysb.grid(row=2, column=2, sticky='NS')
this_txsb.grid(row=3, column=1, sticky='EW')
frame.grid()
frame.grid_columnconfigure(0,weight=1)
frame.grid_columnconfigure(1,weight=1)
frame.grid_columnconfigure(2,weight=1)
frame.grid_rowconfigure(0,weight=1)
frame.grid_rowconfigure(1,weight=1)
frame.grid_rowconfigure(2,weight=1)
frame.grid_rowconfigure(3,weight=1)
frame.update()

this_img_id = this_canvas.create_image(int(0.5*this_canvas.winfo_width()), int(0.5*this_canvas.winfo_height()), anchor="center") 

# geotags = get_geotagging(exifdata)
# print(geotags)

root.mainloop()