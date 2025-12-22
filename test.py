import os
import tkinter as tk
from tkinter import *

from PIL import Image, ImageTk, ExifTags

src = "G:\\SUTT 150 kV BMS\\Unclassified";
# src = "H:\My Drive\PROYEK UPP SBT 3\06. SUTT 150 kV Kuala Tungkal - Pelabuhan Dagang\Dokumentasi\Drone FC KTPD Sept 2025\KP70 - KP78"

print(os.getcwd());
os.chdir(src);
files = os.listdir();
foto = files[12]
print(os.getcwd())

window = Tk()
window.title("Pictures transformer")
window.geometry("900x500+100+100")
window.configure(bg="#ffffff")

# logo
image = Image.open(foto)
print(image.size)
height, width = image.size;
height = height/8; width = width/8;
img1 = image.resize((int(height),int(width)))
logo = ImageTk.PhotoImage(img1)
Label(image=logo, bg="#fff").place(x=10, y=10)

import PIL.Image
img = PIL.Image.open(foto)
exif = {
    PIL.ExifTags.TAGS[k]: v
    for k, v in img._getexif().items()
    if k in PIL.ExifTags.TAGS
}
print(exif['GPSInfo'])
south = exif['GPSInfo'][2]
east = exif['GPSInfo'][4]
print("N:",south, " , E :", east)
lat = -1*(((south[0]) + south[1]/60) + south[2]/3600) # convert north to south
long = (((east[0]) + east[1]/60) + east[2]/3600)
lat, long = float(lat), float(long)

print("file:",foto)
print("lat,long:", lat, ",", long)

top_label = tk.Label(window, text=["lat,long:", lat, ",", long], image=logo, compound='top')
top_label.pack(side=tk.TOP, fill=tk.X)

bottom_label = tk.Label(window, text=foto, bg="lightgreen")
bottom_label.pack(side=tk.BOTTOM, fill=tk.X)


# import geopy
# object=geopy.Nominatim(user_agent="Nikki")
# location = input("Enter the location ")
# h=object.geocode(ation)
# import folium
# map = folium.Map(location=[h.latitude,h.longitude], zoom_start=13)
# folium.Marker([h.latitude,h.longitude], popup='My Home').add_to(map)
# map

window.mainloop()