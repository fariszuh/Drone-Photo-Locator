import customtkinter
from tkintermapview import TkinterMapView
from tower_location_500kv import add_new_marker_label

import os
import tkinter
from PIL import Image, ImageTk

# customtkinter.set_default_color_theme("bcsvBMS.pylue")

class App(customtkinter.CTk):

    APP_NAME = "Drone Photos Locator by FarisZ"
    WIDTH = 1000
    HEIGHT = 500

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        src = "D:\Project+Lomba\csv Drive Downloader\SLO\Drone Tower Reroute";

        print(os.getcwd());
        os.chdir(src);
        files = sorted(os.listdir());
        foto = files[0]
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
        self.entry_widget.grid(row=2, column=3, sticky="swe", padx=(10, 10), pady=(10,10))
       # self.entry_widget.pack(pady=10)

        # Optional: Insert a default value
        # self.entry_widget.insert(0, "Enter text here...")

        # Function to retrieve the input
        def get_entry_text():
            entered_text = self.entry_widget.get()
            print(f"User entered: {entered_text}")

        # Button to trigger the retrieval
        self.get_text_button = customtkinter.CTkButton(master=self.frame_right,
                                                text="Change",
                                                width=90,command=get_entry_text)
        self.get_text_button.grid(row=2, column=4, sticky="swe", padx=(10, 10), pady=10)
        # get_text_button.pack()

        # # Widgets for new filename
        # my_entry = customtkinter.CTkEntry(self.frame_right,
        #                                   placeholder_text="Type New Filename",
        #                                   height=50,
        #                                   width=200,
        #                                   font=("Helvetica", 18),
        #                                   corner_radius=50,
        #                                   text_color="green",
        #                                   placeholder_text_color="darkblue",
        #                                   fg_color=("blue", "lightblue"),  # outer, inner
        #                                   state="normal",
        #                                   )
        # self.my_entry.grid(row=1, column=3, sticky="swe", padx=(10, 10), pady=(10, 10))
        # tk.Label(root, text="New Filename:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        # new_filename_entry = tk.Entry(root, width=50)
        # new_filename_entry.grid(row=1, column=1, padx=5, pady=5)
        #
        # # Button to perform rename
        # tk.Button(root, text="Rename File", command=perform_rename).grid(row=2, column=1, padx=5, pady=10)

        # my_image = customtkinter.CTkImage(light_image=original_image,
        #                                   dark_image=original_image,
        #                                   size=(100, 70))  # WidthxHeight
        #
        # self.my_label = customtkinter.CTkLabel(self.frame_right, image=my_image)
        # self.map_label.grid(row=0, column=3, sticky="nswe", padx=100, pady=70)
        # my_label.pack(pady=10)

        # window2 = customtkinter.Tk()
        # window2.title("Pictures transformer")
        # window2.geometry("900x500+100+100")
        # window2.configure(bg="#ffffff")
        # original_image = Image.open(foto)
        # tk_image = ImageTk.PhotoImage(original_image.resize((100, 70)))
        #
        # image2 = Image.open(foto)
        # print(image2.size)
        # height, width = image2.size;
        # height = height / 8;
        # width = width / 8;
        # img1 = image2.resize((int(height), int(width)))
        # logo = ImageTk.PhotoImage(img1)
        # Label(image=logo, bg="#fff").place(x=10, y=10)
        # import PIL.Image
        # img = PIL.Image.open(foto)

        # set a position marker (also with a custom color and command on click)
        # marker_2 = self.map_widget.set_marker(-2.1126580277777776 , 101.94536872222223, text="Brandenburger Tor")
        # marker_3 = self.map_widget.set_marker(-2.13648725 , 101.9292875, text="52.55, 13.4")
        # marker_4 = self.map_widget.set_marker(-2.3, 101.9292875, text="52.55, 13.4")
        # marker_3.set_position(-2.13648725 , 101.9292875)
        # marker_3.set_text(...)
        # marker_3.delete()

        add_new_marker_label(self)

        # set a path
        # path_1 = self.map_widget.set_path([marker_2.position, marker_3.position, marker_4.position, (-2.1126580277777776 , 101.94536872222223), (-2.13648725 , 101.9292875)])

        # marker_2 = self.map_widget.set_marker(101.753634, -2.217404, text="taping arah s.penuh")
        # marker_3 = self.map_widget.set_marker(101.754628, -2.21593, text="T5.L2 BB+6")
        # marker_4 = self.map_widget.set_marker(101.755802, -2.214174, text="T4.L2 BB+0")
        # path1 = self.map_widget.set_path([marker_2.position, marker_3.position, marker_4.position])


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
