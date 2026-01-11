import customtkinter
from CTkTable import *
from tkintermapview import TkinterMapView
# from tower_location_BMS_pointdata import add_new_marker_label
import tower_location_BMS_pointdata
from geopy.distance import great_circle

import os
from PIL import Image, ImageTk

# customtkinter.set_default_color_theme("bcsvBMS.pylue")
index_foto = 0

APP_NAME = "Drone Photos Locator by FarisZ"
WIDTH = 1000
HEIGHT = 500

App = customtkinter.CTk() # CTk() serves as the main app window
App.geometry(str(WIDTH) + "x" + str(HEIGHT)) # Set the initial size of the window
App.title(APP_NAME) # Set the window title
App.minsize(WIDTH, HEIGHT)
# ============ create two CTkFrames ============
App.grid_columnconfigure(0, weight=0)
App.grid_columnconfigure(1, weight=1)
App.grid_rowconfigure(0, weight=1)

App.frame_left = customtkinter.CTkFrame(master=App, width=150, corner_radius=0, fg_color=None)
App.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

App.frame_right = customtkinter.CTkFrame(master=App, corner_radius=0)
App.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

def search_event():
    App.map_widget.set_address(App.entry.get())

def set_marker_event():
    print("start get pos")
    current_position = App.map_widget.get_position()
    print("current pos: " + str(current_position))
    marker_list.append(App.map_widget.set_marker(current_position[0], current_position[1], text_color="yellow", marker_color_circle="white"))

def clear_marker_event():
    for marker in marker_list:
        marker.delete()

def change_appearance_mode(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)

def change_map(new_map: str):
    if new_map == "OpenStreetMap":
        map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
    elif new_map == "Google normal":
        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
    elif new_map == "Google satellite":
        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
    elif new_map == "Google terrain":
        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=t&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

def rename_event():
    input_text = App.entry_widget.get()
    print(f"Text from entry: {input_text}")
    # You can add other actions here, such as clearing the entry
    # self.entry_widget.delete(0, customtkinter.END)
    current_name = foto
    new_name = input_text + ".JPG"
    # os.rename(current_name, new_name)

    if new_name and current_name:
        try:
            # Use os.rename() to change the file name
            print("current name: " + current_name + " ; new name: " + new_name)
            # App.map_label2.configure(image=None) # = None #customtkinter.CTkLabel(App.frame_right, image=None, text="")
            original_image.close()
            img.close()
            os.rename(current_name, new_name)
            print(f"File renamed from '{current_name}' to '{new_name}'")
            App.destroy()
            # Optional: Update a label in the GUI to confirm success
            # status_label.configure(text=f"Renamed to: {new_name}", text_color="green")

        except FileExistsError:
            print(f"Error: File '{new_name}' already exists.")
            # status_label.configure(text=f"Error: '{new_name}' already exists", text_color="red")
        except FileNotFoundError:
            print(f"Error: File '{current_name}' not found.")
            # status_label.configure(text=f"Error: '{current_name}' not found", text_color="red")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            # status_label.configure(text=f"An error occurred: {e}", text_color="red")
    else:
        print("Please enter a new file name.")
        # status_label.configure(text="Please enter a name", text_color="orange")

def find_closest_point_to_center():
    # 2. Get the reference point (e.g., current map center)
    center_coords = map_widget.get_position()
    center_point = (center_coords[0], center_coords[1])

    # 3. Use min() to find the closest point by distance
    # The key function calculates the great_circle distance for each point
    closest_point_info = min(markers, key=lambda p: great_circle(center_point, (p[0], p[1])).kilometers)

    lat, lon, name, marker_obj = closest_point_info
    distance = great_circle(center_point, (lat, lon)).kilometers

    print(f"Closest point to map center is {name} at {lat:.3f}, {lon:.3f}")
    print(f"Distance: {distance:.2f} KM")
    return name, distance

def on_closing(event=0):
    App.destroy()

def start():
    App.mainloop()

marker_list = []

src = "D:\\drone\\New folder\\test\\";
print(os.getcwd());
os.chdir(src);
files = sorted(os.listdir());

foto = files[index_foto]
# self.foto = foto
from PIL import Image, ImageTk, ExifTags
import PIL.ImageTk
img = PIL.Image.open(foto)
exif = {
    PIL.ExifTags.TAGS[k]: v
    for k, v in img._getexif().items()
    if k in PIL.ExifTags.TAGS
}
print(exif['GPSInfo'])
waktu_drone = exif['DateTime']

south = exif['GPSInfo'][2]
east = exif['GPSInfo'][4]
altitude = exif['GPSInfo'][6]
# print(exif['GPSLatitudeRef'])

print("N:", south, " , E :", east)
lat_foto = -1 * (((south[0]) + south[1] / 60) + south[2] / 3600)  # convert north to south
long_foto = (((east[0]) + east[1] / 60) + east[2] / 3600)
lat_foto, long_foto = float(lat_foto), float(long_foto)

print("file:", foto)
print("lat,long:", lat_foto, ",", long_foto)

# change_map("OpenStreetMap")
# App.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
# ============ frame_left ============

App.frame_left.grid_rowconfigure(2, weight=1)

App.button_1 = customtkinter.CTkButton(master=App.frame_left,
                                        text="Set Marker",
                                        command=set_marker_event)
