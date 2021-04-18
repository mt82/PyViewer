import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
import os
from datetime import datetime
from PIL import ImageTk,Image 
from PIL.ExifTags import TAGS
import json

## see here: https://stackoverflow.com/questions/40533812/tkinter-treeview-click-event-for-selected-item

current_directory = "C:/Users/mt/OneDrive - Istituto Nazionale di Fisica Nucleare/Pictures/from Google/Takeout/Google Photos/AcetAia 2018"
this_tree = None
this_canvas = None
this_img_id = None
this_img = None
this_text = None

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
    global this_text
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
            scale = 250./max([h,w])
            h, w = int(h*scale),int(w*scale)
            img = img.resize((h,w))
            this_img = ImageTk.PhotoImage(img)
            this_canvas.itemconfig(this_img_id, image = this_img)
            # fjson = fname + ".json"
            # if os.path.isfile(fjson):
            #     json_info = json.load(open(fjson))
            #     this_text.delete(1.0,tk.END)
            #     this_text.insert(1.0,json.dumps(json_info, indent=4, separators=(". ", " = ")))
            tt = ""
            exifdata = img.getexif()
            for tag_id in exifdata:
                # get the tag name, instead of human unreadable tag id
                tag = TAGS.get(tag_id, tag_id)
                data = exifdata.get(tag_id)
                # decode bytes 
                if isinstance(data, bytes):
                    #data = data.decode('utf-8', errors='ignore')
                    pass
                tt += f"{tag:30}: {data}\n"
            text.delete(1.0,tk.END)
            text.insert(1.0,tt)


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
root.geometry('800x500')

# frames
frameup = tk.Frame(root)

# menu bar
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar)
filemenu.add_command(label="Open Folder",command=onOpenFolder)
filemenu.add_command(label="Exit",command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)


# tree viewer

tree = ttk.Treeview(frameup,height=10)
ysb = ttk.Scrollbar(frameup, orient='vertical', command=tree.yview)
xsb = ttk.Scrollbar(frameup, orient='horizontal', command=tree.xview)
tree.configure(yscroll=ysb.set, xscroll=xsb.set)
tree["columns"] = ("1","2","3")
tree.column("#0",width=475,minwidth=100)
tree.column("1",width=100,minwidth=100)
tree.column("2",width=100,minwidth=100)
tree.column("3",width=100,minwidth=100)
tree.heading('#0', text="Name", anchor='w')
tree.heading('1', text="Date", anchor='w')
tree.heading('2', text="Size", anchor='w')
tree.heading('3', text="Extension", anchor='w')

this_tree = tree
date, size, fext, fname = get_info(current_directory)
root_node = tree.insert('', 'end', values=(date,size,fext), text=fname, open=True)
tree.bind('<<TreeviewSelect>>', onClickedItem)
process_directory(root_node, current_directory,tree)

tree.grid(row=0, column=0)
ysb.grid(row=0, column=1, sticky='ns')
xsb.grid(row=1, column=0, sticky='ew')
frameup.grid()

frameup.pack(side="top", fill="both", expand=True)


# canvas
framedw = tk.Frame(root)

canvas = tk.Canvas(framedw, width = 250, height = 250)  
#canvas.pack(side="left",fill="both",expand=True)
canvas.grid(row=0, column=0)
fname = current_directory + "/IMG_20180402_120459.jpg"
img = Image.open(fname)
h,w = img.size
scale = 250./max([h,w])
h, w = int(h*scale),int(w*scale)
img = img.resize((h,w))
image = ImageTk.PhotoImage(img)
image_id = canvas.create_image(125, 125, image=image, anchor="center") 
this_canvas = canvas
this_img_id = image_id
this_img = image

# text
text = tk.Text(framedw, height=15)
#text.pack(side = "right",fill="both",expand=True)
text.grid(row=0, column=1, sticky='ns')
# fjson = fname + ".json"
# if os.path.isfile(fjson):
#     json_info = json.load(open(fjson))
#     text.delete(1.0,tk.END)
#     text.insert(1.0,json.dumps(json_info, indent=4, separators=(". ", " = ")))
tt = ""
exifdata = img.getexif()
for tag_id in exifdata:
    # get the tag name, instead of human unreadable tag id
    tag = TAGS.get(tag_id, tag_id)
    data = exifdata.get(tag_id)
    # decode bytes 
    if isinstance(data, bytes):
        #data = data.decode('utf-8', errors='ignore')
        pass
    tt += f"{tag:27}: {data}\n"
text.delete(1.0,tk.END)
text.insert(1.0,tt)
this_text = text

#framedw.grid()

framedw.pack(side="top", fill="both", expand=True)

root.mainloop()