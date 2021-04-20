import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
import os
from datetime import datetime
from PIL import ImageTk,Image 
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
import json

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

current_directory = "C:/Users/mt/OneDrive - Istituto Nazionale di Fisica Nucleare/Pictures/from Google/Takeout/Google Photos/AcetAia 2018"
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

extensions = ["jpg","jpeg","png","mp4","3gp","dng","gif","webp"]
img_format = ["jpg","jpeg","png","dng","gif"]
vid_format = ["mp4","3gp","webp"]
units = ["Byte","kB","MB","GB","TB","PB"]

def get_info(item):
    date = datetime.fromtimestamp(os.path.getctime(item)).strftime('%Y-%m-%d %H:%M:%S')
    unit = 0
    size = os.path.getsize(item)
    while(size > 10000):
        size /= 1000
        unit += 1
    size = f"{int(size)} {units[unit]}"
    fname, fext = os.path.splitext(item)
    fname = os.path.basename(item)
    return date, size, fext[1:], fname

def onClickedItem(event):
    global current_directory
    global this_canvas
    global this_img_id
    global this_img
    global this_text1
    global this_text2
    tree = event.widget
    item = tree.focus()
    if tree.item(item,'values')[2] != "":
        fname = tree.item(item,"text")
        parent = tree.parent(item)
        while(parent):
            fname = f"{tree.item(parent,'text')}/{fname}"
            parent = tree.parent(parent)
        if current_directory != ".":
            fname = f"{os.path.dirname(current_directory)}/{fname}"
        if tree.item(item,'values')[2] in img_format:
            img = Image.open(fname)
            h,w = img.size
            hh, ww = canvas.winfo_height(), canvas.winfo_width()
            scale = min([ww/h,hh/w])
            h, w = int(h*scale),int(w*scale)
            img = img.resize((h,w))
            this_img = ImageTk.PhotoImage(img)
            this_canvas.itemconfig(this_img_id, image = this_img)
            fjson = fname + ".json"
            if os.path.isfile(fjson):
                json_info = json.load(open(fjson))
                this_text2.delete(1.0,tk.END)
                this_text2.insert(1.0,json.dumps(json_info, indent=4, separators=(". ", " = ")))
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

def onNotebookTabChange(event):
    global this_txsb
    global this_tysb
    global this_text1
    global this_text2
    global this_nb
    if this_nb.tab(nb.select(), "text") == "JSON":
        this_tysb.configure(command=text2.yview)
        this_txsb.configure(command=text2.xview)
        this_text2.configure(yscroll=this_tysb.set, xscroll=this_txsb.set)
    elif this_nb.tab(nb.select(), "text") == "Metadata":
        this_tysb.configure(command=text1.yview)
        this_txsb.configure(command=text1.xview)
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
    
root = tk.Tk()
root.title("PyViewer")

# frames
frame = tk.Frame(root)

# menu bar
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar)
filemenu.add_command(label="Open Folder",command=onOpenFolder)
filemenu.add_command(label="Exit",command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)


# tree viewer

tree = ttk.Treeview(frame)
ysb = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
xsb = ttk.Scrollbar(frame, orient='horizontal', command=tree.xview)
tree.configure(yscroll=ysb.set, xscroll=xsb.set)
tree["columns"] = ("1","2","3")
tree.column("#0",width=150,minwidth=10)
tree.column("1",width=50,minwidth=10)
tree.column("2",width=50,minwidth=10)
tree.column("3",width=50,minwidth=10)
tree.heading('#0', text="Name", anchor='w')
tree.heading('1', text="Date", anchor='w')
tree.heading('2', text="Size", anchor='w')
tree.heading('3', text="Extension", anchor='w')

this_tree = tree
date, size, fext, fname = get_info(current_directory)
root_node = tree.insert('', 'end', values=(date,size,fext), text=fname, open=True)
tree.bind('<<TreeviewSelect>>', onClickedItem)
process_directory(root_node, current_directory,tree)

# canvas

canvas = tk.Canvas(frame) 

# notebook
nb = ttk.Notebook(frame)
text1 = tk.Text(nb, height=15, wrap='none')
nb.add(text1,text="Metadata")
text2 = tk.Text(nb, height=15, wrap='none')
nb.add(text2,text="JSON")
tysb = ttk.Scrollbar(frame, orient='vertical', command=text1.yview)
txsb = ttk.Scrollbar(frame, orient='horizontal', command=text1.xview)
text1.configure(yscroll=tysb.set, xscroll=txsb.set)
nb.bind("<<NotebookTabChanged>>", onNotebookTabChange)
nb.enable_traversal()
this_text1 = text1
this_text2 = text2
this_tysb = tysb
this_txsb = txsb
this_nb = nb


tree.grid(row=0, column=0, columnspan=2, sticky='NESW')
ysb.grid(row=0, column=2, sticky='NS')
xsb.grid(row=1, column=0, columnspan=2, sticky='EW')
canvas.grid(row=2,column=0, rowspan=2, sticky='NESW')
nb.grid(row=2,column=1,sticky="NESW")
# text.grid(row=2, column=1, sticky='NS')
tysb.grid(row=2, column=2, sticky='NS')
txsb.grid(row=3, column=1, sticky='EW')
frame.grid()

frame.update()

image_id = canvas.create_image(int(0.5*canvas.winfo_width()), int(0.5*canvas.winfo_height()), anchor="center") 
this_canvas = canvas
this_img_id = image_id

# geotags = get_geotagging(exifdata)
# print(geotags)

root.mainloop()