import customtkinter
from tkintermapview import TkinterMapView
from tower_location_BMS import add_new_marker_label
from geopy.distance import great_circle

import os
import tkinter
from PIL import Image, ImageTk

# customtkinter.set_default_color_theme("bcsvBMS.pylue")
index_foto = 0

class App(customtkinter.CTk):

    APP_NAME = "Drone Photos Locator by FarisZ"
    WIDTH = 1000
    HEIGHT = 500

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        src = "D:\\drone\\New folder\\test\\";

        print(os.getcwd());
        os.chdir(src);
        files = sorted(os.listdir());

        foto = files[index_foto]
        self.foto = foto
        from PIL import Image, ImageTk, ExifTags
        import PIL.Image
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

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        self.marker_list = []

        # ============ create two CTkFrames ============



        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(2, weight=1)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Set Marker",
                                                command=self.set_marker_event)
        self.button_1.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Clear Markers",
                                                command=self.clear_marker_event)
        self.button_2.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

        self.map_label = customtkinter.CTkLabel(self.frame_left, text="Tile Server:", anchor="w")
        self.map_label.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))
        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["OpenStreetMap", "Google normal", "Google satellite"],
                                                                       command=self.change_map)
        self.map_option_menu.grid(row=4, column=0, padx=(20, 20), pady=(10, 0))

        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=(20, 20), pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=(20, 20), pady=(10, 20))

        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

        self.map_widget.set_zoom(18)
        # self.map_widget.set_position(-2.13648725 , 101.9292875)
        self.map_widget.set_position(lat_foto,long_foto)
        self.map_widget.set_marker(lat_foto, long_foto, text="Titik Drone")

        # self.map_label = customtkinter.CTkLabel(self.frame_right, text="Drone Capture", anchor="w")
        # self.map_label.grid(row=0, column=3, padx=(40, 40), pady=(20, 0))

        # self.map_widget2 = TkinterMapView(self.frame_right, corner_radius=0)
        original_image = Image.open(foto) # Load images for light and dark mode
        # Create a CTkImage instance
        my_image = customtkinter.CTkImage(
            light_image=original_image,
            dark_image=original_image,
            size=(320, 240)
        )

        # tk_image = ImageTk.PhotoImage(original_image.resize((400, 300)))
        self.map_label2 = customtkinter.CTkLabel(self.frame_right, image=my_image, text="")
        self.map_label2.grid(row=1, rowspan=2, column=3, columnspan=3, sticky="n", padx=(10,10), pady=(10,0))

        textbox = "File Name: \n" + foto + "\n\n Capture Datetime: \n" + waktu_drone + "\n\n Altitude: \n" + str(
            altitude) + " m"
        self.map_label = customtkinter.CTkLabel(self.frame_right, text=textbox, anchor="e")
        self.map_label.grid(row=1, column=3, sticky="swe", padx=(10,10), pady=(10,10))

        # Create an Entry widget
        self.entry_widget = customtkinter.CTkEntry(master=self.frame_right,
                                                   placeholder_text="type namefile")
        self.entry_widget.grid(row=2, column=3, sticky="we", padx=(10, 10), pady=(10, 10))
        # self.entry.bind("<Return>", rename_event(foto,new_namefile))

        self.button_entry = customtkinter.CTkButton(master=self.frame_right,
                                                text="Rename",
                                                width=90,
                                                command=self.rename_event)
        self.button_entry.grid(row=2, column=4, sticky="w", padx=(12, 0), pady=12)
        self.button_entry.bind("<Return>", self.rename_event)

        self.button_next = customtkinter.CTkButton(master=self.frame_right,
                                                    text="Next",
                                                    width=20,
                                                    command=None)
        self.button_next.grid(row=2, column=5, sticky="w", padx=(5, 0), pady=2)

        #
        # # Button to perform rename
        # tk.Button(root, text="Rename File", command=perform_rename).grid(row=2, column=1, padx=5, pady=10)

        add_new_marker_label(self)

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            placeholder_text="type address")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.search_event)

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Search",
                                                width=90,
                                                command=self.search_event)
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        # Set default values
        self.map_widget.set_address("Berlin")
        self.map_option_menu.set("OpenStreetMap")
        self.appearance_mode_optionemenu.set("Dark")


    def rename_event(self):

        input_text = self.entry_widget.get()
        print(f"Text from entry: {input_text}")
        # You can add other actions here, such as clearing the entry
        # self.entry_widget.delete(0, customtkinter.END)
        current_name = self.foto
        new_name = input_text + ".JPG"
        print("current name: " + current_name + " ; new name: " + new_name)
        # os.rename(current_name, new_name)
        if new_name and current_name:
            try:
                # Use os.rename() to change the file name
                self.map_label2.configure(image=None)
                os.rename(current_name, new_name)
                print(f"File renamed from '{current_name}' to '{new_name}'")
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

    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())

    def set_marker_event(self):
        current_position = self.map_widget.get_position()
        self.marker_list.append(self.map_widget.set_marker(current_position[0], current_position[1]))

    def clear_marker_event(self):
        for marker in self.marker_list:
            marker.delete()

    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
