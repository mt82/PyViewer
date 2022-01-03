"""
utils package
"""

import os
import io
import sys
from subprocess import PIPE, Popen
import mimetypes
import folium

from PIL import Image

EXIFTOOL_PATH = ""


def get_home():
    """ get home directory from environmental variable """
    return os.path.expanduser("~")


def get_exiftool_path():
    """ get exiftool path """
    relative_path = "OneDrive - Istituto Nazionale di Fisica Nucleare/" \
        "PyViewer/tools/exiftool-12.30/exiftool.exe"
    home = get_home()
    full_path = os.path.join(home, relative_path)
    return full_path


def get_and_check_exiftool_path():
    """ init exiftool path """
    full_path = get_exiftool_path()
    if not os.path.exists(full_path):
        raise BaseException("  -- exiftool not found --")
    return full_path


def get_decimal_coord(gps):
    """ transform coordinates to decimal format """
    coord = []
    if gps is not None:
        if all(k in gps for k in range(1, 5)):
            lat = (-1 if gps[1] == 'S' else 1) * \
                (gps[2][0] + gps[2][1]/60. + gps[2][2]/3600.)
            lng = (-1 if gps[3] == 'W' else 1) * \
                (gps[4][0] + gps[4][1]/60. + gps[4][2]/3600.)
            coord = [lat, lng]
    return coord


def get_video_info(filepath):
    """ get video info """
    # get video info: path, filename, date
    path_raw = r'{}'.format(filepath)
    process = Popen([EXIFTOOL_PATH, path_raw],
                    stdout=PIPE, stderr=None, shell=True)
    out = process.communicate()[0].decode("utf-8")
    date = [x.split(" : ")[1].strip() for x in out.split('\r\n')[:-1]
            if x.split(" : ")[0].strip() == 'Create Date']
    return {"name": os.path.basename(filepath),
            "path": filepath,
            "date": date[0] if len(date) > 0 else "",
            "gps": []}


def get_image_info(filepath):
    """ get image info """
    # get image info: path, filename, date
    img = Image.open(filepath)
    exif = img.getexif()
    return {"name": os.path.basename(filepath),
            "path": filepath,
            "date": exif.get(306),
            "gps": get_decimal_coord(exif.get(34853))}


def get_list_of_files_with_info(directory):
    """ get list of files with infos """
    # dictionary with images and videos
    # each items has filename, path and creation date
    folder_items = {"image": [],
                    "video": []}

    # 1 - list content of the directory
    # 2 - filter images and videos
    # 3 - retrieve information
    if os.path.isdir(directory):
        items_in_folder = os.listdir(directory)
        files_in_folder = [x for x in items_in_folder if os.path.isfile(
            os.path.join(directory, x))]
        image_in_folder = [x for x in files_in_folder if "image" in mimetypes.guess_type(x)[
            0]]
        video_in_folder = [x for x in files_in_folder if "video" in mimetypes.guess_type(x)[
            0]]
        folder_items["image"] = [get_image_info(os.path.join(directory, img))
                                 for img in image_in_folder]
        folder_items["video"] = [get_video_info(os.path.join(directory, vid))
                                 for vid in video_in_folder]
    return folder_items


def dump(folder_items):
    """ dump info """
    for item_format in folder_items:
        print(f" -- {item_format} --")
        for item in folder_items[item_format]:
            print(
                f"    name: {item['name']} date: {item['date']} coord: {item['gps']}")


def build_map(items):
    """ put markers in map """
    my_map = folium.Map(tiles="OpenStreetMap")

    points = []

    for item in items:
        if len(item["gps"]) == 2:
            points.append([item["gps"][0], item["gps"][1]])
            folium.Marker(
                location=item["gps"],
                popup=f"{item['name']}: {item['date']}",
            ).add_to(my_map)

    my_map.fit_bounds(points)

    # save map data to data object
    data = io.BytesIO()
    my_map.save(data, close_file=False)

    return data

def next_index(this_index, collection):
    """ get next index """
    if len(collection) == 0:
        this_index = -1
    elif this_index == len(collection) - 1:
        this_index = 0
    else:
        this_index += 1
    return this_index


def prev_index(this_index, collection):
    """ get previous index """
    if len(collection) == 0:
        this_index = -1
    elif this_index == 0:
        this_index = len(collection) - 1
    else:
        this_index -= 1
    return this_index

EXIFTOOL_PATH = get_and_check_exiftool_path()

if __name__ == "__main__":
    NARGS = len(sys.argv)
    if NARGS == 1:
        pass
    elif NARGS == 2:
        items = get_list_of_files_with_info(sys.argv[1])
        build_map(items["image"])

    else:
        print("  -- Too many arguments --")
        sys.exit(1)