App.button_1.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

App.button_2 = customtkinter.CTkButton(master=App.frame_left,
                                        text="Clear Markers",
                                        command=clear_marker_event)
App.button_2.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

App.map_label = customtkinter.CTkLabel(App.frame_left, text="Tile Server:", anchor="w")
App.map_label.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))
App.map_option_menu = customtkinter.CTkOptionMenu(App.frame_left, values=["OpenStreetMap", "Google normal", "Google satellite","Google terrain"],
                                                               command=change_map)
App.map_option_menu.grid(row=4, column=0, padx=(20, 20), pady=(10, 0))

App.appearance_mode_label = customtkinter.CTkLabel(App.frame_left, text="Appearance Mode:", anchor="w")
App.appearance_mode_label.grid(row=5, column=0, padx=(20, 20), pady=(20, 0))
App.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(App.frame_left, values=["Light", "Dark", "System"],
                                                               command=change_appearance_mode)
App.appearance_mode_optionemenu.grid(row=6, column=0, padx=(20, 20), pady=(10, 20))

# ============ frame_right ============

App.frame_right.grid_rowconfigure(1, weight=1)
App.frame_right.grid_rowconfigure(0, weight=0)
App.frame_right.grid_columnconfigure(0, weight=1)
App.frame_right.grid_columnconfigure(1, weight=0)
App.frame_right.grid_columnconfigure(2, weight=1)

map_widget = TkinterMapView(App.frame_right, corner_radius=0)
# map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))
map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

map_widget.set_zoom(18)
# self.map_widget.set_position(-2.13648725 , 101.9292875)
map_widget.set_position(lat_foto,long_foto)
map_widget.set_marker(lat_foto, long_foto, text="Titik Drone", text_color="red")
# change_map to google satellite
# map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

# self.map_widget2 = TkinterMapView(self.frame_right, corner_radius=0)
original_image = Image.open(foto) # Load images for light and dark mode
# Create a CTkImage instance
# my_image = customtkinter.CTkImage(
#     light_image=original_image,
#     dark_image=original_image,
#     size=(320, 240)
# )
my_image = customtkinter.CTkImage(
    light_image=original_image,
    dark_image=original_image,
    size=(120, 90)
)

# tk_image = ImageTk.PhotoImage(original_image.resize((400, 300)))
App.map_label2 = customtkinter.CTkLabel(App.frame_right, image=my_image, text="")
# App.map_label2.grid(row=1, rowspan=2, column=3, columnspan=3, sticky="n", padx=(10,10), pady=(10,0))
App.map_label2.grid(row=1, rowspan=2, column=1, columnspan=2, sticky="n", padx=(10,10), pady=(10,0))

markers = []
jalur = []
for lat, lon, name in tower_location_BMS_pointdata.points_data:
    marker = map_widget.set_marker(lat, lon, text=name, text_color="red",marker_color_circle="white",marker_color_outside="gray40")
    markers.append((lat, lon, name, marker))
    jalur = jalur + [(lat,lon)]

continuous_route = map_widget.set_path(jalur, color="blue", width=4)

name, distance = find_closest_point_to_center()

textbox = f"File:\n{foto}\n\nDatetime:\n{waktu_drone}\n\nAltitude:\n{altitude} m\n\nClosest Point:\n{name}\n\nDistance:\n{distance:.2f} km"
App.map_label = customtkinter.CTkLabel(App.frame_right, text=textbox, anchor="e")
App.map_label.grid(row=1, column=3, sticky="n", padx=(0,0), pady=10)

# Create an Entry widget
App.entry_widget = customtkinter.CTkEntry(master=App.frame_right,
                                           placeholder_text="Type Namefile")
App.entry_widget.grid(row=1, column=3, sticky="swe", padx=(10, 10), pady=75)
# self.entry.bind("<Return>", rename_event(foto,new_namefile))

App.button_entry = customtkinter.CTkButton(master=App.frame_right,
                                        text="Rename",
                                        width=90,
                                        command=rename_event)
App.button_entry.bind("<Return>", rename_event)
App.button_entry.grid(row=1, column=3, sticky="swe", padx=(10,10), pady=45)

App.button_next = customtkinter.CTkButton(master=App.frame_right,
                                        text="Next",
                                        width=90,
                                        command=None)
App.button_next.grid(row=1, column=3, sticky="swe", padx=(10,10), pady=10)

# App.button_findclosestpoint = customtkinter.CTkButton(master=App.frame_right,
#                                             text="Find Closest",
#                                             width=20,
#                                             command=find_closest_point_to_center)
# App.button_findclosestpoint.grid(row=2, column=5, sticky="w", padx=(5, 0), pady=2)
# print("closest : " + find_closest_point_to_center.name)



App.entry = customtkinter.CTkEntry(master=App.frame_right,
                                    placeholder_text="type address")
App.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
App.entry.bind("<Return>", search_event)

App.button_5 = customtkinter.CTkButton(master=App.frame_right,
                                        text="Search",
                                        width=90,
                                        command=search_event)
App.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

# Set default values
map_widget.set_address("Berlin")
App.map_option_menu.set("OpenStreetMap")
App.appearance_mode_optionemenu.set("Dark")

App.mainloop()
# if __name__ == "__main__":
#     app = App()
#     app.start()
