import os
import sys
import mimetypes
import folium

from PIL import ImageTk,Image 
from subprocess import PIPE, Popen

exiftool_path = ""

def get_home():
    return os.path.expanduser("~")

def get_exiftool_path():
    relative_path = r"OneDrive - Istituto Nazionale di Fisica Nucleare\PyViewer\tools\exiftool-12.30\exiftool.exe"
    home = get_home()
    full_path = os.path.join(home,relative_path)
    return full_path

def init_exiftool():
    global exiftool_path
    full_path = get_exiftool_path()
    if not os.path.exists(full_path):
        raise BaseException("  -- exiftool not found --")
    exiftool_path = full_path

def get_decimal_coord(gps):
    coord = []
    if gps is not None:
        if all (k in gps for k in range(1,5)):
            lat = (-1 if gps[1] == 'S' else 1) * (gps[2][0] + gps[2][1]/60. + gps[2][2]/3600.)
            lng = (-1 if gps[3] == 'W' else 1) * (gps[4][0] + gps[4][1]/60. + gps[4][2]/3600.)
            coord = [ lat, lng]
    return coord

def getVideoInfo(filepath):
    # get video info: path, filename, date
    path_raw = r'{}'.format(filepath)
    process = Popen([exiftool_path , path_raw], stdout=PIPE, stderr=None, shell=True)
    out = process.communicate()[0].decode("utf-8")
    date = [x.split(" : ")[1].strip() for x in out.split('\r\n')[:-1] if x.split(" : ")[0].strip() == 'Create Date']
    return {"name": os.path.basename(filepath),
            "path": filepath,
            "date": date[0] if len(date) > 0 else "",
            "gps" : []}

def getImageInfo(filepath):
    # get image info: path, filename, date
    img = Image.open(filepath)
    exif = img.getexif()
    return {"name": os.path.basename(filepath),
            "path": filepath,
            "date": exif.get(306),
            "gps" : get_decimal_coord(exif.get(34853))}

def getListOfFilesWithInfo(directory):
    # dictionary with images and videos
    # each items has filename, path and creation date
    items = {"image" : [], 
             "video" : [] }
    
    # 1 - list content of the directory
    # 2 - filter images and videos
    # 3 - retrieve information
    if os.path.isdir(directory):
        items_in_folder = os.listdir(directory)
        files_in_folder = [x for x in items_in_folder if os.path.isfile(os.path.join(directory,x))]
        image_in_folder = [x for x in files_in_folder if "image" in mimetypes.guess_type(x)[0]]
        video_in_folder = [x for x in files_in_folder if "video" in mimetypes.guess_type(x)[0]]
        items["image"] = [getImageInfo(os.path.join(directory,img)) for img in image_in_folder]
        items["video"] = [getVideoInfo(os.path.join(directory,vid)) for vid in video_in_folder]
    return items

def dump(items):
    for type in items:
        print(f" -- {type} --")
        for item in items[type]:
            print(f"    name: {item['name']} date: {item['date']} coord: {item['gps']}")

def put_in_map(item):
    center_lat = 0.
    center_lon = 0.
    counter = 0

    for it in item:
        if len(it["gps"]) == 2:
            center_lat += it["gps"][0]
            center_lon += it["gps"][1]
            counter += 1
    center_lat /= counter
    center_lon /= counter

    m = folium.Map(location=[center_lat,center_lon], tiles="OpenStreetMap", zoom_start=2)

    for it in item:
        if len(it["gps"]) == 2:
            folium.Marker(
                location=it["gps"],
                popup=f"{it['name']}: {it['date']}",
            ).add_to(m)
    
    m.save('map.html')

def main():
    print("  -- this is utils module --")
    init_exiftool()

main()

if __name__ == "__main__":
    nargs = len(sys.argv)
    if nargs == 1:
        pass
    elif nargs == 2:
        items = getListOfFilesWithInfo(sys.argv[1])
        dump(items)
        put_in_map(items["image"])

    else:
        print("  -- Too many arguments --")
        sys.exit(1)
    